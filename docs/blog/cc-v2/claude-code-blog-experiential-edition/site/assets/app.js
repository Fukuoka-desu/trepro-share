
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

  // TOC active highlight via IntersectionObserver
  const toc = document.querySelector('.toc');
  if (toc) {
    const links = Array.from(toc.querySelectorAll('a[href^="#"]'));
    const map = new Map();
    links.forEach(a => {
      const id = a.getAttribute('href').slice(1);
      if (id) map.set(id, a);
    });
    const targets = [];
    map.forEach((_, id) => { const el = document.getElementById(id); if (el) targets.push(el); });
    if (targets.length && 'IntersectionObserver' in window) {
      const visible = new Set();
      const setActive = () => {
        if (!visible.size) return;
        // pick the topmost visible target
        let topId = null, topY = Infinity;
        visible.forEach(id => {
          const el = document.getElementById(id);
          if (!el) return;
          const y = el.getBoundingClientRect().top;
          if (y >= -40 && y < topY) { topY = y; topId = id; }
        });
        if (!topId) {
          // fallback to any visible
          topId = Array.from(visible)[0];
        }
        links.forEach(a => a.classList.remove('active'));
        const link = map.get(topId);
        if (link) {
          link.classList.add('active');
          // also activate the part-link of the surrounding part if chapter
          const el = document.getElementById(topId);
          const part = el?.closest('section.part');
          if (part && part.id) {
            const partLink = map.get(part.id);
            if (partLink && partLink !== link) partLink.classList.add('active');
          }
        }
      };
      const io = new IntersectionObserver(entries => {
        entries.forEach(e => {
          const id = e.target.id;
          if (e.isIntersecting) visible.add(id); else visible.delete(id);
        });
        setActive();
      }, {rootMargin: '-80px 0px -70% 0px', threshold: 0});
      targets.forEach(t => io.observe(t));
    }

    // Drawer toggle for mobile
    const toggle = document.querySelector('.toc-toggle');
    const overlay = document.querySelector('.toc-overlay');
    const closeBtn = toc.querySelector('.toc-drawer-close');
    const openDrawer = () => { toc.classList.add('open'); overlay && overlay.classList.add('open'); };
    const closeDrawer = () => { toc.classList.remove('open'); overlay && overlay.classList.remove('open'); };
    toggle && toggle.addEventListener('click', () => {
      if (toc.classList.contains('open')) closeDrawer(); else openDrawer();
    });
    overlay && overlay.addEventListener('click', closeDrawer);
    closeBtn && closeBtn.addEventListener('click', closeDrawer);
    // Close drawer on link click (mobile only)
    toc.addEventListener('click', e => {
      if (e.target.tagName === 'A' && window.matchMedia('(max-width:980px)').matches) {
        closeDrawer();
      }
    });
  }
})();
