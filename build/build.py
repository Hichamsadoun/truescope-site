#!/usr/bin/env python3
"""Builds the site into dist/ from the content/ files edited in the dashboard (/admin).

Netlify runs this on every publish. Locally: pip install -r requirements.txt && python3 build/build.py
"""
import json
import shutil
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

from assets import ICON, LOGO_MARK, FAVICON

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
DIST = ROOT / "dist"

CSS = (BUILD / "base.css").read_text() + (BUILD / "extra.css").read_text()
RTL_CSS = (BUILD / "rtl.css").read_text()
SVC_ICONS = ["branch", "file", "clip", "cal", "trend", "shield", "settings"]
WHY_ICONS = ["pin", "wrench", "bars", "users"]
FONTS = {
    "en": "family=Inter:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400",
    "ar": "family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;600;700;800&family=Newsreader:opsz,wght@6..72,500",
}


def load(name):
    return json.loads((ROOT / "content" / name).read_text(encoding="utf-8"))


def highlight(text, phrase):
    """Escape text and wrap the first occurrence of phrase in <em>."""
    text, phrase = text or "", (phrase or "").strip()
    if phrase and phrase in text:
        a, b = text.split(phrase, 1)
        return Markup(f"{escape(a)}<em>{escape(phrase)}</em>{escape(b)}")
    return escape(text)


def schema(s, c):
    org = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": s["domain"] + "/#website", "url": s["domain"] + "/",
             "name": "True Scope for Business Consulting", "alternateName": "ترو سكوب لاستشارات الأعمال",
             "inLanguage": ["en", "ar"]},
            {"@type": "ProfessionalService", "@id": s["domain"] + "/#org",
             "name": "True Scope for Business Consulting", "alternateName": "ترو سكوب لاستشارات الأعمال",
             "description": c["ui"]["organization_description"], "url": s["domain"] + "/",
             "logo": s["domain"] + s["images"]["logo"], "image": s["domain"] + s["images"]["hero"],
             "email": s["email"],
             "address": {"@type": "PostalAddress", "streetAddress": "Laffan Tower, Floor 34",
                         "addressLocality": "Doha", "addressCountry": "QA"},
             "areaServed": [{"@type": "Country", "name": "Qatar"}, "Gulf Cooperation Council"],
             "knowsAbout": ["Project Management", "PMBOK", "Organizational Governance",
                            "Administrative Development", "Risk Management", "Quality Assurance"]},
        ],
    }
    if s.get("phone_link"):
        org["@graph"][1]["telephone"] = s["phone_link"]
    if s.get("linkedin"):
        org["@graph"][1]["sameAs"] = [s["linkedin"]]
    # "</" must not appear raw inside a <script> block
    return Markup(json.dumps(org, ensure_ascii=False, indent=1).replace("</", "<\\/"))


def render(env, lang, s, c):
    s = dict(s)
    s["domain"] = s["domain"].rstrip("/")
    icons = {k: Markup(v) for k, v in ICON.items()}
    f = c["contact"]["form"]
    js_cfg = json.dumps({"email": s["email"], "sending": f["sending"], "ok": f["success"], "err": f["error"]},
                        ensure_ascii=False).replace("</", "<\\/")
    return env.get_template("page.html").render(
        lang=lang, dir="rtl" if lang == "ar" else "ltr", c=c, s=s, i=icons,
        url=s["domain"] + ("/ar/" if lang == "ar" else "/"),
        home="/ar/" if lang == "ar" else "/",
        other_href="/" if lang == "ar" else "/ar/", other_lang="en" if lang == "ar" else "ar",
        fonts=FONTS[lang], css=Markup(CSS + (RTL_CSS if lang == "ar" else "")), favicon=FAVICON,
        logo_mark=Markup(LOGO_MARK.format(c1="#59636b", c2="#0f7a52")),
        logo_mark_foot=Markup(LOGO_MARK.format(c1="rgba(255,255,255,.5)", c2="#5fcf9c")),
        wa_link=f"https://wa.me/{''.join(ch for ch in s.get('whatsapp', '') if ch.isdigit())}?text={quote(c['contact']['whatsapp_message'])}",
        abs=lambda p: p if p.startswith("http") else s["domain"] + p,
        highlight=highlight, schema=schema(s, c), js_cfg=Markup(js_cfg),
        svc_icon=lambda n: icons[SVC_ICONS[n % len(SVC_ICONS)]],
        why_icon=lambda n: icons[WHY_ICONS[n % len(WHY_ICONS)]],
    )


def main():
    env = Environment(loader=FileSystemLoader(BUILD), autoescape=select_autoescape(["html"]),
                      trim_blocks=False, lstrip_blocks=False)
    s = load("settings.json")
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "ar").mkdir(parents=True)
    (DIST / "index.html").write_text(render(env, "en", s, load("en.json")), encoding="utf-8")
    (DIST / "ar" / "index.html").write_text(render(env, "ar", s, load("ar.json")), encoding="utf-8")
    shutil.copytree(ROOT / "images", DIST / "images")
    shutil.copytree(ROOT / "admin", DIST / "admin")
    # The dashboard preview reads the current images from here
    shutil.copy(ROOT / "content" / "settings.json", DIST / "admin" / "settings.json")
    print("Built dist/index.html and dist/ar/index.html")


if __name__ == "__main__":
    main()
