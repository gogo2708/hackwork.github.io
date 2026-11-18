// Menu mobile
document.querySelectorAll('#menu a').forEach((a) => a.addEventListener('click', () => document.getElementById('menu').classList.remove('open')));

// Modulo contatti → /api/contact
const form = document.getElementById('contactForm');
if (form) {
  const note = document.getElementById('formNote');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true; btn.textContent = 'Invio in corso…';
    try {
      const r = await fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(Object.fromEntries(new FormData(form))) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(j.error || 'Invio non riuscito');
      form.reset(); form.classList.add('form--sent');
      note.textContent = 'Grazie! Abbiamo ricevuto la tua richiesta: ti rispondiamo entro 24 ore lavorative.';
      btn.textContent = 'Richiesta inviata ✓';
    } catch (err) {
      note.innerHTML = (err.message || 'Invio non riuscito') + ' — oppure scrivici a <a href="mailto:info@hackwork.space">info@hackwork.space</a>.';
      btn.disabled = false; btn.textContent = 'Invia richiesta';
    }
  });
}
