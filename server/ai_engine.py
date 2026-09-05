import re
import random
from typing import Dict, Any, List, Tuple

class InstaViralAIEngine:
    def __init__(self, brand_name: str = "Jasper Brand", default_price: str = "250,000 so'm"):
        self.brand_name = brand_name
        self.default_price = default_price

    def classify_intent_and_sentiment(self, text: str) -> Tuple[str, str, float]:
        t = text.lower().strip()

        # Emojis & Praise
        positive_emojis = ["🔥", "❤️", "😍", "👏", "👍", "🚀", "💯", "✨", "🙌"]
        if any(emoji in text for emoji in positive_emojis) and len(t) < 15:
            return "COMPLIMENT", "POSITIVE", 0.98

        # Purchase / Order intent (check before general location)
        order_patterns = [
            r"sotib ol", r"olmoqchiman", r"zakaz", r"buyurtma", r"xarid", r"qanday ol",
            r"kupit", r"zakazat", r"order", r"buy", r"bron", r"olaman"
        ]
        if any(re.search(p, t) for p in order_patterns):
            return "PURCHASE_INTENT", "POSITIVE", 0.94

        # Pricing check
        price_patterns = [
            r"narx", r"qancha", r"nechpul", r"necha pul", r"nech pul", r"qanchadan",
            r"how much", r"price", r"cost", r"цена", r"почем", r"скольк", r"стоим"
        ]
        if any(re.search(p, t) for p in price_patterns):
            return "PRICING", "NEUTRAL", 0.95

        # Location & Shipping
        shipping_patterns = [
            r"dastavk", r"yetkaz", r"dostavk", r"viloyat", r"manzil", r"qayerda",
            r"lokatsiya", r"qattan", r"adres", r"delivery", r"shipping", r"где"
        ]
        if any(re.search(p, t) for p in shipping_patterns):
            return "SHIPPING_LOCATION", "NEUTRAL", 0.92

        # Praise / Compliments
        praise_patterns = [
            r"zo['`]?r", r"gap yo['`]?q", r"daxshat", r"chiroyli", r"super",
            r"klass", r"molodets", r"ajoyib", r"krasivo", r"great", r"awesome", r"love"
        ]
        if any(re.search(p, t) for p in praise_patterns):
            return "COMPLIMENT", "POSITIVE", 0.96

        # Greetings
        greeting_patterns = [
            r"salom", r"assalom", r"privet", r"zdravstvuyte", r"hello", r"hi", r"hey"
        ]
        if any(re.search(p, t) for p in greeting_patterns):
            return "GREETING", "NEUTRAL", 0.90

        # Complaint / Negative
        negative_patterns = [
            r"yomon", r"yoqmadi", r"aldov", r"qimmat", r"brak", r"ploxo", r"bad", r"scam", r"musor"
        ]
        if any(re.search(p, t) for p in negative_patterns):
            return "COMPLAINT", "NEGATIVE", 0.88

        return "GENERAL_INQUIRY", "NEUTRAL", 0.75

    def generate_reply(self, comment_text: str, username: str = "aziz_foydalanuvchi", custom_rules: Dict[str, str] = None) -> Dict[str, Any]:
        intent, sentiment, confidence = self.classify_intent_and_sentiment(comment_text)

        price_val = (custom_rules or {}).get("price", self.default_price)
        brand = (custom_rules or {}).get("brand_name", self.brand_name)

        replies = {
            "PRICING": [
                f"Assalomu alaykum @{username}! 💫 Narxi: {price_val}. To'liq ma'lumot va maxsus taklifni Directingizga yubordik! 📩",
                f"Salom @{username}! Ushbu mahsulotimiz narxi {price_val}. Batafsil ko'rish uchun Direct xabaringizni tekshirib ko'ring! 🎁",
                f"Assalomu alaykum @{username}! Narxi {price_val} tashkil qiladi. Havola Directingizda kutmoqda! ✨"
            ],
            "COMPLIMENT": [
                f"Katta rahmat @{username}! Sizning fikringiz biz uchun juda qadrli! ❤️🔥",
                f"Ajoyib so'zlaringiz uchun tashakkur @{username}! Yangi videolarimizni kuzatib boring! 🚀✨",
                f"Minnatdormiz @{username}! Sizga yoqqanidan judayam xursandmiz! 💫😊"
            ],
            "SHIPPING_LOCATION": [
                f"Assalomu alaykum @{username}! Barcha viloyatlarga 1-2 kunda tezkor yetkazib berish xizmati mavjud! 🚚📦 Directingizga ma'lumot yubordik.",
                f"Salom @{username}! Butun respublika bo'ylab yetkazib beramiz. Toshkent shahrida 24 soat ichida yetib boradi! 📍✈️",
                f"Assalomu alaykum @{username}! Manzilimiz va yetkazib berish shartlarini Direct orqali yubordik! 🗺️📩"
            ],
            "PURCHASE_INTENT": [
                f"Assalomu alaykum @{username}! Buyurtma qilish juda oson: hoziroq Directga o'ting yoki profilingizdagi havolani bosing! 🛒⚡",
                f"Ajoyib tanlov @{username}! Tezkor buyurtma rasmiylashtirish uchun Directingizga xabar yo'lladik! 📩🎉",
                f"Salom @{username}! Buyurtma uchun Directga yozishingiz yoki havoladan foydalanishingiz mumkin. Hoziroq bog'lanamiz! 🤝"
            ],
            "GREETING": [
                f"Assalomu alaykum @{username}! {brand} sahifasiga xush kelibsiz! Qanday yordam bera olamiz? 😊✨",
                f"Salom @{username}! Xush ko'rdik! Savollaringiz bo'lsa bemalol yozing! 🌟",
                f"Va alaykum assalom @{username}! Kuningiz xayrli va unumli o'tsin! 💫"
            ],
            "COMPLAINT": [
                f"Assalomu alaykum @{username}. Noqulaylik uchun uzr so'raymiz. Masalani zudlik bilan hal qilish uchun Direct orqali bog'lanishingizni so'raymiz! 🙏",
                f"Fikringiz uchun rahmat @{username}. Biz sifatga jiddiy qaraymiz, iltimos Direct orqali telefon raqamingizni qoldiring, bog'lanamiz! 📞"
            ],
            "GENERAL_INQUIRY": [
                f"Assalomu alaykum @{username}! Fikringiz uchun rahmat. Qo'shimcha savollaringiz bo'lsa Directga marhamat! 💬✨",
                f"Salom @{username}! Sahifamizda ekanligingizdan mamnunmiz. Yangiliklarni kuzatib boring! 🚀"
            ]
        }

        chosen_reply = random.choice(replies.get(intent, replies["GENERAL_INQUIRY"]))
        send_dm = intent in ["PRICING", "PURCHASE_INTENT", "SHIPPING_LOCATION"]
        dm_text = f"Assalomu alaykum @{username}! Postimizdagi izohingiz bo'yicha bog'lanmoqdamiz. Mahsulotimiz narxi: {price_val}. Buyurtma berish uchun telefon raqamingizni qoldiring yoki saytimizga o'ting!" if send_dm else None
        simulated_delay = random.uniform(3.5, 9.0)

        return {
            "intent": intent,
            "sentiment": sentiment,
            "confidence": confidence,
            "reply_text": chosen_reply,
            "send_dm": send_dm,
            "dm_text": dm_text,
            "humanized_delay_sec": round(simulated_delay, 2)
        }
