# LinkHub Backend API

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/JWT-black?logo=jsonwebtokens" alt="JWT">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker" alt="Docker">
</p>

## 📖 درباره پروژه

بک‌اند پلتفرم LinkHub - سرویسی مشابه Linktree برای اشتراک‌گذاری لینک‌ها.

### ✨ قابلیت‌ها

- 🔐 احراز هویت با JWT در کوکی‌های HTTP-only
- 📝 مدیریت کامل لینک‌ها (ایجاد، ویرایش، حذف)
- 👤 مدیریت پروفایل کاربر
- 🌐 صفحات عمومی برای هر کاربر
- 📊 آمار کلیک لینک‌ها
- 🎯 پشتیبانی از ۲۱ پلتفرم مختلف (اینستاگرام، تلگرام، سروش، ایتا، ...)

### 🛠 تکنولوژی‌ها

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Migration**: Alembic
- **Auth**: JWT + HTTP-only cookies
- **Validation**: Pydantic v2

## 🚀 نصب و اجرا

### پیش‌نیازها

- Python 3.11+
- PostgreSQL
- pip

### مراحل نصب

```bash
# 1. کلون کردن پروژه
git clone https://github.com/yourusername/linkhub-backend.git
cd linkhub-backend

# 2. ایجاد محیط مجازی
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate  # Windows

# 3. نصب وابستگی‌ها
pip install -r requirements.txt

# 4. تنظیم متغیرهای محیطی
cp .env.example .env
# ویرایش فایل .env با اطلاعات دیتابیس خودت

# 5. اجرای migrations
alembic upgrade head

# 6. اجرای سرور
uvicorn app.main:app --reload
```
