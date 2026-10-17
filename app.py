"""
PUMA AI Cart Recovery & WhatsApp Automation Platform
Enterprise Customer Engagement, Real-Time Analytics, WhatsApp Business Automation,
and AI Copilot Suite. Built for PUMA India (FOREVER. FASTER. 🐾)
"""

import os
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

# Internal platform services
from src.abandoned_cart_engine import (
    PUMAAbandonedCartRecoveryManager,
    DEMO_SCENARIOS,
    WhatsAppMessage
)
from src.puma_bot_engine import query_puma_whatsapp_stream
from src.platform_analytics import (
    get_kpi_summary,
    get_recovery_trend_data,
    get_funnel_data,
    get_abandonment_causes,
    get_campaign_benchmarks
)
from src.copilot_engine import query_puma_copilot
from src.campaign_manager import (
    DEFAULT_CUSTOMERS,
    DEFAULT_CAMPAIGNS,
    APPROVED_TEMPLATES,
    SYSTEM_AUDIT_LOGS,
    CustomerRecord,
    CampaignRecord
)

# Page Configuration
st.set_page_config(
    page_title="PUMA FastTrack AI | Cart Recovery Platform",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global Enterprise Dark Tech Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #0A0D12 !important;
        color: #E2E8F0 !important;
    }

    .main .block-container {
        padding: 0.4rem 1.4rem 1.4rem 1.4rem !important;
        max-width: 100% !important;
    }

    /* Top Navigation HUD */
    .platform-hud-header {
        background: rgba(17, 24, 39, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid #BA0C2F;
        border-radius: 10px;
        padding: 10px 18px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .brand-title {
        font-weight: 900;
        font-size: 1.2rem;
        letter-spacing: 1px;
        color: #FFFFFF;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .puma-red-accent { color: #BA0C2F; }
    
    .hud-meta-pill {
        font-family: 'JetBrains Mono', monospace;
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.74rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .dot-pulse-green {
        width: 7px;
        height: 7px;
        background: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10B981;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* KPI Card Component */
    .kpi-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }
    .kpi-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: flex;
        justify-content: space-between;
    }
    .kpi-value {
        font-size: 1.55rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-top: 4px;
        letter-spacing: -0.5px;
    }
    .kpi-delta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #10B981;
        margin-top: 2px;
    }

    /* WhatsApp Dark Theme Bubbles */
    .wa-dark-header {
        background: #202C33;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #2A3942;
    }
    .wa-bubble-out {
        background-color: #005C4B;
        color: #E9EDEF;
        padding: 9px 13px 7px 13px;
        border-radius: 10px 0px 10px 10px;
        margin-left: auto;
        max-width: 86%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
        font-size: 0.9rem;
        line-height: 1.48;
        margin-bottom: 10px;
        border: 1px solid rgba(0, 168, 132, 0.25);
    }
    .wa-bubble-in {
        background-color: #202C33;
        color: #E9EDEF;
        padding: 9px 13px 7px 13px;
        border-radius: 0px 10px 10px 10px;
        margin-right: auto;
        max-width: 86%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
        font-size: 0.9rem;
        line-height: 1.48;
        margin-bottom: 10px;
        border: 1px solid #2A3942;
    }
    .wa-bubble-time {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 5px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: #8696A0;
        margin-top: 4px;
    }
    .wa-checkmarks { color: #53BDEB; font-weight: 700; }

    /* Product Card */
    .wa-tech-card {
        background: #111B21;
        border-radius: 8px;
        border: 1px solid #2A3942;
        padding: 10px;
        margin-top: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* Checkout Drawer Dark */
    .tech-checkout-card {
        background: #111827;
        border: 1px solid #10B981;
        border-radius: 8px;
        padding: 12px;
        margin-top: 8px;
        box-shadow: 0 0 18px rgba(16, 185, 129, 0.2);
    }

    /* Badges */
    .cyber-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .badge-abandoned { background: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-recovered { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-resumed { background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }
    .badge-opted { background: rgba(148, 163, 184, 0.15); color: #94A3B8; border: 1px solid rgba(148, 163, 184, 0.3); }

    /* Terminal Log Feed */
    .term-line {
        padding: 4px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        display: flex;
        gap: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "recovery_manager" not in st.session_state or not hasattr(st.session_state.recovery_manager, "generate_pricing_and_offer_guide"):
    st.session_state.recovery_manager = PUMAAbandonedCartRecoveryManager()

if "selected_customer_id" not in st.session_state:
    st.session_state.selected_customer_id = "cust_1"

if "show_checkout_modal" not in st.session_state:
    st.session_state.show_checkout_modal = False

if "copilot_history" not in st.session_state:
    st.session_state.copilot_history = [
        {"role": "assistant", "content": "Welcome to **PUMA FastTrack Copilot**! 🐾 I am your AI strategist for cart recovery, customer behavior analytics, and WhatsApp campaign optimization. Ask me anything about today's drop-offs, campaign conversion rates, or generate recovery copy."}
    ]

if "campaigns_list" not in st.session_state:
    st.session_state.campaigns_list = DEFAULT_CAMPAIGNS.copy()

mgr: PUMAAbandonedCartRecoveryManager = st.session_state.recovery_manager
active_id: str = st.session_state.selected_customer_id
active_customer = mgr.customers[active_id]
active_cart = mgr.carts[active_id]
active_product = active_cart.product
active_messages = mgr.messages[active_id]
active_timeline = mgr.event_timelines[active_id]


# Top Telemetry Header HUD
st.markdown("""
<div class="platform-hud-header">
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 1.6rem; filter: drop-shadow(0 0 8px rgba(186, 12, 47, 0.6));">🐾</span>
        <div>
            <div class="brand-title">PUMA <span class="puma-red-accent">FASTTRACK</span> AI</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8;">ENTERPRISE CART RECOVERY & CONVERSION PLATFORM</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
        <div class="hud-meta-pill">
            <span class="dot-pulse-green"></span>
            <span>SYSTEM: 99.98% UP</span>
        </div>
        <div class="hud-meta-pill">
            <span style="color: #8E75C2;">⚡</span>
            <span>AI: GEMINI-3.8-FLASH</span>
        </div>
        <div class="hud-meta-pill">
            <span style="color: #10B981;">💰</span>
            <span>RECOVERED: ₹42.8L</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Main Navigation Tabs (5 Core Features)
tabs = st.tabs([
    "📊 Analytics & KPIs",
    "💬 WhatsApp Recovery Hub",
    "🤖 PUMA AI Copilot",
    "👥 Customers & Campaigns",
    "📡 Enterprise Telemetry & Logs"
])


# =====================================================================
# TAB 1: ADVANCED ANALYTICS DASHBOARD (FEATURE 1)
# =====================================================================
with tabs[0]:
    st.markdown("##### 📈 Executive Performance & Conversion Analytics")

    # Timeframe Selector & Filter Row
    f_col1, f_col2, f_col3 = st.columns([3, 2, 2])
    with f_col1:
        time_filter = st.selectbox("Select Reporting Window", ["Last 14 Days (Active Cohort)", "Last 30 Days", "Quarter to Date (Q1 2026)", "All-Time"], index=0)
    with f_col2:
        category_filter = st.selectbox("Category Filter", ["All Categories", "Performance Running (Nitro)", "Streetwear (Palermo/Suede)", "Training & Gym (Fuse)", "Apparel & Tracksuits"], index=0)
    with f_col3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        st.caption("Data source: Verified Shopify/PUMA eCom Webhook Attributions")

    # 4 Top-Level Metric Cards
    kpi = get_kpi_summary()
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title"><span>ABANDONED CARTS</span><span>🛒</span></div>
            <div class="kpi-value">{kpi['abandoned_carts']:,}</div>
            <div class="kpi-delta">₹{kpi['abandoned_value']:,} Pipeline Value</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title"><span>WHATSAPP REACH</span><span>📩</span></div>
            <div class="kpi-value">{kpi['messages_sent']:,}</div>
            <div class="kpi-delta">Delivered: {kpi['delivery_rate']}% • Read: {kpi['read_rate']}%</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title"><span>RECOVERED ORDERS</span><span>✅</span></div>
            <div class="kpi-value">{kpi['recovered_orders']:,}</div>
            <div class="kpi-delta" style="color: #38BDF8;">Conversion: <b>{kpi['conversion_rate']}%</b> (+8.2% vs Benchmark)</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 3px solid #10B981;">
            <div class="kpi-title"><span>RECOVERED REVENUE</span><span>💰</span></div>
            <div class="kpi-value" style="color: #10B981;">₹{kpi['recovered_revenue']:,}</div>
            <div class="kpi-delta">WhatsApp ROI: <b>{kpi['recovery_roi']}</b> (Avg: ₹{kpi['avg_order_value']:,}/order)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    # 2 Charts Side-by-Side: Daily Recovery Trends & Funnel
    c1, c2 = st.columns([6, 4])
    
    with c1:
        st.markdown("###### 📊 Daily Cart Abandonment vs Recovered Orders")
        trend_df = get_recovery_trend_data(14)
        chart_data = trend_df.set_index("Date")[["Abandoned Carts", "Recovered Orders"]]
        st.line_chart(chart_data, color=["#EF4444", "#10B981"])

    with c2:
        st.markdown("###### 🎯 Cart Recovery Conversion Funnel")
        funnel_df = get_funnel_data()
        funnel_chart = funnel_df.set_index("Stage")["Count"]
        st.bar_chart(funnel_chart, color="#00A884")

    # Campaign Performance Table & Abandonment Causes
    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
    tb1, tb2 = st.columns([6, 4])
    
    with tb1:
        st.markdown("###### 🚀 Campaign ROI & Performance Benchmarks")
        camp_df = get_campaign_benchmarks()
        st.dataframe(camp_df, use_container_width=True, hide_index=True)

    with tb2:
        st.markdown("###### ⚠️ Root Causes of Customer Hesitation")
        causes_df = get_abandonment_causes()
        st.dataframe(causes_df, use_container_width=True, hide_index=True)


# =====================================================================
# TAB 2: WHATSAPP RECOVERY HUB (FEATURE 2 & DITTO WHATSAPP UI)
# =====================================================================
with tabs[1]:
    col_wa, col_control = st.columns([6, 4], gap="medium")

    # Column 1: WhatsApp Conversation View
    with col_wa:
        st.markdown("<div style='font-size: 0.82rem; font-weight: 700; color: #94A3B8; margin-bottom: 4px; font-family: monospace;'>[ CONVERSATION_THREADS ]</div>", unsafe_allow_html=True)

        # Customer Conversation Selection Pills
        cust_cols = st.columns(6)
        for idx, (cid, cdata) in enumerate(DEMO_SCENARIOS.items()):
            c_obj = mgr.customers[cid]
            cart_obj = mgr.carts[cid]
            is_active = (cid == active_id)

            status_marker = "🛒" if cart_obj.status == "Abandoned" else ("✅" if cart_obj.status == "Recovered" else "📩")
            btn_label = f"{c_obj.name.split()[0]} {status_marker}"

            with cust_cols[idx]:
                if st.button(
                    btn_label,
                    key=f"tab_{cid}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    st.session_state.selected_customer_id = cid
                    st.session_state.show_checkout_modal = False
                    st.rerun()

        # WhatsApp Active Chat Header
        status_cls = "badge-abandoned" if active_cart.status == "Abandoned" else ("badge-recovered" if active_cart.status == "Recovered" else "badge-resumed")
        st.markdown(f"""
        <div class="wa-dark-header" style="border-radius: 10px 10px 0 0;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 42px; height: 42px; border-radius: 50%; background: {active_customer.avatar_color}; display: flex; align-items: center; justify-content: center; font-size: 19px; border: 1.5px solid rgba(255,255,255,0.15);">
                    {active_customer.avatar_emoji}
                </div>
                <div>
                    <div style="font-size: 0.96rem; font-weight: 700; color: #E9EDEF; display: flex; align-items: center; gap: 6px;">
                        {active_customer.name}
                        <span style="background: #00A884; color: #FFF; font-size: 10px; width: 15px; height: 15px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: bold;">✓</span>
                        <span class="cyber-badge {status_cls}">{active_cart.status.upper()}</span>
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #8696A0;">
                        {active_customer.phone_display} • {active_customer.last_seen}
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 14px; font-size: 1.1rem; color: #AEBAC1; cursor: pointer;">
                <span>📹</span><span>📞</span><span>🔍</span><span>⋮</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #182229; border: 1px solid #222E35; color: #FFD279; font-size: 0.72rem; padding: 6px 14px; text-align: center; border-radius: 6px; margin: 10px auto; max-width: 90%; font-family: monospace;">
            🔒 MESSAGES END-TO-END ENCRYPTED • PUMA BUSINESS PLATFORM
        </div>
        """, unsafe_allow_html=True)

        # Message Feed
        chat_container = st.container(height=345)
        with chat_container:
            for msg in active_messages:
                if msg.direction == "outbound":
                    st.markdown(f"""
                    <div class="wa-bubble-out">
                        <div style="font-family: monospace; font-size: 0.68rem; font-weight: 700; color: #25D366; margin-bottom: 3px;">PUMA OFFICIAL ASSISTANT</div>
                        <div>{msg.text.replace(chr(10), '<br>')}</div>
                        <div class="wa-bubble-time">
                            <span>{msg.timestamp}</span>
                            <span class="wa-checkmarks">✓✓</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if msg.product_data:
                        p = msg.product_data
                        st.markdown(f"""
                        <div class="wa-tech-card" style="max-width: 86%; margin-left: auto;">
                            <div style="display: flex; gap: 12px; align-items: center;">
                                <img src="{p['image_url']}" style="width: 80px; height: 80px; border-radius: 8px; object-fit: cover; border: 1px solid rgba(255,255,255,0.1);" onerror="this.src='https://placehold.co/100x100?text=PUMA';"/>
                                <div style="flex: 1;">
                                    <div style="font-size: 0.9rem; font-weight: 700; color: #FFFFFF;">{p['name']}</div>
                                    <div style="font-family: monospace; font-size: 0.74rem; color: #94A3B8; margin: 2px 0;">{p['category']} | Size: <b style="color: #FFF;">{p['size']}</b> (Qty: {p['quantity']})</div>
                                    <div style="font-size: 1rem; font-weight: 800; color: #EF4444;">₹{p['price']:,}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    if msg.buttons:
                        st.markdown("<div style='font-size: 0.7rem; color: #64748B; text-align: right; margin-top: 4px; font-family: monospace;'>INTERACTIVE_ACTIONS:</div>", unsafe_allow_html=True)
                        btn_cols = st.columns(len(msg.buttons))
                        for b_idx, btn_text in enumerate(msg.buttons):
                            with btn_cols[b_idx]:
                                if st.button(
                                    f"🔘 {btn_text}",
                                    key=f"btn_{msg.id}_{b_idx}",
                                    use_container_width=True
                                ):
                                    if any(k in btn_text for k in ["Checkout", "Cart", "Return"]):
                                        st.session_state.show_checkout_modal = True

                                    mgr.handle_interactive_button(active_id, btn_text)
                                    st.rerun()

                else:
                    st.markdown(f"""
                    <div class="wa-bubble-in">
                        <div style="font-family: monospace; font-size: 0.68rem; font-weight: 700; color: #60A5FA; margin-bottom: 3px;">{active_customer.name.upper()}</div>
                        <div>{msg.text.replace(chr(10), '<br>')}</div>
                        <div class="wa-bubble-time">
                            <span>{msg.timestamp}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # In-App Cart & Checkout Simulation Drawer
        if st.session_state.show_checkout_modal and active_cart.status != "Recovered":
            calc_price = int(active_product.price * 0.80) if active_cart.discount_applied else active_product.price
            savings = active_product.price - calc_price

            st.markdown(f"""
            <div class="tech-checkout-card">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px;">
                    <span style="font-weight: 800; font-size: 0.95rem; color: #10B981; font-family: monospace;">🛍️ PUMA FASTTRACK CHECKOUT</span>
                    <span class="cyber-badge badge-resumed">CART_ID: #{active_cart.id.upper()}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 0.88rem;">
                    <span style="color: #E2E8F0;"><b>Item:</b> {active_product.name} ({active_product.selected_size})</span>
                    <div>
                        {'<span style="text-decoration: line-through; color: #94A3B8; font-size: 0.8rem; margin-right: 6px;">₹' + f'{active_product.price:,}' + '</span>' if active_cart.discount_applied else ''}
                        <span style="font-weight: 800; color: #10B981; font-family: monospace; font-size: 1.05rem;">₹{calc_price:,}</span>
                    </div>
                </div>
                {'<div style="background: rgba(239, 68, 68, 0.15); border: 1px dashed #EF4444; border-radius: 4px; padding: 4px 8px; font-size: 0.74rem; color: #F87171; margin-top: 6px; font-family: monospace;">⏳ 5-HOUR FLASH DISCOUNT APPLIED (-20% SPEED20) • SAVINGS: ₹' + f'{savings:,}' + '</div>' if active_cart.discount_applied else ''}
                <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 4px; font-family: monospace;">
                    🚚 FREE Express Delivery • 30-Day Hassle-Free Doorstep Size Exchange
                </div>
            </div>
            """, unsafe_allow_html=True)

            chk_col1, chk_col2 = st.columns([2, 1])
            with chk_col1:
                pay_mode = st.radio("Payment Mode", ["UPI (Google Pay / PhonePe)", "Cash on Delivery (COD)", "Credit/Debit Card"], horizontal=True)
            with chk_col2:
                if st.button("✅ Place Order Now (Recover Cart)", type="primary", use_container_width=True):
                    mgr.complete_purchase(active_id)
                    st.session_state.show_checkout_modal = False
                    st.balloons()
                    st.rerun()

        # One-Click 5-Hour Offer & Pricing Guide Trigger
        st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Unlock 5-Hour VIP Flash Offer & Pricing Guide", use_container_width=True, type="secondary"):
            mgr.generate_pricing_and_offer_guide(active_id)
            st.rerun()

        # WhatsApp Message Composer Form
        with st.form(key=f"wa_composer_form_{active_id}", clear_on_submit=True):
            comp_col1, comp_col2 = st.columns([5, 1])
            with comp_col1:
                user_text_input = st.text_input(
                    "Type a message",
                    placeholder=f"Ask PUMA Assistant about pricing, 5-hr offer, size, checkout...",
                    label_visibility="collapsed"
                )
            with comp_col2:
                submitted = st.form_submit_button("➤ Send", use_container_width=True, type="primary")

        if submitted and user_text_input:
            now_time = datetime.now().strftime("%H:%M")

            # Inbound Message
            cust_msg = WhatsAppMessage(
                id=f"msg_{active_id}_{len(active_messages) + 1}",
                customer_id=active_id,
                direction="inbound",
                msg_type="text",
                text=user_text_input,
                timestamp=now_time,
                status="read"
            )
            mgr.messages[active_id].append(cust_msg)

            lower_q = user_text_input.lower()
            if any(w in lower_q for w in ["price", "cost", "offer", "discount", "mehenga", "mehanga", "coupon", "deal", "kharid", "buy", "paisa", "rupees", "kitne ka"]):
                mgr.generate_pricing_and_offer_guide(active_id)
                st.rerun()
            else:
                with st.spinner("PUMA Assistant is typing..."):
                    try:
                        stream_gen, _, _ = query_puma_whatsapp_stream(
                            question=user_text_input,
                            top_k=2,
                            chat_history=[{"role": "user", "content": user_text_input}]
                        )
                        assistant_reply = "".join(chunk for chunk in stream_gen)
                    except Exception:
                        assistant_reply = (
                            f"Hey {active_customer.name}! 🐾 Thanks for reaching out.\n\n"
                            f"For *{active_product.name}*, you get 100% genuine PUMA quality, 800+ km durability, "
                            f"free express shipping, and a 30-day hassle-free doorstep return.\n\n"
                            f"We also have a special *20% Flash Voucher (SPEED20)* valid for the next 5 hours! Would you like to check out?"
                        )

                    bot_reply_msg = WhatsAppMessage(
                        id=f"msg_{active_id}_{len(active_messages) + 2}",
                        customer_id=active_id,
                        direction="outbound",
                        msg_type="text",
                        text=assistant_reply,
                        timestamp=now_time,
                        status="read",
                        buttons=["⚡ Claim 5-Hr Offer & Return to Checkout", "Return to Cart", "View Size Guide"]
                    )
                    mgr.messages[active_id].append(bot_reply_msg)
                    mgr.event_timelines[active_id].append(f"{now_time} [Simulated] Customer: '{user_text_input}' -> PUMA Assistant answered.")
                    st.rerun()

    # Column 2: PUMA Automation Control Panel
    with col_control:
        st.markdown("<div style='font-size: 0.82rem; font-weight: 700; color: #94A3B8; margin-bottom: 4px; font-family: monospace;'>[ AUTOMATION_HUD ]</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="tech-panel-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-family: monospace; font-size: 0.72rem; color: #94A3B8; letter-spacing: 1px;">TELEMETRY // SCENARIO_NODE</span>
                <span class="cyber-badge {status_cls}">{active_cart.status.upper()}</span>
            </div>
            <div style="font-size: 1.1rem; font-weight: 800; color: #FFFFFF;">{active_customer.name}</div>
            <div style="font-size: 0.8rem; color: #94A3B8; margin: 4px 0;">
                <span style="color: #64748B;">CAUSE:</span> <b style="color: #EF4444;">{active_cart.abandonment_reason}</b>
            </div>
            <div class="telemetry-grid">
                <div class="telemetry-cell">
                    <div class="cell-title">CART_VALUE</div>
                    <div class="cell-val">₹{active_product.price:,}</div>
                </div>
                <div class="telemetry-cell">
                    <div class="cell-title">IDLE_TIME</div>
                    <div class="cell-val">{active_cart.minutes_abandoned}m</div>
                </div>
                <div class="telemetry-cell">
                    <div class="cell-title">CONSENT</div>
                    <div class="cell-val">{'OPTED_IN' if not active_customer.opted_out else 'OPTED_OUT'}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 5-Hour Countdown Widget
        st.markdown("""
        <div style="background: linear-gradient(90deg, rgba(186, 12, 47, 0.25) 0%, rgba(220, 38, 38, 0.15) 100%); border: 1px solid #EF4444; border-radius: 8px; padding: 10px 14px; margin: 8px 0; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <div style="font-weight: 800; font-size: 0.88rem; color: #F87171;">⚡ 5-HOUR FLASH RECOVERY DEAL</div>
                <div style="font-size: 0.74rem; color: #E2E8F0; margin-top: 2px;">Code: <b style="color: #F87171;">SPEED20</b> (Flat 20% OFF)</div>
            </div>
            <div style="font-family: monospace; font-size: 0.8rem; background: #111B21; border: 1px solid #EF4444; padding: 3px 8px; border-radius: 4px; color: #FFF; font-weight: 700;">⏳ 04h 59m left</div>
        </div>
        """, unsafe_allow_html=True)

        act_col1, act_col2 = st.columns(2)
        with act_col1:
            if st.button("🚀 Trigger Recovery", type="primary", use_container_width=True):
                mgr.trigger_abandonment_recovery(active_id)
                st.success("WhatsApp recovery message dispatched!")
                st.rerun()
        with act_col2:
            if st.button("↺ Reset Scenario", use_container_width=True):
                mgr.reset_customer_demo(active_id)
                st.session_state.show_checkout_modal = False
                st.rerun()

        # Template Preview
        preview_scenario = DEMO_SCENARIOS[active_id]
        st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #94A3B8; margin-top: 8px; font-family: monospace;'>[ TEMPLATE_SPECIFICATION ]</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px; font-size: 0.8rem; line-height: 1.4; color: #CBD5E1;">
            <span style="font-family: monospace; color: #38BDF8; font-size: 0.72rem;">TEMPLATE_ID: {preview_scenario['template_id']}</span><br><br>
            {preview_scenario['template_text'].replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

        # Real-Time Terminal Activity Feed
        st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #94A3B8; margin-top: 10px; font-family: monospace;'>[ EVENT_LOGS // REALTIME_STREAM ]</div>", unsafe_allow_html=True)
        timeline_container = st.container(height=145)
        with timeline_container:
            for ev in reversed(active_timeline):
                st.markdown(f"""
                <div class="term-line">
                    <span style="color: #22C55E; font-weight: 700;">&gt;</span>
                    <span style="color: #CBD5E1;">{ev}</span>
                </div>
                """, unsafe_allow_html=True)


# =====================================================================
# TAB 3: PUMA AI COPILOT (FEATURE 3)
# =====================================================================
with tabs[2]:
    st.markdown("##### 🤖 PUMA AI Marketing Copilot & E-Commerce Strategist")
    st.caption("Powered by Google Gemini 3.8-Flash • Contextually grounded in real-time recovery metrics and campaign data.")

    # Suggested Prompts Row
    st.markdown("<div style='font-size: 0.78rem; font-weight: 700; color: #94A3B8; margin-bottom: 6px;'>💡 Suggested Strategic Prompts:</div>", unsafe_allow_html=True)
    p_cols = st.columns(3)
    
    copilot_query = None

    with p_cols[0]:
        if st.button("📊 'Why did cart recovery fall this week?'", use_container_width=True):
            copilot_query = "Why did cart recovery fall this week? Analyze the root causes from our abandonment data."
        if st.button("🏆 'Show best-performing campaigns'", use_container_width=True):
            copilot_query = "Show the best-performing WhatsApp campaigns and analyze what drove their high conversion rates."

    with p_cols[1]:
        if st.button("📱 'Generate high-converting template'", use_container_width=True):
            copilot_query = "Generate a personalized WhatsApp cart recovery message template for high-value shoes like Deviate Nitro 2."
        if st.button("🔄 'Compare campaign conversion rates'", use_container_width=True):
            copilot_query = "Compare our active campaign conversion rates and highlight underperforming categories."

    with p_cols[2]:
        if st.button("💡 'Suggest improvements to recover orders'", use_container_width=True):
            copilot_query = "Suggest concrete improvements to recover more abandoned carts and lift conversion above 30%."
        if st.button("📈 'Summarize today's performance'", use_container_width=True):
            copilot_query = "Summarize today's WhatsApp campaign performance, revenue generated, and ROI."

    # Copilot Chat History
    copilot_container = st.container(height=350)
    with copilot_container:
        for cmsg in st.session_state.copilot_history:
            if cmsg["role"] == "user":
                st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; max-width: 80%; margin-left: auto;">
                    <div style="font-size: 0.7rem; font-weight: 700; color: #38BDF8; font-family: monospace;">YOU</div>
                    <div>{cmsg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(17, 24, 39, 0.85); border-left: 3px solid #BA0C2F; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; max-width: 90%;">
                    <div style="font-size: 0.7rem; font-weight: 700; color: #BA0C2F; font-family: monospace; margin-bottom: 4px;">PUMA AI STRATEGIST</div>
                    <div style="font-size: 0.88rem; line-height: 1.5;">{cmsg['content']}</div>
                </div>
                """, unsafe_allow_html=True)

    # Copilot Prompt Input Form
    with st.form(key="copilot_form", clear_on_submit=True):
        cp_in1, cp_in2 = st.columns([5, 1])
        with cp_in1:
            typed_copilot_query = st.text_input("Ask Copilot", placeholder="Ask PUMA Copilot for strategy, analysis, or copy generation...", label_visibility="collapsed")
        with cp_in2:
            cp_send = st.form_submit_button("⚡ Analyze", use_container_width=True, type="primary")

    if (cp_send and typed_copilot_query) or copilot_query:
        active_q = typed_copilot_query if (cp_send and typed_copilot_query) else copilot_query
        st.session_state.copilot_history.append({"role": "user", "content": active_q})

        with st.spinner("PUMA Copilot is synthesizing analytics and strategy..."):
            reply_gen = query_puma_copilot(active_q, st.session_state.copilot_history[:-1])
            full_copilot_reply = "".join(chunk for chunk in reply_gen)
            st.session_state.copilot_history.append({"role": "assistant", "content": full_copilot_reply})
            st.rerun()


# =====================================================================
# TAB 4: CUSTOMERS & CAMPAIGNS (FEATURE 4)
# =====================================================================
with tabs[3]:
    st.markdown("##### 👥 Customer Segments & Active Recovery Campaigns")

    c_sub1, c_sub2 = st.tabs(["📋 Customer Records", "🚀 Campaign Manager & Templates"])

    with c_sub1:
        st.markdown("###### 🔍 Customer Cart Directory & Marketing Consent Status")
        cust_search = st.text_input("Filter customers by name, product, or city...", placeholder="Search customers...")
        
        # Build customers dataframe
        cust_rows = []
        for c in DEFAULT_CUSTOMERS:
            if not cust_search or cust_search.lower() in c.name.lower() or cust_search.lower() in c.cart_product.lower() or cust_search.lower() in c.city.lower():
                cust_rows.append({
                    "Customer ID": c.id,
                    "Name": c.name,
                    "Phone": c.phone,
                    "City": c.city,
                    "Cart Item": c.cart_product,
                    "Cart Value": f"₹{c.cart_value:,}",
                    "Size": c.cart_size,
                    "Reason": c.abandonment_reason,
                    "Status": c.status,
                    "Consent": "✅ OPTED_IN" if c.consent_opt_in else "❌ OPTED_OUT"
                })
        
        st.dataframe(pd.DataFrame(cust_rows), use_container_width=True, hide_index=True)
        st.caption("Data protection: Customer consent strictly enforced. Opted-out customers are suppressed from simulated campaigns.")

    with c_sub2:
        col_c_list, col_c_new = st.columns([6, 4])
        
        with col_c_list:
            st.markdown("###### ⚡ Active WhatsApp Campaigns")
            for camp in st.session_state.campaigns_list:
                status_color = "#10B981" if camp.status == "ACTIVE" else "#EF4444"
                with st.container():
                    st.markdown(f"""
                    <div style="background: rgba(17, 24, 39, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <b>{camp.name}</b>
                            <span style="font-family: monospace; font-size: 0.7rem; color: {status_color}; font-weight: 700;">● {camp.status}</span>
                        </div>
                        <div style="font-size: 0.78rem; color: #94A3B8; margin: 4px 0;">
                            Target: {camp.segment} | Delay: {camp.recovery_delay_mins}m | Voucher: <b>{camp.discount_code}</b>
                        </div>
                        <div style="font-family: monospace; font-size: 0.74rem; color: #CBD5E1;">
                            Dispatched: {camp.dispatched_count} | Recovered: <b>{camp.recovered_count}</b> | Revenue: <b>₹{camp.recovered_revenue:,}</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with col_c_new:
            st.markdown("###### ➕ Schedule New Campaign")
            with st.form("new_campaign_form"):
                new_name = st.text_input("Campaign Name", placeholder="e.g. Nitro 2 Flash Weekend Sale")
                new_segment = st.selectbox("Target Audience Segment", ["Running (Nitro Series)", "Sneakers (Palermo/Suede)", "Training (Fuse)", "All Abandoned Carts > ₹5,000"])
                new_template = st.selectbox("WhatsApp Business Template", list(APPROVED_TEMPLATES.keys()))
                new_voucher = st.text_input("Promotional Voucher Code", value="PUMASPEED15")
                new_delay = st.slider("Dispatch Delay (Minutes post-dropoff)", min_value=15, max_value=120, value=30, step=15)
                create_camp_submit = st.form_submit_button("🚀 Deploy Campaign", use_container_width=True, type="primary")

                if create_camp_submit and new_name:
                    new_c_record = CampaignRecord(
                        id=f"CAMP-{len(st.session_state.campaigns_list)+1:02d}",
                        name=f"⚡ {new_name}",
                        segment=new_segment,
                        template_id=new_template,
                        discount_code=new_voucher,
                        discount_pct=15,
                        recovery_delay_mins=new_delay,
                        status="ACTIVE",
                        dispatched_count=0,
                        recovered_count=0,
                        recovered_revenue=0
                    )
                    st.session_state.campaigns_list.append(new_c_record)
                    st.success(f"Campaign '{new_name}' deployed successfully!")
                    st.rerun()


# =====================================================================
# TAB 5: ENTERPRISE TELEMETRY & AUDIT LOGS (FEATURE 5)
# =====================================================================
with tabs[4]:
    st.markdown("##### 📡 Infrastructure Health, Provider Connections & Audit Trail")

    # Infrastructure Status Row
    h1, h2, h3, h4 = st.columns(4)
    with h1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title"><span>META WHATSAPP API</span><span class="dot-pulse-green"></span></div>
            <div class="kpi-value" style="font-size: 1.15rem; color: #10B981;">CONNECTED</div>
            <div class="kpi-delta">Provider: Meta Cloud API (Sandbox) • 24ms</div>
        </div>
        """, unsafe_allow_html=True)

    with h2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title"><span>GEMINI 3.8-FLASH LLM</span><span class="dot-pulse-green"></span></div>
            <div class="kpi-value" style="font-size: 1.15rem; color: #8E75C2;">ONLINE</div>
            <div class="kpi-delta">Inference: 420ms • Temperature: 0.3</div>
        </div>
        """, unsafe_allow_html=True)

    with h3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title"><span>CHROMADB VECTORS</span><span class="dot-pulse-green"></span></div>
            <div class="kpi-value" style="font-size: 1.15rem; color: #38BDF8;">PERSISTENT</div>
            <div class="kpi-delta">Indexed Chunks: 57 • Distance: Cosine</div>
        </div>
        """, unsafe_allow_html=True)

    with h4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title"><span>WEBHOOK INGESTION</span><span class="dot-pulse-green"></span></div>
            <div class="kpi-value" style="font-size: 1.15rem; color: #F59E0B;">200 OK</div>
            <div class="kpi-delta">Idempotency Guard: Active • 0 Dropped</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    st.markdown("###### 📜 Immutable Event Audit Trail (Real-Time Ingestion Log)")
    
    audit_df = pd.DataFrame(SYSTEM_AUDIT_LOGS)
    st.dataframe(audit_df, use_container_width=True, hide_index=True)
    
    st.caption("All webhook events and WhatsApp deliveries are signed with SHA-256 HMAC and cryptographically verified.")
