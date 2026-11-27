# Writes the site's pages with one shared header and footer:  python _build.py
# (GitHub Pages skips files starting with "_", so this script isn't published.)
import io, os
D = os.path.dirname(os.path.abspath(__file__))
EMAIL = 'vfratto@vcinnovationsgroup.com'
UPDATED = 'November 27, 2026'

GOOGLE = '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.6 5.4 2.6 13.2l7.9 6.2C12.4 13.6 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.1 24.6c0-1.6-.1-3.1-.4-4.6H24v8.7h12.4c-.5 2.9-2.2 5.3-4.6 6.9l7.4 5.8c4.3-4 6.9-9.9 6.9-16.8z"/><path fill="#FBBC05" d="M10.5 28.6c-.5-1.4-.8-2.9-.8-4.6s.3-3.2.8-4.6l-7.9-6.2C.9 16.6 0 20.2 0 24s.9 7.4 2.6 10.8l7.9-6.2z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.4-5.8c-2.1 1.4-4.8 2.3-8.5 2.3-6.3 0-11.6-4.1-13.5-9.9l-7.9 6.2C6.6 42.6 14.6 48 24 48z"/></svg>'
GITHUB = '<svg viewBox="0 0 16 16" aria-hidden="true"><path fill="#313131" d="M8 0C3.6 0 0 3.6 0 8c0 3.5 2.3 6.5 5.5 7.6.4.1.5-.2.5-.4v-1.4c-2.2.5-2.7-1-2.7-1-.4-.9-.9-1.2-.9-1.2-.7-.5.1-.5.1-.5.8.1 1.2.8 1.2.8.7 1.2 1.9.9 2.3.7.1-.5.3-.9.5-1.1-1.8-.2-3.6-.9-3.6-3.9 0-.9.3-1.6.8-2.1-.1-.2-.4-1 .1-2.1 0 0 .7-.2 2.2.8.6-.2 1.3-.3 2-.3s1.4.1 2 .3c1.5-1 2.2-.8 2.2-.8.4 1.1.2 1.9.1 2.1.5.6.8 1.3.8 2.1 0 3.1-1.9 3.7-3.6 3.9.3.3.6.8.6 1.5v2.2c0 .2.1.5.6.4C13.7 14.5 16 11.5 16 8c0-4.4-3.6-8-8-8z"/></svg>'


def head(title, desc, robots=''):
    robots = f'\n  <meta name="robots" content="{robots}" />' if robots else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />{robots}
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:type" content="website" />
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
    links = [('/', 'Bot Manager', 'home'), ('/privacy.html', 'Privacy', 'privacy'), ('/terms.html', 'Terms', 'terms')]
    nav = ''.join(f'\n        <a href="{h}"{" class=\"on\"" if k == on else ""}>{l}</a>' for h, l, k in links)
    return f'''  <header>
    <div class="wrap nav">
      <a class="brand" href="https://vcinnovationsgroup.com/">
        <span class="mark">VC</span>
        <span class="name">VC Innovations Group</span>
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
        <a class="brand" href="https://vcinnovationsgroup.com/">
          <span class="mark">VC</span>
          <span class="name">VC Innovations Group</span>
        </a>
        <div class="foot-links">
          <div class="foot-col">
            <h4>Bot Manager</h4>
            <a href="/">Overview</a>
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
        <span>Bot Manager · under development</span>
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


# ---------- home ----------
page('index.html', 'Bot Manager · VC Innovations Group', 'Bot Manager is a desktop app to create, schedule, run, and review AI bots for your projects, on your own Claude plan.', f'''
  <section class="hero">
    <div class="wrap">
      <span class="eyebrow">A VC Innovations Group product</span><span class="pill"><span class="dot"></span>Under development</span>
      <h1>Bot Manager: <span class="italic">AI bots</span> that work while you do</h1>
      <p class="lede">A desktop app for Windows to create, schedule, run, and review AI bots. Each bot does one job, like reviewing code, researching a topic, or watching for secrets, with its own rules and schedule, for one project or many. Bot Manager is under development and in early use within our team.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/account/signup/" data-bm-signup>Create your account</a>
        <a class="btn btn-ghost" href="/account/login/" data-bm-account>Log in</a>
      </div>
    </div>
  </section>

  <section class="block" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head">
        <span class="eyebrow">How it works</span>
        <h2>Your bots, your PC, <span class="italic">your plan</span></h2>
      </div>
      <div class="cards">
        <div class="card"><div class="num">01</div><h3>Runs on your PC</h3><p>Bots run with Claude Code on your own computer and your own Claude plan. Your code and your bots' work stay on your PC.</p></div>
        <div class="card"><div class="num">02</div><h3>Safe by default</h3><p>Bots are read-only unless you give them more. They never commit, push, deploy, or publish.</p></div>
        <div class="card"><div class="num">03</div><h3>Built for teams</h3><p>One account, with email, Google, or GitHub, works in the app and here. An owner invites people by email with a one-time code.</p></div>
      </div>
    </div>
  </section>

  <section class="block" style="padding-top:0">
    <div class="wrap">
      <div class="note"><b>Your account.</b> Sign up with email, Google, or GitHub. Bot Manager uses it to know who you are on a team, and to keep your plan and your PCs. The <a class="text-link" href="/privacy.html">privacy policy</a> says what is kept and how to have it deleted.</div>
    </div>
  </section>
