# Writes the site's pages with one shared header and footer:  python _build.py
# (GitHub Pages skips files starting with "_", so this script isn't published.)
import io, os
D = os.path.dirname(os.path.abspath(__file__))
EMAIL = 'vfratto@vcinnovationsgroup.com'
UPDATED = 'November 27, 2026'

# The price list, in one place (docs/02-subscriptions.md in the app repo).
PRO_YEAR, PRO_SALE, SALE_ENDS = 39, 29, 'January 31, 2027'  # Vinny, Nov 27: two tiers, Pro and Enterprise (contact us)
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
      <a class="brand" href="/" aria-label="AI Project Hub, home">
        <img class="logo" src="/assets/brand/logo.svg" alt="AI Project Hub" width="273" height="64" />
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
          <a class="brand" href="/" aria-label="AI Project Hub, home">
            <img class="logo" src="/assets/brand/logo-dark.svg" alt="AI Project Hub" width="273" height="64" />
          </a>
          <a class="by" href="https://vcinnovationsgroup.com/">by VC Innovations Group</a>
        </div>
        <div class="foot-links">
          <div class="foot-col">
            <h4>AI Project Hub</h4>
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
            <a href="mailto:{EMAIL}?subject=AI%20Project%20Hub%20question">Have questions? Email us</a>
          </div>
        </div>
      </div>
      <div class="foot-bottom">
        <span>© 2026 VC Innovations Group. All rights reserved.</span>
        <span>AI Project Hub · under development</span>
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
      <div class="plans plans-2">
        <div class="plan plan-main">
          <span class="plan-tag">Holiday price</span>
          <h3>Pro</h3>
          <p class="plan-for">For one person: every tool in AI Project Hub, on your main PC and a remote one.</p>
          <div class="price"><span class="was">${PRO_YEAR}</span><span class="amt">${PRO_SALE}</span><span class="per">/ year</span></div>
          <p class="price-sub"><b>${PRO_SALE} a year through {SALE_ENDS}</b>, then ${PRO_YEAR} a year. 2 devices: your main PC and a remote one.</p>
          <ul class="plan-list">
            <li>Groups that link projects, Code threads, and claude.ai chats into one shared brain</li>
            <li>Work on the same code from your desktop or your laptop</li>
            <li>Bots you build as a visual flow, on a schedule or after each commit</li>
            <li>Every Claude Code thread and claude.ai chat in one list</li>
            <li>Inbox, run history, skills, and connectors</li>
            <li>Teams: invite people by email</li>
          </ul>
          <a class="btn btn-primary" href="/account/?buy=pro">Get Pro</a>
        </div>
        <div class="plan">
          <h3>Enterprise</h3>
          <p class="plan-for">For companies: every tool, plus a server of your own so departments and teams work from the same notes.</p>
          <div class="price"><span class="amt amt-text">Let's talk</span></div>
          <p class="price-sub">Priced for your company, by seats and departments.</p>
          <ul class="plan-list">
            <li>Everything in Pro, for every seat</li>
            <li>A dedicated server that keeps your threads available from any approved PC</li>
            <li>Groups across departments, teams, or the whole company</li>
            <li>Threads, projects, and bots in a group work from that group's notes</li>
            <li>Seats assigned by email, and invoices</li>
          </ul>
          <a class="btn btn-ghost" href="mailto:{EMAIL}?subject=AI%20Project%20Hub%20Enterprise">Contact us</a>
        </div>
      </div>
      <div class="note plans-note"><b>Every plan includes every tool.</b> Enterprise adds a server for your company. <b>Your Claude plan runs the AI:</b> AI Project Hub runs Claude Code on your own Claude plan (Pro or Max) with Anthropic, never an API key, so its price covers the app, not AI usage. <b>No free trial</b>: cancel within {REFUND_DAYS} days of making your account for a full refund.</div>
