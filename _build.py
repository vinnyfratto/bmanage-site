# Writes the site's pages with one shared header and footer:  python _build.py
# (GitHub Pages skips files starting with "_", so this script isn't published.)
import io, os
D = os.path.dirname(os.path.abspath(__file__))
EMAIL = 'vfratto@vcinnovationsgroup.com'
UPDATED = 'November 27, 2026'

# The price list, in one place (docs/02-subscriptions.md in the app repo; the suggested set, Nov 27).
PRO_YEAR, PRO_MONTH, FOUNDING, EXTRA_PC = 48, 6, 29, 10
SEAT_YEAR, SEAT_YEAR_25, MIN_SEATS = 72, 60, 5
REFUND_DAYS = 30

GOOGLE = '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.6 5.4 2.6 13.2l7.9 6.2C12.4 13.6 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.1 24.6c0-1.6-.1-3.1-.4-4.6H24v8.7h12.4c-.5 2.9-2.2 5.3-4.6 6.9l7.4 5.8c4.3-4 6.9-9.9 6.9-16.8z"/><path fill="#FBBC05" d="M10.5 28.6c-.5-1.4-.8-2.9-.8-4.6s.3-3.2.8-4.6l-7.9-6.2C.9 16.6 0 20.2 0 24s.9 7.4 2.6 10.8l7.9-6.2z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.4-5.8c-2.1 1.4-4.8 2.3-8.5 2.3-6.3 0-11.6-4.1-13.5-9.9l-7.9 6.2C6.6 42.6 14.6 48 24 48z"/></svg>'
GITHUB = '<svg viewBox="0 0 16 16" aria-hidden="true"><path fill="#313131" d="M8 0C3.6 0 0 3.6 0 8c0 3.5 2.3 6.5 5.5 7.6.4.1.5-.2.5-.4v-1.4c-2.2.5-2.7-1-2.7-1-.4-.9-.9-1.2-.9-1.2-.7-.5.1-.5.1-.5.8.1 1.2.8 1.2.8.7 1.2 1.9.9 2.3.7.1-.5.3-.9.5-1.1-1.8-.2-3.6-.9-3.6-3.9 0-.9.3-1.6.8-2.1-.1-.2-.4-1 .1-2.1 0 0 .7-.2 2.2.8.6-.2 1.3-.3 2-.3s1.4.1 2 .3c1.5-1 2.2-.8 2.2-.8.4 1.1.2 1.9.1 2.1.5.6.8 1.3.8 2.1 0 3.1-1.9 3.7-3.6 3.9.3.3.6.8.6 1.5v2.2c0 .2.1.5.6.4C13.7 14.5 16 11.5 16 8c0-4.4-3.6-8-8-8z"/></svg>'


def head(title, desc, robots=''):
    robots = f'\n  <meta name="robots" content="{robots}" />' if robots else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <!-- Google Search Console: proves getaiprojecthub.com is ours (needed for Google sign-in brand verification). Keep it. -->
  <meta name="google-site-verification" content="gZs-N-mG1hgnbAYeKJ3I3-_aKPQKovTtpEwuGJue6WQ" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />{robots}
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="https://getaiprojecthub.com/assets/brand/logo-mark-512.png" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="/assets/brand/favicon-32.png" type="image/png" sizes="32x32" />
  <link rel="apple-touch-icon" href="/assets/brand/favicon-180.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/style.css" />
  <script src="/assets/bm-config.js"></script>
  <script type="module" src="/assets/bm-auth.js"></script>
</head>
<body>
'''


def header(on=''):
    links = [('/', 'Overview', 'home'), ('/#features', 'Features', 'features'), ('/pricing/', 'Pricing', 'pricing'), ('/privacy.html', 'Privacy', 'privacy'), ('/terms.html', 'Terms', 'terms')]
    nav = ''.join(f'\n        <a href="{h}"{" class=\"on\"" if k == on else ""}>{l}</a>' for h, l, k in links)
    return f'''  <header>
    <div class="wrap nav">
      <a class="brand" href="/" aria-label="Ai Project Hub, home">
        <img class="logo" src="/assets/brand/logo.svg" alt="Ai Project Hub" width="273" height="64" />
      </a>
      <nav class="nav-links">{nav}
      </nav>
      <div class="nav-cta">
        <a class="btn btn-ghost" href="/account/login/" data-bm-account>Log in</a>
        <a class="btn btn-primary" href="/account/signup/" data-bm-signup>Create account</a>
      </div>
    </div>
  </header>
