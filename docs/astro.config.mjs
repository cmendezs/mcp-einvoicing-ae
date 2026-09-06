import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import starlightLlmsTxt from "starlight-llms-txt";

export default defineConfig({
  site: "https://cmendezs.github.io",
  base: "/mcp-einvoicing-ae/",
  integrations: [
    starlight({
      title: "mcp-einvoicing-ae",
      description: "MCP server for United Arab Emirates electronic invoicing",
      customCss: ["./src/styles/docs-theme.css"],
      social: [
        { icon: "github", label: "GitHub", href: "https://github.com/cmendezs/mcp-einvoicing-ae" },
      ],
      locales: {
        root: { label: "English", lang: "en" },
        ar: { label: "العربية", lang: "ar", dir: "rtl" },
      },
      sidebar: [
        { label: "Overview", link: "/" },
        { label: "Tools", link: "/tools/" },
        { label: "Changelog", link: "/changelog/" },
        { label: "Contributing", link: "/contributing/" },
        { label: "Security", link: "/security/" },
        { label: "Code of Conduct", link: "/code-of-conduct/" },
      ],
      plugins: [
        starlightLlmsTxt({
          projectName: "mcp-einvoicing-ae",
          description: "MCP server for United Arab Emirates electronic invoicing",
          customSets: [
            {
              label: "Key links",
              description: "PyPI and MCP registry entries",
              links: ["https://pypi.org/project/mcp-einvoicing-ae/", "https://registry.modelcontextprotocol.io/v0/servers?search=io.github.cmendezs/mcp-einvoicing-ae"],
            },
          ],
        }),
      ],
    }),
  ],
});
