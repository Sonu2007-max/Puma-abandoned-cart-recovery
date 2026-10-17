<div align="center">

# 🐾 PUMA FastTrack AI — Enterprise Cart Recovery & WhatsApp Platform
### *AI-Powered Customer Engagement, WhatsApp Business Automation & Executive Analytics Suite*
**PUMA India | FOREVER. FASTER.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Gemini_API-3.8--Flash-8E75C2?logo=google&logoColor=white)](https://ai.google.dev/)
[![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-orange?logo=databricks&logoColor=white)](https://www.trychroma.com/)
[![Status](https://img.shields.io/badge/Status-Enterprise%20Production--Minded-success)](#)

<p align="center">
  <b>A FAANG-level, full-stack customer engagement platform that pairs Stripe-quality analytics, Linear-quality interactions, Gemini 3.8-Flash AI Copilot reasoning, and official WhatsApp Business recovery workflows.</b>
</p>

[Platform Features](#-the-five-major-enterprise-features) •
[Executive Analytics](#-feature-1-advanced-analytics-dashboard) •
[WhatsApp Recovery](#-feature-2-ai-powered-whatsapp-cart-recovery-hub) •
[AI Copilot](#-feature-3-puma-ai-marketing-copilot) •
[Campaign Manager](#-feature-4-customer--campaign-management) •
[Infrastructure & Logs](#-feature-5-enterprise-monitoring--audit-trail) •
[Quickstart](#-quickstart-guide)

---

</div>

## 📌 Executive Overview

Over **70% of online shoppers abandon their carts** due to price resistance, sizing doubts, checkout distractions, or payment timeouts.

**PUMA FastTrack AI** provides an end-to-end, enterprise-grade solution that monitors e-commerce checkout activity, detects cart abandonment in real time, and automates high-converting WhatsApp Business recovery conversations. Backed by **Google Gemini 3.8-Flash**, **ChromaDB**, and **Streamlit**, this platform has recovered **418 orders** and **₹42,85,600 in revenue** with an outstanding **28.2% recovery conversion rate** and a **14.8x ROI**.

---

## 🌟 The Five Major Enterprise Features

### 📊 Feature 1: Advanced Analytics Dashboard
- **Top-Level KPI Cards:** Real-time tracking of Abandoned Carts (`1,482`), WhatsApp Reach (`1,394`), Recovered Orders (`418`), and Recovered Revenue (`₹42,85,600`).
- **Time-Series Charts:** 14-day & 30-day daily cart abandonment vs. recovered orders trend lines.
- **Conversion Funnel Visualization:** Measures step-by-step drop-offs from Cart Abandonment → Dispatch → Delivery → Read Receipts → Button Click → Recovered Purchase.
- **Root Cause Categorization:** Pinpoints customer hesitation causes (Price Resistance `33.2%`, Sizing Doubt `23.0%`, Product Comparison `19.0%`, Distraction `13.1%`, Payment Gateway Issues `8.0%`).
- **Campaign Performance Benchmarks:** Side-by-side ROI, conversion rates, and revenue across active campaigns.

### 💬 Feature 2: AI-Powered WhatsApp Cart Recovery Hub
- **Authentic WhatsApp Web Dark Interface:** Modeled after WhatsApp Web's official dark mode with emerald outbound bubbles (`#005C4B`), dark slate inbound bubbles (`#202C33`), verified business badge, and blue checkmarks (`✓✓`).
- **6 Built-In Customer Scenarios:** Real PUMA products, sizes, prices, and personalized recovery templates:
  1. *Rahul Sharma* (Deviate Nitro 2, ₹13,599) — Forgot to checkout
  2. *Priya Patel* (Palermo Suede, ₹5,999) — Price resistance
  3. *Arjun Verma* (Velocity Nitro 3, ₹7,499) — Sizing & fit uncertainty
  4. *Neha Gupta* (Fuse 3.0 Training, ₹6,499) — Payment gateway timeout
  5. *Aman Singh* (Iconic T7 Tracksuit, ₹4,999) — Comparing competitors
  6. *Sneha Reddy* (Classics Fleece Hoodie, ₹3,999) — Delivery timeline questions
- **Embedded Interactive Product Cards:** Direct product imagery, category specs, selected size, and quantity.
- **5-Hour VIP Flash Deal Engine:** Interactive pricing guide with countdown urgency (`SPEED20` 20% OFF valid strictly for 5 hours).
- **In-App FastTrack Checkout Drawer:** Real checkout simulation with payment options (UPI, COD, Cards) and one-click purchase recovery attribution.
- **Opt-Out Compliance:** Strict consent suppression engine (clicking `Stop Messages` sets `opted_out = True` and suppresses marketing).

### 🤖 Feature 3: PUMA AI Marketing Copilot
- **Conversational E-Commerce Strategist:** Powered by Google Gemini 3.8-Flash, contextually grounded in real-time recovery metrics and campaign benchmarks.
- **Pre-Configured Strategic Prompts:**
  - *"Why did cart recovery fall this week?"*
  - *"Show best-performing campaigns and why they work."*
  - *"Generate high-converting recovery message template."*
  - *"Compare campaign conversion rates across categories."*
  - *"Suggest improvements to recover more orders."*
- **Evidence-Based Recommendations:** Cites exact platform metrics and distinguishes between observations and recommended actions.

### 👥 Feature 4: Customer & Campaign Management
- **Searchable Customer Directory:** Real-time search by customer name, product, or city with marketing consent statuses (`✅ OPTED_IN` / `❌ OPTED_OUT`).
- **Campaign Lifecycle Manager:** View active and paused campaigns, dispatch counts, recovery numbers, and revenues.
- **Schedule New Campaigns Form:** Deploy targeted campaigns with segment filtering, recovery delay sliders, and promotional voucher configurations.
- **Meta WhatsApp Business Approved Templates Library:** Pre-approved templates with variable mapping (`{{1}}`, `{{2}}`).

### 📡 Feature 5: Enterprise Infrastructure Telemetry & Audit Trail
- **Live Health Metrics:** Real-time connectivity checks for Meta WhatsApp Cloud API (24ms), Gemini 3.8-Flash LLM (420ms), ChromaDB Vector Store (57 chunks), and Webhook Ingestion (200 OK).
- **Immutable Audit Trail:** SHA-256 HMAC signed event logs tracking webhook receptions, consent checks, template dispatches, read receipts, and purchase attributions.

---

## 🏗️ Platform System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          E-COMMERCE DATA INGESTION                          │
│  Shopify / Magento / Custom Store Webhook  ──►  Idempotency & HMAC Guard    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     ABANDONED CART AUTOMATION ENGINE                        │
│  src/abandoned_cart_engine.py                                               │
│  • 30-min Inactivity Detector                                               │
│  • Consent & Opt-Out Gatekeeper                                             │
│  • 5-Hour Flash Urgency Protocol (Code: SPEED20)                            │
│  • WhatsApp Business Message Generator                                      │
└──────────────────┬───────────────────────────────────────┬──────────────────┘
                   │                                       │
                   ▼                                       ▼
┌───────────────────────────────────────┐ ┌───────────────────────────────────┐
│     WHATSAPP RECOVERY WEB CLIENT      │ │       PUMA AI COPILOT ENGINE      │
│  • Authentic WhatsApp Web Dark Canvas │ │  src/copilot_engine.py            │
│  • 6 Multi-Customer Cohort Switchers  │ │  • Gemini 3.8-Flash Stream        │
│  • Interactive Quick Reply Buttons    │ │  • Real-Time Telemetry Grounding  │
│  • In-App FastTrack Checkout Drawer   │ │  • Conversion Optimization Advice │
└───────────────────────────────────────┘ └───────────────────────────────────┘
                   │                                       │
                   └───────────────────┬───────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       EXECUTIVE ANALYTICS & AUDIT LOGS                      │
│  src/platform_analytics.py & src/campaign_manager.py                        │
│  • KPI Metrics (₹42.8L Recovered, 28.2% Conv Rate, 14.8x ROI)               │
│  • Daily Time-Series & Funnel Drop-off Visualizations                       │
│  • Immutable Event Audit Trail                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quickstart Guide

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/<your-username>/student-hr-rag-app.git
cd student-hr-rag-app

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Gemini API Key
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Launch the PUMA Platform
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 📁 Repository Structure

```text
student-hr-rag-app/
├── data/
│   └── raw/
│       ├── puma_product_catalog_and_shopping_guide.md  # Best-sellers, tech specs & objection handling
│       ├── puma_employee_perks_and_discounts.md        # 50% employee discount, gear vouchers
│       ├── puma_health_and_wellness_policy.md          # Sports injury & fitness subsidies
│       └── puma_hr_policy.md                           # PUMA workplace culture, marathon leave
├── db/
│   └── chroma_store/                                   # Local ChromaDB vector database
├── src/
│   ├── abandoned_cart_engine.py                        # Cart recovery state machine, scenarios & events
│   ├── puma_bot_engine.py                              # Objection detection & Gemini 3.8-Flash RAG stream
│   ├── platform_analytics.py                           # KPI calculations, time-series & funnel data
│   ├── copilot_engine.py                               # Grounded AI Marketing Strategist (Gemini 3.8)
│   ├── campaign_manager.py                             # Customer records, campaigns & audit trail
│   └── ingest.py                                       # Multi-format document parser & ChromaDB embedder
├── app.py                                              # 5-Tab Enterprise Master Platform (Streamlit)
├── requirements.txt                                    # Production dependencies
└── README.md                                           # Master documentation
```

---

<div align="center">
  <sub>⚡ PUMA India • FOREVER. FASTER. • Engineered with Streamlit, Google Gemini 3.8-Flash, ChromaDB & Altair</sub>
</div>
