# Genera le pagine del sito HackWork in public/ (header e footer condivisi)
import json, os, html
from datetime import date

P = json.load(open('posts.json'))
MESI = ['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre']
def data_it(s):
    y, m, d = map(int, s.split('-')); return f'{d} {MESI[m-1]} {y}'

NAV = [('/chi-siamo', 'Chi siamo'), ('/servizi', 'Servizi'), ('/lavori', 'Lavori'), ('/blog', 'Blog')]

def page(path, title, desc, body, active=''):
    nav = ''.join(f'<a href="{h}"{" class=\"is-active\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://hackwork.space/img/hackwork-og.png">
<link rel="canonical" href="https://hackwork.space{path}">
<link rel="icon" href="/img/logo-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css">
</head>
<body>
<header class="nav" id="top">
  <div class="wrap nav__inner">
    <a href="/" class="logo" aria-label="HackWork home"><img src="/img/logo-mark.png" alt="" class="logo__mark"><span class="logo__text">HACKWORK<small>CORPORATION</small></span></a>
    <nav class="nav__links" id="menu">{nav}<a href="/contatti" class="btn btn--small">Consulenza gratuita</a></nav>
    <button class="nav__toggle" aria-label="Apri menu" onclick="document.getElementById('menu').classList.toggle('open')"><span></span><span></span></button>
  </div>
</header>
<main>
{body}
</main>
<footer class="footer">
  <div class="wrap footer__inner">
    <a href="/" class="logo"><img src="/img/logo-mark.png" alt="" class="logo__mark"><span class="logo__text">HACKWORK<small>CORPORATION</small></span></a>
    <nav><a href="/chi-siamo">Chi siamo</a><a href="/servizi">Servizi</a><a href="/lavori">Lavori</a><a href="/blog">Blog</a><a href="/contatti">Contatti</a></nav>
    <p class="footer__claim">Facciamo crescere la tua azienda, una soluzione alla volta.</p>
    <p>HackWork Corporation · Milano · <a href="tel:+393248861951">+39 324 886 1951</a> · <a href="mailto:info@hackwork.space">info@hackwork.space</a> · P.IVA 14118980961 · © {date.today().year}</p>
  </div>
</footer>
<script src="/js/site.js" defer></script>
</body>
</html>
'''

def page_hero(label, title, lead, img=None):
    pic = f'<div class="phero__img"><img src="/img/{img}" alt="" loading="eager"></div>' if img else ''
    return f'''<section class="phero{' phero--img' if img else ''}">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="wrap phero__inner">
    <div><p class="label">{label}</p><h1>{title}</h1><p class="phero__lead">{lead}</p></div>
    {pic}
  </div>
</section>'''

CTA = '''<section class="cta">
  <div class="wrap cta__inner">
    <div><p class="label">Parliamone</p><h2>Hai un processo che ti fa perdere tempo?<br>Raccontacelo.</h2></div>
    <a href="/contatti" class="btn">Prenota una consulenza gratuita</a>
  </div>
</section>'''

PARTNERS = ['zoho', 'sap', 'apple-developer', 'android-developers', 'siemens', 'python', 'java', 'zapier']
PARTNER_NAMES = {'zoho':'Zoho','sap':'SAP','apple-developer':'Apple Developer','android-developers':'Android Developers','siemens':'Siemens','python':'Python','java':'Java','zapier':'Zapier'}
LOGOS = '''<section class="logos">
  <div class="wrap">
    <p class="label">Tecnologie e partner</p>
    <div class="logos__row">''' + ''.join(f'<span class="logos__item"><img src="/img/partner/{p}.png" alt="{PARTNER_NAMES[p]}" loading="lazy"></span>' for p in PARTNERS) + '''</div>
  </div>
</section>'''

SERVIZI = [
  ('ottimizzazione-processi', 'Ottimizzazione dei processi', 'codice.jpg',
   'Analizziamo e miglioriamo i processi operativi per aumentare efficienza e produttività.',
   ['Consulenza di ottimizzazione aziendale con soluzioni IT su misura, pensate per le sfide specifiche di ogni cliente.',
    '<b>Controllo delle informazioni:</b> sapere sempre come sta andando il lavoro, dove migliorare e in che direzione sta andando l\'azienda.',
    '<b>Gestione del flusso operativo:</b> ogni persona del team sa cosa fare ogni giorno. Coordiniamo le attività in modo chiaro, con visibilità e controllo a 360°.'],
   ['Gestionali ed ERP su misura', 'Dashboard di controllo di gestione', 'Calendari, appuntamenti e obiettivi del team']),
  ('dati-ai', 'Analisi dati e intelligenza artificiale', 'digitale.jpg',
   'Trasformiamo i dati in decisioni, con analisi predittive e automazioni intelligenti.',
   ['Aiutiamo le aziende a sfruttare davvero i propri dati, trasformandoli in un vantaggio competitivo.',
    'L\'ottimizzazione basata sui dati riduce i costi operativi e migliora margini ed efficienza.',
    'Capire meglio i bisogni dei clienti aumenta la fidelizzazione e il valore di ogni cliente nel tempo.'],
   ['Report e KPI automatici', 'Previsioni e analisi predittive', 'Automazioni con l\'AI']),
  ('integrazioni', 'Integrazione di sistemi', 'scrivania.jpg',
   'Facciamo parlare tra loro software, processi e tecnologie della tua azienda.',
   ['Progettiamo e realizziamo integrazioni su misura perché processi, software e tecnologie comunichino senza intoppi.',
    'Se il tuo sistema sembra caotico è solo perché non è ancora progettato per lavorare in armonia. Trasformiamo la complessità in chiarezza: più efficienza, meno complessità operativa, una base solida per crescere.'],
   ['CRM, e-commerce, magazzino e contabilità collegati', 'Zoho, SAP, Zapier e API personalizzate', 'Fine del copia-incolla tra programmi']),
  ('siti-web', 'Siti web ed e-commerce', 'laptop.jpg',
   'Siti moderni, responsive e pensati per chi li usa.',
   ['Realizziamo siti belli da vedere e soprattutto semplici da usare, senza rinunciare alle funzionalità.',
    'Uniamo design e funzionalità per far emergere il tuo business. Il sito non è solo una presenza online: è un percorso che ottimizziamo per i tuoi utenti.'],
   ['Siti aziendali e landing page', 'E-commerce con pagamenti e ordini automatici', 'Ottimizzati per mobile e motori di ricerca']),
  ('consulenza-it', 'Consulenza IT e progetti elettrici', 'citta.jpg',
   'Progettazione e ottimizzazione di sistemi IT e impianti elettrici.',
   ['Offriamo consulenza su misura per progettare e ottimizzare sistemi IT e progetti elettrici, garantendo integrazione, affidabilità ed efficienza.'],
   ['Infrastrutture IT', 'Progettazione elettrica ed elettronica', 'Supporto tecnico all\'implementazione']),
  ('formazione', 'Formazione e assistenza', 'team.jpg',
   'Formazione, assistenza tecnica e supporto personalizzato per il tuo team.',
   ['Anche il programma più efficiente del mondo non rende senza formazione e supporto. Al centro di ogni azienda ci sono le persone: sono le prime a usare il sistema.',
    'Per questo accompagniamo il tuo team passo dopo passo, perché si senta preparato, valorizzato e in grado di ottenere risultati.'],
   ['Formazione sul nuovo sistema', 'Assistenza tecnica continua', 'Un referente dedicato']),
]

LAVORI = [
  ('erp-idraulico', 'Gestionale per il settore idraulico', 'ERP · Controllo di gestione', 'lavori/erp-idraulico.jpg',
   'ERP su misura per il settore idraulico, con una dashboard interattiva dedicata ai commerciali.',
   ['La piattaforma mostra gli appuntamenti da svolgere, lo stato degli obiettivi settimanali e mensili e motiva la rete vendita con una panoramica chiara delle performance.',
    'Calendario dinamico, tracciamento degli appuntamenti e gestione clienti integrata coprono l\'intero processo commerciale: dalla creazione del preventivo alla chiusura della trattativa.'],
   ['Dashboard commerciali', 'Calendario appuntamenti', 'Obiettivi settimanali e mensili', 'Preventivi e CRM']),
  ('elysian-luxe', 'Elysian Luxe', 'Sito web · Lusso', 'lavori/elysian-luxe.jpg',
   'Sito per un brand di esperienze di lusso su misura: viaggi esclusivi, cene gourmet, personal shopper e styling.',
   ['Estetica elegante e immersiva, pensata per evocare emozioni e desiderio.',
    'La homepage comunica subito il valore dell\'esperienza personalizzata, con call to action ben visibili, navigazione fluida e design responsive per un pubblico raffinato e internazionale.'],
   ['Design su misura', 'Responsive', 'Call to action', 'Pubblico internazionale']),
]

def post_card(p):
    return f'''<a class="post" href="/blog/{p['slug']}">
  <div class="post__img"><img src="/img/foto/{p['img']}.jpg" alt="" loading="lazy"></div>
  <div class="post__body"><time>{data_it(p['date'])}</time><h3>{html.escape(p['title'])}</h3><span>Leggi l'articolo →</span></div>
</a>'''

FORM = '''<form class="form" id="contactForm">
  <label>Nome e cognome<input name="nome" required placeholder="Mario Rossi" autocomplete="name"></label>
  <label>Azienda<input name="azienda" placeholder="Nome azienda" autocomplete="organization"></label>
  <label>Email<input type="email" name="email" required placeholder="mario@azienda.it" autocomplete="email"></label>
  <label>Telefono <span class="opt">(facoltativo)</span><input type="tel" name="telefono" placeholder="+39 ..." autocomplete="tel"></label>
  <input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
  <label>Di cosa hai bisogno?
    <select name="servizio">
      <option>Gestionale / ERP su misura</option><option>Analisi dati e AI</option><option>Integrazione di sistemi</option>
      <option>Sito web / E-commerce</option><option>Consulenza IT / elettrica</option><option>Formazione e assistenza</option><option>Altro</option>
    </select>
  </label>
  <label>Messaggio<textarea name="messaggio" rows="4" placeholder="Raccontaci in breve il progetto"></textarea></label>
  <button class="btn" type="submit">Invia richiesta</button>
  <p class="form__note" id="formNote">Rispondiamo entro 24 ore lavorative.</p>
</form>'''

pages = {}

# ─── HOME ───
servizi_cards = ''.join(f'''<a class="card" href="/servizi#{s[0]}"><span class="card__num">/0{i+1}</span><h3>{s[1]}</h3><p>{s[3]}</p><span class="card__more">Scopri →</span></a>''' for i, s in enumerate(SERVIZI))
lavori_home = ''.join(f'''<a class="work__item{' work__item--rev' if i % 2 else ''}" href="/lavori#{l[0]}">
  <div class="work__visual"><img src="/img/{l[3]}" alt="{html.escape(l[1])}" loading="lazy"></div>
  <div class="work__text"><p class="tag">{l[2]}</p><h3>{l[1]}</h3><p>{l[4]}</p><span class="link">Vedi il progetto →</span></div>
</a>''' for i, l in enumerate(LAVORI))
home = f'''<section class="hero">
  <div class="grid-bg" aria-hidden="true"></div>
  <div class="wrap hero__inner">
    <p class="eyebrow"><span class="dot"></span> Ingegneria software · Milano</p>
    <h1>Software su misura che fa lavorare <em>meno</em> la tua azienda.</h1>
    <p class="hero__lead">Semplifichiamo e potenziamo il tuo lavoro. Gestionali, ERP, e-commerce e automazioni con l'AI per PMI: costruiti sul tuo modo di lavorare, non comprati a scaffale.</p>
    <div class="hero__cta"><a href="/contatti" class="btn">Prenota una consulenza gratuita</a><a href="/lavori" class="btn btn--ghost">Guarda i lavori →</a></div>
    <div class="hero__panel" aria-hidden="true">
      <div class="panel__bar"><i></i><i></i><i></i><span>dashboard.hackwork</span></div>
      <div class="panel__body">
        <div class="kpi"><small>Ore risparmiate / sett.</small><b>+20h</b><div class="spark"><span style="height:30%"></span><span style="height:45%"></span><span style="height:40%"></span><span style="height:62%"></span><span style="height:70%"></span><span style="height:88%"></span><span style="height:100%"></span></div></div>
        <div class="kpi"><small>Efficienza</small><b>+35%</b><div class="bar"><span style="width:72%"></span></div></div>
        <div class="log"><p><span class="ok">✓</span> ordine #4821 sincronizzato con ERP</p><p><span class="ok">✓</span> preventivo inviato al cliente</p><p><span class="ok">✓</span> magazzino aggiornato</p><p class="cursor">_</p></div>
      </div>
    </div>
  </div>
</section>
<section class="stats"><div class="wrap stats__grid">
  <div><b>+120</b><span>aziende supportate</span></div><div><b>+35%</b><span>efficienza migliorata</span></div>
  <div><b>€50k</b><span>risparmio medio per azienda all'anno</span></div><div><b>+20h</b><span>risparmiate ogni settimana</span></div>
</div></section>
<section class="section split">
  <div class="wrap split__grid">
    <div class="split__img"><img src="/img/foto/scrivania.jpg" alt="Postazione di lavoro HackWork" loading="lazy"></div>
    <div>
      <p class="label">Chi siamo</p>
      <h2>Non siamo fornitori.<br>Siamo <em>partner</em>.</h2>
      <p class="muted">Un gruppo di giovani professionisti con esperienze in settori diversi. Abbiamo visto troppi sistemi fallire perché scelti per il marchio invece che costruiti sul modo di lavorare dell'azienda. Noi facciamo il contrario.</p>
      <a href="/chi-siamo" class="btn btn--ghost">Scopri chi siamo →</a>
    </div>
  </div>
</section>
<section class="section section--tight" id="servizi">
  <div class="wrap">
    <div class="section__head section__head--row"><div><p class="label">Servizi</p><h2>Un unico team per digitalizzare la tua azienda.</h2></div><a href="/servizi" class="btn btn--ghost">Tutti i servizi →</a></div>
    <div class="cards">{servizi_cards}</div>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap">
    <div class="section__head section__head--row"><div><p class="label">Lavori</p><h2>Progetti reali, risultati concreti.</h2></div><a href="/lavori" class="btn btn--ghost">Tutti i lavori →</a></div>
    <div class="work">{lavori_home}</div>
  </div>
</section>
{LOGOS}
<section class="section section--tight">
  <div class="wrap">
    <div class="section__head section__head--row"><div><p class="label">Blog</p><h2>Idee per far crescere la tua azienda.</h2></div><a href="/blog" class="btn btn--ghost">Tutti gli articoli →</a></div>
    <div class="posts">{''.join(post_card(p) for p in P[:3])}</div>
  </div>
</section>
{CTA}'''
pages['index.html'] = page('/', 'HackWork — Software su misura per PMI · Milano', 'HackWork è un team di ingegneri a Milano: gestionali ed ERP su misura, e-commerce, integrazioni e intelligenza artificiale per PMI.', home)

# ─── CHI SIAMO ───
chi = page_hero('Chi siamo', 'Non siamo fornitori.<br>Siamo <em>partner</em>. Cresciamo insieme.', 'Un team di ingegneri e professionisti che costruisce sistemi su misura, con la passione per la tecnologia e l\'ottimizzazione dei processi.', 'foto/astratto.jpg') + '''
<section class="section about">
  <div class="wrap about__grid">
    <div>
      <p class="label">La nostra storia</p>
      <h2>Tecnologia e innovazione sono il nostro DNA.</h2>
    </div>
    <div class="about__text">
      <p>Siamo un gruppo di giovani professionisti con esperienze in settori diversi. Ci unisce una cosa: abbiamo tutti lavorato con sistemi che potevano essere i migliori al mondo, ma sono falliti per cattiva gestione o per orgoglio. Spesso i titolari non si fidavano degli esperti, e i sistemi crollavano.</p>
      <p>Per questo la nostra missione è anche aiutare gli imprenditori a evitare errori costosi e soluzioni inadatte. Oggi è facile affidarsi a un sistema scelto solo per il marchio o il prestigio. È l'errore più grande: si compra un prodotto invece di creare un sistema costruito sul proprio modo di lavorare.</p>
      <p>Crediamo nell'innovazione come motore di crescita e nel design funzionale come chiave per migliorare l'efficienza.</p>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap vm">
    <div class="vm__item">
      <p class="label">Visione</p>
      <h3>Un ecosistema per gestire l'azienda nel cloud.</h3>
      <p>Immaginiamo un futuro in cui aziende di ogni dimensione accedono in modo semplice e sicuro alle risorse e ai servizi cloud di cui hanno bisogno per crescere e innovare.</p>
    </div>
    <div class="vm__item">
      <p class="label">Missione</p>
      <h3>Semplificare e potenziare il tuo lavoro.</h3>
      <p>Farti risparmiare tempo, risorse e stress, così ti concentri su quello che conta davvero: far crescere la tua azienda. Il tuo obiettivo è anche il nostro.</p>
    </div>
  </div>
</section>
<section class="section" id="metodo">
  <div class="wrap">
    <div class="section__head"><p class="label">Metodo</p><h2>Dal progetto alla realizzazione, in quattro passi.</h2></div>
    <ol class="steps steps--dark">
      <li><span>01</span><h3>Analisi della situazione</h3><p>Studiamo come lavori oggi: punti di forza, aree da migliorare e strumenti già in uso.</p></li>
      <li><span>02</span><h3>Obiettivo e strategia</h3><p>Definiamo l'obiettivo e una strategia mirata, ottimizzando le risorse per arrivarci.</p></li>
      <li><span>03</span><h3>Sviluppo</h3><p>Implementiamo prima le funzionalità principali, con rilasci frequenti da provare subito.</p></li>
      <li><span>04</span><h3>Test e ottimizzazione</h3><p>Test approfonditi su affidabilità, sicurezza e prestazioni, per un sistema stabile e veloce.</p></li>
    </ol>
  </div>
</section>
''' + LOGOS + CTA
pages['chi-siamo.html'] = page('/chi-siamo', 'Chi siamo — HackWork', 'Giovani professionisti e ingegneri a Milano: costruiamo sistemi su misura e accompagniamo le aziende come partner.', chi, '/chi-siamo')

# ─── SERVIZI ───
idx = ''.join(f'<a href="#{s[0]}">{s[1]}</a>' for s in SERVIZI)
blocks = ''.join(f'''<article class="svc{' svc--rev' if i % 2 else ''}" id="{s[0]}">
  <div class="svc__img"><img src="/img/foto/{s[2]}" alt="" loading="lazy"></div>
  <div class="svc__text">
    <span class="card__num">/0{i+1}</span>
    <h2>{s[1]}</h2>
    <p class="svc__lead">{s[3]}</p>
    {''.join(f'<p>{t}</p>' for t in s[4])}
    <ul class="checks">{''.join(f'<li>{b}</li>' for b in s[5])}</ul>
  </div>
</article>''' for i, s in enumerate(SERVIZI))
serv = page_hero('Servizi', 'Soluzioni digitali su misura, <em>dall\'analisi al supporto</em>.', 'Dallo sviluppo di piattaforme alla gestione di e-commerce e sistemi ERP per PMI: semplifichiamo i processi aziendali con la tecnologia.') + f'''
<nav class="subnav"><div class="wrap subnav__inner">{idx}</div></nav>
<section class="section section--tight"><div class="wrap svcs">{blocks}</div></section>
{LOGOS}{CTA}'''
pages['servizi.html'] = page('/servizi', 'Servizi — HackWork', 'Ottimizzazione dei processi, gestionali ed ERP, analisi dati e AI, integrazioni, siti ed e-commerce, consulenza IT e formazione.', serv, '/servizi')

# ─── LAVORI ───
case = ''.join(f'''<article class="case" id="{l[0]}">
  <div class="case__img"><img src="/img/{l[3]}" alt="{html.escape(l[1])}" loading="lazy"></div>
  <div class="case__text">
    <p class="tag">{l[2]}</p>
    <h2>{l[1]}</h2>
    <p class="svc__lead">{l[4]}</p>
    {''.join(f'<p>{t}</p>' for t in l[5])}
    <div class="chips">{''.join(f'<span>{c}</span>' for c in l[6])}</div>
  </div>
</article>''' for l in LAVORI)
lav = page_hero('Lavori', 'Progetti reali, <em>risultati concreti</em>.', 'Alcuni dei sistemi e dei siti che abbiamo progettato e sviluppato per i nostri clienti.') + f'''
<section class="section section--tight"><div class="wrap cases">{case}</div></section>
{CTA}'''
pages['lavori.html'] = page('/lavori', 'Lavori — HackWork', 'Gestionale ERP per il settore idraulico e sito per Elysian Luxe: alcuni progetti di HackWork.', lav, '/lavori')

# ─── BLOG ───
blog = page_hero('Blog', 'Idee per far <em>crescere</em> la tua azienda.', 'Digitalizzazione, gestionali, costi e servizio clienti: articoli pratici per imprenditori.') + f'''
<section class="section section--tight"><div class="wrap posts posts--grid">{''.join(post_card(p) for p in P)}</div></section>
{CTA}'''
pages['blog.html'] = page('/blog', 'Blog — HackWork', 'Articoli su digitalizzazione aziendale, gestionali, ottimizzazione dei costi e servizio clienti.', blog, '/blog')

for i, p in enumerate(P):
    others = [q for q in P if q is not p][:2]
    art = f'''<article class="article">
  <header class="article__head">
    <div class="grid-bg" aria-hidden="true"></div>
    <div class="wrap wrap--narrow">
      <a href="/blog" class="back">← Tutti gli articoli</a>
      <time>{data_it(p['date'])}</time>
      <h1>{html.escape(p['title'])}</h1>
    </div>
  </header>
  <div class="wrap wrap--narrow">
    <div class="article__img"><img src="/img/foto/{p['img']}.jpg" alt="" loading="eager"></div>
    <div class="prose">{p['body']}</div>
    <div class="article__cta"><h3>Vuoi applicarlo alla tua azienda?</h3><p>La prima consulenza è gratuita: analizziamo insieme come lavori oggi.</p><a href="/contatti" class="btn">Prenota una consulenza</a></div>
  </div>
</article>
<section class="section section--tight"><div class="wrap"><div class="section__head"><p class="label">Continua a leggere</p></div><div class="posts posts--two">{''.join(post_card(q) for q in others)}</div></div></section>'''
    pages[f'blog/{p["slug"]}.html'] = page(f'/blog/{p["slug"]}', f'{p["title"]} — HackWork', p['excerpt'][:155], art, '/blog')

# ─── CONTATTI ───
cont = f'''<section class="contact contact--page">
  <div class="wrap contact__grid">
    <div>
      <p class="label">Contatti</p>
      <h1>Trasformiamo le sfide in opportunità.</h1>
      <p class="contact__lead">Raccontaci il tuo progetto: la prima consulenza è gratuita e ti rispondiamo entro 24 ore lavorative.</p>
      <ul class="contact__list">
        <li><small>Telefono</small><a href="tel:+393248861951">+39 324 886 1951</a></li>
        <li><small>Email</small><a href="mailto:info@hackwork.space">info@hackwork.space</a></li>
        <li><small>Sede</small><span>Milano, Italia</span></li>
      </ul>
      <p class="contact__work"><b>Lavora con noi:</b> mandaci il tuo CV a <a href="mailto:info@hackwork.space?subject=Candidatura">info@hackwork.space</a>.</p>
    </div>
    {FORM}
  </div>
</section>'''
pages['contatti.html'] = page('/contatti', 'Contatti — HackWork', 'Contatta HackWork a Milano: consulenza gratuita per gestionali, ERP, integrazioni, siti ed e-commerce.', cont, '/contatti')

for f, c in pages.items():
    path = os.path.join('public', f); os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(c)
print('\n'.join(sorted(pages)))

nf = page_hero('Errore 404', 'Questa pagina <em>non esiste</em>.', 'Forse il link è vecchio o la pagina è stata spostata.') + '''<section class="section section--tight"><div class="wrap"><a href="/" class="btn">Torna alla home</a> <a href="/contatti" class="btn btn--ghost">Contattaci</a></div></section>'''
open('public/404.html','w').write(page('/404', 'Pagina non trovata — HackWork', 'Pagina non trovata', nf))
import os
urls=['/','/chi-siamo','/servizi','/lavori','/blog','/contatti']+['/blog/'+f[:-5] for f in sorted(os.listdir('public/blog'))]
open('public/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://hackwork.space{u}</loc></url>\n' for u in urls)+'</urlset>\n')
open('public/robots.txt','w').write('User-agent: *\nDisallow: /admin/\nSitemap: https://hackwork.space/sitemap.xml\n')
