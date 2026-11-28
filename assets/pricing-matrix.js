// The pricing matrix for Chris: every input is a number in S; the page redraws from S on each change, and the URL's
// #hash carries S so "Copy a link" sends someone exactly these numbers. Nothing is sent anywhere.
(function () {
  'use strict';
  const PRESETS = {
    first: { proYear: 10, proMonth: 0, founding: 10, extraPc: 0, seatYear: 7, seatYear25: 7, minSeats: 5 },
    suggested: { proYear: 48, proMonth: 6, founding: 29, extraPc: 10, seatYear: 72, seatYear25: 60, minSeats: 5 },
    lower: { proYear: 36, proMonth: 4, founding: 19, extraPc: 8, seatYear: 48, seatYear25: 40, minSeats: 5 },
  };
  const DEFAULTS = Object.assign({}, PRESETS.suggested, {
    proUsers: 1000, foundingPct: 30, monthlyPct: 20, extraPcPct: 5, companies: 20, seats: 10,
    paddlePct: 5, paddleFixed: 0.5, paddleSmall: 1,
    stripePct: 2.9, stripeFixed: 0.3, billingPct: 0.7, taxPct: 0.5, mpPct: 3.5, filingCost: 1200,
    intlPct: 35, fxPct: 20,
  });

  // One person, per year (their yearly price where they have one, else 12 months). ai = AI usage included.
  const PERSON = [
    { name: 'Raycast Pro', price: 96, ai: false, note: '$8/mo billed yearly. Desktop command bar with AI.' },
    { name: 'GitHub Copilot Pro', price: 120, ai: true, note: '$10/mo. Coding agent and review; AI included.' },
    { name: 'Warp Build', price: 216, ai: true, note: '$18/mo billed yearly, $20 of AI a month included. Terminal with agents.' },
    { name: 'Relevance AI Pro', price: 228, ai: true, note: '$19/mo billed yearly, plus credits. Agent builder.' },
    { name: 'Cursor Pro', price: 240, ai: true, note: '$20/mo. AI editor, cloud agents.' },
    { name: 'Devin Desktop Pro', price: 240, ai: true, note: '$20/mo (formerly Windsurf). Editor and agents.' },
    { name: 'n8n Starter', price: 240, ai: false, note: 'About $20/mo billed yearly. Scheduled workflows and agents.' },
    { name: 'Zapier Professional', price: 240, ai: false, note: '$19.99/mo billed yearly. Automations, agents use tasks.' },
    { name: 'CodeRabbit', price: 288, ai: true, note: 'About $24 per developer per month billed yearly. Code-review bot.' },
    { name: 'Conductor Pro', price: 600, ai: false, note: '$50/mo. Runs many Claude Code agents side by side (Mac). The closest match.' },
    { name: 'Lindy Plus', price: 600, ai: true, note: '$49.99/mo, 7-day trial, no free tier. Agent builder.' },
  ];
  // One team seat, per year
  const SEAT = [
    { name: 'Raycast Teams', price: 144, ai: false, note: '$12 per user per month billed yearly.' },
    { name: 'GitHub Copilot Business', price: 228, ai: true, note: '$19 per user per month.' },
    { name: 'CodeRabbit', price: 288, ai: true, note: 'About $24 per developer per month billed yearly.' },
    { name: 'Cursor Teams', price: 384, ai: true, note: '$32 per seat per month billed yearly (Standard seat).' },
    { name: 'Devin Desktop Teams', price: 480, ai: true, note: '$40 per seat per month, $80 a month at least.' },
    { name: 'Warp Business', price: 540, ai: true, note: '$45 per user per month billed yearly.' },
    { name: 'Conductor Teams', price: 720, ai: false, note: '$60 per user per month.' },
  ];

  const S = Object.assign({}, DEFAULTS);
  const $ = (s) => document.querySelector(s);
  const num = (v) => (Number.isFinite(+v) ? +v : 0);
  const money = (n, cents) => (n < 0 ? '-' : '') + '$' + Math.abs(n).toLocaleString('en-US', { minimumFractionDigits: cents ? 2 : 0, maximumFractionDigits: cents ? 2 : 0 });
  const pct = (n) => (Math.round(n * 10) / 10).toLocaleString('en-US') + '%';
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  // ---------- the state and the URL ----------
  function readHash() {
    const p = new URLSearchParams(location.hash.slice(1));
    for (const k of Object.keys(DEFAULTS)) if (p.has(k) && p.get(k) !== '' && Number.isFinite(+p.get(k))) S[k] = +p.get(k);
  }
  function writeHash() {
    const p = new URLSearchParams();
    for (const k of Object.keys(DEFAULTS)) if (S[k] !== DEFAULTS[k]) p.set(k, String(S[k]));
    const h = p.toString();
    history.replaceState(null, '', h ? '#' + h : location.pathname);
  }
  function fillInputs() {
    document.querySelectorAll('[data-k]').forEach((el) => {
      const k = el.dataset.k;
      if (el.type === 'checkbox') el.checked = !!S[k]; else el.value = S[k];
    });
    document.querySelectorAll('[data-preset]').forEach((b) => {
      const pr = PRESETS[b.dataset.preset];
      b.classList.toggle('on', Object.keys(pr).every((k) => S[k] === pr[k]));
    });
  }

  // ---------- fees ----------
  // Fees on one payment of `a` dollars, for each way of taking payment.
  function feePaddle(a) {
    if (a <= 0) return 0;
    if (S.paddleSmall && a < 10) return a * 0.10;
    return a * S.paddlePct / 100 + S.paddleFixed;
  }
  function stripeCard(a) { return a * (S.stripePct + S.intlPct / 100 * 1.5 + S.fxPct / 100 * 1) / 100 + S.stripeFixed; }
  function feeStripe(a) { return a <= 0 ? 0 : stripeCard(a) + a * (S.billingPct + S.taxPct) / 100; }
  function feeManaged(a) { return a <= 0 ? 0 : stripeCard(a) + a * (S.billingPct + S.mpPct) / 100; }
  const WAYS = [
    { key: 'paddle', name: 'Paddle', fee: feePaddle, fixedYear: () => 0 },
    { key: 'stripe', name: 'Stripe (we file taxes)', fee: feeStripe, fixedYear: () => S.filingCost },
    { key: 'managed', name: 'Stripe Managed Payments', fee: feeManaged, fixedYear: () => 0 },
  ];

  // the fee for one row's payment: an add-on pays only what it adds to the payment it rides on
  const rowFee = (w, r) => (r.on ? w.fee(r.on + r.amount) - w.fee(r.on) : w.fee(r.amount));

  // The year's payments at the numbers on the page: [{ label, count, amount }]
  function payments() {
    const n = Math.max(0, S.proUsers);
    const monthly = S.proMonth > 0 ? n * S.monthlyPct / 100 : 0;
    const yearly = n - monthly;
    const founding = yearly * S.foundingPct / 100;
    const regular = yearly - founding;
    const extras = n * S.extraPcPct / 100;
    const seats = Math.max(S.minSeats, S.seats);
    const seatPrice = seats >= 25 ? S.seatYear25 : S.seatYear;
    return [
      { label: 'Pro, yearly', count: regular, amount: S.proYear },
      { label: 'Pro, founding price', count: founding, amount: S.founding },
      // an extra PC rides on the person's yearly payment: its fee is only what it adds to that payment's fee
      { label: 'Extra PCs (added to a yearly payment)', count: extras, amount: S.extraPc, on: S.proYear },
      { label: 'Pro, month to month (12 payments each)', count: monthly * 12, amount: S.proMonth },
      { label: `Enterprise (${seats} seats each)`, count: Math.max(0, S.companies), amount: seats * seatPrice },
    ].filter((r) => r.count > 0 && r.amount > 0);
  }

  // ---------- drawing ----------
  function tiles() {
    const cheapestPerson = Math.min(...PERSON.map((r) => r.price));
    const cheapestSeat = Math.min(...SEAT.map((r) => r.price));
    const ourSeat = S.seatYear;
    const pays = payments();
    const gross = pays.reduce((s, r) => s + r.count * r.amount, 0);
    const net = gross - pays.reduce((s, r) => s + r.count * rowFee(WAYS[0], r), 0);
    const below = (us, them) => (us <= 0 ? '100%' : us >= them ? 'Not below' : pct((1 - us / them) * 100));
    const t = [
      { big: money(S.proYear), small: `Pro per year (${money(S.proYear / 12, true)} a month)` },
      { big: below(S.proYear, cheapestPerson), small: `below the cheapest similar tool (Raycast Pro, ${money(cheapestPerson)}/yr)` },
      { big: below(ourSeat, cheapestSeat), small: `per seat below the cheapest team plan (Raycast Teams, ${money(cheapestSeat)}/yr)` },
      { big: money(net), small: `a year after Paddle's fees, at the numbers in section 1` },
    ];
    $('#pm-tiles').innerHTML = t.map((x) => `<div class="pm-tile"><div class="pm-big">${esc(x.big)}</div><div class="pm-small">${esc(x.small)}</div></div>`).join('');
  }

  // a horizontal bar chart, sorted by price; ours in the accent, the others in a quiet gray
  function chart(el, rows) {
    const W = 520, row = 30, gap = 2, left = 168, right = 84, top = 6;
    const max = Math.max(...rows.map((r) => r.price), 1);
    const H = top + rows.length * row + 22;
    const x = (v) => left + (W - left - right) * (v / max);
    const ticks = niceTicks(max);
    let svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(el.parentNode.querySelector('figcaption').textContent)}">`;
    for (const tv of ticks) svg += `<line x1="${x(tv)}" x2="${x(tv)}" y1="${top}" y2="${H - 20}" class="pm-grid-l"/><text x="${x(tv)}" y="${H - 6}" class="pm-axis" text-anchor="middle">${money(tv)}</text>`;
    rows.forEach((r, i) => {
      const y = top + i * row, h = row - 8 - gap, w = Math.max(2, x(r.price) - left);
      const cls = r.us ? 'pm-bar pm-us' : 'pm-bar';
      svg += `<g class="pm-row" data-i="${i}"><rect x="0" y="${y}" width="${W}" height="${row}" fill="transparent"/>`;
      svg += `<text x="${left - 10}" y="${y + row / 2 + 1}" class="pm-name${r.us ? ' pm-name-us' : ''}" text-anchor="end" dominant-baseline="middle">${esc(r.name)}</text>`;
      svg += `<path class="${cls}" d="${barPath(left, y + 4, w, h)}"/>`;
      svg += `<text x="${left + w + 8}" y="${y + row / 2 + 1}" class="pm-val" dominant-baseline="middle">${money(r.price)}${r.ai ? ' <tspan class="pm-ai">AI</tspan>' : ''}</text></g>`;
    });
    svg += `<line x1="${left}" x2="${left}" y1="${top}" y2="${H - 20}" class="pm-base"/></svg>`;
    el.innerHTML = svg;
    el.querySelectorAll('.pm-row').forEach((g) => {
      const r = rows[+g.dataset.i];
      g.addEventListener('mousemove', (e) => showTip(e, r, rows));
      g.addEventListener('mouseleave', hideTip);
    });
  }
  // a bar with a 4px rounded end on the value side, square on the baseline
  function barPath(x0, y, w, h) {
    const r = Math.min(4, w / 2, h / 2);
    return `M${x0},${y}H${x0 + w - r}Q${x0 + w},${y} ${x0 + w},${y + r}V${y + h - r}Q${x0 + w},${y + h} ${x0 + w - r},${y + h}H${x0}Z`;
  }
  function niceTicks(max) {
    const step = [50, 100, 200, 250, 500].find((s) => max / s <= 6) || 1000;
    const out = []; for (let v = 0; v <= max; v += step) out.push(v); return out;
  }
  function showTip(e, r, rows) {
    const us = rows.find((x) => x.us);
    const tip = $('#pm-tip');
    let cmp = '';
    if (!r.us && us) cmp = us.price < r.price ? `Ai Project Hub is ${pct((1 - us.price / r.price) * 100)} less.` : `Ai Project Hub is ${money(us.price - r.price)} more.`;
    tip.innerHTML = `<b>${esc(r.name)}</b><span>${money(r.price)} a year</span>${r.note ? `<span>${esc(r.note)}</span>` : ''}${cmp ? `<span class="pm-tip-cmp">${cmp}</span>` : ''}`;
    tip.hidden = false;
    const pad = 14, tw = tip.offsetWidth, th = tip.offsetHeight;
    let left = e.clientX + pad, top = e.clientY + pad;
    if (left + tw > innerWidth - 8) left = e.clientX - tw - pad;
    if (top + th > innerHeight - 8) top = e.clientY - th - pad;
    tip.style.left = left + 'px'; tip.style.top = top + 'px';
  }
  function hideTip() { $('#pm-tip').hidden = true; }

  function charts() {
    const person = PERSON.concat([{ name: 'Ai Project Hub Pro', price: S.proYear, us: true, note: S.proMonth > 0 ? `Or ${money(S.proMonth, true)} month to month. Founding price ${money(S.founding)}/yr.` : `Founding price ${money(S.founding)}/yr.` }]);
    if (S.founding !== S.proYear) person.push({ name: 'BM Pro, founding', price: S.founding, us: true, note: 'Kept for life by early buyers.' });
    const seat = SEAT.concat([{ name: 'Ai Project Hub seat', price: S.seatYear, us: true, note: `${S.minSeats} seats at least. ${money(S.seatYear25)} per seat from 25 seats.` }]);
    chart($('#pm-chart-person'), person.sort((a, b) => a.price - b.price));
    chart($('#pm-chart-seat'), seat.sort((a, b) => a.price - b.price));
  }

  function moneyTable() {
    const pays = payments();
    const gross = pays.reduce((s, r) => s + r.count * r.amount, 0);
    let h = `<thead><tr><th>Payments in a year</th><th class="n">How many</th><th class="n">Each</th><th class="n">Takes in</th>${WAYS.map((w) => `<th class="n">Fees: ${esc(w.name)}</th>`).join('')}</tr></thead><tbody>`;
    for (const r of pays) {
      h += `<tr><th>${esc(r.label)}</th><td class="n">${Math.round(r.count).toLocaleString('en-US')}</td><td class="n">${money(r.amount, true)}</td><td class="n">${money(r.count * r.amount)}</td>`;
      h += WAYS.map((w) => `<td class="n">${money(r.count * rowFee(w, r))}</td>`).join('') + '</tr>';
    }
    const fees = WAYS.map((w) => pays.reduce((s, r) => s + r.count * rowFee(w, r), 0) + w.fixedYear());
    h += `<tr class="pm-sub"><th>Tax filing (accountant or service)</th><td></td><td></td><td></td>${WAYS.map((w) => `<td class="n">${w.fixedYear() ? money(w.fixedYear()) : 'Included'}</td>`).join('')}</tr>`;
    h += `</tbody><tfoot><tr><th>Total</th><td></td><td></td><td class="n">${money(gross)}</td>${fees.map((f) => `<td class="n">${money(f)}</td>`).join('')}</tr>`;
    h += `<tr><th>Kept</th><td></td><td></td><td></td>${fees.map((f) => `<td class="n"><b>${money(gross - f)}</b><small>${gross ? pct(f / gross * 100) + ' to fees' : ''}</small></td>`).join('')}</tr></tfoot>`;
    $('#pm-money').innerHTML = h;
  }

  function singleTable() {
    const seats = Math.max(S.minSeats, S.seats);
    const pts = [
      ['Pro, month to month', S.proMonth], ['Pro, founding', S.founding], ['Pro, yearly', S.proYear],
      [`Enterprise, ${seats} seats`, seats * (seats >= 25 ? S.seatYear25 : S.seatYear)],
    ].filter((p) => p[1] > 0);
    let h = `<thead><tr><th>Payment</th><th class="n">Amount</th>${WAYS.map((w) => `<th class="n">${esc(w.name)}</th>`).join('')}</tr></thead><tbody>`;
    for (const [label, a] of pts) {
      h += `<tr><th>${esc(label)}</th><td class="n">${money(a, true)}</td>${WAYS.map((w) => { const f = w.fee(a); return `<td class="n">${money(f, true)}<small>${pct(f / a * 100)}</small></td>`; }).join('')}</tr>`;
    }
    $('#pm-single').innerHTML = h + '</tbody>';
  }

  function rivals() {
    const all = new Map();
    for (const r of PERSON) all.set(r.name.replace(/ (Pro|Plus|Starter|Professional|Build)$/, ''), { person: r });
    for (const r of SEAT) { const k = r.name.replace(/ (Teams|Business)$/, ''); all.set(k, Object.assign(all.get(k) || {}, { seat: r })); }
    let h = '<thead><tr><th>Tool</th><th>What it does</th><th class="n">One person, per year</th><th class="n">One seat, per year</th><th>AI</th></tr></thead><tbody>';
    const us = `<tr class="pm-us-row"><th>Ai Project Hub</th><td>Bots with schedules, Claude Code threads, claude.ai chats, Groups, Teams (Windows)</td><td class="n">${money(S.proYear)}</td><td class="n">${money(S.seatYear)}</td><td>Brings own AI</td></tr>`;
    h += us;
    for (const [name, v] of [...all.entries()].sort((a, b) => ((a[1].person || a[1].seat).price - (b[1].person || b[1].seat).price))) {
      const any = v.person || v.seat;
      h += `<tr><th>${esc(name)}</th><td>${esc(any.note.replace(/^[^.]*\.\s*/, '') || any.note)}</td><td class="n">${v.person ? money(v.person.price) : ''}</td><td class="n">${v.seat ? money(v.seat.price) : ''}</td><td>${any.ai ? 'Included' : 'Brings own AI'}</td></tr>`;
    }
    $('#pm-rivals').innerHTML = h + '</tbody>';
  }

  function features() {
    const show = {
      proLine: `${money(S.proYear)}/yr${S.proMonth > 0 ? ` or ${money(S.proMonth, true)}/mo` : ''}${S.founding !== S.proYear ? `; founding ${money(S.founding)}/yr` : ''}`,
      seatLine: `${money(S.seatYear)} per seat per year, ${S.minSeats}+ seats`,
      pcLine: `2${S.extraPc > 0 ? ` (+${money(S.extraPc)}/yr each extra)` : ''}`,
    };
    document.querySelectorAll('[data-show]').forEach((el) => { el.textContent = show[el.dataset.show] || ''; });
  }

  function draw() { tiles(); charts(); moneyTable(); singleTable(); rivals(); features(); fillInputs(); }

  // ---------- events ----------
  document.addEventListener('input', (e) => {
    const k = e.target.dataset && e.target.dataset.k;
    if (!k) return;
    S[k] = e.target.type === 'checkbox' ? (e.target.checked ? 1 : 0) : Math.max(0, num(e.target.value));
    writeHash(); draw();
  });
  document.querySelectorAll('[data-preset]').forEach((b) => b.addEventListener('click', () => {
    Object.assign(S, PRESETS[b.dataset.preset]); writeHash(); draw();
  }));
  $('#pm-copy').addEventListener('click', async () => {
    writeHash();
    try { await navigator.clipboard.writeText(location.href); $('#pm-copied').textContent = 'Link copied.'; }
    catch { $('#pm-copied').textContent = 'Copy this page\'s address from the address bar.'; }
    setTimeout(() => { $('#pm-copied').textContent = ''; }, 3000);
  });
  window.addEventListener('hashchange', () => { Object.assign(S, DEFAULTS); readHash(); draw(); });

  readHash(); draw();
})();