'''


FOOTER = f'''  <footer>
    <div class="wrap">
      <div class="foot-grid">
        <div class="foot-brand">
          <a class="brand" href="/" aria-label="Ai Project Hub, home">
            <img class="logo" src="/assets/brand/logo-dark.svg" alt="Ai Project Hub" width="273" height="64" />
          </a>
          <a class="by" href="https://vcinnovationsgroup.com/">by VC Innovations Group</a>
        </div>
        <div class="foot-links">
          <div class="foot-col">
            <h4>Ai Project Hub</h4>
            <a href="/">Overview</a>
            <a href="/#features">Features</a>
            <a href="/pricing/">Pricing</a>
            <a href="/account/">Your account</a>
            <a href="/privacy.html">Privacy policy</a>
            <a href="/terms.html">Terms of service</a>
          </div>
          <div class="foot-col">
            <h4>Studio</h4>
            <a href="https://vcinnovationsgroup.com/">vcinnovationsgroup.com</a>
          </div>
          <div class="foot-col">
            <h4>Contact</h4>
            <a href="mailto:{EMAIL}">{EMAIL}</a>
            <span>San Antonio, TX</span>
          </div>
        </div>
      </div>
      <div class="foot-bottom">
        <span>© 2026 VC Innovations Group. All rights reserved.</span>
        <span>Ai Project Hub · under development</span>
      </div>
    </div>
  </footer>
</body>
</html>
'''

OAUTH = f'''    <div class="oauth">
      <button type="button" class="btn btn-oauth" data-provider="google">{GOOGLE}Continue with Google</button>
      <button type="button" class="btn btn-oauth" data-provider="github">{GITHUB}Continue with GitHub</button>
    </div>
    <div class="or-line">or with email</div>
'''


def page(path, title, desc, body, on='', robots=''):
    full = os.path.join(D, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    io.open(full, 'w', encoding='utf-8', newline='\n').write(head(title, desc, robots) + header(on) + body + FOOTER)


# ---------- shared bits for the home and pricing pages ----------
YES = '<span class="yes" aria-label="Included">&#10003;</span>'
NO = '<span class="no" aria-label="Not included">&ndash;</span>'

PLANS = f'''
      <div class="plans">
        <div class="plan">
          <h3>Free</h3>
          <p class="plan-for">Try it, and keep your Claude threads in one place.</p>
          <div class="price"><span class="amt">$0</span></div>
          <p class="price-sub">Free for good. 1 PC.</p>
          <ul class="plan-list">
            <li>Every Claude Code thread and claude.ai chat in one place</li>
            <li>Reply, paste pictures, and approve what Claude asks</li>
            <li>Build a bot and test-run it</li>
            <li>The last run's report</li>
          </ul>
          <a class="btn btn-ghost" href="/account/signup/" data-bm-signup>Create account</a>
        </div>
        <div class="plan plan-main">
          <span class="plan-tag">Most people</span>
          <h3>Pro</h3>
          <p class="plan-for">For one person running bots across their projects.</p>
          <div class="price"><span class="amt">${PRO_YEAR}</span><span class="per">/ year</span></div>
          <p class="price-sub">or ${PRO_MONTH} a month. 2 PCs, ${EXTRA_PC} a year for each extra PC.</p>
          <p class="founding"><b>Founding price: ${FOUNDING} a year, kept for life</b>, for people who join before launch.</p>
          <ul class="plan-list">
            <li>Everything in Free</li>
            <li>Saved bots that run on a schedule, even with the app closed</li>
            <li>Every report, kept</li>
            <li>Groups and group brains</li>
            <li>Skills, plugins, and connectors in your bots</li>
            <li>Join a team</li>
          </ul>
          <a class="btn btn-primary" href="/account/signup/" data-bm-signup>Get started</a>
        </div>
        <div class="plan">
          <h3>Enterprise</h3>
          <p class="plan-for">For companies that run teams and manage seats.</p>
          <div class="price"><span class="amt">${SEAT_YEAR}</span><span class="per">/ seat / year</span></div>
          <p class="price-sub">{MIN_SEATS} seats or more. ${SEAT_YEAR_25} a seat from 25 seats. 2 PCs per seat.</p>
          <ul class="plan-list">
            <li>Everything in Pro</li>
            <li>Make teams and invite people by email</li>
            <li>Buy seats and assign them by email</li>
            <li>Pay by invoice</li>
            <li>100 seats or more: <a class="text-link" href="mailto:{EMAIL}?subject=Ai%20Project%20Hub%20Enterprise">talk to us</a></li>
          </ul>
          <a class="btn btn-ghost" href="mailto:{EMAIL}?subject=Ai%20Project%20Hub%20Enterprise">Contact us</a>
        </div>
      </div>
      <div class="note plans-note"><b>Your Claude plan runs the AI.</b> Ai Project Hub runs Claude Code on your own Claude plan (Pro or Max) with Anthropic, never an API key, so its price covers the app, not AI usage. That's most of why it costs a fraction of tools that include the AI. <b>No free trial</b>: cancel within {REFUND_DAYS} days of making your account for a full refund. <b>Paid plans open at launch.</b> Until then, every feature is included.</div>
