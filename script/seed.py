import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.models import User, Link
from app.core.security import get_password_hash


def seed():
    db = SessionLocal()

    try:
        print("\n" + "=" * 50)
        print("🌱 شروع مقداردهی اولیه دیتابیس...")
        print("=" * 50)

        # ساخت 150 کاربر
        print("\n👤 مرحله 1: ساخت 150 کاربر...")
        users = []
        
        for i in range(1, 151):
            username = f"user{i}"
            email = f"user{i}@example.com"
            name = f"کاربر {i}"
            namelink = f"user{i}"
            
            user = User(
                name=name,
                namelink=namelink,
                username=username,
                email=email,
                password_hash=get_password_hash("123456")
            )
            users.append(user)
            db.add(user)
            
            if i % 30 == 0:
                print(f"   ✅ {i} کاربر ساخته شد...")
        
        db.flush()  # برای گرفتن id کاربرها
        
        print("   ✅ 150 کاربر با موفقیت ساخته شدند!")
        
        # ساخت لینک برای هر کاربر (0 تا 10 لینک)
        print("\n🔗 مرحله 2: ساخت لینک برای کاربران (0 تا 10 لینک)...")
        
        links_data = [
            # (title, url, icon)
            ("اینستاگرام", "https://instagram.com/user", "instagram"),
            ("تلگرام", "https://t.me/user", "telegram"),
            ("توییتر", "https://twitter.com/user", "twitter"),
            ("یوتیوب", "https://youtube.com/@user", "youtube"),
            ("گیت‌هاب", "https://github.com/user", "github"),
            ("لینکدین", "https://linkedin.com/in/user", "linkedin"),
            ("فیس بوک", "https://facebook.com/user", "facebook"),
            ("وبسایت شخصی", "https://example.com", "website"),
            ("بلاگ", "https://blog.example.com", "link"),
            ("واتساپ", "https://wa.me/09123456789", "whatsapp"),
        ]
        
        total_links = 0
        
        for idx, user in enumerate(users):
            # تعداد لینک تصادفی بین 0 تا 10
            import random
            num_links = random.randint(0, 10)
            
            if num_links > 0:
                # انتخاب لینک‌های تصادفی از لیست بالا
                selected_links = random.sample(links_data, min(num_links, len(links_data)))
                
                # اگه تعداد لینک بیشتر از لیست بود، تکرار کن
                while len(selected_links) < num_links:
                    selected_links.append(random.choice(links_data))
                
                for order, (title, url, icon) in enumerate(selected_links):
                    # اضافه کردن شماره کاربر به یوآرال برای یکتا شدن
                    unique_url = url.replace("user", f"user{user.id}")
                    
                    link = Link(
                        user_id=user.id,
                        title=f"{title} {user.id}" if num_links > 5 else title,
                        url=unique_url,
                        icon=icon,
                        clicks=random.randint(0, 1000),
                        order=order
                    )
                    db.add(link)
                    total_links += 1
            
            # نمایش پیشرفت هر 30 کاربر
            if (idx + 1) % 30 == 0:
                print(f"   📝 {idx + 1} کاربر پردازش شد...")
        
        db.commit()
        
        # آمار نهایی
        print("\n" + "=" * 50)
        print("✅ مقداردهی اولیه با موفقیت انجام شد!")
        print("=" * 50)
        print(f"\n📊 آمار نهایی:")
        print(f"   👥 تعداد کاربران: {len(users)}")
        print(f"   🔗 تعداد کل لینک‌ها: {total_links}")
        print(f"   📈 میانگین لینک به ازای هر کاربر: {total_links/len(users):.1f}")
        
        # نمایش نمونه کاربران (10 کاربر اول به جای 5)
        print("\n🎯 نمونه کاربران ساخته شده (10 کاربر اول):")
        sample_users = users[:10]
        for user in sample_users:
            user_links = db.query(Link).filter(Link.user_id == user.id).count()
            print(f"   • {user.username} ({user.name}) - {user_links} لینک")
        
        print("\n🔑 اطلاعات ورود:")
        print("   ایمیل: user1@example.com تا user150@example.com")
        print("   رمز عبور: 123456")
        print("\n✨ عملیات با موفقیت پایان یافت!\n")

    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed()