// yoshibase.com — the player. Progressive enhancement: without this file the
// page is three plain links; with it, the covers become a Cover Flow that
// recolors the page, and the deck plays a short synthesized track through an
// equalizer whose bands are the five keywords.
(() => {
  const root = document.documentElement;
  root.classList.add("js");
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const flow = document.querySelector(".flow");
  if (!flow) return;
  const slots = [...flow.querySelectorAll(".slot")];
  const pips = [...flow.querySelectorAll(".pips i")];
  const marqueeTexts = [...document.querySelectorAll(".m-text")];
  const stateEl = document.getElementById("state");
  const clockEl = document.getElementById("clock");
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  let current = 0;

  // ---------- Cover Flow ----------
  // The ring wraps, so with three covers both neighbours are always in view.
  const offset = (n) => ((n - current + slots.length + 1) % slots.length) - 1;
  function select(i, { focus = false } = {}) {
    current = (i + slots.length) % slots.length;
    slots.forEach((slot, n) => {
      const d = offset(n);
      slot.style.setProperty("--d", d);
      slot.style.setProperty("--ad", Math.abs(d));
      slot.querySelector(".cover").setAttribute("aria-current", d === 0 ? "true" : "false");
    });
    pips.forEach((p, n) => p.classList.toggle("on", n === current));
    const s = slots[current].dataset;
    root.style.setProperty("--field", s.color);
    root.style.setProperty("--ink", s.ink);
    themeMeta && themeMeta.setAttribute("content", s.color);
    const line = `HASAN OZDEMIR · ${s.title.toUpperCase()} · ${s.time} · 320 KBPS · STEREO · `;
    marqueeTexts.forEach((m) => (m.textContent = line));
    if (!playing) clockEl.textContent = s.time;
    if (focus) slots[current].querySelector(".cover").focus({ preventScroll: true });
    if (playing) restartTrack();
  }
  slots.forEach((slot, n) => slot.style.setProperty("--n", n));

  // Side covers select; only the centre cover follows its link.
  flow.addEventListener("click", (e) => {
    const cover = e.target.closest(".cover");
    if (!cover) return;
    const i = slots.indexOf(cover.closest(".slot"));
    if (dragged || i !== current) { e.preventDefault(); if (!dragged) select(i); }
  });
  flow.addEventListener("focusin", (e) => {
    const slot = e.target.closest(".slot");
    if (slot && slots.indexOf(slot) !== current) select(slots.indexOf(slot));
  });
  document.addEventListener("keydown", (e) => {
    if (e.target.matches("input, textarea")) return;
    if (e.key === "ArrowRight") { select(current + 1, { focus: flow.contains(document.activeElement) }); e.preventDefault(); }
    if (e.key === "ArrowLeft") { select(current - 1, { focus: flow.contains(document.activeElement) }); e.preventDefault(); }
  });
  document.querySelectorAll("[data-step]").forEach((b) =>
    b.addEventListener("click", () => select(current + Number(b.dataset.step))));

  // Drag / swipe with a little rubber band.
  let startX = null, dx = 0, dragged = false;
  const covers = flow.querySelector(".covers");
  covers.addEventListener("pointerdown", (e) => {
    if (e.button !== 0) return;
    startX = e.clientX; dx = 0; dragged = false;
  });
  window.addEventListener("pointermove", (e) => {
    if (startX === null) return;
    dx = e.clientX - startX;
    if (Math.abs(dx) > 6) dragged = true;
    if (!dragged || calm) return;
    const w = slots[0].offsetWidth * 0.66;
    slots.forEach((slot, n) => {
      const d = offset(n) + dx / w;
      slot.classList.add("dragging");
      slot.style.setProperty("--d", d.toFixed(3));
      slot.style.setProperty("--ad", Math.min(1, Math.abs(d)).toFixed(3));
    });
  });
  window.addEventListener("pointerup", () => {
    if (startX === null) return;
    slots.forEach((s) => s.classList.remove("dragging"));
    if (dragged) select(current + (dx < -40 ? 1 : dx > 40 ? -1 : 0));
    startX = null;
    setTimeout(() => (dragged = false), 0);
  });

  // ---------- Equalizer + audio ----------
  const bands = [...document.querySelectorAll(".eq input")];
  const FREQS = [110, 420, 1100, 2800, 7000];
  const paintFill = (input) => input.style.setProperty("--fill", `${(input.value / input.max) * 100}%`);
  bands.forEach((b) => {
    paintFill(b);
    b.addEventListener("input", () => {
      paintFill(b);
      if (filters[b.dataset.band]) filters[b.dataset.band].gain.value = gainFor(b);
    });
  });
  const gainFor = (b) => (Number(b.value) - 7) * 1.6;

  // Chord progressions per cover, as MIDI roots + intervals.
  const SONGS = [
    [[48, [0, 4, 7, 11]], [45, [0, 3, 7, 10]], [41, [0, 4, 7, 11]], [43, [0, 4, 7, 10]]], // GitHub: C  Am  F  G7
    [[45, [0, 3, 7, 10]], [41, [0, 4, 7, 11]], [48, [0, 4, 7, 14]], [43, [0, 4, 7, 9]]],  // LinkedIn: Am F Cadd9 G6
    [[40, [0, 4, 7, 11]], [49, [0, 3, 7, 10]], [45, [0, 4, 7, 14]], [47, [0, 4, 7, 10]]], // ActiveFactor: E C#m A B7
  ];
  const BPM = 112, STEP = 60 / BPM / 4, BARS = 4, STEPS = BARS * 16;
  const mtof = (m) => 440 * 2 ** ((m - 69) / 12);

  let ctx = null, master = null, analyser = null, filters = [], playing = false, startedAt = 0, stopTimer = 0, voices = [];
  const playBtn = document.getElementById("b-play");

  function ensureAudio() {
    if (ctx) return;
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    master = ctx.createGain(); master.gain.value = 0.16;
    filters = FREQS.map((f, i) => {
      const q = ctx.createBiquadFilter();
      q.type = i === 0 ? "lowshelf" : i === FREQS.length - 1 ? "highshelf" : "peaking";
      q.frequency.value = f; q.Q.value = 0.9; q.gain.value = gainFor(bands[i]);
      return q;
    });
    analyser = ctx.createAnalyser(); analyser.fftSize = 256; analyser.smoothingTimeConstant = 0.78;
    master.connect(filters[0]);
    filters.reduce((a, b) => (a.connect(b), b)).connect(analyser);
    analyser.connect(ctx.destination);
  }

  function note(type, freq, t, dur, vol, glideTo) {
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.type = type; o.frequency.setValueAtTime(freq, t);
    if (glideTo) o.frequency.exponentialRampToValueAtTime(glideTo, t + dur);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.008);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g).connect(master); o.start(t); o.stop(t + dur + 0.02);
    voices.push(o);
  }
  function hat(t) {
    const len = 0.04, buf = ctx.createBuffer(1, ctx.sampleRate * len, ctx.sampleRate), d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length);
    const s = ctx.createBufferSource(), hp = ctx.createBiquadFilter(), g = ctx.createGain();
    hp.type = "highpass"; hp.frequency.value = 7000; g.gain.value = 0.35;
    s.buffer = buf; s.connect(hp).connect(g).connect(master); s.start(t); voices.push(s);
  }

  function schedule() {
    const song = SONGS[current], t0 = ctx.currentTime + 0.06;
    for (let step = 0; step < STEPS; step++) {
      const t = t0 + step * STEP, [root, iv] = song[Math.floor(step / 16) % song.length], s16 = step % 16;
      if (s16 % 4 === 0) note("sine", 110, t, 0.22, 0.9, 42);                       // kick
      if (s16 % 4 === 2) hat(t);                                                     // offbeat hat
      if (s16 === 0 || s16 === 10) note("triangle", mtof(root - 12), t, STEP * 5, 0.5); // bass
      const arp = iv[[0, 1, 2, 3, 2, 1, 3, 2][s16 % 8]];
      note("square", mtof(root + 24 + arp), t, STEP * 0.9, 0.07);                  // arpeggio
      if (s16 === 0) iv.forEach((x) => note("sawtooth", mtof(root + 12 + x), t, STEP * 15, 0.025)); // pad
    }
    return STEPS * STEP;
  }
  function stopVoices() { voices.forEach((v) => { try { v.stop(); } catch (_) {} }); voices = []; }
  function restartTrack() { stopVoices(); clearTimeout(stopTimer); startedAt = ctx.currentTime; const len = schedule(); stopTimer = setTimeout(stop, len * 1000 + 300); }
  function play() {
    ensureAudio(); ctx.resume();
    playing = true; playBtn.setAttribute("aria-pressed", "true"); playBtn.setAttribute("aria-label", "Pause");
    stateEl.textContent = "PLAY"; restartTrack();
    if (calm) requestAnimationFrame(draw);
  }
  function stop() {
    playing = false; clearTimeout(stopTimer); stopVoices();
    playBtn.setAttribute("aria-pressed", "false"); playBtn.setAttribute("aria-label", "Play a short track");
    stateEl.textContent = "STOP"; clockEl.textContent = slots[current].dataset.time;
  }
  playBtn.addEventListener("click", () => (playing ? stop() : play()));

  // ---------- Visualizer: bars with falling peak caps ----------
  const canvas = document.getElementById("viz");
  const g2 = canvas.getContext("2d");
  const N = 28, peaks = new Array(N).fill(0);
  // At rest the panel shows the real contribution year, resampled to N bars.
  const weeks = JSON.parse(canvas.dataset.weeks || "[]");
  const year = Array.from({ length: N }, (_, i) => {
    const slice = weeks.slice(Math.floor(i * weeks.length / N), Math.floor((i + 1) * weeks.length / N));
    return slice.reduce((a, b) => a + b, 0);
  });
  const yearPeak = Math.max(1, ...year);
  let freq = null, frame = 0;
  function resize() {
    const r = canvas.getBoundingClientRect(), dpr = Math.min(2, devicePixelRatio || 1);
    canvas.width = Math.max(1, r.width * dpr); canvas.height = Math.max(1, r.height * dpr);
  }
  resize(); addEventListener("resize", resize);
  function draw() {
    frame++;
    const w = canvas.width, h = canvas.height, gap = w / N * 0.22, bw = w / N - gap;
    g2.clearRect(0, 0, w, h);
    const color = getComputedStyle(root).getPropertyValue("--field").trim() || "#C6FF3D";
    if (playing && analyser) { freq = freq || new Uint8Array(analyser.frequencyBinCount); analyser.getByteFrequencyData(freq); }
    for (let i = 0; i < N; i++) {
      let v;
      if (playing && freq) v = freq[Math.floor((i / N) ** 1.6 * freq.length * 0.7)] / 255;
      else {
        const base = 0.14 + 0.78 * (year[i] / yearPeak) ** 0.6;
        v = calm ? base : base * (0.94 + 0.06 * Math.sin(frame / 30 + i * 0.6));
      }
      const bh = Math.max(2, v * h * 0.92);
      peaks[i] = Math.max(bh, peaks[i] - h * 0.012);
      const x = i * (bw + gap) + gap / 2;
      g2.fillStyle = color; g2.globalAlpha = 0.95; g2.fillRect(x, h - bh, bw, bh);
      g2.globalAlpha = 1; g2.fillStyle = "#F2F2F4"; g2.fillRect(x, h - peaks[i] - 3, bw, 2);
    }
    if (playing && ctx) {
      const t = Math.max(0, ctx.currentTime - startedAt);
      clockEl.textContent = `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, "0")}`;
    }
    if (!calm || playing) requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);

  select(0);
})();