'''

COMPARE = [
    ('Your Claude work', None),
    ('Every Claude Code thread, from the Claude app and the terminal', (YES, YES, YES)),
    ('claude.ai chats and Projects, live', (YES, YES, YES)),
    ('Reply in a thread: pictures, lists, a queue, Claude asks first', (YES, YES, YES)),
    ('File viewer for files Claude mentions', (YES, YES, YES)),
    ('Bots', None),
    ('Build a bot from a template or plain words, and test-run it', (YES, YES, YES)),
    ('Save bots', (NO, YES, YES)),
    ('Schedules, after each commit, and runs with the app closed', (NO, YES, YES)),
    ('Inbox and report history', ('Last run', YES, YES)),
    ('Skills, plugins, and connectors in bots', (NO, YES, YES)),
    ('Organize', None),
    ('Groups: projects, threads, bots, and files by client or task', (NO, YES, YES)),
    ('Group brains: shared background for every run and reply', (NO, YES, YES)),
    ('Teams', None),
    ('Join a team', (NO, YES, YES)),
    ('Make teams and invite people', (NO, NO, YES)),
    ('Buy seats, assign them by email, pay by invoice', (NO, NO, YES)),
    ('Your PCs', None),
    ('PCs included', ('1', f'2 (+${EXTRA_PC}/yr each)', '2 per seat')),
]


def compare_table():
    rows = []
    for label, cells in COMPARE:
        if cells is None:
            rows.append(f'<tr class="grp"><th colspan="4">{label}</th></tr>')
        else:
            rows.append(f'<tr><th scope="row">{label}</th>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
    body = '\n          '.join(rows)
    return f'''<div class="table-wrap">
        <table class="compare">
          <thead><tr><th></th><th>Free</th><th class="hl">Pro</th><th>Enterprise</th></tr></thead>
          <tbody>
          {body}
          </tbody>
        </table>
      </div>'''


FEATURES = [
    ('Bots that do one job', 'A code reviewer, a topic researcher, a secrets watch, a docs check, a weekly changelog. Start from a template or describe it in plain words. Each bot is drawn as a simple flow: when it runs, where, its job, its rules, what it may do, and where results go.'),
    ('Runs on its own', 'On a schedule, after each commit, or when you click Run now. A Windows task runs bots even with the app closed. Each run has a token limit, and all bots share a daily one.'),
    ('Inbox, Runs, and Rules', 'What bots find lands in your Inbox: open it in your editor, fix it with Claude, or mark it done. Every run is kept step by step with its token count. House rules, like US English or no secrets in code, apply to every bot.'),
    ('Every Claude thread in one place', 'Your Claude Code sessions, from the Claude app and the terminal, listed by project. Open one, read it, and reply: Claude continues the same session, and it shows in the Claude app too.'),
    ('A better reply box', 'Paste pictures, mention files with @, write lists, and queue a message while Claude works. When Claude asks before a change, a popup lets you allow it, always allow it, or say no. Pick the model and effort per message.'),
    ('claude.ai chats, live', 'Sign in to claude.ai inside Ai Project Hub and your chats and Projects show beside your code threads. Read them, reply, start a new chat in a Project.'),
    ('Groups', 'Put projects, threads, bots, and files together by client, product, or task, drawn as one chart. Things in a group take its color everywhere, and Focus shows only that group.'),
    ('Group brains', 'One shared page per group: what it is about, what was decided, how the pieces connect, and what is going on now. Every bot run and reply in the group starts with it, and a keeper proposes updates as work happens.'),
    ('Teams', 'Make a team and invite people by email with a one-time code. See who is online.'),
]


def features_grid():
    return '\n'.join(f'        <div class="feat"><h3>{t}</h3><p>{p}</p></div>' for t, p in FEATURES)


# ---------- home ----------
page('index.html', 'Ai Project Hub · Your Claude work, bots, and projects in one place', 'Ai Project Hub is a Windows app that keeps every Claude thread in one place and runs AI bots on your projects, on your own Claude plan. Free, Pro, and Enterprise plans.', f'''
  <section class="hero">
    <div class="wrap">
      <span class="eyebrow">A VC Innovations Group product</span><span class="pill"><span class="dot"></span>Under development</span>
      <h1>Your Claude work, <span class="italic">in one place</span></h1>
      <p class="lede">Ai Project Hub is a Windows app for people who build with Claude. It keeps every Claude Code thread and claude.ai chat together by project, runs AI bots that review, research, and watch your projects on a schedule, and gives each group of projects a shared brain. It all runs on your PC, on your own Claude plan.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/account/signup/" data-bm-signup>Create your account</a>
        <a class="btn btn-ghost" href="/pricing/">See pricing</a>
      </div>
    </div>
  </section>

  <section class="shot-block">
    <div class="wrap">
      <figure class="shot">
        <img src="/assets/shots/bot-flow.png" alt="Ai Project Hub with a bot drawn as a flow: when it runs, where, its job, its rules, and what it may do" width="1424" height="861" loading="eager" />
        <figcaption>A bot, drawn as a flow. Click any step to change it; the sentence on top says the whole bot in plain words.</figcaption>
      </figure>
    </div>
  </section>

  <section class="block" id="features">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">What it does</span>
        <h2>More than a bot runner: <span class="italic">a hub</span> for your Claude projects</h2>
        <p class="lede">Bots, threads, chats, files, and the people you work with, organized the way you think about your work.</p>
      </div>
      <div class="feats">
{features_grid()}
      </div>
    </div>
  </section>

  <section class="block alt">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">How it works</span>
        <h2>Your PC, your plan, <span class="italic">your rules</span></h2>
      </div>
      <div class="cards">
        <div class="card"><div class="num">01</div><h3>Runs on your PC</h3><p>Bots and replies run with Claude Code on your computer, on your own Claude plan. Your code, threads, and reports stay on your PC.</p></div>
        <div class="card"><div class="num">02</div><h3>Safe by default</h3><p>Bots are read-only unless you give them more. They never commit, push, deploy, or publish, and a bot that edits works in its own copy of the project.</p></div>
        <div class="card"><div class="num">03</div><h3>Plain words</h3><p>No YAML to learn. Say what a bot should do, pick what it may use, and read what it found. Usage is shown in tokens, the way Claude Code shows it.</p></div>
      </div>
    </div>
  </section>

  <section class="block" id="pricing">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">Pricing</span>
        <h2>Simple plans, <span class="italic">no AI markup</span></h2>
        <p class="lede">Pay for the app once a year, or month to month. The AI runs on the Claude plan you already have.</p>
      </div>
{PLANS}
      <p class="more"><a class="text-link" href="/pricing/">Compare every feature and read the questions people ask &rarr;</a></p>
    </div>
  </section>

  <section class="block alt">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">What you need</span>
        <h2>Ready in <span class="italic">a few minutes</span></h2>
      </div>
      <div class="cards">
        <div class="card"><div class="num">01</div><h3>Windows 10 or 11</h3><p>Ai Project Hub is a desktop app for Windows, with a tray icon for runs in the background.</p></div>
        <div class="card"><div class="num">02</div><h3>A Claude plan</h3><p>Claude Pro or Max, with Claude Code (the Claude app includes it). Link it once in Settings; Ai Project Hub never sees your password.</p></div>
        <div class="card"><div class="num">03</div><h3>An Ai Project Hub account</h3><p>Sign up with email, Google, or GitHub. The same account works in the app and here, and keeps your plan, PCs, and teams.</p></div>
      </div>
    </div>
  </section>
