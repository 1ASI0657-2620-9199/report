// Screenshot views of real provider API responses already collected privately.
// Does not access credentials or imitate the providers' dashboards.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.FINANZEN_PLAYWRIGHT_MODULE || 'playwright');
const folder = path.resolve(__dirname, '../evidencias/deployment/publico');
const read = (file) => JSON.parse(fs.readFileSync(path.join(folder, file), 'utf8'));
const escape = (value) => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const logs = (file) => read(file).logs.slice().sort((a, b) => a.timestamp.localeCompare(b.timestamp))
  .map((row) => `${row.timestamp} ${row.message.replace(/\x1b\[[0-9;]*m/g, '')}`).join('\n');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    const items = [
      ['Render Free: servicio y deploy Live', JSON.stringify({service:read('render-service.json'),deploys:read('render-deploys.json')},null,2),'12-render-live.png'],
      ['Neon Free: organización, PostgreSQL y recursos', JSON.stringify(read('neon-resources.json'),null,2),'13-neon-free.png'],
      ['Render: registro real del build', logs('render-build-logs.json'),'14-render-build.png'],
      ['Render: registro real del arranque y reinicio', logs('render-runtime-logs.json'),'15-render-runtime.png'],
      ['Persistencia cloud después de reiniciar Render', JSON.stringify(read('persistencia.json'),null,2),'16-persistence.png'],
    ];
    for (const [title, body, name] of items) {
      await page.setContent(`<!doctype html><html lang="es"><meta charset="utf-8"><style>
        body{font:17px Arial;background:#f5f7fa;color:#132437;margin:32px}
        h1{font-size:26px}.meta{padding:16px;background:#e3eef6;line-height:1.7}
        pre{background:#101a27;color:#e5f0f5;padding:24px;white-space:pre-wrap;overflow-wrap:anywhere;font:15px Consolas;line-height:1.55}
        </style><h1>${escape(title)}</h1><div class="meta">FinanZen — entorno cloud real<br>
        API pública: https://finanzen-financial-records.onrender.com<br>
        Vista de respuestas y registros reales obtenidos de las APIs de los proveedores.<br>
        No es una captura de la interfaz del dashboard de Render o Neon.<br>
        Las fechas UTC y los IDs originales se conservan en los registros.</div><pre>${escape(body)}</pre></html>`);
      await page.screenshot({path:path.join(folder,name),fullPage:true});
    }
    console.log('Captured five views of real cloud records.');
  } finally { await browser.close(); }
})().catch((error) => {console.error(error.message);process.exitCode=1;});
