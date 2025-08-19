// assets/js/ws-sprinkle.js
(function () {
  function start() {
    const layer = document.getElementById('ws-sprinkle');
    if (!layer) return;

    // index.html 쪽 data-seedling 에서 경로를 읽어옵니다.
    const SEEDLING_SRC = layer.dataset.seedling || '/images/seedling.png';

    const maxLive = 12; // 동시에 떠 있을 새싹 수
    let live = 0;

    function spawn() {
      if (document.hidden || live >= maxLive) return;
      live++;

      const n = document.createElement('div');
      n.className = 'ws-floating-sprout';

      const vw = Math.random() * 100;
      const vh = 10 + Math.random() * 75;
      n.style.left = vw + 'vw';
      n.style.top  = vh + 'vh';
      n.style.setProperty('--dx',    (Math.random()*8  - 4).toFixed(1) + 'px');
      n.style.setProperty('--dxEnd', (Math.random()*10 - 5).toFixed(1) + 'px');
      n.style.setProperty('--r',     (Math.random()*6  - 3).toFixed(1) + 'deg');

      const img = document.createElement('img');
      img.src = SEEDLING_SRC;
      img.alt = 'seedling';
      img.decoding = 'async';
      n.appendChild(img);

      n.addEventListener('animationend', () => { n.remove(); live--; }, { once: true });
      layer.appendChild(n);
    }

    setInterval(spawn, 900 + Math.random() * 500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
})();
