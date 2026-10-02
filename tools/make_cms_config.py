"""Generates admin/config.yml (Decap CMS) from the shape of content/*.json. YAML accepts JSON, so it is written as JSON."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "Hichamsadoun/truescope-site"

L = {  # Arabic labels for the dashboard
 "seo": "محركات البحث والمشاركة", "title": "العنوان", "description": "الوصف", "share_text": "نص المشاركة على وسائل التواصل",
 "nav": "القائمة العلوية", "mission": "الرسالة", "services": "الخدمات", "approach": "المنهجية", "why": "لماذا نحن", "team": "فريق العمل", "cta": "زر طلب الاستشارة",
 "hero": "الواجهة الرئيسية", "eyebrow": "السطر الصغير فوق العنوان", "title_start": "العنوان: بداية الجملة", "title_highlight": "العنوان: الجزء الملوّن بالأخضر",
 "title_end": "العنوان: نهاية الجملة", "text": "النص", "button_secondary": "الزر الثاني", "image_alt": "وصف الصورة (لمحركات البحث)",
 "badges": "الشارات تحت الأزرار", "purpose": "الرسالة والرؤية", "heading": "عنوان القسم", "mission_label": "كلمة \"الرسالة\"",
 "mission_text": "نص الرسالة", "mission_highlight": "الجزء الملوّن من نص الرسالة", "vision_label": "كلمة \"الرؤية\"", "vision_text": "نص الرؤية",
 "vision_highlight": "الجزء الملوّن من نص الرؤية", "stats": "شريط الأرقام", "show": "إظهار هذا القسم في الموقع", "items": "العناصر",
 "number": "الرقم", "label": "الوصف", "clients": "شركاؤنا وعملاؤنا", "steps": "الخطوات", "case": "أهم مشاريعنا (دراسة حالة)",
 "sector": "القطاع", "details": "التفاصيل", "value": "القيمة", "results": "النتائج بالأرقام", "members": "الأعضاء", "name": "الاسم",
 "role": "المنصب", "photo": "الصورة الشخصية", "certificates": "الشهادات (افصل بينها بفاصلة)", "contact": "تواصل معنا",
 "phone_label": "عنوان الهاتف", "email_label": "عنوان البريد", "office_label": "عنوان المكتب", "office": "المكتب", "city": "المدينة",
 "map_title": "وصف الخريطة", "open_maps": "زر فتح الخرائط", "form": "نموذج التواصل", "organization": "خانة الجهة", "email": "خانة البريد",
 "phone": "خانة الهاتف", "interest": "خانة مجال الاهتمام", "interest_placeholder": "النص الافتراضي لمجال الاهتمام", "interests": "خيارات مجال الاهتمام",
 "message": "خانة الرسالة", "message_placeholder": "النص الافتراضي للرسالة", "send": "زر الإرسال", "note": "ملاحظة تحت الزر",
 "sending": "رسالة جارٍ الإرسال", "success": "رسالة نجاح الإرسال", "error": "رسالة الخطأ", "whatsapp_label": "وصف زر واتساب",
 "whatsapp_message": "الرسالة الجاهزة في واتساب", "footer": "التذييل أسفل الصفحة", "about": "نبذة", "explore": "عنوان روابط التصفح",
 "copyright": "حقوق النشر", "tagline": "السطر الأخير", "links": "روابط التذييل", "ui": "نصوص صغيرة أخرى", "skip": "رابط تخطي للمحتوى",
 "logo_subtitle": "النص تحت الشعار", "home_label": "وصف رابط الشعار", "open_menu": "زر فتح القائمة", "close_menu": "زر إغلاق القائمة",
 "switch_language": "زر تبديل اللغة", "client_logo_placeholder": "نص مكان شعار العميل", "organization_description": "وصف الشركة لمحركات البحث",
}
COLLAPSED = {"seo", "nav", "footer", "ui", "form", "badges", "details", "links"}
LONG = {"text", "description", "mission_text", "vision_text", "about", "share_text", "organization_description", "whatsapp_message"}
IMAGE = {"photo", "logo", "hero", "approach", "why"}


def field(key, val, top=False):
    f = {"name": key, "label": L.get(key, key)}
    if isinstance(val, bool):
        f.update(widget="boolean", default=False)
    elif isinstance(val, dict):
        f.update(widget="object", fields=[field(k, v) for k, v in val.items()])
        if key in COLLAPSED or top:
            f["collapsed"] = key in COLLAPSED or key not in {"hero"}
    elif isinstance(val, list):
        if val and isinstance(val[0], dict):
            f.update(widget="list", collapsed=True, fields=[field(k, v) for k, v in val[0].items()])
            f["summary"] = "{{fields.%s}}" % next(iter(val[0]))
        else:
            f.update(widget="list")
    elif key in IMAGE:
        f.update(widget="image", required=False)
    else:
        # Decap labels optional fields "(optional)"; only fields that may be blank stay optional.
        f.update(widget="text" if key in LONG else "string", required=bool(val))
    return f


def lang_file(name, label, path):
    data = json.loads((ROOT / path).read_text(encoding="utf-8"))
    return {"name": name, "label": label, "file": path, "fields": [field(k, v, top=True) for k, v in data.items()]}


settings = {"name": "settings", "label": "الإعدادات العامة (تواصل، صور، شعارات العملاء)", "file": "content/settings.json", "fields": [
    {"name": "domain", "label": "رابط الموقع (مثل https://www.truescopebc.com)", "widget": "string"},
    {"name": "email", "label": "البريد الإلكتروني", "widget": "string"},
    {"name": "phone_display", "label": "رقم الهاتف كما يظهر (مثل +974 5555 1234)", "widget": "string", "required": False},
    {"name": "phone_link", "label": "رقم الهاتف للاتصال المباشر (بدون مسافات، مثل +97455551234)", "widget": "string", "required": False},
    {"name": "whatsapp", "label": "رقم واتساب (أرقام فقط مع 974، مثل 97455551234)", "widget": "string", "required": False},
    {"name": "linkedin", "label": "رابط LinkedIn", "widget": "string", "required": False},
    {"name": "address_for_maps", "label": "العنوان على خرائط Google", "widget": "string"},
    {"name": "images", "label": "صور الموقع", "widget": "object", "fields": [
        {"name": "hero", "label": "صورة الخلفية الرئيسية (عرض 1600 بكسل أو أكثر)", "widget": "image"},
        {"name": "approach", "label": "صورة قسم المنهجية", "widget": "image"},
        {"name": "why", "label": "صورة قسم لماذا نحن", "widget": "image"},
        {"name": "logo", "label": "شعار الشركة (لمحركات البحث)", "widget": "image"}]},
    {"name": "clients", "label": "شعارات العملاء والشركاء", "widget": "list", "collapsed": True, "summary": "{{fields.name}}", "fields": [
        {"name": "name", "label": "اسم الجهة", "widget": "string"},
        {"name": "logo", "label": "الشعار", "widget": "image", "required": False}]},
]}

config = {
    "backend": {"name": "github", "repo": REPO, "branch": "main", "commit_messages": {"update": "Update {{slug}} from dashboard", "uploadMedia": "Upload {{path}}"}},
    "site_url": "https://www.truescopebc.com",
    "display_url": "https://www.truescopebc.com",
    "media_folder": "images/uploads",
    "public_folder": "/images/uploads",
    "collections": [{"name": "site", "label": "محتوى الموقع", "editor": {"preview": True}, "files": [
        lang_file("ar", "الصفحة العربية", "content/ar.json"),
        lang_file("en", "الصفحة الإنجليزية (English)", "content/en.json"),
        settings]}],
}
(ROOT / "admin" / "config.yml").write_text("# Generated by tools/make_cms_config.py\n" + json.dumps(config, ensure_ascii=False, indent=1), encoding="utf-8")
print("admin/config.yml written")
