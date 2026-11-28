// bm-auth.js: AI Project Hub website accounts, modeled on WhereTo's wt-auth.js. A browser module that talks to the
// AI Project Hub server (Supabase) with the public key; the server's locked tables and row rules protect the data.
// Pages opt in with data-bm-page="signup|login|reset|account". Every page also gets the header account button.
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const cfg = window.BM_SUPABASE || {};
export const supabase = createClient(cfg.url, cfg.key, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, flowType: 'pkce' },
});
const SITE = window.location.origin;

// ---------- helpers ----------
function show(el, type, msg) { if (!el) return; el.className = 'alert show alert-' + type; el.textContent = msg; }
function hide(el) { if (el) el.className = 'alert'; }
function busy(btn, on, label) {
  if (!btn) return;
  btn.disabled = on;
  if (on) { btn.dataset.label = btn.textContent; btn.textContent = label || 'Working...'; }
  else if (btn.dataset.label) btn.textContent = btn.dataset.label;
}
function friendly(error) {
  const m = (error && error.message) || 'Something went wrong. Please try again.';
  if (/already registered/i.test(m)) return 'An account with this email already exists. Try logging in.';
  if (/invalid login/i.test(m)) return 'Email or password is incorrect.';
  if (/email not confirmed/i.test(m)) return 'Please confirm your email first. Check your inbox.';
  if (/rate limit/i.test(m)) return 'Too many tries for now. Wait a few minutes, then try again.';
  return m;
}
// a same-site place to go after signing in (?next=/path), never another site
function nextTarget(fallback) {
  try { const n = new URLSearchParams(location.search).get('next'); if (n && n[0] === '/' && n[1] !== '/') return n; } catch (_e) { /* ignore */ }
  return fallback;
}
const EYE = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1.5 12S5 5 12 5s10.5 7 10.5 7-3.5 7-10.5 7S1.5 12 1.5 12z"/><circle cx="12" cy="12" r="3.2"/></svg>';
const EYE_OFF = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3l18 18"/><path d="M10.6 5.2A10.9 10.9 0 0 1 12 5c7 0 10.5 7 10.5 7a13.2 13.2 0 0 1-3.1 3.9M6.6 6.6C3.7 8.4 1.5 12 1.5 12s3.5 7 10.5 7a10.4 10.4 0 0 0 4.2-.9"/><path d="M9.5 9.9a3.2 3.2 0 0 0 4.6 4.5"/></svg>';
function initPasswordToggles() {
  document.querySelectorAll('.pw-toggle').forEach((btn) => {
    const input = btn.closest('.pw-field')?.querySelector('input'); if (!input) return;
    btn.innerHTML = EYE;
    btn.addEventListener('click', () => {
      const showing = input.type === 'text';
      input.type = showing ? 'password' : 'text';
      btn.innerHTML = showing ? EYE : EYE_OFF;
      btn.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
    });
  });
}

// ---------- Google and GitHub ----------
function initProviders() {
  const alertEl = document.getElementById('bm-alert');
  document.querySelectorAll('[data-provider]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      hide(alertEl);
      const terms = document.querySelector('input[name="terms"]');
      if (terms && !terms.checked) { show(alertEl, 'error', 'Please accept the Terms to continue.'); return; }
      busy(btn, true, 'Opening ' + (btn.dataset.provider === 'github' ? 'GitHub' : 'Google') + '...');
      const { error } = await supabase.auth.signInWithOAuth({
        provider: btn.dataset.provider,
        options: { redirectTo: SITE + nextTarget('/account/') },
      });
      if (error) { busy(btn, false); show(alertEl, 'error', friendly(error)); }
    });
  });
}

// ---------- sign up ----------
function initSignup() {
  const form = document.getElementById('bm-signup-form'); if (!form) return;
  const alertEl = document.getElementById('bm-alert');
  const btn = form.querySelector('button[type="submit"]');
  supabase.auth.getSession().then(({ data }) => { if (data.session) location.href = '/account/'; });
  form.addEventListener('submit', async (e) => {
    e.preventDefault(); hide(alertEl);
    const fd = new FormData(form);
    const first = String(fd.get('first_name') || '').trim(), last = String(fd.get('last_name') || '').trim();
    const email = String(fd.get('email') || '').trim(), password = String(fd.get('password') || '');
    if (fd.get('terms') !== 'on') { show(alertEl, 'error', 'Please accept the Terms to continue.'); return; }
    if (password.length < 8) { show(alertEl, 'error', 'Password must be at least 8 characters.'); return; }
    busy(btn, true, 'Creating your account...');
    const { data, error } = await supabase.auth.signUp({
      email, password,
      options: {
        emailRedirectTo: SITE + '/account/login/',
        data: { first_name: first, last_name: last, full_name: (first + ' ' + last).trim(), signup_source: 'web', marketing_opt_in: fd.get('marketing_opt_in') === 'on', terms_accepted: true },
      },
    });
    busy(btn, false);
    if (error) { show(alertEl, 'error', friendly(error)); return; }
    if (data.session) { location.href = '/account/'; return; }
    form.style.display = 'none';
    document.querySelectorAll('.oauth, .or-line').forEach((el) => { el.style.display = 'none'; });
    show(alertEl, 'success', 'Account created! Check your email to confirm your address, then log in.');
  });
}