'''

COMPARE = [
    ('Your Claude work', None),
    ('Every Claude Code thread, from the Claude app and the terminal', (YES, YES)),
    ('claude.ai chats and Projects, live', (YES, YES)),
    ('Reply in a thread: pictures, lists, a queue, Claude asks first', (YES, YES)),
    ('File viewer for files Claude mentions', (YES, YES)),
    ('Bots', None),
    ('Build a bot from a template or plain words, and test-run it', (YES, YES)),
    ('Schedules, after each commit, and runs with the app closed', (YES, YES)),
    ('Inbox, run history, and house rules', (YES, YES)),
    ('Skills, plugins, and connectors in bots', (YES, YES)),
    ('Organize and share', None),
    ('Groups: projects, threads, bots, and files by client or task', (YES, YES)),
    ('Group brains: shared background for every run and reply', (YES, YES)),
    ('Teams: invite people by email, see who is online', (YES, YES)),
    ('Your company', None),
    ('A dedicated server that hosts your threads, always available', (NO, YES)),
    ('Groups across departments, teams, or the whole company', (NO, YES)),
    ('Shared company, department, and team knowledge in linked threads, projects, and bots', (NO, YES)),
    ('Seats assigned by email, invoices', (NO, YES)),
    ('Devices', None),
    ('Devices included', ('2: main and remote', 'Per seat')),
]


def compare_table():
    rows = []
    for label, cells in COMPARE:
        if cells is None:
            rows.append(f'<tr class="grp"><th colspan="3">{label}</th></tr>')
        else:
            rows.append(f'<tr><th scope="row">{label}</th>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
    body = '\n          '.join(rows)
    return f'''<div class="table-wrap">
        <table class="compare compare-2">
          <thead><tr><th></th><th class="hl">Pro</th><th>Enterprise</th></tr></thead>
          <tbody>
          {body}
          </tbody>
        </table>
      </div>'''


PROMO = f'''      <a class="promo" href="/pricing/">
        <span class="promo-tag">Holiday price</span>
        <span class="promo-text">Pro is <b>${PRO_SALE}</b> for your first year, normally ${PRO_YEAR}. Sign up by {SALE_ENDS.replace(' ', '&nbsp;')}.</span>
        <span class="promo-go">See Pro &rarr;</span>
      </a>
'''

# ---------- home ----------
# The home page is its own design (Vinny, Nov 28: the Virtuware template's layout, mocked up in _Mockups/virtuware/):
# _home.html holds its styles and body; the prices, dates, and email come from the constants at the top.
def home_head(title, desc):
    h = head(title, desc)
    h = h.replace('family=Noto+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400', 'family=Heebo:wght@400;500;600;700;800')
    return h.replace('  <link rel="stylesheet" href="/style.css" />\n', '').replace('</head>\n<body>\n', '')

HOME = io.open(os.path.join(D, '_home.html'), encoding='utf-8').read()
for k, v in {'SALE': PRO_SALE, 'YEAR': PRO_YEAR, 'ENDS_NB': SALE_ENDS.replace(' ', '&nbsp;'), 'ENDS': SALE_ENDS, 'REFUND': REFUND_DAYS, 'EMAIL': EMAIL}.items():
    HOME = HOME.replace('{{' + k + '}}', str(v))
assert '{{' not in HOME
io.open(os.path.join(D, 'index.html'), 'w', encoding='utf-8', newline='\n').write(home_head(
    'AI Project Hub · A shared brain for your Claude projects, on two machines',
    f'AI Project Hub is a Windows app for Claude Code. Link projects in groups so Code threads and claude.ai chats feed one shared brain, work on the same code from your desktop or laptop, and build bots by drawing them. Pro is ${PRO_SALE} for your first year through {SALE_ENDS}.') + HOME)

# ---------- pricing ----------
page('pricing/index.html', 'Pricing · AI Project Hub', f'AI Project Hub Pro is ${PRO_SALE} for your first year through {SALE_ENDS}, then ${PRO_YEAR} a year, with every tool on 2 devices. Enterprise adds a dedicated server for your company.', f'''
  <section class="hero hero-tight">
    <div class="wrap">
{PROMO}
      <span class="eyebrow">Pricing</span>
      <h1>Two plans. <span class="italic">Every tool in both.</span></h1>
      <p class="lede">Pro is for one person on a main PC and a laptop. Enterprise adds a server for your company, so departments and teams work from the same notes. The AI runs on the Claude plan you already have.</p>
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
        <h2>Pro and Enterprise, side by side</h2>
      </div>
      {compare_table()}
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">Questions</span>
        <h2>Before you buy</h2>
      </div>
      <div class="faq">
        <details><summary>Do I need a Claude plan?</summary><p>Yes. AI Project Hub runs Claude Code on your PC under your own Claude account, on Claude Pro or Max. It never uses an API key and never charges for AI. Your Claude usage counts against your Claude plan, the same as running Claude Code yourself.</p></details>
        <details><summary>How does the holiday price work?</summary><p>Sign up for Pro by {SALE_ENDS} and your first year is ${PRO_SALE}. It renews at ${PRO_YEAR} a year.</p></details>
        <details><summary>Is there a free trial?</summary><p>No. If you cancel within {REFUND_DAYS} days of making your account, you get a full refund.</p></details>
        <details><summary>What are the 2 devices?</summary><p>Your main PC and a remote one, like a laptop. Pair them once and the laptop can use everything on the main PC. You can remove a device any time from <a class="text-link" href="/account/">your account</a>.</p></details>
        <details><summary>Does Pro leave anything out?</summary><p>No. Pro has every tool: groups and brains, two devices, bots and schedules, threads and claude.ai chats, skills and connectors, and Teams. Enterprise adds a server for your company.</p></details>
        <details><summary>What does the Enterprise server do?</summary><p>It hosts your company's threads, so they're available from any approved PC, not only the one where they started. Groups can cover a department, a team, or the whole company, and every thread, project, and bot in a group works from that group's notes.</p></details>
        <details><summary>Does my code leave my PC?</summary><p>On Pro, no. Projects, bots, runs, reports, and threads stay on your computer. Our server keeps only your account, plan, devices, and teams; the <a class="text-link" href="/privacy.html">privacy policy</a> lists all of it. On Enterprise, threads are kept on your company's server.</p></details>
        <details><summary>What if I stop paying?</summary><p>Nothing you made is deleted. Your bots stay in their files, and your groups and brains stay on your PC.</p></details>
      </div>
    </div>
  </section>
