# mcp-einvoicing-ae 🇦🇪

[English](README.md) | [العربية](README.ar.md)

<!-- mcp-name: io.github.cmendezs/mcp-einvoicing-ae -->

[![PyPI version](https://badge.fury.io/py/mcp-einvoicing-ae.svg)](https://badge.fury.io/py/mcp-einvoicing-ae)
[![Python](https://img.shields.io/pypi/pyversions/mcp-einvoicing-ae.svg)](https://pypi.org/project/mcp-einvoicing-ae/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

---

> **تم توفير المواصفات، والحزمة لم تُنشر بعد.** انتهى شرط النشر الخاص بـ PINT AE وTDD في
> 2026-08-26 بعد توفير المواصفات المعيارية وإرشادات الهيئة الاتحادية للضرائب. لا توجد شيفرة
> نموذج أو أدوات تحقق أو أدوات MCP حتى الآن، ولم يُصدر أي إصدار موسوم.
> راجع [الحالة الراهنة](#الحالة-الراهنة) لمعرفة ما تبقى معيقاً للتنفيذ.

---

## المقدمة

`mcp-einvoicing-ae` هو خادم [MCP (Model Context Protocol)](https://modelcontextprotocol.io)
سيوفر أدوات للفوترة الإلكترونية في دولة الإمارات العربية المتحدة. وهو جزء من عائلة الخوادم
القُطرية `mcp-einvoicing-*`، وجميعها مبنية على
[`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core)، الذي يوفر محرك
التحقق المشترك، وتجريدات EN 16931، وأدوات شبكة Peppol.

---

## الحالة الراهنة

تم توفير المواصفات المعيارية وإرشادات الهيئة الاتحادية للضرائب بتاريخ 2026-08-26، ما أدى إلى
حسم شرط حالة النشر ومسار شجرة الفاتورة. لا توجد بعد شيفرة للنموذج أو أدوات التحقق أو الأدوات،
إذ يلزم أولاً فحص الفجوات في مكتبة `mcp-einvoicing-core` المشتركة.

| المجال | الحالة |
|---|---|
| المستودع، والتكامل المستمر، ووثائق الحوكمة | مكتمل |
| هيكل الحزمة (بنية `src/`، ونقطة دخول الخادم) | مكتمل |
| حالة نشر PINT AE | **مؤكدة** (2026-08-26) |
| المواصفات المعيارية ضمن `specs/` | **متوفرة** (2026-08-26) |
| مسار شجرة الفاتورة | **مؤكد** — `EN16931Invoice` |
| المعايير المدعومة ومعرفات الملفات (URN) | **معروفة** — انظر أدناه |
| فحص فجوات `mcp-einvoicing-core` | معلَّق |
| نموذج الفاتورة وأدوات التحقق | معطَّل (بانتظار فحص الفجوات) |
| أدوات MCP | معطَّل |
| الإصدار الأول (`v0.1.0`) | معطَّل |

### شرط النشر — تم حسمه في 2026-08-26

عند التحقق السابق من فهرس وثائق ملفات الاعتماد القُطرية لدى OpenPeppol بتاريخ 2026-06-29، كانت
الملفات المنشورة هي: الاتحاد الأوروبي، وسنغافورة، وأستراليا ونيوزيلندا، واليابان، وماليزيا،
ولم تكن دولة الإمارات ضمنها. تحسم الوثائق الموفَّرة بتاريخ 2026-08-26 هذه المسألة: تُسجّل
ملاحظات الإصدار الخاصة بهيئة Peppol الإماراتية ملف PINT AE (الفوترة) بحالة **"Status: Final"**،
الإصدار 1.0.4، الصادر في 2026-06-02، ووثيقة بيانات الضريبة Peppol AE TDD (وهي الزاوية الخامسة
لمسار الإبلاغ) بحالة **"Status: Final"**، الإصدار 1.0.3، الصادر في 2026-05-25. كما تنص إرشادات
الهيئة الاتحادية للضرائب الصادرة في يونيو 2026 صراحةً على أن مواصفات PINT-AE للفوترة
*"منشورة على موقعها الإلكتروني."*

يبقى تحفظ واحد مفتوحاً: هذه تسمية حالة الإصدار الخاصة بجهة نشر المواصفة نفسها، وليست تأكيداً
مستقلاً من صفحة سجل حوكمة OpenPeppol. تُعامَل كدليل قوي، لا كيقين تام. للاطلاع على التفاصيل
والمراجع الكاملة: [`specs/README.md`](specs/README.md) وملف
[`context-library/countries/ae.md`](https://github.com/cmendezs/mcp-einvoicing/blob/main/context-library/countries/ae.md)
في المستودع الرئيسي للمشروع.

---

## المعايير المدعومة

- **PINT AE (الفوترة)** — UBL 2.1، `CustomizationID: urn:peppol:pint:billing-1@ae-1`،
  `ProfileID: urn:peppol:bis:billing`. الإصدار 1.0.4 (2026-06-02).
- **PINT AE (الفوترة الذاتية)** — `CustomizationID: urn:peppol:pint:selfbilling-1@ae-1`،
  `ProfileID: urn:peppol:bis:selfbilling`.
- **وثيقة بيانات الضريبة Peppol AE TDD** — وثيقة الإبلاغ للزاوية الخامسة المرسَلة إلى الهيئة
  الاتحادية للضرائب؛ لها مساحة اسم XML خاصة بها (`urn:peppol:schema:taxdata:1.0`)، وليست فاتورة
  UBL. الإصدار 1.0.3 (2026-05-25).

البرنامج الإماراتي هو نموذج Peppol لامركزي بخمس زوايا يمر عبر مزودي خدمة معتمدين (ASPs)،
يضيف مسار إبلاغ إلى السلطة الضريبية (وثيقة TDD أعلاه) يتجاوز التبادل رباعي الزوايا المستخدم في
بقية حزم هذه العائلة. مسار شجرة الفاتورة مؤكَّد وهو `EN16931Invoice` (فملف PINT AE هو نسخة
تخصيص من UBL 2.1 لمعيار EN 16931-1:2017) — ولم يُعثر على أي ربط بصيغة JSON في المواصفات
الموفَّرة. تنتظر شيفرة النموذج وأدوات التحقق والأدوات فحص فجوات في المكتبة المشتركة
(`TaxIdentifier.validate_ae_trn()`، وثوابت سجل ملفات PINT AE، وآلية نقل وثيقة TDD هي الفجوات
المعروفة). للتفاصيل الكاملة: [`specs/README.md`](specs/README.md).

---

## التثبيت

### المتطلبات

- Python ≥ 3.11
- [`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core) (يُثبَّت تلقائياً
  باعتباره اعتمادية)

### باستخدام `uvx` (الأسلوب المفضل، بعد النشر)

```bash
uvx mcp-einvoicing-ae
```

### باستخدام `uv`

```bash
uv add mcp-einvoicing-ae
```

### من الشيفرة المصدرية

```bash
git clone https://github.com/cmendezs/mcp-einvoicing-ae.git
cd mcp-einvoicing-ae
uv sync --all-extras
```

---

## الإعداد

أضف الخادم إلى إعدادات عميل MCP لديك:

```json
{
  "mcpServers": {
    "einvoicing-ae": {
      "command": "uvx",
      "args": ["mcp-einvoicing-ae"]
    }
  }
}
```

### متغيرات البيئة

| المتغير | مطلوب | القيمة الافتراضية | الوصف |
|---|---|---|---|
| `LOG_LEVEL` | لا | `INFO` | مستوى السجل: `DEBUG` أو `INFO` أو `WARNING` أو `ERROR` |

تُضاف المتغيرات الخاصة بالدولة (نقاط النقل، وبيانات الاعتماد، ومفاتيح تبديل البيئة) بمجرد أن
توثّقها المواصفة. راجع [`.env.example`](.env.example).

---

## الأدوات

لا توجد أدوات بعد. يعمل الخادم في هذه المرحلة دون تسجيل أي أداة.

يُولَّد مرجع الأدوات في [`docs/TOOLS.md`](docs/TOOLS.md) من الخادم أثناء تشغيله:

```bash
uv run python scripts/gen_tool_reference.py
```

---

## المساهمة

راجع [CONTRIBUTING.md](CONTRIBUTING.md) للاطلاع على إعداد بيئة التطوير، وأوامر الاختبار
والتدقيق، وقائمة تحقق طلبات السحب. أما المشكلات الأمنية فتتبع مسار الإفصاح الخاص الموضح في
[SECURITY.md](SECURITY.md).

---

## Other e-invoicing MCP servers

| Country | Server |
|---------|--------|
| 🌍 Global | [mcp-einvoicing-core](https://github.com/cmendezs/mcp-einvoicing-core) |
| 🇧🇪 Belgium | [mcp-einvoicing-be](https://github.com/cmendezs/mcp-einvoicing-be) |
| 🇧🇷 Brazil | [mcp-nfe-br](https://github.com/cmendezs/mcp-nfe-br) |
| 🇫🇷 France | [mcp-facture-electronique-fr](https://github.com/cmendezs/mcp-facture-electronique-fr) |
| 🇩🇪 Germany | [mcp-einvoicing-de](https://github.com/cmendezs/mcp-einvoicing-de) |
| 🇮🇹 Italy | [mcp-fattura-elettronica-it](https://github.com/cmendezs/mcp-fattura-elettronica-it) |
| 🇵🇱 Poland | [mcp-ksef-pl](https://github.com/cmendezs/mcp-ksef-pl) |
| 🇸🇬 Singapore | [mcp-invoicenow-sg](https://github.com/cmendezs/mcp-invoicenow-sg) |
| 🇪🇸 Spain | [mcp-facturacion-electronica-es](https://github.com/cmendezs/mcp-facturacion-electronica-es) |
| 🇦🇪 United Arab Emirates | [mcp-einvoicing-ae](https://github.com/cmendezs/mcp-einvoicing-ae) |

---

## الترخيص

هذا المشروع مرخَّص بموجب رخصة **Apache 2.0**، راجع [LICENSE](LICENSE) للتفاصيل.
