"""
PUMA Cart Recovery Enterprise Analytics Engine
Provides structured KPIs, time-series data, conversion funnels,
and campaign performance benchmarks for the PUMA executive dashboard.
"""

from datetime import datetime, timedelta
import pandas as pd


def get_kpi_summary():
    """Returns top-level business recovery KPIs."""
    return {
        "abandoned_carts": 1482,
        "abandoned_value": 14250000,
        "messages_sent": 1394,
        "delivery_rate": 98.6,
        "read_rate": 84.2,
        "reply_rate": 42.8,
        "recovered_orders": 418,
        "recovered_revenue": 4285600,
        "conversion_rate": 28.2,
        "avg_order_value": 10252,
        "recovery_roi": "14.8x",
        "avg_recovery_time_mins": 38
    }


def get_recovery_trend_data(days: int = 14) -> pd.DataFrame:
    """Generates daily time-series metrics for recovery vs abandonment."""
    end_date = datetime.now()
    records = []
    
    # 14-day trending simulation
    base_abandoned = [95, 104, 112, 98, 120, 135, 128, 110, 102, 118, 125, 140, 132, 115]
    base_recovered = [26, 29, 34, 28, 36, 42, 38, 32, 30, 35, 39, 44, 40, 35]
    base_revenue = [r * 10250 for r in base_recovered]

    for i in range(days):
        d = end_date - timedelta(days=(days - 1 - i))
        records.append({
            "Date": d.strftime("%b %d"),
            "Abandoned Carts": base_abandoned[i % len(base_abandoned)],
            "Recovered Orders": base_recovered[i % len(base_recovered)],
            "Recovered Revenue (₹)": base_revenue[i % len(base_revenue)],
            "Conversion Rate (%)": round((base_recovered[i % len(base_recovered)] / base_abandoned[i % len(base_abandoned)]) * 100, 1)
        })
    return pd.DataFrame(records)


def get_funnel_data() -> pd.DataFrame:
    """Returns step-by-step conversion funnel drop-off data."""
    stages = [
        {"Stage": "1. Cart Abandoned", "Count": 1482, "Dropoff (%)": 0.0},
        {"Stage": "2. WhatsApp Dispatched", "Count": 1394, "Dropoff (%)": 5.9},
        {"Stage": "3. Message Delivered", "Count": 1375, "Dropoff (%)": 1.4},
        {"Stage": "4. Message Read (Blue Ticks)", "Count": 1158, "Dropoff (%)": 15.8},
        {"Stage": "5. Interactive Button Clicked", "Count": 591, "Dropoff (%)": 48.9},
        {"Stage": "6. Order Recovered (Paid)", "Count": 418, "Dropoff (%)": 29.3}
    ]
    return pd.DataFrame(stages)


def get_abandonment_causes() -> pd.DataFrame:
    """Categorized customer hesitation reasons detected by the engine."""
    causes = [
        {"Cause": "Price Resistance & Deal Seeking", "Carts": 492, "Percentage": "33.2%", "Recovery Rate": "34.1%"},
        {"Cause": "Sizing & Fit Uncertainty", "Carts": 341, "Percentage": "23.0%", "Recovery Rate": "29.4%"},
        {"Cause": "Product Indecision / Comparing", "Carts": 282, "Percentage": "19.0%", "Recovery Rate": "24.8%"},
        {"Cause": "Distraction / Forgot to Checkout", "Carts": 194, "Percentage": "13.1%", "Recovery Rate": "31.2%"},
        {"Cause": "Payment Gateway Issues", "Carts": 118, "Percentage": "8.0%", "Recovery Rate": "18.6%"},
        {"Cause": "Delivery Timelines Question", "Carts": 55, "Percentage": "3.7%", "Recovery Rate": "21.8%"}
    ]
    return pd.DataFrame(causes)


def get_campaign_benchmarks() -> pd.DataFrame:
    """Comparison table of active WhatsApp recovery campaigns."""
    campaigns = [
        {
            "Campaign Name": "⚡ Nitro Elite Marathon Re-engagement",
            "Target Segment": "Performance Running (Cart > ₹10k)",
            "Dispatched": 420,
            "Delivered": 414,
            "Recovered": 142,
            "Revenue (₹)": 1931200,
            "Conv. Rate": "33.8%",
            "Active Voucher": "SPEED20 (20% OFF)",
            "Status": "ACTIVE"
        },
        {
            "Campaign Name": "👟 Palermo Terrace Lifestyle Drops",
            "Target Segment": "Streetwear & Retro Sneakers",
            "Dispatched": 380,
            "Delivered": 376,
            "Recovered": 118,
            "Revenue (₹)": 707880,
            "Conv. Rate": "31.0%",
            "Active Voucher": "PUMAFAST15 (15% OFF)",
            "Status": "ACTIVE"
        },
        {
            "Campaign Name": "📏 Size-Fit Rescue with Doorstep Trial",
            "Target Segment": "Customers viewing Size Guide",
            "Dispatched": 310,
            "Delivered": 305,
            "Recovered": 89,
            "Revenue (₹)": 667410,
            "Conv. Rate": "28.7%",
            "Active Voucher": "DOORSTEPTRIAL",
            "Status": "ACTIVE"
        },
        {
            "Campaign Name": "🏋️ Fuse Cross-Training Recovery",
            "Target Segment": "Gym & Training Apparel/Footwear",
            "Dispatched": 184,
            "Delivered": 180,
            "Recovered": 45,
            "Revenue (₹)": 292455,
            "Conv. Rate": "24.5%",
            "Active Voucher": "TRAIN15",
            "Status": "PAUSED"
        },
        {
            "Campaign Name": "💳 Gateway Failure Instant Assist",
            "Target Segment": "Payment Dropped at Gateway",
            "Dispatched": 100,
            "Delivered": 100,
            "Recovered": 24,
            "Revenue (₹)": 156000,
            "Conv. Rate": "24.0%",
            "Active Voucher": "RETRYNOW",
            "Status": "ACTIVE"
        }
    ]
    return pd.DataFrame(campaigns)
