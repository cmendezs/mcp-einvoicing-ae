# mcp-einvoicing-ae 🇦🇪

[English](README.md) | [العربية](README.ar.md)

<!-- mcp-name: io.github.cmendezs/mcp-einvoicing-ae -->

[![PyPI version](https://badge.fury.io/py/mcp-einvoicing-ae.svg)](https://badge.fury.io/py/mcp-einvoicing-ae)
[![Python](https://img.shields.io/pypi/pyversions/mcp-einvoicing-ae.svg)](https://pypi.org/project/mcp-einvoicing-ae/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![mcp-einvoicing-ae MCP server](https://glama.ai/mcp/servers/cmendezs/mcp-einvoicing-ae/badges/score.svg)](https://glama.ai/mcp/servers/cmendezs/mcp-einvoicing-ae)

---

## المقدمة

`mcp-einvoicing-ae` هو خادم [MCP (Model Context Protocol)](https://modelcontextprotocol.io)
يوفر أدوات للفوترة الإلكترونية في دولة الإمارات العربية المتحدة. وهو جزء من عائلة الخوادم
القُطرية `mcp-einvoicing-*`، وجميعها مبنية على
[`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core)، الذي يوفر محرك
التحقق المشترك، وتجريدات EN 16931، وأدوات شبكة Peppol.

أصبحت فواتير PINT AE المُولَّدة مطابقة هيكلياً: يتم إصدار `cbc:UUID` وَ`cbc:ProfileExecutionID`
وَ`cac:ItemPriceExtension` لكل بند، إضافة إلى `trade_license_number`، وتُستعاد جميعها عند
التحليل عبر `parse_invoice_ae`. أصبح معدل ضريبة القيمة المضافة القياسي 5.00% مفروضاً عبر مدقق
نموذجي، كما تتوفر أداة للبحث عن مشاركي شبكة Peppol. تتحقق الأداة `validate_invoice_ae` فقط وفق
مخطط Schematron الأساسي المشترك CEN EN16931 (وليس طبقة الولاية القضائية PINT AE)؛ وتُعيد الأداة
`validate_tdd_ae` حالياً نتيجة "غير متاحة" — انظر [المعايير المدعومة](#المعايير-المدعومة)
وَ[الأدوات المتاحة](#الأدوات-المتاحة) أدناه.

يُصنَّف ملف PINT AE (الفوترة) لدى هيئة Peppol الإماراتية بحالة **Status: Final**، الإصدار
1.0.4 (2026-06-02)؛ وتُصنَّف وثيقة بيانات الضريبة Peppol AE TDD بحالة Status: Final، الإصدار
1.0.3 (2026-05-25). للاطلاع على المراجع الكاملة: [`specs/README.md`](specs/README.md) وملف
[`context-library/countries/ae.md`](https://github.com/cmendezs/mcp-einvoicing/blob/main/context-library/countries/ae.md)
في المستودع الرئيسي للمشروع.

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
الموفَّرة.

يعيد `AEInvoice` استخدام
`mcp_einvoicing_core.wire_formats.EN16931UBLSerializer`/`EN16931UBLParser` مباشرةً بدلاً من
مُسلسِل مخصص، إذ يحمل الحقلان `profile`/`business_process` معرفات Peppol الفعلية. يحمل الحقل
`AEParty.vat_id` رقم TRN المكوَّن من 15 رقماً، ويُتحقق من صيغته عبر
`TaxIdentifier.validate_ae_trn()` (الإصدار 1.22.0 من المكتبة المشتركة)؛ ويُشتق معرف مشارك
Peppol (TIN) تلقائياً من أول 10 أرقام منه. يُمثّل `AETaxDataDocument` الحقول الإلزامية لوثيقة
TDD لكنه ليس فاتورة UBL وليس مبنياً على `AEInvoice`. تعيد أدوات MCP استخدام هذه البنية مباشرةً —
انظر [الأدوات المتاحة](#الأدوات-المتاحة) لمعرفة ما تغطيه وما لا تغطيه. تبقى قناة نقل TDD (القناة
نفسها المستخدمة للفاتورة عبر AS4 أم قناة منفصلة) مسألة توثيقية مفتوحة، لا فجوة برمجية. للتفاصيل
الكاملة: [`specs/README.md`](specs/README.md).

**نطاق التحقق اعتباراً من v0.2.0:** تتحقق الأداة `validate_invoice_ae` وفق مخطط Schematron
الأساسي CEN EN16931 فقط (القواعد البنيوية والحسابية/الإجمالية، المشتركة مع
`mcp-einvoicing-be`/`mcp-ksef-pl`) — وليس وفق قواعد الولاية القضائية لـPINT AE (قواعد
`ibr-*-ae`). من المتوقع أن تظهر القاعدة `BR-CO-09` (يجب أن يحمل معرف ضريبة القيمة المضافة بادئة
ISO 3166-1 alpha-2) في كل فاتورة إماراتية أصيلة، إذ لا تحمل أرقام TRN الإماراتية أي بادئة دولة؛
وهذا أمر مُفصَح عنه في كل نتيجة، وليس عيباً في بياناتك. لا يتوفر حالياً أي تحقق للأداة
`validate_tdd_ae` على الإطلاق. ضمّن الإصدار v0.1.0 خمسة ملفات مُجمَّعة ذاتياً مشتقة من مصادر
Schematron/XSD الخاصة بـPINT AE وTDD لدى OpenPeppol دون تأكيد حقوق إعادة التوزيع — أُزيلت في
الإصدار v0.2.0. راجع [`CHANGELOG.md`](CHANGELOG.md) وملف
[`context-library/decisions/peppol-schematron-artifact.md`](https://github.com/cmendezs/mcp-einvoicing/blob/main/context-library/decisions/peppol-schematron-artifact.md)
في المستودع الرئيسي للمشروع.

## التثبيت

### المتطلبات

- Python ≥ 3.11
- [`mcp-einvoicing-core`](https://github.com/cmendezs/mcp-einvoicing-core) (يُثبَّت تلقائياً
  باعتباره اعتمادية)

### باستخدام `uvx` (الأسلوب المفضل)

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

## الإعداد

### متغيرات البيئة

| المتغير | مطلوب | القيمة الافتراضية | الوصف |
|---|---|---|---|
| `LOG_LEVEL` | لا | `INFO` | مستوى السجل: `DEBUG` أو `INFO` أو `WARNING` أو `ERROR` |

تُضاف المتغيرات الخاصة بالدولة (نقاط النقل، وبيانات الاعتماد، ومفاتيح تبديل البيئة) بمجرد أن
توثّقها المواصفة. راجع [`.env.example`](.env.example). لا يحتاج هذا الخادم إلى بيانات اعتماد
للتشغيل حالياً.

## التكامل مع Claude Desktop

لاستخدام هذا الخادم مع Claude، أضف هذا الإعداد إلى ملف `claude_desktop_config.json`:

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

## التكامل مع Cursor

يدعم Cursor خوادم MCP عبر stdio. أضف الإعداد في:
- **عام** (جميع المشاريع): `~/.cursor/mcp.json`
- **المشروع** (هذا المستودع فقط): `.cursor/mcp.json`

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

أعد تحميل نافذة Cursor (`Ctrl+Shift+P` ثم *Reload Window*) لتطبيق التغييرات.

## التكامل مع Kiro

يدعم Kiro خوادم MCP عبر ملف إعداد مخصص. يتوفر مستويان:
- **عام** (جميع المشاريع): `~/.kiro/settings/mcp.json`
- **مساحة العمل** (هذا المستودع فقط): `.kiro/settings/mcp.json`

```json
{
  "mcpServers": {
    "einvoicing-ae": {
      "command": "uvx",
      "args": ["mcp-einvoicing-ae"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

يُعاد تحميل الملف تلقائياً عند الحفظ. يمكنك أيضاً فتح الإعداد عبر لوحة الأوامر
(`Cmd+Shift+P` / `Ctrl+Shift+P`) ثم *MCP*.

## الأدوات المتاحة

| الأداة | الوصف |
|---|---|
| `generate_invoice_ae` | توليد فاتورة PINT AE بصيغة UBL 2.1 (فوترة أو فوترة ذاتية) من بيانات مُهيكلة عبر `AEUBLSerializer`. يُصدر كل عنصر إلزامي غير مشروط في PINT AE: `cbc:UUID` وَ`cbc:ProfileExecutionID` وَ`cac:ItemPriceExtension` لكل بند، وَ`PartyLegalEntity/CompanyID` (`trade_license_number`، عند تحديده). |
| `validate_invoice_ae` | التحقق من فاتورة PINT AE بصيغة UBL 2.1 وفق مخطط Schematron الأساسي المشترك CEN EN16931 (القواعد البنيوية والحسابية/الإجمالية فقط — وليس قواعد الولاية القضائية لـPINT AE). تتطلب إضافة `xslt2`. |
| `validate_tdd_ae` | تُعيد دائماً نتيجة صريحة بعدم التوفر — لا تتوفر حالياً أي أداة تحقق مرخَّصة لوثيقة بيانات الضريبة Peppol AE (TDD). |
| `parse_invoice_ae` | تحليل فاتورة PINT AE بصيغة UBL 2.1 إلى قاموس مُهيكل. يُعيد استخراج `document_uuid` وَ`profile_execution_id` وَ`trade_license_number` من ملف XML الخام، ويُعيد التحقق من النتيجة كنموذج `AEInvoice` — بحيث تُطبَّق قواعد تنسيق TRN ومعدل/فئة الضريبة على المحتوى المُحلَّل أيضاً، لا على الفواتير المُنشأة حديثاً فقط. |

البحث عن مشاركي شبكة Peppol (إضافة `register_peppol_tools` من المكتبة المشتركة، بمُحوِّل معرِّف
قائم على رقم TIN — النطاق `0235`، أول 10 أرقام من رقم TRN):

| الأداة | الوصف |
|---|---|
| `peppol_lookup_participant` | التحقق مما إذا كانت الجهة مسجَّلة على شبكة Peppol؛ تُعيد حالة التسجيل وأنواع المستندات المدعومة |
| `peppol_get_service_endpoint` | جلب نقطة نهاية AS4 لنوع مستند مشارك معيّن |
| `resolve_peppol_dns` | تشخيص DNS فقط (SML)، مستقل عن إمكانية الوصول إلى SMP |
| `peppol_send` | إرسال فاتورة UBL/CII عبر AS4 |

تتطلب الأدوات `generate_invoice_ae`/`validate_invoice_ae`/`parse_invoice_ae` الإضافة
`mcp-einvoicing-ae[xslt2]` (وتضم `saxonche`) حتى تُحمَّل أداة التحقق الأساسية عبر Schematron؛ في
غيابها، تُعيد `validate_invoice_ae` نتيجة صريحة بعدم التوفر بدلاً من نجاح صامت.

يُولَّد مرجع الأدوات في [`docs/TOOLS.md`](docs/TOOLS.md) من الخادم أثناء تشغيله:

```bash
uv run python scripts/gen_tool_reference.py
```

## المساهمة

راجع [CONTRIBUTING.md](CONTRIBUTING.md) للاطلاع على إعداد بيئة التطوير، وأوامر الاختبار
والتدقيق، وقائمة تحقق طلبات السحب. أما المشكلات الأمنية فتتبع مسار الإفصاح الخاص الموضح في
[SECURITY.md](SECURITY.md).

## Other e-invoicing MCP servers

| Country | Server |
|---------|--------|
| 🌍 Global | [mcp-einvoicing-core](https://github.com/cmendezs/mcp-einvoicing-core) |
| 🇧🇪 Belgium | [mcp-einvoicing-be](https://github.com/cmendezs/mcp-einvoicing-be) |
| 🇧🇷 Brazil | [mcp-nfe-br](https://github.com/cmendezs/mcp-nfe-br) |
| 🇫🇷 France | [mcp-facture-electronique-fr](https://github.com/cmendezs/mcp-facture-electronique-fr) |
| 🇩🇪 Germany | [mcp-einvoicing-de](https://github.com/cmendezs/mcp-einvoicing-de) |
| 🇮🇹 Italy | [mcp-fattura-elettronica-it](https://github.com/cmendezs/mcp-fattura-elettronica-it) |
| 🇲🇽 Mexico | [mcp-cfdi-mx](https://github.com/cmendezs/mcp-cfdi-mx) |
| 🇵🇱 Poland | [mcp-ksef-pl](https://github.com/cmendezs/mcp-ksef-pl) |
| 🇸🇬 Singapore | [mcp-invoicenow-sg](https://github.com/cmendezs/mcp-invoicenow-sg) |
| 🇪🇸 Spain | [mcp-facturacion-electronica-es](https://github.com/cmendezs/mcp-facturacion-electronica-es) |
| 🇦🇪 United Arab Emirates | [mcp-einvoicing-ae](https://github.com/cmendezs/mcp-einvoicing-ae) |

## الترخيص

هذا المشروع مرخَّص بموجب رخصة **Apache 2.0**، راجع [LICENSE](LICENSE) للتفاصيل. للاطلاع على
السجل الكامل للإصدارات، راجع [CHANGELOG.md](CHANGELOG.md).