''', 'home')

# ---------- pricing ----------
page('pricing/index.html', 'Pricing · Ai Project Hub', f'Ai Project Hub plans: Free, Pro at ${PRO_YEAR} a year, and Enterprise at ${SEAT_YEAR} a seat a year. The AI runs on your own Claude plan.', f'''
  <section class="hero hero-tight">
    <div class="wrap">
      <span class="eyebrow">Pricing</span><span class="pill"><span class="dot"></span>Paid plans open at launch</span>
      <h1>Simple plans, <span class="italic">no AI markup</span></h1>
      <p class="lede">Ai Project Hub's price covers the app. The AI runs on the Claude plan you already have, so you never pay for it twice.</p>
    </div>
  </section>

  <section class="block" style="padding-top:0">
    <div class="wrap">
{PLANS}
    </div>
  </section>

  <section class="block alt">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">Compare</span>
        <h2>Every feature, <span class="italic">plan by plan</span></h2>
      </div>
      {compare_table()}
      <p class="table-note">A locked feature shows with a lock and an Upgrade button; it never disappears. Nothing you made is deleted when a plan ends: saved bots stop running but stay in their files.</p>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">Questions</span>
        <h2>Before you <span class="italic">buy</span></h2>
      </div>
      <div class="faq">
        <details><summary>Do I need a Claude plan?</summary><p>Yes. Ai Project Hub runs Claude Code on your PC under your own Claude account, on Claude Pro or Max. It never uses an API key and never charges for AI. Your Claude usage counts against your Claude plan, as if you ran Claude Code yourself.</p></details>
        <details><summary>Is there a free trial?</summary><p>No trial. Instead, if you cancel within {REFUND_DAYS} days of making your account, you get a full refund. The Free plan is free for good.</p></details>
        <details><summary>What is the founding price?</summary><p>People who take Pro before launch pay ${FOUNDING} a year instead of ${PRO_YEAR}, and keep that price for as long as they stay on Pro.</p></details>
        <details><summary>What counts as a PC?</summary><p>Each Windows computer you sign in on. Pro includes 2; each extra PC is ${EXTRA_PC} a year. You can remove a PC any time from <a class="text-link" href="/account/">your account</a> to make room for another.</p></details>
        <details><summary>What happens if I go back to Free?</summary><p>Nothing you made is deleted. Saved bots stop running but stay in their files, groups and brains stay, and your threads and chats keep working.</p></details>
        <details><summary>Does my code leave my PC?</summary><p>No. Your projects, bots, runs, reports, and threads stay on your computer. Our server keeps only your account, plan, PCs, and teams; the <a class="text-link" href="/privacy.html">privacy policy</a> lists all of it.</p></details>
        <details><summary>How does Enterprise work?</summary><p>A company buys {MIN_SEATS} seats or more (${SEAT_YEAR} a seat a year, ${SEAT_YEAR_25} from 25 seats) and assigns each seat by email. Each seat gets everything in Pro on 2 PCs, plus making teams and inviting people. Pay by card or invoice. For 100 seats or more, <a class="text-link" href="mailto:{EMAIL}?subject=Ai%20Project%20Hub%20Enterprise">talk to us</a>.</p></details>
        <details><summary>When can I buy?</summary><p>Paid plans open at launch. Until then, Ai Project Hub is under development and every feature is included with a free account.</p></details>
      </div>
    </div>
  </section>
