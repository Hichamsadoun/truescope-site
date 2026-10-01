# موقع ترو سكوب لاستشارات الأعمال

موقع True Scope for Business Consulting بنسختين: الإنجليزية (`/`) والعربية (`/ar/`).

## تعديل المحتوى
ادخل على `/admin` في موقعك (مثل `https://www.truescopebc.com/admin`) وسجّل الدخول بحساب GitHub.
- **الصفحة العربية / الإنجليزية:** كل النصوص، وأزرار إظهار وإخفاء الأقسام (الأرقام، الشركاء، أهم مشاريعنا، فريق العمل).
- **الإعدادات العامة:** الهاتف، واتساب، البريد، LinkedIn، صور الموقع، شعارات العملاء.

بعد الضغط على **Publish** يعيد Netlify بناء الموقع تلقائيًا خلال دقيقة تقريبًا.

## رسائل نموذج التواصل
تصل إلى لوحة Netlify تحت **Forms**. لتصلك على البريد: Forms ← Form notifications ← Add notification ← Email.

## للمطوّرين
- المحتوى: `content/*.json`، والقالب: `build/page.html`، والتنسيق: `build/*.css`.
- البناء: `pip install -r requirements.txt && python3 build/build.py` ينتج مجلد `dist/`.
- إعداد اللوحة: `admin/config.yml` يُولَّد من `tools/make_cms_config.py`. أعد تشغيله إذا أضفت حقولًا جديدة إلى ملفات المحتوى.