''', 'home')

# ---------- privacy ----------
page('privacy.html', 'Privacy policy · Bot Manager', 'What Bot Manager, by VC Innovations Group, keeps about you and why.', f'''
  <section class="legal">
    <div class="wrap">
      <div class="prose">
        <span class="eyebrow">Bot Manager</span>
        <h1>Privacy policy</h1>
        <p class="meta">Last updated {UPDATED}</p>
        <p>This policy explains what Bot Manager, a desktop app and website made by VC Innovations Group ("we"), keeps about you and why. Bot Manager is under development; we'll update this page as it grows.</p>
        <h2>Your account</h2>
        <p>You can sign up with your email and a password, or with Google or GitHub. With email, we keep your name and email; your password is stored only as a one-way hash, never readable. With Google or GitHub, they tell us your <b>email address</b> and your <b>name</b>, and we ask for nothing else: no contacts, files, mail, calendar, or repositories. We never see your Google or GitHub password.</p>
        <p>We use your email address to match you to invitations, since an invitation works only for the email it was sent to, and we show your name and email to the people on your teams.</p>
        <h2>What we keep on our server</h2>
        <ul>
          <li>Your name, email address, and how you sign in (email, Google, or GitHub), and whether you asked for product email.</li>
          <li>Your plan (Free, Pro, or Enterprise) and its status. Once paid plans exist: the price, billing dates, and the payment service's reference numbers. Card details are handled by the payment service and never stored by us.</li>
          <li>The PCs you use Bot Manager on, so a plan can allow a set number: a name, the app version, and when each was last used.</li>
          <li>The teams you make or join, your role on each, and when you joined.</li>
          <li>Invitations: the email invited and when. The invitation code itself is never stored, only a one-way fingerprint of it.</li>
          <li>When your Bot Manager last checked in, so teammates can see you're online.</li>
        </ul>
        <p>This is kept in a database hosted by Supabase in the United States, encrypted at rest. You can see your own account; teammates see only your name, email, and whether you're online.</p>
        <h2>What stays on your computer</h2>
        <p>Your bots, their runs and reports, your projects and code, your Claude threads, and your Claude account all stay on your computer. Bots run with Claude Code under your own Claude account with Anthropic, which has its own terms and privacy policy. The Bot Manager app keeps your sign-in on your computer encrypted by Windows.</p>
        <h2>This website</h2>
        <p>When you sign in here, your browser keeps the sign-in in its local storage until you sign out. The site uses no cookies of its own and no analytics or ads.</p>
        <h2>What we don't do</h2>
        <p>We don't sell or share your information, show ads, or track you across apps or websites.</p>
        <h2>Deleting your information</h2>
        <p>You can leave a team or delete a team you own in Bot Manager at any time. To have your account and everything we keep about you deleted, email us at <a href="mailto:{EMAIL}">{EMAIL}</a> from the address you sign in with. We delete it within 30 days. You can also remove Bot Manager's access in your Google or GitHub account settings.</p>
        <h2>Changes</h2>
        <p>If this policy changes, we'll update this page and the date above.</p>
        <h2>Contact</h2>
        <p>VC Innovations Group · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
    </div>
  </section>