// ---------- log in ----------
function initLogin() {
  const form = document.getElementById('bm-login-form'); if (!form) return;
  const alertEl = document.getElementById('bm-alert');
  const btn = form.querySelector('button[type="submit"]');
  supabase.auth.getSession().then(({ data }) => { if (data.session) location.href = nextTarget('/account/'); });
  form.addEventListener('submit', async (e) => {
    e.preventDefault(); hide(alertEl);
    const fd = new FormData(form);
    busy(btn, true, 'Signing in...');
    const { error } = await supabase.auth.signInWithPassword({ email: String(fd.get('email') || '').trim(), password: String(fd.get('password') || '') });
    busy(btn, false);
    if (error) { show(alertEl, 'error', friendly(error)); return; }
    location.href = nextTarget('/account/');
  });
}

// ---------- password reset (ask for a link, then set a new password from it) ----------
function initReset() {
  const reqForm = document.getElementById('bm-reset-request-form');
  const setForm = document.getElementById('bm-reset-set-form');
  const alertEl = document.getElementById('bm-alert');
  supabase.auth.onAuthStateChange((event) => {
    if (event === 'PASSWORD_RECOVERY') {
      if (reqForm) reqForm.style.display = 'none';
      if (setForm) setForm.style.display = 'block';
      show(alertEl, 'info', 'Enter a new password for your account.');
    }
  });
  if (reqForm) {
    const btn = reqForm.querySelector('button[type="submit"]');
    reqForm.addEventListener('submit', async (e) => {
      e.preventDefault(); hide(alertEl);
      const email = String(new FormData(reqForm).get('email') || '').trim();
      busy(btn, true, 'Sending...');
      await supabase.auth.resetPasswordForEmail(email, { redirectTo: SITE + '/account/reset/' });
      busy(btn, false);
      // the same answer either way, so nobody can tell which emails have accounts
      show(alertEl, 'success', 'If an account exists for that email, a password-reset link is on its way.');
      reqForm.reset();
    });
  }
  if (setForm) {
    const btn = setForm.querySelector('button[type="submit"]');
    setForm.addEventListener('submit', async (e) => {
      e.preventDefault(); hide(alertEl);
      const pw = String(new FormData(setForm).get('password') || '');
      if (pw.length < 8) { show(alertEl, 'error', 'Password must be at least 8 characters.'); return; }
      busy(btn, true, 'Updating...');
      const { error } = await supabase.auth.updateUser({ password: pw });
      busy(btn, false);
      if (error) { show(alertEl, 'error', friendly(error)); return; }
      show(alertEl, 'success', 'Password updated. Taking you to your account...');
      setTimeout(() => { location.href = '/account/'; }, 1200);
    });
  }
}

