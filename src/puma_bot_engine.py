"""
PUMA WhatsApp RAG Engine
Powers the official PUMA WhatsApp conversational experience:
1. Semantic search over PUMA product catalog, pricing, policies & perks via ChromaDB
2. AI Objection & Purchase Hesitation Detection (detects why customer did not buy)
3. Conversational real-time token streaming with Gemini 3.8-Flash in authentic WhatsApp tone
"""

import os
import re
from pathlib import Path
from typing import Generator, Tuple, Dict, Any
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
    """Retrieve the PUMA collection from ChromaDB."""
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


def detect_customer_objection(message: str) -> Dict[str, Any]:
    """
    Analyzes user message to detect purchase hesitation / why they didn't buy:
    - Price / Too expensive
    - Sizing & Fit uncertainty
    - Product choice confusion
    - Trust / Return fears
    - Procrastination / Cart abandonment
    """
    m = message.lower()

    # 1. Price / Cost Objections
    if any(k in m for k in [
        "expensive", "mehenga", "mehanga", "price", "cost", "budget", "discount", "coupon",
        "offer", "cheaper", "sasta", "afford", "high price", "paiso", "paisa", "rupees", "emi"
    ]):
        return {
            "detected": True,
            "category": "Price Resistance",
            "icon": "🏷️",
            "badge_color": "#EF4444",
            "root_cause": "Customer perceives product as high-investment or is seeking a deal.",
            "bot_strategy": "Highlight cost-per-km durability + Offer 15% VIP code *PUMAFAST15* or No-Cost EMI (₹2,999/mo).",
            "suggested_action": "Unlock 15% Coupon"
        }

    # 2. Sizing / Fit Hesitation
    if any(k in m for k in [
        "size", "fit", "fitting", "tight", "loose", "wide feet", "chhota", "bada",
        "measure", "uk 7", "uk 8", "uk 9", "uk 10", "shoe size", "exchange", "fit aayega"
    ]):
        return {
            "detected": True,
            "category": "Sizing & Fit Uncertainty",
            "icon": "📏",
            "badge_color": "#F59E0B",
            "root_cause": "Uncertainty about online shoe sizing or wide-foot compatibility.",
            "bot_strategy": "Explain true-to-UK sizing + Reassure with Free Doorstep Size Exchange (courier brings new size & collects old for ₹0).",
            "suggested_action": "View Sizing Guide"
        }

    # 3. Model Confusion / Choice Overload
    if any(k in m for k in [
        "which one", "difference", "confused", "suggest", "recommend", "deviate vs",
        "velocity vs", "palermo vs", "better", "best shoe", "marathon vs daily", "kaun sa lu"
    ]):
        return {
            "detected": True,
            "category": "Product Indecision",
            "icon": "🤔",
            "badge_color": "#3B82F6",
            "root_cause": "Overwhelmed by multiple options (Deviate Nitro vs Velocity Nitro vs Palermo).",
            "bot_strategy": "Provide quick 10-second buyer guide matching shoe tech directly to their running or style goal.",
            "suggested_action": "Compare Models"
        }

    # 4. Procrastination / Cart Drop-off
    if any(k in m for k in [
        "later", "baad me", "sochunga", "thinking", "not now", "check later", "kal",
        "next month", "drop", "hold", "just looking", "dekh raha hu"
    ]):
        return {
            "detected": True,
            "category": "Cart Abandonment / Procrastination",
            "icon": "⏳",
            "badge_color": "#8B5CF6",
            "root_cause": "Delaying decision without a compelling immediate reason to complete order.",
            "bot_strategy": "Create soft urgency (e.g. 'Only 3 pairs left in your size in central warehouse') + Offer to hold cart for 24h.",
            "suggested_action": "Hold My Size (24h)"
        }

    # 5. Risk & Return / Authenticity Concern
    if any(k in m for k in [
        "return", "refund", "original", "fake", "duplicate", "genuine", "guarantee",
        "warranty", "trust", "cod", "cash on delivery", "kharaab nikla"
    ]):
        return {
            "detected": True,
            "category": "Trust & Return Anxiety",
            "icon": "🛡️",
            "badge_color": "#10B981",
            "root_cause": "Fear of getting wrong/faulty item or having money locked in return disputes.",
            "bot_strategy": "Highlight 100% Genuine Direct PUMA guarantee + 30-Day Hassle-Free No-Questions Return with COD.",
            "suggested_action": "Check 30-Day Policy"
        }

    return {
        "detected": False,
        "category": "High Purchase Intent / Exploration",
        "icon": "⚡",
        "badge_color": "#10B981",
        "root_cause": "Customer exploring PUMA catalog, tech specs, or company benefits.",
        "bot_strategy": "Deliver prompt, energetic product guidance and highlight key athletic features (NITRO Foam, PUMAGRIP).",
        "suggested_action": "Show PUMA Best-Sellers"
    }


