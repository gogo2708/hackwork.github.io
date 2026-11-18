// HackWork — sito + raccolta contatti (stessa struttura del sito Atomic Studios: Express + Resend su Render)
const express = require('express');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { Resend } = require('resend');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_DIR = process.env.DATA_DIR || path.join(__dirname, 'data');
const CONTACTS_FILE = path.join(DATA_DIR, 'contatti.json');
const CONTACT_EMAIL = process.env.CONTACT_EMAIL || 'info@hackwork.space';

app.use(express.json({ limit: '100kb' }));
app.use(express.urlencoded({ extended: true, limit: '100kb' }));

// ─── Redirect dai vecchi indirizzi WordPress (link già condivisi e Google) ───
const OLD = {
  '/chi-siamo/': '/chi-siamo', '/servizi/': '/servizi', '/contatti/': '/contatti', '/references': '/lavori', '/references/': '/lavori',
  '/blog/': '/blog', '/author/admin/': '/blog', '/feed/': '/blog',
  '/2025/08/09/servizio-clienti-e-comunicazione-il-vero-ostacolo-alla-crescita-aziendale/': '/blog/servizio-clienti-e-comunicazione-il-vero-ostacolo-alla-crescita-aziendale',
  '/2025/03/04/risparmio-aziendale-strategie-e-dati-per-ottimizzare-i-costi-senza-rinunciare-alla-crescita/': '/blog/risparmio-aziendale-strategie-e-dati-per-ottimizzare-i-costi-senza-rinunciare-alla-crescita',
  '/2025/03/04/digitalizzazione-aziendale-come-trasformare-la-tua-impresa-per-il-successo/': '/blog/digitalizzazione-aziendale-come-trasformare-la-tua-impresa-per-il-successo',
  '/2025/02/09/ciao-mondo/': '/blog/ottimizzazione-aziendale-gestionali',
};
app.use((req, res, next) => {
  if (OLD[req.path]) return res.redirect(301, OLD[req.path]);
  if (req.path.startsWith('/wp-') || /^\/20\d\d\//.test(req.path)) return res.redirect(301, '/blog');
  // /pagina/ → /pagina
  if (req.path.length > 1 && req.path.endsWith('/')) return res.redirect(301, req.path.slice(0, -1) + (req.url.slice(req.path.length) || ''));
  next();
});

// ─── File pubblici del sito: solo la cartella public/ (server.js, data/ ecc. restano privati) ───
const PUBLIC = path.join(__dirname, 'public');
app.get('/blog', (req, res) => res.sendFile(path.join(PUBLIC, 'blog.html')));
app.use(express.static(PUBLIC, { extensions: ['html'], redirect: false, maxAge: '1h', setHeaders: (res, p) => { if (/\.(jpe?g|png|webp|svg)$/.test(p)) res.setHeader('Cache-Control', 'public, max-age=604800'); } }));
app.get('/favicon.ico', (req, res) => res.sendFile(path.join(PUBLIC, 'img', 'logo-mark.png')));

// ─── Archivio contatti ───
function readContacts() {
  try { return JSON.parse(fs.readFileSync(CONTACTS_FILE, 'utf8')); } catch { return []; }
}
function saveContact(c) {
  const all = readContacts();
  all.unshift(c);
  fs.mkdirSync(DATA_DIR, { recursive: true });
  fs.writeFileSync(CONTACTS_FILE, JSON.stringify(all, null, 2));
}

// ─── Email con Resend ───
const esc = (s) => String(s || '').replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
async function sendContactEmail(c) {
  if (!process.env.RESEND_API_KEY) { console.warn('RESEND_API_KEY mancante: contatto salvato ma email non inviata'); return; }
  const resend = new Resend(process.env.RESEND_API_KEY);
  const row = (k, v) => v ? `<tr><td style="padding:8px 0;font-size:12px;color:#888;width:130px;vertical-align:top">${k}</td><td style="padding:8px 0">${v}</td></tr>` : '';
  const { error } = await resend.emails.send({
    from: process.env.RESEND_FROM || 'HackWork <noreply@hackwork.space>',
    to: CONTACT_EMAIL,
    reply_to: c.email,
    subject: `[Nuovo contatto] ${c.nome}${c.azienda ? ' — ' + c.azienda : ''} · ${c.servizio}`,
    html: `
      <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#111">
        <div style="background:#07090C;padding:22px 30px;border-radius:12px 12px 0 0">
          <h1 style="color:#B2E840;font-size:22px;margin:0;letter-spacing:.04em">HACKWORK</h1>
          <p style="color:#aaa;font-size:12px;margin:4px 0 0;letter-spacing:.12em">NUOVA RICHIESTA DAL SITO</p>
        </div>
        <div style="border:1px solid #e5e5e5;border-top:none;padding:28px 30px;border-radius:0 0 12px 12px">
          <table style="width:100%;border-collapse:collapse">
            ${row('NOME', '<b>' + esc(c.nome) + '</b>')}
            ${row('AZIENDA', esc(c.azienda))}
            ${row('EMAIL', `<a href="mailto:${esc(c.email)}" style="color:#5E8A0F">${esc(c.email)}</a>`)}
            ${row('TELEFONO', esc(c.telefono))}
            ${row('SERVIZIO', esc(c.servizio))}
          </table>
          ${c.messaggio ? `<div style="margin-top:20px;padding:18px;background:#F4F6F1;border-radius:8px;line-height:1.6">${esc(c.messaggio).replace(/\n/g, '<br>')}</div>` : ''}
          <p style="margin-top:26px;font-size:11px;color:#aaa">Ricevuto il ${new Date(c.data).toLocaleString('it-IT', { timeZone: 'Europe/Rome' })}</p>
        </div>
      </div>`,
  });
  if (error) throw new Error(error.message || JSON.stringify(error));
}

// ─── API contatti ───
const recent = new Map(); // limite semplice anti-spam per IP
app.post('/api/contact', async (req, res) => {
  const b = req.body || {};
  if (b.website) return res.json({ ok: true }); // campo trappola per i bot
  const ip = (req.headers['x-forwarded-for'] || req.ip || '').split(',')[0].trim();
  const now = Date.now();
  const hits = (recent.get(ip) || []).filter((t) => now - t < 10 * 60e3);
  if (hits.length >= 5) return res.status(429).json({ error: 'Troppe richieste, riprova tra qualche minuto.' });
  recent.set(ip, [...hits, now]);

  const clip = (v, n) => String(v || '').trim().slice(0, n);
  const c = {
    id: crypto.randomUUID(),
    data: new Date().toISOString(),
    nome: clip(b.nome, 120),
    azienda: clip(b.azienda, 160),
    email: clip(b.email, 200),
    telefono: clip(b.telefono, 40),
    servizio: clip(b.servizio, 80) || 'Non specificato',
    messaggio: clip(b.messaggio, 5000),
  };
  if (!c.nome || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(c.email)) {
    return res.status(400).json({ error: 'Inserisci nome e un indirizzo email valido.' });
  }
  try { saveContact(c); } catch (e) { console.error('Salvataggio contatto:', e.message); }
  try {
    await sendContactEmail(c);
  } catch (e) {
    console.error('Email Resend:', e.message);
  }
  res.json({ ok: true });
});

// ─── Area riservata: elenco contatti (password in ADMIN_PASSWORD) ───
function requireAdmin(req, res, next) {
  const pass = process.env.ADMIN_PASSWORD || '';
  const [type, value] = (req.headers.authorization || '').split(' ');
  if (pass.length >= 8 && type === 'Basic' && value) {
    const given = Buffer.from(value, 'base64').toString().split(':').slice(1).join(':');
    const a = Buffer.from(given), b2 = Buffer.from(pass);
    if (a.length === b2.length && crypto.timingSafeEqual(a, b2)) return next();
  }
  res.set('WWW-Authenticate', 'Basic realm="HackWork admin"').status(401).send('Accesso riservato');
}
app.get('/admin/contatti', requireAdmin, (req, res) => {
  const list = readContacts();
  const rows = list.map((c) => `<tr>
      <td>${esc(new Date(c.data).toLocaleString('it-IT', { timeZone: 'Europe/Rome' }))}</td>
      <td><b>${esc(c.nome)}</b><br><small>${esc(c.azienda)}</small></td>
      <td><a href="mailto:${esc(c.email)}">${esc(c.email)}</a><br><small>${esc(c.telefono)}</small></td>
      <td>${esc(c.servizio)}</td>
      <td>${esc(c.messaggio).replace(/\n/g, '<br>')}</td></tr>`).join('');
  res.send(`<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Contatti — HackWork</title><style>
  body{font-family:Inter,system-ui,sans-serif;background:#07090C;color:#E8ECF1;margin:0;padding:32px}
  h1{color:#B2E840;font-size:24px;margin:0 0 6px}p{color:#8C96A3;margin:0 0 24px}
  table{width:100%;border-collapse:collapse;background:#0E1218;border-radius:12px;overflow:hidden}
  th,td{text-align:left;padding:14px;border-bottom:1px solid rgba(255,255,255,.08);vertical-align:top;font-size:14px}
  th{color:#8C96A3;font-weight:500;font-size:12px;text-transform:uppercase;letter-spacing:.08em}
  a{color:#B2E840}small{color:#8C96A3}</style></head><body>
  <h1>Contatti dal sito</h1><p>${list.length} richieste · <a href="/admin/contatti.csv">Scarica CSV</a></p>
  <table><thead><tr><th>Data</th><th>Nome</th><th>Contatto</th><th>Servizio</th><th>Messaggio</th></tr></thead>
  <tbody>${rows || '<tr><td colspan="5">Nessun contatto ancora.</td></tr>'}</tbody></table></body></html>`);
});
app.get('/admin/contatti.csv', requireAdmin, (req, res) => {
  const q = (v) => '"' + String(v || '').replace(/"/g, '""') + '"';
  const csv = ['data,nome,azienda,email,telefono,servizio,messaggio']
    .concat(readContacts().map((c) => [c.data, c.nome, c.azienda, c.email, c.telefono, c.servizio, c.messaggio].map(q).join(',')))
    .join('\n');
  res.set('Content-Type', 'text/csv; charset=utf-8').set('Content-Disposition', 'attachment; filename="contatti-hackwork.csv"').send('﻿' + csv);
});

app.use((req, res) => res.status(404).sendFile(path.join(PUBLIC, '404.html')));

app.listen(PORT, () => console.log(`HackWork online sulla porta ${PORT}`));
