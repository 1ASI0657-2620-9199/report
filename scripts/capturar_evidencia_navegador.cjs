// Real HTTP, Newman and browser captures. Requires Playwright and Newman.
// Optional FINANZEN_PLAYWRIGHT_MODULE / FINANZEN_NEWMAN_CLI select local tools.
const fs = require('node:fs');
const path = require('node:path');
const { spawn, spawnSync } = require('node:child_process');
const { randomUUID } = require('node:crypto');
const { chromium } = require(process.env.FINANZEN_PLAYWRIGHT_MODULE || 'playwright');

const report = path.resolve(__dirname, '..');
const back = path.resolve(report, '../back');
const remote = Boolean(process.env.FINANZEN_EVIDENCE_BASE_URL);
const baseUrl = process.env.FINANZEN_EVIDENCE_BASE_URL || 'http://127.0.0.1:8766';
if (remote && new URL(baseUrl).protocol !== 'https:') {
  throw new Error('Remote evidence requires an HTTPS URL.');
}
const output = path.join(report, 'evidencias/deployment', remote ? 'publico' : 'local');
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const escapeHtml = (text) => String(text).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');

async function main() {
  fs.mkdirSync(output, { recursive: true });
  const captured = new Date().toISOString();
  const commit = spawnSync('git', ['-C', back, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).stdout.trim();
  const metadata = { captured_at_utc: captured, timezone: 'America/Lima', base_url: baseUrl,
    environment: remote ? 'Public HTTPS service' : 'Local Uvicorn with PostgreSQL 17 in Docker',
    backend_commit: commit };
  let server;
  let serverLog = '';
  const startServer = async () => {
    server = spawn('python', ['-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8766'], {
      cwd: back, env: { ...process.env,
        DATABASE_URL: process.env.FINANZEN_EVIDENCE_DATABASE_URL ||
          'postgresql://postgres:finanzen-local-validation@127.0.0.1:55439/finanzen_validation?sslmode=disable',
        FINANZEN_FRONTEND_PATH: path.resolve(report, '../front') },
    });
    server.stdout.on('data', (data) => { serverLog += data.toString(); });
    server.stderr.on('data', (data) => { serverLog += data.toString(); });
    for (let i = 0; i < 120; i++) {
      if (server.exitCode !== null) throw new Error('Local API exited; check its startup log.');
      try { if ((await fetch(`${baseUrl}/health`)).ok) return; } catch {}
      await sleep(250);
    }
    throw new Error('Local API did not become healthy.');
  };
  const stopServer = async () => {
    if (server && server.exitCode === null) {
      const exited = new Promise((resolve) => server.once('exit', resolve));
      server.kill();
      await exited;
    }
  };
  let browser;
  let context;
  let video;
  try {
    if (!remote) await startServer();
    const newmanCli = process.env.FINANZEN_NEWMAN_CLI || require.resolve('newman/bin/newman.js');
    const run = spawnSync(process.execPath, [newmanCli, 'run',
      path.join(report, 'evidencias/sprint-1/FinanZen-Sprint1.postman_collection.json'),
      '--env-var', `baseUrl=${baseUrl}`, '--reporters', 'cli,json',
      '--reporter-json-export', path.join(output, 'newman.json'), '--color', 'off'],
      { encoding: 'utf8', timeout: 120000 });
    fs.writeFileSync(path.join(output, 'newman.txt'), `${JSON.stringify(metadata, null, 2)}\n\n${run.stdout}${run.stderr}`);
    if (run.status !== 0) throw new Error('Newman collection failed; inspect newman.txt.');

    if (!remote) {
      const pytest = spawnSync('python', ['-m', 'pytest', '-q', '-p', 'no:cacheprovider'], {
        cwd: back, env: { ...process.env,
          TEST_DATABASE_URL: process.env.FINANZEN_EVIDENCE_DATABASE_URL ||
            'postgresql://postgres:finanzen-local-validation@127.0.0.1:55439/finanzen_validation?sslmode=disable' },
        encoding: 'utf8', timeout: 90000,
      });
      fs.writeFileSync(path.join(output, 'pytest.txt'), `${JSON.stringify(metadata, null, 2)}\n\n${pytest.stdout}${pytest.stderr}`);
      if (pytest.status !== 0) throw new Error('Backend suite failed.');
    }

    browser = await chromium.launch({ channel: 'chrome', headless: true });
    try {
      context = await browser.newContext({ viewport: { width: 1440, height: 1000 },
        recordVideo: { dir: path.join(output, 'video'), size: { width: 1440, height: 1000 } } });
    } catch (error) {
      metadata.video_unavailable = error.message.split('\n')[0];
      context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    }
    const page = await context.newPage();
    video = page.video();
    const shot = async (name) => {
      await sleep(700);
      await page.screenshot({ path: path.join(output, name), fullPage: true });
    };
    const evidencePage = async (title, text, name) => {
      await page.setContent(`<!doctype html><html lang="es"><meta charset="utf-8"><style>
        body{font:17px Arial;background:#f5f7fa;color:#132437;margin:32px}
        h1{font-size:26px} .meta{padding:14px;background:#e3eef6;line-height:1.7}
        pre{background:#101a27;color:#e5f0f5;padding:24px;white-space:pre-wrap;font:15px Consolas;line-height:1.55}
        </style><h1>${escapeHtml(title)}</h1><div class="meta">FinanZen — ${escapeHtml(metadata.environment)}<br>
        URL: ${escapeHtml(baseUrl)}<br>Commit: ${escapeHtml(commit)}<br>Registro UTC: ${escapeHtml(captured)}<br>
        Vista del registro real de ejecución; no es una captura de la interfaz de Postman.</div>
        <pre>${escapeHtml(text)}</pre></html>`);
      await shot(name);
    };
    await evidencePage('Colección Postman ejecutada con Newman', run.stdout, '01-newman.png');
    if (!remote) await evidencePage('Suite SQLite y PostgreSQL',
      fs.readFileSync(path.join(output, 'pytest.txt'), 'utf8'), '02-pytest.png');

    await page.goto(`${baseUrl}/docs`, { waitUntil: 'networkidle' });
    await page.locator('.swagger-ui').waitFor();
    await shot('03-swagger-endpoints.png');
    const cases = [
      ['operations-Operations-health_health_get', '04-health.png'],
      ['operations-Transactions-create_transaction_api_v1_transactions_post', '05-create-income.png'],
      ['operations-Transactions-list_transactions_api_v1_transactions_get', '06-list.png'],
      ['operations-Reports-monthly_summary_api_v1_summary_get', '07-summary.png'],
    ];
    const user = 'browser-' + randomUUID();
    const key = 'browser-income-' + randomUUID();
    const payload = { account_id: 'cash-account', type: 'income', amount: '1000.00', currency: 'PEN',
      category: 'salary', occurred_at: '2026-10-01T10:00:00Z', description: 'Evidencia HTTP real' };
    const requests = [];
    for (const [id, file] of cases) {
      await page.goto(`${baseUrl}/docs`, { waitUntil: 'networkidle' });
      const operation = page.locator(`#${id}`);
      await operation.locator('.opblock-summary').click();
      await operation.getByRole('button', { name: 'Try it out', exact: true }).click();
      const fillParameter = async (name, value) => {
        const row = operation.locator(`tr[data-param-name="${name}"]`);
        if (await row.count()) await row.locator('input').fill(value);
      };
      await fillParameter('X-User-Id', user);
      await fillParameter('Idempotency-Key', key);
      await fillParameter('month', '2026-10');
      await fillParameter('currency', 'PEN');
      if (id.includes('create_transaction')) {
        await operation.locator('textarea').fill(JSON.stringify(payload, null, 2));
      }
      const responsePromise = page.waitForResponse((response) => response.url().startsWith(baseUrl) &&
        !['/docs', '/openapi.json'].some((suffix) => response.url().endsWith(suffix)));
      await operation.getByRole('button', { name: 'Execute', exact: true }).click();
      const response = await responsePromise;
      requests.push({ operation: id, method: response.request().method(), url: response.url(),
        status: response.status(), body: await response.json() });
      if (response.status() >= 400) throw new Error(`Swagger operation failed: ${id}`);
      await shot(file);
      if (id.includes('create_transaction')) {
        const replayPromise = page.waitForResponse((r) => r.request().method() === 'POST');
        await operation.getByRole('button', { name: 'Execute', exact: true }).click();
        const replay = await replayPromise;
        requests.push({ operation: 'replay', status: replay.status(), body: await replay.json() });
        if (replay.status() !== 200) throw new Error('Replay did not return HTTP 200.');
        await shot('08-replay.png');
        await operation.locator('textarea').fill(JSON.stringify({ ...payload, amount: '2000.00' }, null, 2));
        const conflictPromise = page.waitForResponse((r) => r.request().method() === 'POST');
        await operation.getByRole('button', { name: 'Execute', exact: true }).click();
        const conflict = await conflictPromise;
        requests.push({ operation: 'conflict', status: conflict.status(), body: await conflict.json() });
        if (conflict.status() !== 409) throw new Error('Conflict did not return HTTP 409.');
        await shot('09-conflict.png');
        const expense = await page.request.post(`${baseUrl}/api/v1/transactions`, {
          headers: { 'X-User-Id': user, 'Idempotency-Key': 'browser-expense-' + randomUUID() },
          data: { ...payload, type: 'expense', amount: '125.50', category: 'food' },
        });
        if (expense.status() !== 201) throw new Error('Expense was not created.');
      }
    }
    if (!remote) {
      const before = requests.find((r) => r.operation.includes('list_transactions')).body;
      await stopServer();
      await startServer();
      const response = await fetch(`${baseUrl}/api/v1/transactions`, { headers: { 'X-User-Id': user } });
      const after = await response.json();
      if (JSON.stringify(before.map((r) => r.id).sort()) !== JSON.stringify(after.map((r) => r.id).sort())) {
        throw new Error('Data did not survive the Uvicorn process restart.');
      }
      const persistence = { ...metadata, verification: 'Local Uvicorn process stopped and restarted',
        before_ids: before.map((r) => r.id), after_ids: after.map((r) => r.id), preserved: true };
      fs.writeFileSync(path.join(output, 'persistencia.json'), JSON.stringify(persistence, null, 2));
      await evidencePage('Persistencia tras reiniciar el proceso Uvicorn',
        JSON.stringify(persistence, null, 2), '10-persistence.png');
    }
    fs.writeFileSync(path.join(output, 'swagger-http.json'), JSON.stringify({ ...metadata, requests }, null, 2));
    if (!remote) {
      await evidencePage('Arranque y peticiones del servidor local', serverLog, '11-server-log.png');
      fs.writeFileSync(path.join(output, 'uvicorn.txt'), serverLog);
    }
    await context.close();
    context = null;
    if (video) await video.saveAs(path.join(output, 'demostracion.webm'));
    fs.writeFileSync(path.join(output, 'metadata.json'), JSON.stringify(metadata, null, 2));
    console.log(`Captured real evidence for ${metadata.environment}.`);
  } finally {
    if (context) await context.close();
    if (browser) await browser.close();
    await stopServer();
  }
}

main().catch((error) => { console.error(error.message); process.exitCode = 1; });