def retrieve_relevant_chunks(
    question: str,
    top_k: int = 3,
    category_filter: str = None
) -> Tuple[str, list[dict]]:
    """
    Vector search in ChromaDB across PUMA documents with category filtering.
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
        category = meta.get("category", "PUMA Knowledge")
        relevance = "High" if dist < 0.6 else ("Medium" if dist < 0.9 else "Low")

        context_blocks.append(
            f"--- [Doc: {source_name} | Category: {category} | Chunk #{chunk_id}] ---\n{doc}"
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


def build_whatsapp_prompt(
    question: str,
    context_str: str,
    chat_history: list[dict] = None,
    objection_info: dict = None
) -> tuple[str, str]:
    """
    Constructs prompt tailored for official PUMA WhatsApp conversational bot.
    """
    objection_guidance = ""
    if objection_info and objection_info.get("detected"):
        objection_guidance = f"""
SPECIAL SALES RECOVERY DIRECTIVE:
Customer Hesitation Detected: '{objection_info['category']}'.
Root Cause: {objection_info['root_cause']}
Tactic: {objection_info['bot_strategy']}
Address this hesitation naturally, warmly, and helpfully right in your WhatsApp reply so the customer feels completely confident to purchase!
"""

    system_instruction = f"""You are the official PUMA WhatsApp Assistant (PUMA India | FOREVER. FASTER. 🐾).
You assist customers, runners, sneakerheads, and PUMA employees directly on WhatsApp.

WHATSAPP TONE & BEHAVIOR:
1. Speak in an authentic, athletic, warm, and helpful WhatsApp tone.
2. Use natural formatting:
   - *bold* for product names, prices, and coupon codes.
   - Bullet points for specs or comparisons.
   - Emojis (👟, 🐾, ⚡, 🔥, 📦, 🏷️) naturally, as an official sports brand assistant.
3. If the user writes in Hinglish or Hindi, answer fluently in friendly Hinglish (e.g., "Arre don't worry, PUMA pe 30-day free doorstep exchange hai! 👟").
4. If the customer hesitates to buy (e.g. price, size, doubt, return fear), actively address it using official PUMA policies (e.g., VIP discount code *PUMAFAST15* for 15% off, 3-month No-Cost EMI, free doorstep size exchange, 30-day refund).
5. Ground all facts (prices, technologies like NITRO Foam / INNOPLATE, policies, discounts) strictly on the provided PUMA context.
6. Keep messages clean, punchy, and mobile-friendly—avoid giant blocks of dry corporate text.
{objection_guidance}
"""

    history_str = ""
    if chat_history:
        recent = chat_history[-6:]
        formatted_history = []
        for msg in recent:
            role = "Customer" if msg["role"] == "user" else "PUMA WhatsApp Assistant"
            formatted_history.append(f"{role}: {msg['content']}")
        if formatted_history:
            history_str = "Recent WhatsApp Chat:\n" + "\n".join(formatted_history) + "\n\n"

    prompt = f"""{history_str}Official PUMA Context:
{context_str}

Customer WhatsApp Message:
{question}

PUMA WhatsApp Response:"""

    return system_instruction, prompt


def query_puma_whatsapp_stream(
    question: str,
    top_k: int = 3,
    category_filter: str = None,
    chat_history: list[dict] = None
) -> Tuple[Generator, list[dict], dict]:
    """
    1. Runs objection detection (why the user hesitated/didn't buy).
    2. Retrieves matching PUMA catalog & policy chunks.
    3. Streams the response in WhatsApp style.
    Returns: (stream_generator, sources, objection_info)
    """
    objection_info = detect_customer_objection(question)
    context_str, sources = retrieve_relevant_chunks(question, top_k, category_filter)

    if not context_str:
        def empty_generator():
            yield "Hey there! 🐾 Thanks for reaching out to *PUMA WhatsApp Support*. I couldn't find exact details for this in our current catalog or policy handbooks. Feel free to connect directly with our PUMA team at *customercare@puma.com* or call our toll-free line *1800-102-PUMA*! ⚡"
        return empty_generator(), [], objection_info

    system_instruction, prompt = build_whatsapp_prompt(
        question=question,
        context_str=context_str,
        chat_history=chat_history,
        objection_info=objection_info
    )

    stream = client.models.generate_content_stream(
        model="gemini-3.8-flash",
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3,
        )
    )

    def text_generator():
        for chunk in stream:
            if chunk.text:
                yield chunk.text

    return text_generator(), sources, objection_info
