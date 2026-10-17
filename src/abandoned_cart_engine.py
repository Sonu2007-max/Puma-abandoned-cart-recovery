"""
PUMA Abandoned Cart Recovery Engine
Simulates e-commerce cart events, abandonment detection, WhatsApp Business message generation,
interactive template actions, and conversion tracking.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any


@dataclass
class Product:
    id: str
    name: str
    category: str
    price: int
    image_url: str
    selected_size: str
    quantity: int = 1
    features: List[str] = field(default_factory=list)


@dataclass
class Customer:
    id: str
    name: str
    phone_display: str
    avatar_color: str
    avatar_emoji: str
    last_seen: str
    consent_status: bool = True
    opted_out: bool = False


@dataclass
class Cart:
    id: str
    customer_id: str
    product: Product
    abandonment_reason: str
    reason_code: str
    created_at_str: str = "14:02"
    checkout_started_at_str: str = "14:06"
    abandoned_at_str: str = "14:12"
    recovery_sent_at_str: str = "14:43"
    minutes_abandoned: int = 42
    status: str = "Abandoned"  # "In Cart", "Checkout Started", "Abandoned", "Recovery Sent", "Recovered", "Opted Out"
    recovery_attempts: int = 0
    max_recovery_attempts: int = 2
    discount_applied: bool = False
    discount_percent: int = 20



@dataclass
class WhatsAppMessage:
    id: str
    customer_id: str
    direction: str  # "inbound" (from customer) or "outbound" (from PUMA)
    msg_type: str   # "text", "template_recovery", "interactive_buttons", "product_card", "system_notice"
    text: str
    timestamp: str
    status: str = "read"  # "sent", "delivered", "read"
    product_data: Optional[Dict[str, Any]] = None
    buttons: List[str] = field(default_factory=list)
    template_tag: Optional[str] = None


# Pre-configured 6 Scenarios as specified in the Master Prompt
DEMO_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "cust_1": {
        "customer": Customer(
            id="cust_1",
            name="Rahul Sharma",
            phone_display="+91 98765 43210",
            avatar_color="#BA0C2F",
            avatar_emoji="🏃",
            last_seen="Today at 14:12"
        ),
        "product": Product(
            id="prod_deviate",
            name="PUMA Deviate Nitro 2 Running Shoes",
            category="Performance Running",
            price=13599,
            image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80",
            selected_size="UK 9",
            quantity=1,
            features=["NITRO Elite Foam", "INNOPLATE Carbon Composite", "PUMAGRIP Outsole"]
        ),
        "reason": "Forgot to Checkout / Distracted",
        "reason_code": "forgot_checkout",
        "cart_value": 13599,
        "minutes_ago": 35,
        "template_id": "puma_cart_reminder_general",
        "template_text": (
            "Hey Rahul 👋\n\n"
            "Still thinking about your PUMA kicks? 👟\n\n"
            "Your selected *PUMA Deviate Nitro 2 Running Shoes* (Size UK 9) is waiting in your cart. "
            "Pick up where you left off whenever you're ready.\n\n"
            "— Team PUMA"
        ),
        "buttons": ["Return to Cart", "Need Help?", "Stop Messages"]
    },
    "cust_2": {
        "customer": Customer(
            id="cust_2",
            name="Priya Patel",
            phone_display="+91 98123 67890",
            avatar_color="#7C3AED",
            avatar_emoji="👟",
            last_seen="Today at 15:40"
        ),
        "product": Product(
            id="prod_palermo",
            name="PUMA Palermo Retro Suede Sneakers",
            category="Streetwear & Lifestyle",
            price=5999,
            image_url="https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=600&auto=format&fit=crop&q=80",
            selected_size="UK 6",
            quantity=1,
            features=["Authentic 1980s Terrace Design", "Gum Rubber Sole", "Gold Foil Logo"]
        ),
        "reason": "Price Concern / Seeking Offer",
        "reason_code": "price_concern",
        "cart_value": 5999,
        "minutes_ago": 48,
        "template_id": "puma_cart_price_inquiry",
        "template_text": (
            "Hey Priya! 👋\n\n"
            "We noticed you were checking out these *PUMA Palermo Retro Suede Sneakers*.\n\n"
            "Have a question about pricing or available offers? We're here to help you make the right choice.\n\n"
            "— Team PUMA"
        ),
        "buttons": ["View My Cart", "Explore Offers", "Stop Messages"]
    },
    "cust_3": {
        "customer": Customer(
            id="cust_3",
            name="Arjun Verma",
            phone_display="+91 97654 32109",
            avatar_color="#2563EB",
            avatar_emoji="⚡",
            last_seen="Today at 12:20"
        ),
        "product": Product(
            id="prod_velocity",
            name="PUMA Velocity Nitro 3 Distance Trainer",
            category="Daily Distance Running",
            price=7499,
            image_url="https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=600&auto=format&fit=crop&q=80",
            selected_size="UK 10",
            quantity=1,
            features=["NITRO Nitrogen-Infused Foam", "Engineered Breathable Mesh", "800+ KM Tested"]
        ),
        "reason": "Size or Fit Uncertainty",
        "reason_code": "size_fit_doubt",
        "cart_value": 7499,
        "minutes_ago": 40,
        "template_id": "puma_cart_sizing_assist",
        "template_text": (
            "Hey Arjun! 👟\n\n"
            "Need help finding your perfect fit?\n\n"
            "Your PUMA selection (*PUMA Velocity Nitro 3* - UK 10) is still in your cart. "
            "We can help you explore sizing and fit information before you decide.\n\n"
            "— Team PUMA"
        ),
        "buttons": ["View Size Guide", "Return to Cart", "Stop Messages"]
    },
    "cust_4": {
        "customer": Customer(
            id="cust_4",
            name="Neha Gupta",
            phone_display="+91 99887 76655",
            avatar_color="#059669",
            avatar_emoji="🏋️",
            last_seen="Today at 16:05"
        ),
        "product": Product(
            id="prod_fuse",
            name="PUMA Fuse 3.0 Cross-Training Shoes",
            category="Training & Gym",
            price=6499,
            image_url="https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&auto=format&fit=crop&q=80",
            selected_size="UK 7",
            quantity=1,
            features=["PUMAGRIP Rubber Stability Base", "Wider Toe Box for Lifting", "High-Abrasion Mesh"]
        ),
        "reason": "Payment Gateway Timeout",
        "reason_code": "payment_failure",
        "cart_value": 6499,
        "minutes_ago": 32,
        "template_id": "puma_cart_payment_recovery",
        "template_text": (
            "Hey Neha! 👋\n\n"
            "Looks like your PUMA order may not have been completed.\n\n"
            "If you ran into a payment issue, you can return to checkout and try again. "
            "Please don't share your OTP or payment credentials in this chat.\n\n"
            "— Team PUMA"
        ),
        "buttons": ["Resume Checkout", "Get Help", "Stop Messages"]
    },
    "cust_5": {
        "customer": Customer(
            id="cust_5",
            name="Aman Singh",
            phone_display="+91 91234 56780",
            avatar_color="#D97706",
            avatar_emoji="🏃",
            last_seen="Today at 11:15"
        ),
        "product": Product(
            id="prod_t7",
            name="PUMA Iconic T7 Track Jacket & Pants",
            category="Activewear & Tracksuits",
            price=4999,
            image_url="https://images.unsplash.com/photo-1556906781-9a412961c28c?w=600&auto=format&fit=crop&q=80",
            selected_size="Size L",
            quantity=1,
            features=["Signature 7cm T7 Sleeve Inserts", "French Terry Fabric", "Full-Zip Standup Collar"]
        ),
        "reason": "Comparing Products / Alternate Brands",
        "reason_code": "comparing_products",
        "cart_value": 4999,
        "minutes_ago": 55,
        "template_id": "puma_cart_comparison_assist",
        "template_text": (
            "Hey Aman! 👋\n\n"
            "Still exploring your options? No problem.\n\n"
            "Your selected *PUMA Iconic T7 Track Jacket* is waiting for you. Take another look whenever you're ready.\n\n"
            "— Team PUMA"
        ),
        "buttons": ["View My Cart", "Explore Similar Products", "Stop Messages"]
    },
    "cust_6": {
        "customer": Customer(
            id="cust_6",
            name="Sneha Reddy",
            phone_display="+91 93456 78901",
            avatar_color="#DB2777",
            avatar_emoji="🧥",
            last_seen="Today at 13:45"
        ),
        "product": Product(
            id="prod_hoodie",
            name="PUMA Classics Relaxed Fleece Hoodie",
            category="Winterwear & Outerwear",
            price=3999,
            image_url="https://images.unsplash.com/photo-1509967419530-da38b4704bc6?w=600&auto=format&fit=crop&q=80",
            selected_size="Size S",
            quantity=1,
            features=["Brushed Fleece Comfort Lining", "Kangaroo Pocket", "Embroidered PUMA Archive No. 1 Logo"]
        ),
        "reason": "Delivery Question & Timelines",
        "reason_code": "delivery_question",
        "cart_value": 3999,
        "minutes_ago": 60,
        "template_id": "puma_cart_delivery_assist",
        "template_text": (
            "Hey Sneha! 👋\n\n"
            "Have a question about delivery for your PUMA selection?\n\n"
            "Check the available delivery details during checkout, or ask us for help before placing your order.\n\n"
            "— Team PUMA"
        ),
        "buttons": ["Return to Cart", "Delivery Help", "Stop Messages"]
    }
}


class PUMAAbandonedCartRecoveryManager:
    """
    Manages state, simulation pipelines, WhatsApp message logging,
    interactive button dispatch, and cart checkout conversions.
    """

    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self.carts: Dict[str, Cart] = {}
        self.messages: Dict[str, List[WhatsAppMessage]] = {}
        self.event_timelines: Dict[str, List[str]] = {}
        self.initialize_demo_data()

    def initialize_demo_data(self):
        """Pre-populates the 6 standard demo customer scenarios."""
        for cust_id, data in DEMO_SCENARIOS.items():
            customer: Customer = data["customer"]
            product: Product = data["product"]

            self.customers[cust_id] = customer
            self.carts[cust_id] = Cart(
                id=f"cart_{cust_id}",
                customer_id=cust_id,
                product=product,
                abandonment_reason=data["reason"],
                reason_code=data["reason_code"],
                minutes_abandoned=data["minutes_ago"],
                status="Abandoned"
            )

            # Initialize Simulated Event Timeline
            self.event_timelines[cust_id] = [
                f"14:02 [Simulated] Product '{product.name}' added to cart (Size: {product.selected_size}, ₹{product.price:,})",
                f"14:06 [Simulated] Customer proceeded to checkout step",
                f"14:12 [Simulated] Customer stopped activity ({data['reason']})",
                f"14:42 [Simulated] Cart crossed 30-min abandonment threshold (Eligible for Recovery)"
            ]

            # Initialize Messages with the recovery message already prepared / sent
            self.messages[cust_id] = [
                WhatsAppMessage(
                    id=f"msg_{cust_id}_init",
                    customer_id=cust_id,
                    direction="outbound",
                    msg_type="template_recovery",
                    text=data["template_text"],
                    timestamp="14:43",
                    status="read",
                    product_data={
                        "name": product.name,
                        "category": product.category,
                        "price": product.price,
                        "size": product.selected_size,
                        "image_url": product.image_url,
                        "quantity": product.quantity
                    },
                    buttons=data["buttons"],
                    template_tag=data["template_id"]
                )
            ]

    def trigger_abandonment_recovery(self, customer_id: str) -> Optional[WhatsAppMessage]:
        """
        Executes the detection rules and delivers recovery message:
        1. Checks customer consent & opt-out.
        2. Validates unrecovered cart existence.
        3. Generates personalized message template.
        4. Updates timeline.
        """
        customer = self.customers.get(customer_id)
        cart = self.carts.get(customer_id)

        if not customer or not cart:
            return None

        if customer.opted_out:
            self.event_timelines[customer_id].append(
                f"{datetime.now().strftime('%H:%M')} [Simulated] Recovery Skipped: Customer has opted out of WhatsApp messages."
            )
            return None

        if cart.status == "Recovered":
            self.event_timelines[customer_id].append(
                f"{datetime.now().strftime('%H:%M')} [Simulated] Recovery Skipped: Cart has already been purchased/recovered."
            )
            return None

        data = DEMO_SCENARIOS[customer_id]
        now_str = datetime.now().strftime("%H:%M")

        # Create WhatsApp template message
        msg = WhatsAppMessage(
            id=f"msg_{customer_id}_{len(self.messages[customer_id]) + 1}",
            customer_id=customer_id,
            direction="outbound",
            msg_type="template_recovery",
            text=data["template_text"],
            timestamp=now_str,
            status="delivered",
            product_data={
                "name": cart.product.name,
                "category": cart.product.category,
                "price": cart.product.price,
                "size": cart.product.selected_size,
                "image_url": cart.product.image_url,
                "quantity": cart.product.quantity
            },
            buttons=data["buttons"],
            template_tag=data["template_id"]
        )

        self.messages[customer_id].append(msg)
        cart.status = "Recovery Sent"
        cart.recovery_attempts += 1

        self.event_timelines[customer_id].append(
            f"{now_str} [Simulated] WhatsApp recovery template '{data['template_id']}' dispatched to {customer.phone_display}"
        )
        return msg

    def handle_interactive_button(self, customer_id: str, button_label: str) -> tuple[WhatsAppMessage, WhatsAppMessage]:
        """
        Handles click on WhatsApp interactive button:
        1. Creates simulated inbound message from customer.
        2. Dispatches appropriate automated assistant response.
        3. Updates cart status / timeline.
        """
        now_str = datetime.now().strftime("%H:%M")
        cart = self.carts[customer_id]
        product = cart.product
        customer = self.customers[customer_id]

        # 1. Inbound Customer Message
        inbound_msg = WhatsAppMessage(
            id=f"msg_{customer_id}_{len(self.messages[customer_id]) + 1}",
            customer_id=customer_id,
            direction="inbound",
            msg_type="text",
            text=f"👉 Clicked: *{button_label}*",
            timestamp=now_str,
            status="read"
        )
        self.messages[customer_id].append(inbound_msg)

        # 2. Assistant Response based on button clicked
        outbound_text = ""
        outbound_buttons = []

        if button_label in ["Return to Cart", "View My Cart", "Resume Checkout"]:
            outbound_text = (
                f"Awesome, {customer.name}! 🎉 We've loaded your cart.\n\n"
                f"🛍️ *Item:* {product.name}\n"
                f"📏 *Size:* {product.selected_size} | 💰 *Total:* ₹{product.price:,}\n\n"
                f"Click below to review delivery details and place your order directly."
            )
            outbound_buttons = ["Proceed to Checkout", "Need Help?"]
            cart.status = "Checkout Resumed"
            self.event_timelines[customer_id].append(
                f"{now_str} [Simulated] Customer resumed cart checkout via WhatsApp button"
            )

        elif button_label == "View Size Guide":
            outbound_text = (
                f"Here is the official *PUMA Size & Fit Guide* for {product.name}: 📏\n\n"
                f"• UK 6: Foot length 25.0 cm\n"
                f"• UK 7: Foot length 26.0 cm\n"
                f"• UK 8: Foot length 27.0 cm\n"
                f"• UK 9: Foot length 28.0 cm\n"
                f"• UK 10: Foot length 29.0 cm\n\n"
                f"💡 *Pro Fit Tip:* For NITRO running shoes, wide-foot runners often prefer going half size up (+0.5 UK). "
                f"Plus, enjoy *Free Doorstep Size Exchange*—if it doesn't fit, our courier exchanges it at your door for ₹0!"
            )
            outbound_buttons = ["Return to Cart", "Resume Checkout"]
            self.event_timelines[customer_id].append(
                f"{now_str} [Simulated] Customer requested and viewed PUMA size guide"
            )

        elif button_label == "Explore Offers":
            outbound_text = (
                f"Here are the active PUMA offers applicable to your cart, {customer.name}: 🏷️\n\n"
                f"1. *Code PUMAFAST15:* Flat 15% Instant Discount on {product.name} (Saves ₹{int(product.price * 0.15):,})!\n"
                f"2. *No-Cost EMI:* Available at ₹{int(product.price / 3):,}/month for 3 months.\n"
                f"3. *Free Delivery:* ₹0 shipping on all orders above ₹999 across India.\n\n"
                f"Would you like to apply the 15% discount code and resume checkout?"
            )
            outbound_buttons = ["Apply 15% & Checkout", "Return to Cart"]
            self.event_timelines[customer_id].append(
                f"{now_str} [Simulated] Customer explored available offers (Presented PUMAFAST15)"
            )

        elif button_label in ["Apply 15% & Checkout"]:
            discounted_price = int(product.price * 0.85)
            outbound_text = (
                f"✅ Code *PUMAFAST15* has been applied to your cart!\n\n"
                f"• Original Price: ~₹{product.price:,}~\n"
                f"• Discounted Total: *₹{discounted_price:,}* (Saved ₹{product.price - discounted_price:,})\n\n"
                f"Ready to complete your order?"
            )
            outbound_buttons = ["Proceed to Checkout", "Stop Messages"]
            cart.status = "Checkout Resumed"
            cart.discount_applied = True
            cart.discount_percent = 15
            self.event_timelines[customer_id].append(
                f"{now_str} [Simulated] Applied promo PUMAFAST15. New Total: ₹{discounted_price:,}"
            )

        elif "Claim 5-Hr Offer" in button_label or "Claim 20%" in button_label:
            cart.discount_applied = True
            cart.discount_percent = 20
            cart.status = "Checkout Resumed"
            discounted_price = int(product.price * 0.80)
            savings = product.price - discounted_price

            outbound_text = (
                f"🎉 *20% FLASH VOUCHER ACTIVATED!* ⚡ (Code: *SPEED20*)\n\n"
                f"• *Item:* {product.name} (Size: {product.selected_size})\n"
                f"• *Regular MRP:* ~₹{product.price:,}~\n"
                f"• *Your Flash Price:* *₹{discounted_price:,}* (You Save *₹{savings:,}*!)\n"
                f"• ⏳ *Time Remaining:* 04 hrs 59 mins (Offer locked to your cart)\n\n"
                f"We've loaded your discounted cart in the checkout drawer. Click *Proceed to Checkout* to confirm delivery address!"
            )
            outbound_buttons = ["Proceed to Checkout", "View Size Guide"]
            self.event_timelines[customer_id].append(
                f"{now_str} [Simulated] Customer claimed 5-hour flash voucher SPEED20 (-20%). New Total: ₹{discounted_price:,}"
            )


        elif button_label in ["Need Help?", "Get Help"]:
            outbound_text = (
                f"We're right here to help, {customer.name}! 🐾\n\n"
                f"You can ask us anything about:\n"
                f"• Sizing & arch support\n"
                f"• Payment modes (Cash on Delivery, UPI, Cards)\n"
                f"• 30-day hassle-free return policy\n\n"
                f"Simply type your question here, or click below for fast options."
            )
            outbound_buttons = ["Return to Cart", "Delivery Help"]
            self.event_timelines[customer_id].append(
                f"{now_str} [Simulated] Customer requested assistance"
            )

        elif button_label == "Delivery Help":
            outbound_text = (
                f"📦 *PUMA India Delivery Information:*\n\n"
                f"• *Metro Cities* (Bangalore, Mumbai, Delhi, Hyderabad): 2 to 3 business days.\n"
                f"• *Rest of India:* 3 to 5 business days.\n"
                f"• *Shipping Fee:* 100% FREE on this order.\n"
                f"• *Cash on Delivery (COD):* Available at no extra charge.\n\n"
                f"All shipments are dispatched directly from official PUMA fulfillment hubs."
            )
            outbound_buttons = ["Return to Cart", "Resume Checkout"]
            self.event_timelines[customer_id].append(
                f"{now_str} [Simulated] Customer inquired about delivery timelines"
            )

        elif button_label == "Explore Similar Products":
            outbound_text = (
                f"Looking for alternatives to {product.name}? Check out these related top-picks:\n\n"
                f"1. *PUMA Velocity Nitro 3* (Daily Trainer) — ₹7,499\n"
                f"2. *PUMA Palermo Suede Sneaker* (Retro Casual) — ₹5,999\n"
                f"3. *PUMA Fuse 3.0* (Cross-Training) — ₹6,499\n\n"
                f"Would you like to stick with your current selection or switch?"
            )
            outbound_buttons = ["Keep Current Cart", "Return to Cart"]
            self.event_timelines[customer_id].append(
                f"{now_str} [Simulated] Customer browsed similar PUMA alternatives"
            )

        elif button_label in ["Stop Messages", "STOP"]:
            customer.opted_out = True
            customer.consent_status = False
            cart.status = "Opted Out"
            outbound_text = (
                "You have successfully unsubscribed from automated PUMA WhatsApp recovery updates. "
                "We will no longer send reminders for this cart. "
                "Reply *START* at any time to re-enable notifications. Thank you! 🐾"
            )
            outbound_buttons = []
            self.event_timelines[customer_id].append(
                f"{now_str} [Simulated] Customer unsubscribed (optedOut = True). Future marketing paused."
            )

        else:
            outbound_text = f"Got it, {customer.name}! Let us know if you need anything else before completing checkout."
            outbound_buttons = ["Return to Cart"]

        outbound_msg = WhatsAppMessage(
            id=f"msg_{customer_id}_{len(self.messages[customer_id]) + 1}",
            customer_id=customer_id,
            direction="outbound",
            msg_type="text",
            text=outbound_text,
            timestamp=now_str,
            status="read",
            buttons=outbound_buttons
        )
        self.messages[customer_id].append(outbound_msg)
        return inbound_msg, outbound_msg

    def complete_purchase(self, customer_id: str) -> bool:
        """Marks the customer's cart as Recovered / Purchased."""
        cart = self.carts.get(customer_id)
        if not cart:
            return False

        now_str = datetime.now().strftime("%H:%M")
        cart.status = "Recovered"

        confirm_msg = WhatsAppMessage(
            id=f"msg_{customer_id}_{len(self.messages[customer_id]) + 1}",
            customer_id=customer_id,
            direction="outbound",
            msg_type="text",
            text=(
                f"🎉 *Order Confirmed!* Thank you for choosing PUMA, {self.customers[customer_id].name}! 🐾\n\n"
                f"Your order for *{cart.product.name}* (Size: {cart.product.selected_size}) has been placed successfully.\n"
                f"📦 *Tracking ID:* #PUMA-REC-{customer_id.upper()}\n"
                f"🚚 Estimated delivery within 2-3 business days.\n\n"
                f"FOREVER. FASTER. ⚡🏃"
            ),
            timestamp=now_str,
            status="read"
        )
        self.messages[customer_id].append(confirm_msg)

        self.event_timelines[customer_id].append(
            f"{now_str} [Simulated] Purchase Completed! Cart #{cart.id} marked as RECOVERED (Value: ₹{cart.product.price:,})"
        )
        return True

    def generate_pricing_and_offer_guide(self, customer_id: str) -> WhatsAppMessage:
        """
        Generates an interactive product pricing guide with an exclusive
        time-limited 5-hour flash offer and immediate checkout action.
        """
        cart = self.carts[customer_id]
        customer = self.customers[customer_id]
        product = cart.product
        now = datetime.now()
        now_str = now.strftime("%H:%M")
        expiry_dt = now + timedelta(hours=5)
        expiry_str = expiry_dt.strftime("%I:%M %p")

        discounted_price = int(product.price * 0.80)
        savings = product.price - discounted_price
        emi = int(discounted_price / 3)

        features_bullets = "\n".join([f"• *{f}*" for f in product.features]) if product.features else "• High-performance athletic engineering"

        guide_text = (
            f"⚡ *EXCLUSIVE PUMA FLASH PRICING & OFFER GUIDE* 🐾\n\n"
            f"Hey {customer.name}! Here is the complete pricing breakdown & VIP recovery deal for *{product.name}*:\n\n"
            f"💰 *Regular MRP:* ~₹{product.price:,}~\n"
            f"🔥 *VIP Flash Price:* *₹{discounted_price:,}* (Flat 20% OFF — You Save *₹{savings:,}*!)\n"
            f"⏳ *Offer Validity:* *STRICTLY VALID FOR NEXT 5 HOURS ONLY!* (Expires today at {expiry_str})\n"
            f"💳 *No-Cost EMI:* ₹{emi:,}/month for 3 months with zero interest.\n\n"
            f"✨ *Why this pair is worth every rupee:*\n"
            f"{features_bullets}\n"
            f"• 800+ KM road-tested durability\n"
            f"• 🔄 30-Day Free Doorstep Return & Size Exchange\n"
            f"• 📦 100% Free Express Delivery across India\n\n"
            f"Click *⚡ Claim 5-Hr Offer & Return to Checkout* below to lock in this special price before the timer runs out!"
        )

        buttons = [
            "⚡ Claim 5-Hr Offer & Return to Checkout",
            "View Size Guide",
            "Delivery Help"
        ]

        outbound_msg = WhatsAppMessage(
            id=f"msg_{customer_id}_{len(self.messages[customer_id]) + 1}",
            customer_id=customer_id,
            direction="outbound",
            msg_type="text",
            text=guide_text,
            timestamp=now_str,
            status="read",
            buttons=buttons
        )
        self.messages[customer_id].append(outbound_msg)
        self.event_timelines[customer_id].append(
            f"{now_str} [Simulated] PUMA Assistant sent 5-Hour Flash Pricing Guide (20% OFF SPEED20, Saves ₹{savings:,})"
        )
        return outbound_msg

    def reset_customer_demo(self, customer_id: str):
        """Resets a customer's scenario back to initial state."""
        self.initialize_demo_data()