''', 'pricing')

# ---------- privacy ----------
page('privacy.html', 'Privacy policy · Ai Project Hub', 'What Ai Project Hub, by VC Innovations Group, keeps about you and why.', f'''
  <section class="legal">
    <div class="wrap">
      <div class="prose">
        <span class="eyebrow">Ai Project Hub</span>
        <h1>Privacy policy</h1>
        <p class="meta">Last updated {UPDATED}</p>
        <p>This policy explains what Ai Project Hub, a desktop app and website made by VC Innovations Group ("we"), keeps about you and why. Ai Project Hub is under development; we'll update this page as it grows.</p>
        <h2>Your account</h2>
        <p>You can sign up with your email and a password, or with Google or GitHub. With email, we keep your name and email; your password is stored only as a one-way hash, never readable. With Google or GitHub, they tell us your <b>email address</b> and your <b>name</b>, and we ask for nothing else: no contacts, files, mail, calendar, or repositories. We never see your Google or GitHub password.</p>
        <p>We use your email address to match you to invitations, since an invitation works only for the email it was sent to, and we show your name and email to the people on your teams.</p>
        <h2>What we keep on our server</h2>
        <ul>
          <li>Your name, email address, and how you sign in (email, Google, or GitHub), and whether you asked for product email.</li>
          <li>Your plan (Free, Pro, or Enterprise) and its status. Once paid plans exist: the price, billing dates, and the payment service's reference numbers. Card details are handled by the payment service and never stored by us.</li>
          <li>The PCs you use Ai Project Hub on, so a plan can allow a set number: a name, the app version, and when each was last used.</li>
          <li>The teams you make or join, your role on each, and when you joined.</li>
          <li>Invitations: the email invited and when. The invitation code itself is never stored, only a one-way fingerprint of it.</li>
          <li>When your Ai Project Hub last checked in, so teammates can see you're online.</li>
        </ul>
        <p>This is kept in a database hosted by Supabase in the United States, encrypted at rest. You can see your own account; teammates see only your name, email, and whether you're online.</p>
        <h2>What stays on your computer</h2>
        <p>Your bots, their runs and reports, your projects and code, your Claude threads, and your Claude account all stay on your computer. Bots run with Claude Code under your own Claude account with Anthropic, which has its own terms and privacy policy. The Ai Project Hub app keeps your sign-in on your computer encrypted by Windows.</p>
        <h2>This website</h2>
        <p>When you sign in here, your browser keeps the sign-in in its local storage until you sign out. The site uses no cookies of its own and no analytics or ads.</p>
        <h2>What we don't do</h2>
        <p>We don't sell or share your information, show ads, or track you across apps or websites.</p>
        <h2>Deleting your information</h2>
        <p>You can leave a team or delete a team you own in Ai Project Hub at any time. To have your account and everything we keep about you deleted, email us at <a href="mailto:{EMAIL}">{EMAIL}</a> from the address you sign in with. We delete it within 30 days. You can also remove Ai Project Hub's access in your Google or GitHub account settings.</p>
        <h2>Changes</h2>
        <p>If this policy changes, we'll update this page and the date above.</p>
        <h2>Contact</h2>
        <p>VC Innovations Group · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
    </div>
  </section>
