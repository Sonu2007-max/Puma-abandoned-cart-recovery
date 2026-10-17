"""
RAG Engine: Retrieval-Augmented Generation Logic
Handles similarity search over ChromaDB with category filtering,
multi-turn context awareness, and Gemini LLM streaming & batch responses.
"""

import os
from pathlib import Path
from typing import Generator, Tuple
from dotenv import load_dotenv
import chromadb
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "your_gemini_api_key_here":
    raise ValueError("GEMINI_API_KEY is not properly set in .env file.")

# Initialize Gemini Client
client = genai.Client(api_key=API_KEY)

# Define directories
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "db" / "chroma_store"
COLLECTION_NAME = "hr_insurance_policy"

# Persistent Chroma Client
chroma_client = chromadb.PersistentClient(path=str(DB_DIR))


def get_collection():
    """Retrieve the policy collection from ChromaDB."""
    try:
        return chroma_client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        raise RuntimeError(
            f"Collection '{COLLECTION_NAME}' not found! Please run document ingestion first."
        ) from e


def query_embeddings(query_text: str) -> list[float]:
    """Generate embedding for the search query."""
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query_text
    )
    return response.embeddings[0].values


def retrieve_relevant_chunks(
    question: str,
    top_k: int = 3,
    category_filter: str = None
) -> Tuple[str, list[dict]]:
    """
    Embeds query, performs vector search (with optional category filter),
    and formats context string and source citations.
    """
    collection = get_collection()
    query_vector = query_embeddings(question)

    query_params = {
        "query_embeddings": [query_vector],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"]
    }

    if category_filter and category_filter not in ["All", "All Policies"]:
        query_params["where"] = {"category": category_filter}

    search_results = collection.query(**query_params)

    documents = search_results["documents"][0] if search_results.get("documents") else []
    metadatas = search_results["metadatas"][0] if search_results.get("metadatas") else []
    distances = search_results["distances"][0] if search_results.get("distances") else []

    if not documents:
        return "", []

    context_blocks = []
    sources = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        source_name = meta.get("source", "Unknown")
        chunk_id = meta.get("chunk_id", "")
        category = meta.get("category", "General")
        
        # Calculate approximate similarity confidence from distance
        # For L2/cosine distances in ChromaDB: lower distance = higher match
        relevance = "High" if dist < 0.6 else ("Medium" if dist < 0.9 else "Low")

        context_blocks.append(
            f"--- [Document: {source_name} | Category: {category} | Chunk #{chunk_id}] ---\n{doc}"
        )
        sources.append({
            "source": source_name,
            "chunk_id": chunk_id,
            "category": category,
            "relevance": relevance,
            "distance": round(float(dist), 3),
            "snippet": doc[:300] + ("..." if len(doc) > 300 else "")
        })

    context_str = "\n\n".join(context_blocks)
    return context_str, sources


def build_prompt(question: str, context_str: str, chat_history: list[dict] = None) -> tuple[str, str]:
    """Constructs system instruction and prompt with conversation context and PUMA policy documents."""
    system_instruction = (
        "You are the official PUMA People & Culture Assistant (PUMA FOREVER. FASTER.). "
        "Your role is to empower PUMA employees with prompt, accurate, and inspiring answers regarding "
        "PUMA workplace policies, corporate health insurance, sports injury coverage, employee merchandise discounts, "
        "footwear allowances, fitness subsidies, and marathon sponsorships.\n\n"
        "STRICT PUMA POLICY GUIDELINES:\n"
        "1. Base your answer strictly on the provided PUMA policy context below.\n"
        "2. If the answer cannot be determined from the context, clearly state: "
        "'This information is not covered in the official PUMA People & Culture and Health policies. "
        "Please reach out to our People & Culture team directly at people.culture@puma.com or log a ticket on MyHR (https://myhr.puma.com).'\n"
        "3. Do not invent or guess policy numbers, monetary allowances, discount percentages, or leave days under any circumstances.\n"
        "4. Embody the PUMA spirit—energetic, athletic, professional, supportive, and concise.\n"
        "5. If the employee asks in Hinglish or Hindi, respond naturally in helpful Hinglish while keeping policy numbers, benefits, and technical terms exact."
    )

    # Add last 2 conversation turns if available
    history_str = ""
    if chat_history:
        recent = chat_history[-4:]  # Last 2 exchanges
        formatted_history = []
        for msg in recent:
            role = "PUMA Employee" if msg["role"] == "user" else "PUMA Assistant"
            formatted_history.append(f"{role}: {msg['content']}")
        if formatted_history:
            history_str = "Recent Conversation Context:\n" + "\n".join(formatted_history) + "\n\n"

    prompt = f"""{history_str}PUMA Policy Context:
{context_str}

PUMA Employee Question:
{question}

PUMA Assistant Answer:"""

    return system_instruction, prompt



def query_rag_stream(
    question: str,
    top_k: int = 3,
    category_filter: str = None,
    chat_history: list[dict] = None
) -> Tuple[Generator, list[dict]]:
    """
    Streams the Gemini response token-by-token.
    Returns: (text_generator, sources_list)
    """
    context_str, sources = retrieve_relevant_chunks(question, top_k, category_filter)

    if not context_str:
        def empty_generator():
            yield "Sorry, I could not find any relevant PUMA policy information for your query. Please contact the PUMA People & Culture team directly at people.culture@puma.com or visit MyHR (https://myhr.puma.com)."
        return empty_generator(), []


    system_instruction, prompt = build_prompt(question, context_str, chat_history)

    stream = client.models.generate_content_stream(
        model="gemini-3.8-flash",
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
        )
    )

    def text_generator():
        for chunk in stream:
            if chunk.text:
                yield chunk.text

    return text_generator(), sources


def query_rag(
    question: str,
    top_k: int = 3,
    category_filter: str = None,
    chat_history: list[dict] = None
) -> dict:
    """Non-streaming query response for direct evaluations."""
    context_str, sources = retrieve_relevant_chunks(question, top_k, category_filter)

    if not context_str:
        return {
            "answer": "Sorry, I could not find any relevant PUMA policy information for your query. Please contact the PUMA People & Culture team directly at people.culture@puma.com or visit MyHR (https://myhr.puma.com).",
            "sources": []
        }


    system_instruction, prompt = build_prompt(question, context_str, chat_history)

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
        )
    )

    return {
        "answer": response.text.strip(),
        "sources": sources
    }

