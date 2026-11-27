// bm-auth.js: Bot Manager website accounts, modeled on WhereTo's wt-auth.js. A browser module that talks to the
// Bot Manager server (Supabase) with the public key; the server's locked tables and row rules protect the data.
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
const PLAN = { free: 'Free', pro: 'Pro', enterprise: 'Enterprise' };
const STATUS = { active: 'Active', trialing: 'Trial', past_due: 'Payment due', canceled: 'Canceled', expired: 'Expired', paused: 'Paused' };
const fmtDate = (iso) => (iso ? new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : '');
function setText(id, v) { const el = document.getElementById(id); if (el) el.textContent = v; }
async function initAccount() {
  const root = document.getElementById('bm-account'); if (!root) return;
  const { data: sess } = await supabase.auth.getSession();
  if (!sess.session) { location.href = '/account/login/?next=/account/'; return; }
  const user = sess.session.user;
  const prov = user.app_metadata?.provider || 'email';
  const m = user.user_metadata || {};
  const { data: acct } = await supabase.from('bm_users')
    .select('full_name, plan, plan_status, max_devices, expires_at, next_due_at, created_at').eq('id', user.id).maybeSingle();
  const { count } = await supabase.from('bm_devices').select('id', { count: 'exact', head: true }).is('removed_at', null);
  setText('acct-name', (acct && acct.full_name) || m.full_name || m.name || m.user_name || user.email);
  setText('acct-email', user.email || '');
  setText('acct-provider', prov === 'github' ? 'GitHub' : prov === 'google' ? 'Google' : 'Email and password');
  setText('acct-plan', acct ? PLAN[acct.plan] || acct.plan : 'Free');
  setText('acct-status', acct ? STATUS[acct.plan_status] || acct.plan_status : 'Active');
  setText('acct-devices', `${count || 0} of ${(acct && acct.max_devices) || 2} in use`);
  setText('acct-since', fmtDate((acct && acct.created_at) || user.created_at));
  const renew = acct && (acct.next_due_at || acct.expires_at);
  ['acct-renew-row', 'acct-renew'].forEach((id) => { const el = document.getElementById(id); if (el) el.style.display = renew ? '' : 'none'; });
  setText('acct-renew', fmtDate(renew));
  document.getElementById('bm-signout')?.addEventListener('click', async () => { await supabase.auth.signOut(); location.href = '/'; });
  root.style.display = '';
  document.getElementById('bm-gate')?.remove();
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