''', 'pricing')

# ---------- privacy ----------
page('privacy.html', 'Privacy policy · AI Project Hub', 'What AI Project Hub, by VC Innovations Group, keeps about you and why.', f'''
  <section class="legal">
    <div class="wrap">
      <div class="prose">
        <span class="eyebrow">AI Project Hub</span>
        <h1>Privacy policy</h1>
        <p class="meta">Last updated {UPDATED}</p>
        <p>This policy explains what AI Project Hub, a desktop app and website made by VC Innovations Group ("we"), keeps about you and why. AI Project Hub is under development; we'll update this page as it grows.</p>
        <h2>Your account</h2>
        <p>You can sign up with your email and a password, or with Google or GitHub. With email, we keep your name and email; your password is stored only as a one-way hash, never readable. With Google or GitHub, they tell us your <b>email address</b> and your <b>name</b>, and we ask for nothing else: no contacts, files, mail, calendar, or repositories. We never see your Google or GitHub password.</p>
        <p>We use your email address to match you to invitations, since an invitation works only for the email it was sent to, and we show your name and email to the people on your teams.</p>
        <h2>What we keep on our server</h2>
        <ul>
          <li>Your name, email address, and how you sign in (email, Google, or GitHub), and whether you asked for product email.</li>
          <li>Your plan (Pro or Enterprise) and its status. Once paid plans exist: the price, billing dates, and the payment service's reference numbers. Card details are handled by the payment service and never stored by us.</li>
          <li>The PCs you use AI Project Hub on, so a plan can allow a set number: a name, the app version, and when each was last used.</li>
          <li>The teams you make or join, your role on each, and when you joined.</li>
          <li>Invitations: the email invited and when. The invitation code itself is never stored, only a one-way fingerprint of it.</li>
          <li>When your AI Project Hub last checked in, so teammates can see you're online.</li>
        </ul>
        <p>This is kept in a database hosted by Supabase in the United States, encrypted at rest. You can see your own account; teammates see only your name, email, and whether you're online.</p>
        <h2>What stays on your computer</h2>
        <p>Your bots, their runs and reports, your projects and code, your Claude threads, and your Claude account all stay on your computer. Bots run with Claude Code under your own Claude account with Anthropic, which has its own terms and privacy policy. The AI Project Hub app keeps your sign-in on your computer encrypted by Windows.</p>
        <h2>This website</h2>
        <p>When you sign in here, your browser keeps the sign-in in its local storage until you sign out. The site uses no cookies of its own and no analytics or ads.</p>
        <h2>What we don't do</h2>
        <p>We don't sell or share your information, show ads, or track you across apps or websites.</p>
        <h2>Deleting your information</h2>
        <p>You can leave a team or delete a team you own in AI Project Hub at any time. To have your account and everything we keep about you deleted, email us at <a href="mailto:{EMAIL}">{EMAIL}</a> from the address you sign in with. We delete it within 30 days. You can also remove AI Project Hub's access in your Google or GitHub account settings.</p>
        <h2>Changes</h2>
        <p>If this policy changes, we'll update this page and the date above.</p>
        <h2>Contact</h2>
        <p>VC Innovations Group · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
    </div>
  </section>