// ---------- my account ----------
// The plan comes from the server's bm_entitlement (supabase/plans.sql): the plan in effect (a paid plan, an
// Enterprise seat, or Free), its end date, the 30 days to cancel for a full refund (from when the account was made;
// there is no trial), and the PCs in use, which can be taken off here.
const STATUS = { active: 'Active', trialing: 'Trial', past_due: 'Payment due', canceled: 'Canceled', expired: 'Expired', paused: 'Paused' };
const fmtDate = (iso) => (iso ? new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : '');
function setText(id, v) { const el = document.getElementById(id); if (el) el.textContent = v; }
function showRow(id, on) { [id + '-row', id].forEach((x) => { const el = document.getElementById(x); if (el) el.style.display = on ? '' : 'none'; }); }
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
function planLine(e) {
  if (e.plan === 'enterprise' && e.source === 'seat') return `Enterprise${e.org && e.org.name ? ', through ' + e.org.name : ''}`;
  return e.name || 'Free';
}
function drawDevices(e) {
  const d = e.devices || { used: 0, max: 1, list: [] };
  setText('acct-devices', `${d.used} of ${d.max} in use`);
  const box = document.getElementById('acct-pcs'); if (!box) return;
  box.innerHTML = (d.list || []).map((x) => `<li><span><b>${esc(x.name || 'A PC')}</b><small>${esc([x.version && 'AI Project Hub ' + x.version, x.last && 'last seen ' + fmtDate(x.last)].filter(Boolean).join(', '))}</small></span><button type="button" class="btn btn-ghost btn-small" data-pc="${esc(x.id)}">Remove</button></li>`).join('')
    || '<li class="none">No PCs yet. Sign in to the AI Project Hub app and it appears here.</li>';
}
// ---------- billing (Stripe, through the server's billing-checkout and billing-portal functions) ----------
// Prices: the site's _build.py and supabase/functions/_shared/billing.ts in the app repo say the same.
const HOLIDAY_ENDS = Date.parse('2027-02-01T06:00:00Z'); // the end of January 31 in Texas
async function callBilling(name) {
  const { data, error } = await supabase.functions.invoke(name, { body: {} });
  if (!error && data && data.url) return { url: data.url };
  let msg = (data && data.error) || '';
  if (!msg && error && error.context && typeof error.context.json === 'function') {
    try { msg = (await error.context.json()).error || ''; } catch (_e) { /* not JSON */ }
  }
  return { error: msg || "Couldn't reach billing. Try again in a minute." };
}
function drawBilling(ent, acct) {
  const box = document.getElementById('acct-billing'); if (!box) return;
  const buy = document.getElementById('bm-buy'); const manage = document.getElementById('bm-manage');
  const free = !ent || ent.plan === 'free';
  const stripe = acct && acct.payment_provider === 'stripe' && ent && ent.plan === 'pro';
  const holiday = Date.now() < HOLIDAY_ENDS;
  if (free) {
    setText('acct-bill-text', holiday
      ? 'Get Pro for $29 for your first year (holiday price through January 31), then $39 a year. Every tool, on your main PC and a remote one.'
      : 'Get Pro for $39 a year. Every tool, on your main PC and a remote one.');
  } else if (stripe) {
    setText('acct-bill-text', 'Cancel, change your card, or get receipts.');
  } else {
    setText('acct-bill-text', '');
  }
  buy.style.display = free ? '' : 'none';
  manage.style.display = stripe ? '' : 'none';
  box.style.display = free || stripe ? '' : 'none';
}
async function goBilling(name, btn, label) {
  const alertEl = document.getElementById('bm-bill-alert');
  hide(alertEl); busy(btn, true, label);
  const r = await callBilling(name);
  if (r.url) { location.href = r.url; return; }
  busy(btn, false); show(alertEl, 'error', r.error);
}

async function initAccount() {
  const root = document.getElementById('bm-account'); if (!root) return;
  const { data: sess } = await supabase.auth.getSession();
  if (!sess.session) { location.href = '/account/login/?next=' + encodeURIComponent('/account/' + location.search); return; }
  const user = sess.session.user;
  const prov = user.app_metadata?.provider || 'email';
  const m = user.user_metadata || {};
  const readAcct = async () => (await supabase.from('bm_users')
    .select('full_name, plan_status, created_at, payment_provider').eq('id', user.id).maybeSingle()).data;
  const acct = await readAcct();
  const { data: ent, error } = await supabase.rpc('bm_entitlement', { p_device: '' });
  setText('acct-name', (acct && acct.full_name) || m.full_name || m.name || m.user_name || user.email);
  setText('acct-email', user.email || '');
  setText('acct-provider', prov === 'github' ? 'GitHub' : prov === 'google' ? 'Google' : 'Email and password');
  setText('acct-since', fmtDate((acct && acct.created_at) || user.created_at));
  drawPlan(ent, acct, error);
  const q = new URLSearchParams(location.search);
  const buyBtn = document.getElementById('bm-buy');
  buyBtn?.addEventListener('click', () => goBilling('billing-checkout', buyBtn, 'Opening checkout...'));
  const manageBtn = document.getElementById('bm-manage');
  manageBtn?.addEventListener('click', () => goBilling('billing-portal', manageBtn, 'Opening billing...'));
  if (q.get('buy') === 'pro' && ent && ent.plan === 'free') {
    history.replaceState(null, '', '/account/');
    goBilling('billing-checkout', buyBtn, 'Opening checkout...');
  }
  document.getElementById('acct-pcs')?.addEventListener('click', async (ev) => {
    const b = ev.target.closest('[data-pc]'); if (!b) return;
    busy(b, true, 'Removing...');
    const { error: e2 } = await supabase.rpc('bm_device_remove', { p_id: b.dataset.pc });
    if (e2) { busy(b, false); return; }
    const { data: again } = await supabase.rpc('bm_entitlement', { p_device: '' });
    if (again) drawDevices(again);
  });
  document.getElementById('bm-signout')?.addEventListener('click', async () => { await supabase.auth.signOut(); location.href = '/'; });
  root.style.display = '';
  document.getElementById('bm-gate')?.remove();
  if (q.get('checkout') === 'done') {
    history.replaceState(null, '', '/account/');
    if (ent && ent.plan !== 'free') { showPaid(); return; }
    confirmPaid(readAcct);
  }
}

