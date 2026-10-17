"""
PUMA Campaign & Customer Management System
Handles campaign lifecycle (Create, Pause, Resume), customer database records,
WhatsApp Business approved templates, and enterprise health/audit telemetry.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any


@dataclass
class CustomerRecord:
    id: str
    name: str
    email: str
    phone: str
    city: str
    cart_product: str
    cart_value: int
    cart_size: str
    abandonment_reason: str
    status: str
    consent_opt_in: bool = True


@dataclass
class CampaignRecord:
    id: str
    name: str
    segment: str
    template_id: str
    discount_code: str
    discount_pct: int
    recovery_delay_mins: int
    status: str  # "ACTIVE", "PAUSED", "COMPLETED"
    dispatched_count: int = 0
    recovered_count: int = 0
    recovered_revenue: int = 0
    created_at: str = "2026-10-15"


# Pre-populated enterprise customers
DEFAULT_CUSTOMERS: List[CustomerRecord] = [
    CustomerRecord("CUST-101", "Rahul Sharma", "rahul.s@gmail.com", "+91 98765 43210", "Bangalore", "PUMA Deviate Nitro 2", 13599, "UK 9", "Forgot to Checkout", "Abandoned"),
    CustomerRecord("CUST-102", "Priya Patel", "priya.p@outlook.com", "+91 98123 67890", "Mumbai", "PUMA Palermo Retro Suede", 5999, "UK 6", "Price Resistance", "Recovered"),
    CustomerRecord("CUST-103", "Arjun Verma", "arjun.v@yahoo.com", "+91 97654 32109", "Delhi NCR", "PUMA Velocity Nitro 3", 7499, "UK 10", "Sizing Uncertainty", "Checkout Resumed"),
    CustomerRecord("CUST-104", "Neha Gupta", "neha.g@gmail.com", "+91 99887 76655", "Pune", "PUMA Fuse 3.0 Training", 6499, "UK 7", "Payment Gateway Timeout", "Abandoned"),
    CustomerRecord("CUST-105", "Aman Singh", "aman.s@hotmail.com", "+91 91234 56780", "Hyderabad", "PUMA Iconic T7 Tracksuit", 4999, "Size L", "Comparing Competitors", "Abandoned"),
    CustomerRecord("CUST-106", "Sneha Reddy", "sneha.r@gmail.com", "+91 93456 78901", "Chennai", "PUMA Classics Fleece Hoodie", 3999, "Size S", "Delivery Questions", "Opted Out", consent_opt_in=False),
    CustomerRecord("CUST-107", "Karan Malhotra", "karan.m@gmail.com", "+91 98222 11334", "Chandigarh", "PUMA Future 7 Ultimate Cleats", 17999, "UK 8", "High Cart Value", "Abandoned"),
    CustomerRecord("CUST-108", "Rhea Sengupta", "rhea.s@gmail.com", "+91 98450 99881", "Kolkata", "PUMA Suede Classic XXI", 5499, "UK 5", "Distracted on Mobile", "Recovered")
]

# Pre-populated campaigns
DEFAULT_CAMPAIGNS: List[CampaignRecord] = [
    CampaignRecord("CAMP-01", "⚡ Nitro Elite Marathon Re-engagement", "Running Shoes > ₹10,000", "puma_cart_reminder_general", "SPEED20", 20, 30, "ACTIVE", 420, 142, 1931200),
    CampaignRecord("CAMP-02", "👟 Palermo Terrace Lifestyle Drops", "Sneakers & Streetwear", "puma_cart_price_inquiry", "PUMAFAST15", 15, 45, "ACTIVE", 380, 118, 707880),
    CampaignRecord("CAMP-03", "📏 Size-Fit Rescue with Doorstep Trial", "Viewed Sizing Guide", "puma_cart_sizing_assist", "DOORSTEPTRIAL", 0, 20, "ACTIVE", 310, 89, 667410),
    CampaignRecord("CAMP-04", "🏋️ Fuse Cross-Training Recovery", "Gym & Training Category", "puma_cart_payment_recovery", "TRAIN15", 15, 60, "PAUSED", 184, 45, 292455),
    CampaignRecord("CAMP-05", "💳 Gateway Failure Instant Assist", "Payment Gateway Dropped", "puma_cart_payment_recovery", "RETRYNOW", 10, 10, "ACTIVE", 100, 24, 156000)
]

# WhatsApp Business Approved Templates
APPROVED_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "puma_cart_reminder_general": {
        "name": "General Cart Reminder",
        "category": "MARKETING",
        "language": "en_US / Hinglish",
        "status": "APPROVED",
        "body": "Hey {{1}} 👋 Still thinking about your PUMA kicks? 👟 Your selected {{2}} is waiting in your cart. Pick up where you left off whenever you're ready. — Team PUMA",
        "buttons": ["Return to Cart", "Need Help?", "Stop Messages"]
    },
    "puma_cart_price_inquiry": {
        "name": "Price Resistance & VIP Offer",
        "category": "MARKETING",
        "language": "en_US / Hinglish",
        "status": "APPROVED",
        "body": "Hey {{1}}! 👋 We noticed you were checking out {{2}}. Have a question about pricing or available offers? Use code {{3}} for an exclusive discount valid for 5 hours. — Team PUMA",
        "buttons": ["Claim Offer & Checkout", "View My Cart", "Stop Messages"]
    },
    "puma_cart_sizing_assist": {
        "name": "Sizing Guide & Doorstep Trial",
        "category": "UTILITY / MARKETING",
        "language": "en_US",
        "status": "APPROVED",
        "body": "Hey {{1}}! 👟 Need help finding your perfect fit for {{2}}? We provide free doorstep size exchange with courier swap at ₹0 extra fee. — Team PUMA",
        "buttons": ["View Size Guide", "Return to Cart", "Stop Messages"]
    },
    "puma_cart_payment_recovery": {
        "name": "Payment Gateway Timeout Recovery",
        "category": "UTILITY",
        "language": "en_US",
        "status": "APPROVED",
        "body": "Hey {{1}}! 👋 Looks like your PUMA order may not have been completed. If you ran into a payment issue, you can safely resume checkout. Please don't share OTPs in this chat. — Team PUMA",
        "buttons": ["Resume Checkout", "Get Help", "Stop Messages"]
    }
}


# System Audit Logs
SYSTEM_AUDIT_LOGS = [
    {"timestamp": "2026-10-16 19:14:02", "service": "WEBHOOK_INGEST", "event": "EVENT_CART_ABANDONED", "payload": "cart_id=1482 value=13599 customer=Rahul Sharma", "status": "200 OK"},
    {"timestamp": "2026-10-16 19:14:35", "service": "CONSENT_GUARD", "event": "CHECK_MARKETING_OPTIN", "payload": "phone=+919876543210 consent=APPROVED", "status": "PASS"},
    {"timestamp": "2026-10-16 19:15:00", "service": "WHATSAPP_DISPATCH", "event": "OUTBOUND_TEMPLATE", "payload": "template=puma_cart_reminder_general recipient=+919876543210", "status": "DELIVERED"},
    {"timestamp": "2026-10-16 19:15:22", "service": "WEBHOOK_EVENT", "event": "MESSAGE_READ_RECEIPT", "payload": "msg_id=wamid_9942 status=read blue_ticks=true", "status": "200 OK"},
    {"timestamp": "2026-10-16 19:16:10", "service": "INTERACTIVE_HANDLER", "event": "BUTTON_CLICKED", "payload": "action=Claim_5Hr_Offer code=SPEED20 discount=-20%", "status": "200 OK"},
    {"timestamp": "2026-10-16 19:17:44", "service": "PAYMENT_ATTRIBUTION", "event": "PURCHASE_VERIFIED", "payload": "order_id=PUMA-REC-CUST_1 recovered_val=10879 channel=WhatsApp", "status": "ATTRIBUTED"}
]