''', 'privacy')

# ---------- terms ----------
page('terms.html', 'Terms of service · AI Project Hub', 'The terms for using AI Project Hub, by VC Innovations Group.', f'''
  <section class="legal">
    <div class="wrap">
      <div class="prose">
        <span class="eyebrow">AI Project Hub</span>
        <h1>Terms of service</h1>
        <p class="meta">Last updated {UPDATED}</p>
        <p>AI Project Hub is a desktop app and website made by VC Innovations Group. By creating an account or using it, you agree to these terms.</p>
        <h2>Using AI Project Hub</h2>
        <p>AI Project Hub is under development. It is provided as is, without warranties of any kind. You're responsible for the bots you set up, what you let them do, and the projects you run them on. Bots run with Claude Code under your own Claude account, so Anthropic's terms apply to that use too.</p>
        <h2>Your account and teams</h2>
        <p>Keep your account secure, whether you sign in with email, Google, or GitHub. Only invite people you mean to work with, and don't use AI Project Hub to break the law or anyone's rights.</p>
        <h2>Plans</h2>
        <p>AI Project Hub has two plans, Pro and Enterprise, listed on the <a href="/pricing/">pricing page</a>. Before you buy, you see the price, the billing period, and how many devices the plan allows. A sale price applies only to sign-ups by its end date. There is no free trial: if you cancel within {REFUND_DAYS} days of making your account, you get a full refund. After that, you can cancel any time and keep your plan until the end of the period you paid for. Enterprise is priced and agreed with each company. AI Project Hub's price doesn't include Claude: your Claude plan with Anthropic is separate.</p>
        <h2>Limits</h2>
        <p>To the extent the law allows, VC Innovations Group isn't liable for indirect or lost-profit damages from using AI Project Hub. We may change or stop the service, and we may update these terms; the date above shows the latest version.</p>
        <h2>Contact</h2>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
    </div>
  </section>
''', 'terms')

# ---------- account: sign up ----------
page('account/signup/index.html', 'Create your AI Project Hub account', 'Create your AI Project Hub account.', f'''
  <main class="acct">
  <div class="acct-card" data-bm-page="signup">
    <span class="eyebrow">Get started</span>
    <h1>Create your account</h1>
    <p class="acct-sub">One account works in the AI Project Hub app and on this website.</p>
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
      <label class="check"><input type="checkbox" name="marketing_opt_in" /><span>Send me AI Project Hub news and product updates by email. (optional)</span></label>
      <button type="submit" class="btn btn-primary">Create account</button>
    </form>
    <p class="acct-links">Already have an account? <a href="/account/login/">Log in</a></p>
  </div>
  </main>
''')

# ---------- account: log in ----------
page('account/login/index.html', 'Log in to AI Project Hub', 'Log in to your AI Project Hub account.', f'''
  <main class="acct">
  <div class="acct-card" data-bm-page="login">
    <span class="eyebrow">Welcome back</span>
    <h1>Log in</h1>
    <p class="acct-sub">Use the same account as the AI Project Hub app.</p>
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
page('account/reset/index.html', 'Reset your AI Project Hub password', 'Reset the password for your AI Project Hub account.', '''
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
page('account/index.html', 'Your AI Project Hub account', 'Your AI Project Hub account: plan, PCs, and sign-in.', '''
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
      <div class="acct-billing" id="acct-billing" style="display:none">
        <div id="bm-bill-alert" class="alert" role="status" aria-live="polite"></div>
        <p class="acct-sub" id="acct-bill-text"></p>
        <button type="button" class="btn btn-primary" id="bm-buy" style="display:none">Get Pro</button>
        <button type="button" class="btn btn-ghost" id="bm-manage" style="display:none">Manage billing</button>
      </div>
      <h2 class="acct-section">Sign-in</h2>
      <dl class="acct-facts">
        <dt>Signs in with</dt><dd id="acct-provider"></dd>
        <dt>Member since</dt><dd id="acct-since"></dd>
      </dl>
      <div class="note" style="margin-bottom:22px"><b>No free trial.</b> Cancel within 30 days of making your account for a full refund. Payments are handled by Stripe; we never see or keep your card.</div>
      <button type="button" class="btn btn-ghost" id="bm-signout">Sign out</button>
    </div>
  </div>
  </main>
''')
# ---------- pricing matrix for Chris (internal: not linked, not indexed) ----------
page('PricingMatrixForChris/index.html', 'AI Project Hub pricing matrix (draft)', 'Internal draft: AI Project Hub plans and prices next to similar tools.',
     io.open(os.path.join(D, '_pricing-matrix.html'), encoding='utf-8').read(), robots='noindex, nofollow')
print('built')