// Back from Stripe: the page shows at once, and the plan arrives when Stripe tells the server (usually a few
// seconds). A spinner says so while it looks again, every 2 seconds for up to a minute.
function showPaid() {
  show(document.getElementById('bm-bill-alert'), 'success', "Thanks! You're on Pro. Every tool is yours on your main PC and a remote one.");
  document.getElementById('acct-billing').style.display = '';
}
async function confirmPaid(readAcct) {
  const box = document.getElementById('acct-billing');
  const wait = document.createElement('div');
  wait.className = 'confirming';
  wait.innerHTML = '<span class="spin" aria-hidden="true"></span><span><b>Confirming your subscription...</b><small>Your payment went through. Stripe is telling our server; this usually takes a few seconds.</small></span>';
  box.prepend(wait);
  box.style.display = '';
  ['bm-buy', 'bm-manage'].forEach((id) => { const b = document.getElementById(id); if (b) b.style.display = 'none'; });
  setText('acct-bill-text', '');
  for (let i = 0; i < 30; i++) {
    await new Promise((r) => setTimeout(r, 2000));
    const { data: e2 } = await supabase.rpc('bm_entitlement', { p_device: '' });
    if (e2 && e2.plan !== 'free') { wait.remove(); drawPlan(e2, await readAcct()); showPaid(); return; }
  }
  wait.remove();
  show(document.getElementById('bm-bill-alert'), 'info', "Your payment went through, but your plan hasn't shown up yet. Refresh this page in a minute. If it still says Free, email us and we'll sort it out.");
}

function drawPlan(ent, acct, error) {
  if (error || !ent) {
    setText('acct-plan', 'Free'); setText('acct-status', "Couldn't load your plan. Refresh to try again.");
    showRow('acct-renew', false); showRow('acct-refund', false); setText('acct-devices', '');
  } else {
    setText('acct-plan', planLine(ent));
    setText('acct-status', ent.source === 'seat' ? 'Seat from your company' : ent.plan === 'free' ? 'Active' : (acct && STATUS[acct.plan_status]) || 'Active');
    const when = ent.canceling ? ['Ends', ent.ends] : ent.renews ? ['Renews', ent.renews] : ['', ''];
    setText('acct-renew-row', when[0]); setText('acct-renew', fmtDate(when[1])); showRow('acct-renew', !!when[1]);
    const left = ent.refund_until ? Math.max(0, Math.ceil((Date.parse(ent.refund_until) - Date.now()) / 864e5)) : 0;
    setText('acct-refund', left ? `If you cancel by ${fmtDate(ent.refund_until)} (${left} day${left === 1 ? '' : 's'} left)` : `Ended ${fmtDate(ent.refund_until)}`);
    showRow('acct-refund', !!ent.refund_until);
    drawDevices(ent);
  }
  drawBilling(error ? null : ent, acct);
}

// ---------- the header's account button, on every page ----------
async function initHeader() {
  const { data } = await supabase.auth.getSession();
  document.querySelectorAll('[data-bm-account]').forEach((a) => {
    if (data.session) { a.textContent = 'My account'; a.setAttribute('href', '/account/'); }
  });
  document.querySelectorAll('[data-bm-signup]').forEach((a) => { if (data.session) a.style.display = 'none'; });
}

function boot() {
  initPasswordToggles();
  initHeader();
  initProviders();
  const page = document.querySelector('[data-bm-page]')?.getAttribute('data-bm-page');
  if (page === 'signup') initSignup();
  else if (page === 'login') initLogin();
  else if (page === 'reset') initReset();
  else if (page === 'account') initAccount();
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