''', 'privacy')

# ---------- terms ----------
page('terms.html', 'Terms of service · Ai Project Hub', 'The terms for using Ai Project Hub, by VC Innovations Group.', f'''
  <section class="legal">
    <div class="wrap">
      <div class="prose">
        <span class="eyebrow">Ai Project Hub</span>
        <h1>Terms of service</h1>
        <p class="meta">Last updated {UPDATED}</p>
        <p>Ai Project Hub is a desktop app and website made by VC Innovations Group. By creating an account or using it, you agree to these terms.</p>
        <h2>Using Ai Project Hub</h2>
        <p>Ai Project Hub is under development. It is provided as is, without warranties of any kind. You're responsible for the bots you set up, what you let them do, and the projects you run them on. Bots run with Claude Code under your own Claude account, so Anthropic's terms apply to that use too.</p>
        <h2>Your account and teams</h2>
        <p>Keep your account secure, whether you sign in with email, Google, or GitHub. Only invite people you mean to work with, and don't use Ai Project Hub to break the law or anyone's rights.</p>
        <h2>Plans</h2>
        <p>Ai Project Hub has a Free plan and paid plans (Pro and Enterprise), listed on the <a href="/pricing/">pricing page</a>. Paid plans open at launch; until then every feature is included. Before you buy, you see the price, the billing period, and how many PCs the plan allows. There is no free trial: if you cancel within {REFUND_DAYS} days of making your account, you get a full refund. After that, you can cancel any time and keep your plan until the end of the period you paid for. Ai Project Hub's price doesn't include Claude: your Claude plan with Anthropic is separate.</p>
        <h2>Limits</h2>
        <p>To the extent the law allows, VC Innovations Group isn't liable for indirect or lost-profit damages from using Ai Project Hub. We may change or stop the service, and we may update these terms; the date above shows the latest version.</p>
        <h2>Contact</h2>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
    </div>
  </section>
