from enum import Enum
from urllib.parse import quote
from typing import Optional
import re


def normalize_username(username: str) -> str:
    """Normalize username: trim, replace spaces/underscores with hyphens"""
    if not username:
        return username
    username = username.strip()
    username = username.replace(" ", "-").replace("_", "-")
    username = re.sub(r"-+", "-", username)
    if len(username) < 3 or len(username) > 50:
        raise ValueError("Username must be between 3 and 50 characters")
    if not re.match(r"^[a-zA-Z0-9-]+$", username):
        raise ValueError("Username can only contain letters, numbers, and hyphens")

    return username


class Platform(str, Enum):
    SOROUSH = "soroush"
    APARAT = "aparat"
    EITAA = "eitaa"
    RUBIKA = "rubika"
    BALE = "bale"
    INSTAGRAM = "instagram"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    GITHUB = "github"
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"
    SPOTIFY = "spotify"
    DISCORD = "discord"
    WEBSITE = "website"
    PHONE = "phone"
    EMAIL = "email"
    LOCATION = "location"
    LINK = "link"


def normalize_url_by_platform(url: str, icon: Optional[Platform]) -> str:
    """Normalize URL based on platform type"""
    if not url or not icon:
        return url

    if icon == Platform.SOROUSH:
        if not url.startswith("soroush://"):
            url = "soroush://" + url.lstrip("/")

    elif icon == Platform.APARAT:
        if not url.startswith("aparat://"):
            url = "aparat://" + url.lstrip("/")

    elif icon == Platform.EITAA:
        if not url.startswith("eitaa://"):
            url = "eitaa://" + url.lstrip("/")
            
    elif icon == Platform.BALE:
        if not url.startswith("bale://"):
            url = "bale://" + url.lstrip("/")

    elif icon == Platform.RUBIKA:
        if not url.startswith("rubika://"):
            url = "rubika://" + url.lstrip("/")

    elif icon == Platform.INSTAGRAM:
        if not url.startswith(("https://instagram.com/", "https://www.instagram.com/")):
            username = url.strip("/").lstrip("@")
            url = f"https://instagram.com/{username}"

    elif icon == Platform.WHATSAPP:
        if not url.startswith(("https://wa.me/", "whatsapp://")):
            clean_url = "".join(filter(str.isdigit, url))
            url = "https://wa.me/" + clean_url.lstrip("0")

    elif icon == Platform.TELEGRAM:
        if not url.startswith(("https://t.me/", "tg://")):
            username = url.lstrip("@")
            url = f"https://t.me/{username}"

    elif icon == Platform.TWITTER:
        if not url.startswith(("https://twitter.com/", "https://x.com/")):
            username = url.lstrip("@")
            url = f"https://x.com/{username}"

    elif icon == Platform.LINKEDIN:
        if not url.startswith("https://linkedin.com/"):
            username = url.lstrip("@")
            url = f"https://linkedin.com/in/{username}"

    elif icon == Platform.GITHUB:
        if not url.startswith("https://github.com/"):
            username = url.lstrip("@")
            url = f"https://github.com/{username}"

    elif icon == Platform.YOUTUBE:
        if not url.startswith(("https://youtube.com/", "https://youtu.be/")):
            channel = url.lstrip("@")
            url = f"https://youtube.com/channel/{channel}"

    elif icon == Platform.FACEBOOK:
        if not url.startswith("https://facebook.com/"):
            username = url.lstrip("@")
            url = f"https://facebook.com/{username}"

    elif icon == Platform.TIKTOK:
        if not url.startswith("https://tiktok.com/@"):
            username = url.lstrip("@")
            url = f"https://tiktok.com/@{username}"

    elif icon == Platform.SPOTIFY:
        if not url.startswith(("https://open.spotify.com/", "spotify://")):
            url = "https://open.spotify.com/" + url.lstrip("/")

    elif icon == Platform.DISCORD:
        if not url.startswith(("https://discord.gg/", "discord://")):
            url = "https://discord.gg/" + url.lstrip("/")

    elif icon == Platform.WEBSITE:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

    elif icon == Platform.PHONE:
        if not url.startswith("tel:"):
            clean_number = "".join(filter(str.isdigit, url))
            url = "tel:" + clean_number

    elif icon == Platform.EMAIL:
        if not url.startswith("mailto:"):
            url = "mailto:" + url

    elif icon == Platform.LOCATION:
        if not url.startswith(("https://maps.google.com/", "geo:")):
            url = "https://maps.google.com/?q=" + quote(url)

    elif icon == Platform.LINK:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

    return url
