const $ = s => document.querySelector(s);
const tok = t => t.toLowerCase().match(/[a-z0-9]{2,}/g) || [];   // sama dengan token_pattern di Python
const EX = ['SELAMAT! Anda memenangkan hadiah mobil, klik bit.ly/klaim99 sekarang!',
  'Besok jadi kumpul jam 13.00 di kantin ya',
  'Pinjaman online cair Rp10 juta tanpa jaminan, daftar gratis sekarang',
  'Tugas basis data dikumpulkan hari Jumat, jangan lupa ya'];

Promise.all([fetch('data/model.json').then(r => r.json()), fetch('data/analysis.json').then(r => r.json())])
  .then(([m, a]) => init(m, a)).catch(() => { $('#err').hidden = false; });

function predict(text, m) {
  let d = m.prior.spam - m.prior.ham; const used = [];
  for (const w of tok(text)) {
    const e = m.words[w];
    if (e) { const c = e[1] - e[0]; d += c; used.push([w, c]); }
  }
  d = Math.max(-30, Math.min(30, d));
  return {p: 1 / (1 + Math.exp(-d)), used};
}

function bars(el, rows, color, fmt = v => v) {
  const mx = Math.max(...rows.map(r => r[1]));
  $(el).innerHTML = rows.map(([k, v]) =>
    `<div class="bar"><span>${k}</span><div><i style="width:${v / mx * 100}%;background:${color}"></i></div><span>${fmt(v)}</span></div>`).join('');
}

function init(m, a) {
  const k = a.metrik, c = a.confusion;
  $('#kpi').innerHTML = [['Akurasi', k.akurasi], ['Presisi', k.presisi], ['Recall', k.recall], ['F1', k.f1]]
    .map(([n, v]) => `<div><small>${n}</small><b>${(v * 100).toFixed(1)}%</b></div>`).join('');
  $('#cm').innerHTML = `<div class="cm"><div></div><div class="h">Prediksi Ham</div><div class="h">Prediksi Spam</div>
    <div class="h">Aktual Ham</div><div class="ok">${c.tn}</div><div class="bad">${c.fp}</div>
    <div class="h">Aktual Spam</div><div class="bad">${c.fn}</div><div class="ok">${c.tp}</div></div>`;
  $('#info').textContent = `${a.n_train} data latih, ${a.n_test} data uji, ${a.vocab} kata unik.`;
  bars('#bs', a.top_spam, 'var(--spam)', v => v.toFixed(1));
  bars('#bh', a.top_ham, 'var(--ham)', v => v.toFixed(1));
  bars('#dist', [['Spam', a.distribusi.spam], ['Ham', a.distribusi.ham]], 'var(--brand)');
  $('#dist').insertAdjacentHTML('beforeend', `<small>Rata-rata panjang pesan: spam ${a.rata_kata.spam} kata, ham ${a.rata_kata.ham} kata.</small>`);

  const run = () => {
    const t = $('#msg').value.trim(); $('#res').hidden = !t; if (!t) return;
    const {p, used} = predict(t, m), spam = p >= .5;
    $('#verdict').innerHTML = spam ? '&#128680; SPAM' : '&#9989; Normal (Ham)';
    $('#verdict').style.color = spam ? 'var(--spam)' : 'var(--ham)';
    $('#verdict').insertAdjacentHTML('beforeend', ` <small>peluang spam ${(p * 100).toFixed(1)}%</small>`);
    $('#mbar').style.width = (p * 100) + '%';
    $('#chips').innerHTML = '';
    used.sort((x, y) => Math.abs(y[1]) - Math.abs(x[1])).slice(0, 12).forEach(([w, v]) => {
      const s = document.createElement('span'); s.className = 'chip'; s.textContent = w;
      s.style.background = v > 0 ? 'var(--spam)' : 'var(--ham)'; $('#chips').appendChild(s);
    });
    if (!used.length) $('#chips').textContent = 'Tidak ada kata yang dikenal model.';
  };
  EX.forEach(t => { const b = document.createElement('button'); b.textContent = t.slice(0, 28) + '...';
    b.onclick = () => { $('#msg').value = t; run(); }; $('#ex').appendChild(b); });
  $('#msg').oninput = run;
}
