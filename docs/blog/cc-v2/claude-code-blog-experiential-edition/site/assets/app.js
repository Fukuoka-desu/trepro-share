
(() => {
  const bar = document.querySelector('.progress > span');
  const update = () => {
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    if (bar) bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  };
  document.addEventListener('scroll', update, {passive:true}); update();
  document.querySelectorAll('.image-shell img').forEach(img => {
    const markMissing = () => img.closest('.image-shell')?.classList.add('missing');
    if (img.complete && img.naturalWidth === 0) markMissing();
    img.addEventListener('error', markMissing);
  });
  document.querySelectorAll('pre code').forEach(code => {
    const pre = code.parentElement;
    if (!pre || pre.closest('.image-brief')) return;
    const wrap = document.createElement('div'); wrap.className = 'code-wrap';
    pre.parentNode.insertBefore(wrap, pre); wrap.appendChild(pre);
    const btn = document.createElement('button'); btn.className='copy-code'; btn.textContent='コピー';
    btn.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(code.textContent || ''); btn.textContent='コピー済み'; setTimeout(()=>btn.textContent='コピー',1200); }
      catch { btn.textContent='失敗'; }
    });
    wrap.appendChild(btn);
  });
})();
