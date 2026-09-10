import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const outDir = join(root, "..", "screenshots");
const base = process.env.FIGURE_BASE || "http://127.0.0.1:43147";

const pages = [
  { id: "gallery", path: "/", title: "Gallery" },
  { id: "catalog", path: "/catalog.html", title: "Catalog", fullPage: true },
  { id: "react-compiler", path: "/walks/react-compiler.html", title: "react/react #36173", deck: true },
  { id: "vite-environments", path: "/walks/vite-environments.html", title: "vitejs/vite #16471", deck: true },
  { id: "next-ppr", path: "/walks/next-ppr.html", title: "vercel/next.js #69282", deck: true },
  { id: "tailwind-oxide", path: "/walks/tailwind-oxide.html", title: "tailwindlabs/tailwindcss #19632", deck: true },
];

await mkdir(outDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 2 });

const report = [];

for (const spec of pages) {
  const url = base + spec.path;
  const response = await page.goto(url, { waitUntil: "networkidle", timeout: 30_000 });
  if (!response || !response.ok()) {
    throw new Error(`Failed to load ${url}: ${response ? response.status() : "no response"}`);
  }
  await page.waitForTimeout(250);

  if (spec.deck) {
    await page.waitForSelector("fig-deck .fig-shell");
    const sceneCount = await page.locator("fig-scene").count();
    for (let i = 0; i < sceneCount; i += 1) {
      if (i > 0) {
        await page.locator(".fig-next").click();
        await page.waitForFunction(
          (n) => document.querySelector("fig-deck")?.getAttribute("data-active") === String(n),
          i,
        );
        await page.waitForTimeout(120);
      }
      const file = `${spec.id}-s${String(i + 1).padStart(2, "0")}.png`;
      await page.locator(".fig-shell").screenshot({ path: join(outDir, file) });
      const title = await page.locator(".fig-scene-head h2").innerText();
      report.push({ page: spec.title, scene: i + 1, title, file, url: `${url}#s=${i + 1}` });
    }
  } else {
    const file = `${spec.id}.png`;
    await page.screenshot({ path: join(outDir, file), fullPage: Boolean(spec.fullPage) });
    report.push({ page: spec.title, scene: null, title: spec.title, file, url });
  }
}

await page.setViewportSize({ width: 390, height: 844 });
await page.goto(base + "/walks/next-ppr.html", { waitUntil: "networkidle" });
await page.waitForSelector("fig-deck .fig-shell");
await page.locator(".fig-shell").screenshot({ path: join(outDir, "next-ppr-mobile.png") });
report.push({
  page: "vercel/next.js #69282",
  scene: 1,
  title: "Mobile viewport",
  file: "next-ppr-mobile.png",
  url: base + "/walks/next-ppr.html",
});

await browser.close();

const md = [
  "# Screenshot pass",
  "",
  `Captured against ${base}. Each walkthrough scene is one click of **Next**.`,
  "",
  "| Page | Scene | Claim | File |",
  "|------|-------|-------|------|",
  ...report.map((row) => `| ${row.page} | ${row.scene ?? "—"} | ${row.title} | \`${row.file}\` |`),
  "",
].join("\n");

await writeFile(join(outDir, "REPORT.md"), md);
console.log(`Wrote ${report.length} screenshots to ${outDir}`);