''', 'terms')

# ---------- account: sign up ----------
page('account/signup/index.html', 'Create your Ai Project Hub account', 'Create a free Ai Project Hub account.', f'''
  <main class="acct">
  <div class="acct-card" data-bm-page="signup">
    <span class="eyebrow">Get started</span>
    <h1>Create your account</h1>
    <p class="acct-sub">One free account works in the Ai Project Hub app and on this website.</p>
    <div id="bm-alert" class="alert" role="status" aria-live="polite"></div>
    <label class="check"><input type="checkbox" name="terms" form="bm-signup-form" required /><span>I agree to the <a href="/terms.html">Terms of Service</a> and <a href="/privacy.html">Privacy Policy</a>.</span></label>
{OAUTH}    <form id="bm-signup-form" novalidate>
      <div class="field-row">
        <div class="field"><label for="su-first">First name</label><input id="su-first" name="first_name" type="text" autocomplete="given-name" required /></div>
        <div class="field"><label for="su-last">Last name</label><input id="su-last" name="last_name" type="text" autocomplete="family-name" required /></div>
      </div>
      <div class="field"><label for="su-email">Email</label><input id="su-email" name="email" type="email" autocomplete="email" required /></div>
      <div class="field"><label for="su-password">Password <span class="hint">(min. 8 characters)</span></label>
        <div class="pw-field"><input id="su-password" name="password" type="password" autocomplete="new-password" minlength="8" required /><button type="button" class="pw-toggle" aria-label="Show password"></button></div></div>
      <label class="check"><input type="checkbox" name="marketing_opt_in" /><span>Send me Ai Project Hub news and product updates by email. (optional)</span></label>
      <button type="submit" class="btn btn-primary">Create account</button>
    </form>
    <p class="acct-links">Already have an account? <a href="/account/login/">Log in</a></p>
  </div>
  </main>