''', 'privacy')

# ---------- terms ----------
page('terms.html', 'Terms of service · Bot Manager', 'The terms for using Bot Manager, by VC Innovations Group.', f'''
  <section class="legal">
    <div class="wrap">
      <div class="prose">
        <span class="eyebrow">Bot Manager</span>
        <h1>Terms of service</h1>
        <p class="meta">Last updated {UPDATED}</p>
        <p>Bot Manager is a desktop app and website made by VC Innovations Group. By creating an account or using it, you agree to these terms.</p>
        <h2>Using Bot Manager</h2>
        <p>Bot Manager is under development. It is provided as is, without warranties of any kind. You're responsible for the bots you set up, what you let them do, and the projects you run them on. Bots run with Claude Code under your own Claude account, so Anthropic's terms apply to that use too.</p>
        <h2>Your account and teams</h2>
        <p>Keep your account secure, whether you sign in with email, Google, or GitHub. Only invite people you mean to work with, and don't use Bot Manager to break the law or anyone's rights.</p>
        <h2>Plans</h2>
        <p>Bot Manager is free while it is under development. If paid plans come, their price, billing period, and the number of PCs each allows will be shown before you buy, and you can cancel before the next billing date.</p>
        <h2>Limits</h2>
        <p>To the extent the law allows, VC Innovations Group isn't liable for indirect or lost-profit damages from using Bot Manager. We may change or stop the service, and we may update these terms; the date above shows the latest version.</p>
        <h2>Contact</h2>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
    </div>
  </section>
''', 'terms')

# ---------- account: sign up ----------
page('account/signup/index.html', 'Create your Bot Manager account', 'Create a free Bot Manager account.', f'''
  <main class="acct">
  <div class="acct-card" data-bm-page="signup">
    <span class="eyebrow">Get started</span>
    <h1>Create your account</h1>
    <p class="acct-sub">One free account works in the Bot Manager app and on this website.</p>
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
      <label class="check"><input type="checkbox" name="marketing_opt_in" /><span>Send me Bot Manager news and product updates by email. (optional)</span></label>
      <button type="submit" class="btn btn-primary">Create account</button>
    </form>
    <p class="acct-links">Already have an account? <a href="/account/login/">Log in</a></p>
  </div>
  </main>
''')

# ---------- account: log in ----------
page('account/login/index.html', 'Log in to Bot Manager', 'Log in to your Bot Manager account.', f'''
  <main class="acct">
  <div class="acct-card" data-bm-page="login">
    <span class="eyebrow">Welcome back</span>
    <h1>Log in</h1>
    <p class="acct-sub">Use the same account as the Bot Manager app.</p>
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
page('account/reset/index.html', 'Reset your Bot Manager password', 'Reset the password for your Bot Manager account.', '''
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
page('account/index.html', 'Your Bot Manager account', 'Your Bot Manager account: plan, PCs, and sign-in.', '''
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
        <dt>PCs</dt><dd id="acct-devices"></dd>
      </dl>
      <h2 class="acct-section">Sign-in</h2>
      <dl class="acct-facts">
        <dt>Signs in with</dt><dd id="acct-provider"></dd>
        <dt>Member since</dt><dd id="acct-since"></dd>
      </dl>
      <div class="note" style="margin-bottom:22px"><b>Bot Manager is under development.</b> Every account is on the Free plan for now. Paid plans and the PC limit come later.</div>
      <button type="button" class="btn btn-ghost" id="bm-signout">Sign out</button>
    </div>
  </div>
  </main>
''')
# ---------- pricing matrix for Chris (internal: not linked, not indexed) ----------
page('PricingMatrixForChris/index.html', 'Bot Manager pricing matrix (draft)', 'Internal draft: Bot Manager plans and prices next to similar tools.',
     io.open(os.path.join(D, '_pricing-matrix.html'), encoding='utf-8').read(), robots='noindex, nofollow')
print('built')
