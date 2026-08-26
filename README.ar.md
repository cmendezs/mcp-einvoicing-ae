# mcp-einvoicing-ae 🇦🇪

[English](README.md) | [العربية](README.ar.md)

<!-- mcp-name: io.github.cmendezs/mcp-einvoicing-ae -->

[![PyPI version](https://badge.fury.io/py/mcp-einvoicing-ae.svg)](https://badge.fury.io/py/mcp-einvoicing-ae)
[![Python](https://img.shields.io/pypi/pyversions/mcp-einvoicing-ae.svg)](https://pypi.org/project/mcp-einvoicing-ae/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

---

> **مرحلة الهيكل الأولي، لم يُنشر بعد.** يحتوي هذا المستودع على هيكل الحزمة فقط.
> لا توجد أدوات أو نماذج أو أدوات تحقق منفَّذة حتى الآن، ولم يُصدر أي إصدار موسوم.
> راجع [الحالة الراهنة](#الحالة-الراهنة) لمعرفة ما يعيق التنفيذ.

---

## المقدمة

`mcp-einvoicing-ae` هو خادم [MCP (Model Context Protocol)](https://modelcontextprotocol.io)
سيوفر أدوات للفوترة الإلكترونية في دولة الإمارات العربية المتحدة. وهو جزء من عائلة الخوادم
القُطرية `mcp-einvoicing-*`، وجميعها مبنية على
[`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core)، الذي يوفر محرك
التحقق المشترك، وتجريدات EN 16931، وأدوات شبكة Peppol.

---

## الحالة الراهنة

الحزمة في مرحلة الهيكل الأولي، وستبقى كذلك مدة أطول من الحزم الشقيقة عن قصد. فإلى جانب
غياب المواصفة المعتادة، لم يتأكد نشر ملف الاعتماد الإماراتي نفسه.

| المجال | الحالة |
|---|---|
| المستودع، والتكامل المستمر، ووثائق الحوكمة | مكتمل |
| هيكل الحزمة (بنية `src/`، ونقطة دخول الخادم) | مكتمل |
| حالة نشر PINT AE | **غير مؤكدة** |
| المواصفات المعيارية ضمن `specs/` | **مفقودة** |
| المعايير المدعومة ومعرفات الملفات (URN) | معطَّل |
| نموذج الفاتورة وأدوات التحقق | معطَّل |
| أدوات MCP | معطَّل |
| الإصدار الأول (`v0.1.0`) | معطَّل |

### شرط النشر

عند آخر تحقق من فهرس وثائق ملفات الاعتماد القُطرية لدى OpenPeppol بتاريخ 2026-06-29، كانت
الملفات المنشورة هي: الاتحاد الأوروبي، وسنغافورة، وأستراليا ونيوزيلندا، واليابان، وماليزيا.
ولم تكن دولة الإمارات ضمن تلك القائمة. توجد أوصاف عامة لملف باسم "PINT AE"، غير أن الوصف
ليس مواصفة معيارية ولا يمكنه إثبات بيان مطابقة أو تحديد قيمة `CustomizationID`.

لذلك ينتظر التنفيذ وثيقةً تُثبت **حالة النشر**، لا محتوى الملف وحده. وإذا لم يوجد سوى مسودة
أو قاموس بيانات، تبقى هذه الحزمة هيكلاً موثَّقاً. راجع [`specs/README.md`](specs/README.md)
للاطلاع على قائمة الوثائق المطلوبة.

---

## المعايير المدعومة

`[NEED: confirm from a published PINT AE specification]`

يوصَف البرنامج الإماراتي بأنه نموذج Peppol لامركزي بخمس زوايا يمر عبر مزودي خدمة معتمدين
(ASPs)، وهو ما يضيف مسار إبلاغ إلى السلطة الضريبية يتجاوز التبادل رباعي الزوايا المستخدم في
بقية حزم هذه العائلة. أما صيغة النقل، ومعرفات الملفات، وعلاقة المطابقة مع EN 16931، وما إذا
كان ربط JSON معيارياً إلى جانب XML، فكلها غير محسومة. يُملأ هذا القسم من المواصفة، لا من
الذاكرة.

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