''')

# ---------- account: log in ----------
page('account/login/index.html', 'Log in to Ai Project Hub', 'Log in to your Ai Project Hub account.', f'''
  <main class="acct">
  <div class="acct-card" data-bm-page="login">
    <span class="eyebrow">Welcome back</span>
    <h1>Log in</h1>
    <p class="acct-sub">Use the same account as the Ai Project Hub app.</p>
    <div id="bm-alert" class="alert" role="status" aria-live="polite"></div>
{OAUTH}    <form id="bm-login-form" novalidate>
      <div class="field"><label for="li-email">Email</label><input id="li-email" name="email" type="email" autocomplete="email" required /></div>
      <div class="field"><label for="li-password">Password</label>
        <div class="pw-field"><input id="li-password" name="password" type="password" autocomplete="current-password" required /><button type="button" class="pw-toggle" aria-label="Show password"></button></div></div>
      <button type="submit" class="btn btn-primary">Log in</button>
    </form>
    <p class="acct-links"><a href="/account/reset/">Forgot password?</a><span class="sep">·</span>New here? <a href="/account/signup/">Create an account</a></p>
  </div>
  </main>
''')

# ---------- account: reset ----------
page('account/reset/index.html', 'Reset your Ai Project Hub password', 'Reset the password for your Ai Project Hub account.', '''
  <main class="acct">
  <div class="acct-card" data-bm-page="reset">
    <span class="eyebrow">Account</span>
    <h1>Reset your password</h1>
    <p class="acct-sub">We'll email you a link to set a new one. Signed up with Google or GitHub? Just log in with it.</p>
    <div id="bm-alert" class="alert" role="status" aria-live="polite"></div>
    <form id="bm-reset-request-form" novalidate>
      <div class="field"><label for="rs-email">Email</label><input id="rs-email" name="email" type="email" autocomplete="email" required /></div>
      <button type="submit" class="btn btn-primary">Send reset link</button>
    </form>
    <form id="bm-reset-set-form" novalidate style="display:none">
      <div class="field"><label for="rs-password">New password <span class="hint">(min. 8 characters)</span></label>
        <div class="pw-field"><input id="rs-password" name="password" type="password" autocomplete="new-password" minlength="8" required /><button type="button" class="pw-toggle" aria-label="Show password"></button></div></div>
      <button type="submit" class="btn btn-primary">Set new password</button>
    </form>
    <p class="acct-links"><a href="/account/login/">Back to log in</a></p>
  </div>
  </main>
''')

# ---------- account: my account ----------
page('account/index.html', 'Your Ai Project Hub account', 'Your Ai Project Hub account: plan, PCs, and sign-in.', '''
  <main class="acct">
  <div class="acct-card" data-bm-page="account">
    <p id="bm-gate" class="acct-sub">Loading your account...</p>
    <div id="bm-account" style="display:none">
      <span class="eyebrow">Your account</span>
      <h1 id="acct-name"></h1>
      <p class="acct-sub" id="acct-email"></p>
      <h2 class="acct-section">Plan</h2>
      <dl class="acct-facts">
        <dt>Plan</dt><dd id="acct-plan"></dd>
        <dt>Status</dt><dd id="acct-status"></dd>
        <dt id="acct-renew-row">Renews</dt><dd id="acct-renew"></dd>
        <dt id="acct-refund-row">Full refund</dt><dd id="acct-refund"></dd>
        <dt>PCs</dt><dd id="acct-devices"></dd>
      </dl>
      <ul class="acct-pcs" id="acct-pcs"></ul>
      <h2 class="acct-section">Sign-in</h2>
      <dl class="acct-facts">
        <dt>Signs in with</dt><dd id="acct-provider"></dd>
        <dt>Member since</dt><dd id="acct-since"></dd>
      </dl>
      <div class="note" style="margin-bottom:22px"><b>Ai Project Hub is under development.</b> There is no free trial: cancel within 30 days of making your account for a full refund. Paid plans come later; nothing is locked yet.</div>
      <button type="button" class="btn btn-ghost" id="bm-signout">Sign out</button>
    </div>
  </div>
  </main>
''')
# ---------- pricing matrix for Chris (internal: not linked, not indexed) ----------
page('PricingMatrixForChris/index.html', 'Ai Project Hub pricing matrix (draft)', 'Internal draft: Ai Project Hub plans and prices next to similar tools.',
     io.open(os.path.join(D, '_pricing-matrix.html'), encoding='utf-8').read(), robots='noindex, nofollow')
print('built')
