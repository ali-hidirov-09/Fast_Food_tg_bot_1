# 🍔 Fast Food Telegram Bot

Telegram orqali fast food buyurtma berish uchun avtomatlashtirilgan bot. Foydalanuvchilar menu ko'rib, buyurtma berib, to'lovni amalga oshirib, delivery tracking qila oladilar.

## 📋 Ihtiyoti

### Asosiy Features

- ✅ **Foydalanuvchi Registratsiyasi** - Ismi, familiyasi, telefon raqami saqlash
- ✅ **Multilingual Interface** - Uzbek, Russian, Kazakh tillarida
- ✅ **Kategoriyalangan Menu** - Iyerarxik kategoriyalar va produktlar
- ✅ **Shopping Cart** - Savatcha boshqaruvi va o'chirish
- ✅ **Order Management** - Buyurtma yaratish va tarixni ko'rish
- ✅ **Location Tracking** - GPS koordinatalar bilan delivery
- ✅ **Admin Notifications** - Adminlarga real-time buyurtma xabarlari
- ✅ **Payment Integration** - Naqd pul va Kaspi.kz to'lovi
- ✅ **Multi-language Messages** - Barcha xabarlar 3 tilda

## 🛠️ Texnologiyalar
Python 3.8+ python-telegram-bot 13.15 sqlite3 APScheduler 3.6.3 python-dotenv 1.1.1




## 🚀 Boshlanish

### 1. Repo-ni Clone Qilish

```bash
git clone https://github.com/ali-hidirov-09/Fast_Food_tg_bot_1.git
cd Fast_Food_tg_bot_1
2. Virtual Environment Yaratish
bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
3. Dependencies O'rnatish
bash
pip install -r requirements.txt
4. Environment Variables Sozlash
.env fayli yaratingiz:

env
TOKEN=your_telegram_bot_token_here
DB_PATH=fast_food.db
ADMIN_IDS=123456789,987654321
Token olish:

Telegram da @BotFather ga yozing
/newbot komandasini yuboring
Bot nomini va username-ni kiriting
TOKEN ni nusxalab oling
5. Database Sozlash
bash
# Database avtomatik yaratiladi, lekin schema uchun:
sqlite3 fast_food.db < structure.sql
Database Tables:

user - Foydalanuvchilar (id, chat_id, ismi, familiyasi, telefon, tili)
category - Kategoriyalar (id, nomi, rasmlar, parent_id)
product - Produktlar (id, nomi, narxi, tasviri, rasmi)
order - Buyurtmalar (id, user_id, status, to'lov turi, lokatsiya)
order_product - Buyurtmadagi produktlar
6. Botni Ishga Tushirish
bash
cd evos_full_bot
python main.py
Bot polling rejimida ishga tushadi va xabarlarni qabul qila boshlaydi.

📱 Foydalanuvchi Flow
Code
User -> /start
    ↓
Tili tanlash (Uz/Ru/Kz)
    ↓
Ismi, familiyasi, tel. raqami kiritish
    ↓
Asosiy menyu
    ├─ 🛒 Buyu

rtma → Kategoriyalar → Produktlar → Savatcha
    ├─ 🛍 Mening buyurtmalarim → Order history
    ├─ 👨‍👩‍👦 Bizimizdagi → About us
    └─ ⚙️ Sozlamalar → User settings
    ↓
Savatcha → To'lov turi (Naqd/Kaspi.kz) → Lokatsiya → Tasdiqlash
    ↓
Admin notifikatsiya + Order saved
🔧 Konfiguratsiya
config.py
Python
TOKEN = os.getenv("TOKEN")           # Telegram Bot Token
DB_PATH = os.getenv("DB_PATH", "fast_food.db")  # Database path
ADMIN_IDS = [123456789, 987654321]   # Admin chat ID-lari
LANGUAGES = ['uz', 'ru', 'en']       # Qo'llab-quvvatlanadigan tillar
globals.py
Barcha xabarlar va tugmalar 3 tilda saqlanadi:

1 - Uzbek (uz)
2 - Russian (ru)
3 - Kazakh (kz)
Python
TEXT_ENTER_FIRST_NAME = {
    1: "Ilтимос, исмингизни киритинг!",
    2: "Пожалуйста, введите ваше имя!",
    3: "Өтінемін, атыңызды енгізіңіз!"
}
Bot Inline Buttons va Reply Keyboards dan foydalanadi:

Inline Buttons (Buyurtma interfeysi)
Code
[Категория 1] [Категория 2]
[Товар 1]     [Товар 2]
     1️⃣  2️⃣  3️⃣
     [Назад]
Reply Keyboards (Lokatsiya, Kontakt)
Code
[📍 Локацию жіберіңіз]
[📞 Контактни юбориш]
📚 Qo'shimcha Resurslar
Telegram Bot API Dokumentatsiyasi
python-telegram-bot Docs
SQLite Tutorials
Python Best Practices
Last Updated: 13.05.2026

Version: 1.0.0

Loyihani yaxshi ko'rsatganingiz uchun rahmat! ⭐ Agar yoqdigan bo'lsa, Star bering 🌟