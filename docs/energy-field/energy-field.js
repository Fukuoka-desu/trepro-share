/*!
 * energy-field.js v1.0.0
 * 講演スライドの背景で「エネルギー体」がじんわり動く部品。WebGL1・依存なし・1ファイル。
 *
 *   const ef = EnergyField.mount({ container: '#deck', theme: 'navy', preset: 'cover' });
 *   ef.set({ preset: 'content', theme: 'white' });   // 画面が変わるたびに呼ぶ
 *
 * 使い方・調整方法は同じフォルダの README.md を参照。
 *
 * シェーダー内で使っている第三者コード:
 *   - 3D simplex noise: Ian McEwan, Stefan Gustavson (Ashima Arts) / MIT License
 *     https://github.com/stegu/webgl-noise
 *   - Hash without Sine: Dave Hoskins / MIT License
 *     https://www.shadertoy.com/view/4djSRW
 */
(function (root) {
  'use strict';

  var VERSION = '1.0.0';
  var TAU = Math.PI * 2;

  // ------------------------------------------------------------------
  // 画面の種類ごとの見え方。
  //   intensity : 強さ (0〜1)
  //   x, y      : 中心の位置 (画面に対する比率。y は上が 0)
  //   radius    : 大きさ (画面の高さに対する比率)
  //   cap       : 濃紺テーマで背景が超えない明るさ (相対輝度)。白文字のコントラスト = 1.05 / (cap + 0.05)
  //   floor     : 白地テーマで背景が下回らない明るさ (相対輝度)
  //   aurora    : 画面全体のゆらぎ
  //   particles : 吸い込まれる光の粒
  // ------------------------------------------------------------------
  var PRESETS = {
    cover:     { intensity: 1.00, x: 0.73, y: 0.50, radius: 0.40, cap: 0.50, floor: 0.45, aurora: 1.00, particles: 1.00 },
    section:   { intensity: 0.85, x: 0.77, y: 0.52, radius: 0.34, cap: 0.34, floor: 0.50, aurora: 0.90, particles: 0.85 },
    statement: { intensity: 0.55, x: 0.50, y: 0.62, radius: 0.40, cap: 0.16, floor: 0.65, aurora: 0.80, particles: 0.60 },
    content:   { intensity: 0.42, x: 0.94, y: 0.90, radius: 0.32, cap: 0.09, floor: 0.80, aurora: 0.60, particles: 0.45 },
    dense:     { intensity: 0.24, x: 0.97, y: 0.96, radius: 0.28, cap: 0.06, floor: 0.90, aurora: 0.40, particles: 0.25 },
    visual:    { intensity: 0.22, x: 0.50, y: 0.54, radius: 0.55, cap: 0.07, floor: 0.85, aurora: 0.50, particles: 0.30 },
    video:     { intensity: 0.08, x: 0.50, y: 0.50, radius: 0.55, cap: 0.04, floor: 0.93, aurora: 0.20, particles: 0.00 },
    ending:    { intensity: 0.90, x: 0.50, y: 0.68, radius: 0.40, cap: 0.24, floor: 0.55, aurora: 1.00, particles: 1.00 },
    quiet:     { intensity: 0.14, x: 0.86, y: 0.82, radius: 0.30, cap: 0.05, floor: 0.92, aurora: 0.40, particles: 0.20 },
    off:       { intensity: 0.00, x: 0.50, y: 0.50, radius: 0.40, cap: 0.04, floor: 0.96, aurora: 0.00, particles: 0.00 }
  };

  // 資料側の呼び名をそのまま渡せるように
  var ALIASES = {
    title: 'cover', hero: 'cover', '表紙': 'cover',
    chapter: 'section', '扉': 'section', '章扉': 'section', 'セクション': 'section',
    message: 'statement', quote: 'statement', '主張': 'statement', '一言': 'statement',
    text: 'content', card: 'content', cards: 'content', list: 'content', '本文': 'content', 'カード': 'content',
    table: 'dense', data: 'dense', '表': 'dense',
    showpiece: 'visual', diagram: 'visual', chart: 'visual', '図解': 'visual', '見せ場': 'visual', '図': 'visual',
    demo: 'video', movie: 'video', '動画': 'video', '実演': 'video',
    closing: 'ending', end: 'ending', '締め': 'ending', '持ち帰り': 'ending', 'まとめ': 'ending',
    calm: 'quiet', '静か': 'quiet',
    none: 'off', blackout: 'off', '暗転': 'off', 'なし': 'off'
  };

  var DEFAULT_COLORS = {
    navyTop: '#0B1736', navyBottom: '#050B1F',
    whiteTop: '#FFFFFF', whiteBottom: '#F2F5FB',
    deep: '#1A3C9E', blue: '#2F6BFF', cyan: '#5AD8FF', violet: '#7C5CFF'
  };

  // :root に書けば資料の色に合わせられる (例: --energy-navy-top: #0A1A3F)
  var CSS_VARS = {
    navyTop: '--energy-navy-top', navyBottom: '--energy-navy-bottom',
    whiteTop: '--energy-white-top', whiteBottom: '--energy-white-bottom',
    deep: '--energy-deep', blue: '--energy-blue', cyan: '--energy-cyan', violet: '--energy-violet'
  };

  var NUM_KEYS = ['intensity', 'x', 'y', 'radius', 'cap', 'floor', 'aurora', 'particles'];

  // ------------------------------------------------------------------
  // shaders
  // ------------------------------------------------------------------
  var VERT = 'attribute vec2 aPos;\nvoid main(){ gl_Position = vec4(aPos, 0.0, 1.0); }\n';

  var FRAG = [
    '#ifdef GL_FRAGMENT_PRECISION_HIGH',
    'precision highp float;',
    '#else',
    'precision mediump float;',
    '#endif',
    '',
    'uniform vec2  uRes;',
    'uniform float uTime;',
    'uniform float uRot;',
    'uniform float uTwT;',
    'uniform vec2  uAnchor;',
    'uniform float uRadius;',
    'uniform float uIntensity;',
    'uniform float uBreath;',
    'uniform float uTheme;',
    'uniform float uCap;',
    'uniform float uFloor;',
    'uniform float uAurora;',
    'uniform float uParticles;',
    'uniform float uSeed;',
    'uniform vec3  uNavyTop;',
    'uniform vec3  uNavyBottom;',
    'uniform vec3  uWhiteTop;',
    'uniform vec3  uWhiteBottom;',
    'uniform vec3  uDeep;',
    'uniform vec3  uBlue;',
    'uniform vec3  uCyan;',
    'uniform vec3  uViolet;',
    'uniform vec3  uAbsBlue;',
    'uniform vec3  uAbsCyan;',
    'uniform vec3  uAbsViolet;',
    'uniform vec4  uSafeA[8];',
    'uniform vec4  uSafeB[8];',
    'uniform float uSafeNA;',
    'uniform float uSafeNB;',
    'uniform float uSafeT;',
    'uniform float uSafeCap;',
    'uniform float uSafeFloor;',
    'uniform float uFeather;',
    '',
    'const vec3 LUMA = vec3(0.2126, 0.7152, 0.0722);',
    '',
    // --- 3D simplex noise (Ashima Arts / Stefan Gustavson, MIT) ---
    'vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }',
    'vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }',
    'vec4 permute(vec4 x) { return mod289(((x * 34.0) + 10.0) * x); }',
    'vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }',
    'float snoise(vec3 v) {',
    '  const vec2 C = vec2(1.0 / 6.0, 1.0 / 3.0);',
    '  const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);',
    '  vec3 i  = floor(v + dot(v, C.yyy));',
    '  vec3 x0 = v - i + dot(i, C.xxx);',
    '  vec3 g = step(x0.yzx, x0.xyz);',
    '  vec3 l = 1.0 - g;',
    '  vec3 i1 = min(g.xyz, l.zxy);',
    '  vec3 i2 = max(g.xyz, l.zxy);',
    '  vec3 x1 = x0 - i1 + C.xxx;',
    '  vec3 x2 = x0 - i2 + C.yyy;',
    '  vec3 x3 = x0 - D.yyy;',
    '  i = mod289(i);',
    '  vec4 p = permute(permute(permute(',
    '            i.z + vec4(0.0, i1.z, i2.z, 1.0))',
    '          + i.y + vec4(0.0, i1.y, i2.y, 1.0))',
    '          + i.x + vec4(0.0, i1.x, i2.x, 1.0));',
    '  float n_ = 0.142857142857;',
    '  vec3 ns = n_ * D.wyz - D.xzx;',
    '  vec4 j = p - 49.0 * floor(p * ns.z * ns.z);',
    '  vec4 x_ = floor(j * ns.z);',
    '  vec4 y_ = floor(j - 7.0 * x_);',
    '  vec4 x = x_ * ns.x + ns.yyyy;',
    '  vec4 y = y_ * ns.x + ns.yyyy;',
    '  vec4 h = 1.0 - abs(x) - abs(y);',
    '  vec4 b0 = vec4(x.xy, y.xy);',
    '  vec4 b1 = vec4(x.zw, y.zw);',
    '  vec4 s0 = floor(b0) * 2.0 + 1.0;',
    '  vec4 s1 = floor(b1) * 2.0 + 1.0;',
    '  vec4 sh = -step(h, vec4(0.0));',
    '  vec4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;',
    '  vec4 a1 = b1.xzyw + s1.xzyw * sh.zzww;',
    '  vec3 p0 = vec3(a0.xy, h.x);',
    '  vec3 p1 = vec3(a0.zw, h.y);',
    '  vec3 p2 = vec3(a1.xy, h.z);',
    '  vec3 p3 = vec3(a1.zw, h.w);',
    '  vec4 norm = taylorInvSqrt(vec4(dot(p0, p0), dot(p1, p1), dot(p2, p2), dot(p3, p3)));',
    '  p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;',
    '  vec4 m = max(0.5 - vec4(dot(x0, x0), dot(x1, x1), dot(x2, x2), dot(x3, x3)), 0.0);',
    '  m = m * m;',
    '  return 105.0 * dot(m * m, vec4(dot(p0, x0), dot(p1, x1), dot(p2, x2), dot(p3, x3)));',
    '}',
    '',
    // --- Hash without Sine (Dave Hoskins, MIT) ---
    'float hash12(vec2 p) {',
    '  vec3 p3 = fract(vec3(p.xyx) * 0.1031);',
    '  p3 += dot(p3, p3.yzx + 33.33);',
    '  return fract((p3.x + p3.y) * p3.z);',
    '}',
    'vec2 hash22(vec2 p) {',
    '  vec3 p3 = fract(vec3(p.xyx) * vec3(0.1031, 0.1030, 0.0973));',
    '  p3 += dot(p3, p3.yzx + 33.33);',
    '  return fract((p3.xx + p3.yz) * p3.zy);',
    '}',
    '',
    'float fbm3(vec3 p) {',
    '  float s = 0.0; float a = 0.5;',
    '  for (int i = 0; i < 3; i++) { s += a * snoise(p); p = p * 2.02 + vec3(17.1, 3.7, 9.3); a *= 0.5; }',
    '  return s / 0.875;',
    '}',
    'float fbm4(vec3 p) {',
    '  float s = 0.0; float a = 0.5;',
    '  for (int i = 0; i < 4; i++) { s += a * snoise(p); p = p * 2.03 + vec3(5.3, 11.9, 2.1); a *= 0.5; }',
    '  return s / 0.9375;',
    '}',
    'mat2 rot2(float a) { float c = cos(a); float s = sin(a); return mat2(c, s, -s, c); }',
    '',
    // 対数極座標の格子に置いた光の粒。格子ごと内側へ流れるので、粒が渦を描いて中心へ吸い込まれる。
    'float vortex(vec2 d, float R, float layer) {',
    '  float r = length(d) / R;',
    '  if (r < 0.12 || r > 4.2) return 0.0;',
    '  float N = layer < 0.5 ? 36.0 : 58.0;',
    '  float k = N / 6.2831853;',
    '  float u = log(r) * k + uTime * (0.085 + 0.04 * layer);',
    '  float v = atan(d.y, d.x) * k + u * 0.42;',
    '  vec2 g = vec2(u, v);',
    '  vec2 cell = floor(g);',
    '  vec2 f = g - cell;',
    '  float cs = r * R / k;',
    '  float thr = layer < 0.5 ? 0.52 : 0.70;',
    '  float acc = 0.0;',
    '  for (int j = -1; j <= 1; j++) {',
    '    for (int i = -1; i <= 1; i++) {',
    '      vec2 o = vec2(float(i), float(j));',
    '      vec2 c = cell + o;',
    '      vec2 cw = vec2(c.x, mod(c.y, N)) + layer * 31.7;',
    '      float alive = step(thr, hash12(cw + 7.31));',
    '      vec2 h = hash22(cw);',
    '      vec2 q = o + h - f;',
    '      vec2 delta = vec2(q.x, q.y - 0.42 * q.x) * cs;',
    '      float sz = (0.0018 + 0.0030 * h.x) * (1.0 - 0.25 * layer);',
    '      float fq = floor(80.0 + h.y * 160.0) / 100.0;',
    '      float tw = 0.55 + 0.45 * sin(uTwT * fq + h.x * 40.0);',
    '      acc += alive * tw * exp(-dot(delta, delta) / (sz * sz));',
    '    }',
    '  }',
    '  return acc * smoothstep(0.12, 0.55, r) * smoothstep(3.6, 1.7, r);',
    '}',
    '',
    // 文字のある矩形 (ぼかし付き) の中だけ、明るさの上限・下限を厳しくする
    'float rectMask(vec2 uv, float aspect, vec4 r) {',
    '  vec2 c = (r.xy + r.zw) * 0.5;',
    '  vec2 h = (r.zw - r.xy) * 0.5;',
    '  vec2 q = abs(uv - c) - h;',
    '  q.x *= aspect;',
    '  float dd = length(max(q, 0.0)) + min(max(q.x, q.y), 0.0);',
    '  return 1.0 - smoothstep(0.0, uFeather, dd);',
    '}',
    'float safeMask(vec2 uv, float aspect) {',
    '  float a = 0.0; float b = 0.0;',
    '  for (int i = 0; i < 8; i++) {',
    '    if (float(i) < uSafeNA) a = max(a, rectMask(uv, aspect, uSafeA[i]));',
    '    if (float(i) < uSafeNB) b = max(b, rectMask(uv, aspect, uSafeB[i]));',
    '  }',
    // 新しい文字の範囲は速く守り、古い範囲はゆっくり手放す。重なる所は守ったまま
    '  return max(max(a * (1.0 - uSafeT), b * min(1.0, uSafeT * 3.0)), min(a, b));',
    '}',
    '',
    'vec3 toSrgb(vec3 c) {',
    '  c = clamp(c, 0.0, 1.0);',
    '  return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(0.0031308, c));',
    '}',
    '',
    'void main() {',
    '  vec2 uv = gl_FragCoord.xy / uRes;',
    '  float aspect = uRes.x / uRes.y;',
    '  vec2 P = vec2(uv.x * aspect, uv.y);',
    '  vec2 A = vec2(uAnchor.x * aspect, uAnchor.y);',
    '  vec2 d = P - A;',
    '  float R = uRadius;',
    '  vec2 b = d / R;',
    '  float rad = length(b);',
    '  float I = uIntensity;',
    '',
    // 画面全体のゆらぎ (とても低い周波数)
    '  float au = 0.0; float au2 = 0.0;',
    '  if (uAurora > 0.002) {',
    '    vec3 q = vec3(P * 0.75 + vec2(uSeed * 1.7, uSeed * 0.3), uTime * 0.010);',
    '    au = snoise(q) * 0.62 + snoise(q * 2.1 + vec3(3.1, 7.7, 1.3)) * 0.38;',
    '    au2 = snoise(vec3(P * 0.45 + 11.0, uTime * 0.006 + 5.0));',
    '  }',
    '',
    // エネルギー体
    '  float halo = 0.0; float body = 0.0; float glow = 0.0; float line = 0.0; float hot = 0.0;',
    '  float ray = 0.0; float hue = 0.0; float rim = 0.0; float x = 9.0;',
    '  if (I > 0.002 && rad < 2.6) {',
    '    float fade = smoothstep(2.6, 1.9, rad);',
    '    float swirl = 1.4 * exp(-rad * 0.9);',
    '    vec2 bs = rot2(uRot + swirl) * b;',
    // 内側のプラズマ (ドメインワープ)
    '    vec3 p1 = vec3(bs * 1.1, uTime * 0.040 + uSeed);',
    '    vec2 q = vec2(fbm3(p1), fbm3(p1 + vec3(5.2, 1.3, 2.8)));',
    '    float f = fbm4(vec3(bs * 1.2 + q * 1.5, uTime * 0.050 + uSeed + 7.3));',
    '    hue = smoothstep(-0.25, 0.45, q.x - 0.6 * q.y);',
    // 輪郭をゆらす
    '    vec2 dir = b / max(rad, 1e-4);',
    '    float edge = snoise(vec3(dir * 1.2, uTime * 0.045 + uSeed + 13.0)) * 0.16',
    '               + snoise(vec3(dir * 2.5 + 3.0, uTime * 0.07 + uSeed + 21.0)) * 0.06;',
    '    x = rad / (1.0 + edge);',
    '    body = exp(-x * x * 2.1) * (0.55 + 0.45 * clamp(0.5 + 0.9 * f, 0.0, 1.0));',
    '    halo = exp(-x * 1.35) * fade;',
    '    hot  = exp(-x * x * 6.5);',
    '    rim  = exp(-(x - 1.0) * (x - 1.0) * 10.0);',
    // 表面をめぐる光の流れ: 角度方向はゆっくり、半径方向は細かく変わるノイズの稜線 = 渦を巻く弧
    '    vec2 sdir = bs / max(length(bs), 1e-4);',
    '    float n1 = snoise(vec3(sdir * 1.0 + q * 0.18, x * 1.7 - uTime * 0.022 + uSeed + 31.0));',
    '    float n2 = snoise(vec3(sdir * 1.6 + q * 0.25, x * 2.9 - uTime * 0.034 + uSeed + 47.0));',
    // 輪を途切れさせて「弧」にする
    '    float arc1 = smoothstep(-0.15, 0.55, snoise(vec3(sdir * 1.3, uTime * 0.020 + uSeed + 71.0)));',
    '    float arc2 = smoothstep(0.05, 0.65, snoise(vec3(sdir * 1.9 + 4.0, uTime * 0.026 + uSeed + 83.0)));',
    '    float l1 = 1.0 - abs(n1);',
    '    float l2 = 1.0 - abs(n2);',
    '    float smask = smoothstep(0.2, 0.75, x) * smoothstep(1.85, 0.9, x);',
    '    line = (pow(l1, 20.0) * arc1 + 0.55 * pow(l2, 26.0) * arc2) * smask;',
    '    glow = (pow(l1, 3.0) * arc1 + 0.35 * pow(l2, 4.0) * arc2) * smask;',
    '    float rn = 0.5 + 0.5 * snoise(vec3(dir * 2.1, uTime * 0.028 + uSeed + 57.0));',
    '    ray = rn * rn * rn * rn * exp(-x * 0.8) * smoothstep(0.35, 1.2, x) * fade;',
    '  }',
    '',
    '  float sp = 0.0;',
    '  if (uParticles > 0.002 && I > 0.002) {',
    '    sp = (vortex(d, R, 0.0) + 0.75 * vortex(d, R, 1.0)) * uParticles;',
    '  }',
    '',
    '  float gain = I * (0.86 + 0.28 * uBreath);',
    '  float vg = length((uv - 0.5) * vec2(aspect, 1.0));',
    '',
    // 濃紺: 光を足す (リニア空間)
    '  vec3 baseN = mix(uNavyBottom, uNavyTop, uv.y);',
    '  vec3 E = uDeep * halo * 0.30',
    '         + mix(uBlue, uViolet, hue) * body * 0.34',
    '         + uCyan * glow * 0.045',
    '         + mix(uCyan, vec3(1.0), 0.5) * line * 0.30',
    '         + vec3(0.85, 0.93, 1.0) * hot * 0.60 * min(I, 1.0)',
    '         + uBlue * rim * 0.05',
    '         + uBlue * ray * 0.08',
    '         + mix(uCyan, vec3(1.0), 0.55) * sp * 0.35;',
    '  E = 1.0 - exp(-E * gain);',
    '  vec3 auN = mix(vec3(0.006, 0.008, 0.060), vec3(0.002, 0.030, 0.045), smoothstep(-0.4, 0.6, au2));',
    '  vec3 cN = baseN + E + auN * max(au, 0.0) * 0.6 * uAurora;',
    '  cN *= 1.0 - 0.30 * smoothstep(0.55, 1.35, vg);',
    // 明るさの上限: 白文字のコントラストを守る
    '  float sm = (uSafeNA + uSafeNB > 0.0) ? safeMask(uv, aspect) : 0.0;',
    '  float capE = mix(uCap, min(uCap, uSafeCap), sm);',
    '  float L = dot(cN, LUMA);',
    '  float knee = capE * 0.6;',
    '  if (L > knee) {',
    '    float Lc = knee + (capE - knee) * (1.0 - exp(-(L - knee) / (capE - knee)));',
    // 青は輝度への寄与が小さいので、青を残して赤と緑を多めに落とす (灰色にくすませない)
    '    float bk = min(cN.b * pow(Lc / L, 0.35), Lc / LUMA.b);',
    '    float rg = dot(cN.rg, LUMA.rg);',
    '    float a = rg > 1e-6 ? max(Lc - LUMA.b * bk, 0.0) / rg : 0.0;',
    '    cN = vec3(cN.rg * a, bk);',
    '  }',
    '',
    // 白地: 色を吸収させる (リニア空間)
    '  vec3 baseW = mix(uWhiteBottom, uWhiteTop, uv.y);',
    '  float rimW = exp(-(x - 1.0) * (x - 1.0) * 34.0);',
    '  vec3 Ab = uAbsBlue * (halo * 0.040 * (1.0 - hot) + glow * 0.080 + line * 0.45 + sp * 0.16 + rim * 0.05 + rimW * 0.10)',
    '          + mix(uAbsBlue, uAbsViolet, hue) * body * 0.14 * (1.0 - 0.85 * hot)',
    '          + uAbsCyan * ray * 0.02;',
    '  Ab *= gain;',
    '  Ab += mix(uAbsBlue, uAbsCyan, smoothstep(-0.4, 0.6, au2)) * max(au, 0.0) * 0.012 * uAurora;',
    '  vec3 ink = baseW * (1.0 - exp(-Ab));',
    // 明るさの下限: 濃紺文字のコントラストを守る
    '  float Lb = dot(baseW, LUMA);',
    '  float Dk = dot(ink, LUMA);',
    '  float floorE = mix(uFloor, max(uFloor, uSafeFloor), sm);',
    '  float Dmax = max(Lb - floorE, 0.0005);',
    '  float kneeW = Dmax * 0.6;',
    '  if (Dk > kneeW) {',
    '    float Dc = kneeW + (Dmax - kneeW) * (1.0 - exp(-(Dk - kneeW) / (Dmax - kneeW)));',
    '    ink *= Dc / Dk;',
    '  }',
    '  vec3 cW = baseW - ink;',
    '',
    '  vec3 col = mix(cN, cW, uTheme);',
    '  vec3 s = toSrgb(col);',
    '  s += (hash12(gl_FragCoord.xy) + hash12(gl_FragCoord.xy + 71.3) - 1.0) / 255.0;',
    '  gl_FragColor = vec4(s, 1.0);',
    '}'
  ].join('\n');

  var UNIFORMS = [
    'uRes', 'uTime', 'uRot', 'uTwT', 'uAnchor', 'uRadius', 'uIntensity', 'uBreath', 'uTheme', 'uCap', 'uFloor',
    'uAurora', 'uParticles', 'uSeed', 'uNavyTop', 'uNavyBottom', 'uWhiteTop', 'uWhiteBottom',
    'uDeep', 'uBlue', 'uCyan', 'uViolet', 'uAbsBlue', 'uAbsCyan', 'uAbsViolet',
    'uSafeA', 'uSafeB', 'uSafeNA', 'uSafeNB', 'uSafeT', 'uSafeCap', 'uSafeFloor', 'uFeather'
  ];

  // ------------------------------------------------------------------
  // helpers
  // ------------------------------------------------------------------
  function parseHex(str) {
    if (typeof str !== 'string') return null;
    var s = str.trim().replace(/^#/, '');
    if (s.length === 3) s = s.charAt(0) + s.charAt(0) + s.charAt(1) + s.charAt(1) + s.charAt(2) + s.charAt(2);
    if (!/^[0-9a-fA-F]{6}$/.test(s)) return null;
    var n = parseInt(s, 16);
    return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
  }
  function toLinear(c) { return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
  function hexToLinear(hex, fallback) {
    var s = parseHex(hex) || parseHex(fallback);
    return [toLinear(s[0]), toLinear(s[1]), toLinear(s[2])];
  }
  function absorption(lin) {
    return [-Math.log(Math.max(lin[0], 0.02)), -Math.log(Math.max(lin[1], 0.02)), -Math.log(Math.max(lin[2], 0.02))];
  }
  function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }
  function num(v) { return typeof v === 'number' && isFinite(v); }

  var warned = {};
  function warnOnce(key, msg) {
    if (warned[key]) return;
    warned[key] = true;
    if (root.console) root.console.warn('[EnergyField] ' + msg);
  }

  function resolvePresetName(name) {
    if (name == null) return null;
    var key = String(name).trim();
    if (PRESETS[key]) return key;
    var lower = key.toLowerCase();
    if (PRESETS[lower]) return lower;
    if (ALIASES[key]) return ALIASES[key];
    if (ALIASES[lower]) return ALIASES[lower];
    warnOnce('preset:' + key, '知らない画面の種類 "' + key + '" なので content として扱います');
    return 'content';
  }

  function readUrl() {
    var out = {};
    try {
      var q = new URLSearchParams(root.location ? root.location.search : '');
      var v;
      if (q.has('energy')) out.mode = q.get('energy');
      if (q.has('energy-time')) { v = parseFloat(q.get('energy-time')); if (isFinite(v)) out.freeze = v; }
      if (q.has('energy-debug')) out.debug = q.get('energy-debug') !== '0';
      if (q.has('energy-scale')) { v = parseFloat(q.get('energy-scale')); if (v > 0) out.scale = v; }
      if (q.has('energy-fps')) { v = parseFloat(q.get('energy-fps')); if (v > 0) out.fps = v; }
      if (q.has('energy-preset')) out.preset = q.get('energy-preset');
      if (q.has('energy-theme')) out.theme = q.get('energy-theme');
      if (q.has('energy-autoq')) out.autoQuality = q.get('energy-autoq') !== '0';
    } catch (e) { /* ignore */ }
    return out;
  }

  function localMidnight() {
    var d = new Date();
    d.setHours(0, 0, 0, 0);
    return d.getTime();
  }

  // ------------------------------------------------------------------
  // mount
  // ------------------------------------------------------------------
  function mount(options) {
    var url = readUrl();
    var o = {
      container: null,          // 要素 or セレクタ。省略時は body に全画面固定
      theme: 'navy',            // 'navy' | 'white'
      preset: 'cover',
      mode: 'live',             // 'live' | 'low' | 'static' | 'off'
      fps: 30,
      scale: 0.5,               // 描画解像度 (CSS ピクセルに対する比率)
      maxPixels: 1200000,
      zIndex: -1,
      colors: null,
      seed: 0,
      respectReducedMotion: true,
      autoQuality: true,
      observe: true,            // <html data-energy="..."> を見張る
      debug: false,
      freeze: null,             // 秒を入れると時間を止める (検品のスクショ用)
      protect: null,            // 文字を守る範囲: セレクタ / 要素 / 要素や矩形の配列 (例: '.slide.is-active')
      safeCap: 0.08,            // 文字の下の明るさの上限 (濃紺)。白文字 11:1、#C8D5F0 でも 5.5:1
      safeFloor: 0.70,          // 文字の下の明るさの下限 (白地)。#0B1630 で 12.7:1、#1F4FD8 でも 5:1
      protectFade: 0.6,         // 文字の範囲が変わったときに切り替える秒数
      themeDuration: 0.35,      // 濃紺⇄白地の切り替えにかける秒数
      fadeDuration: 1.4,        // 強さの変化にかける秒数
      moveDuration: 2.2,        // 位置・大きさの変化にかける秒数
      className: 'energy-field'
    };
    var k;
    options = options || {};
    for (k in options) if (Object.prototype.hasOwnProperty.call(options, k) && options[k] !== undefined) o[k] = options[k];
    for (k in url) if (Object.prototype.hasOwnProperty.call(url, k)) o[k] = url[k];

    if (o.mode === 'low') { o.fps = Math.min(o.fps, 20); o.scale = Math.min(o.scale, 0.35); }

    var doc = root.document;
    var cur = {}, tgt = {};
    var presetName = resolvePresetName(o.preset) || 'cover';
    var p0 = PRESETS[presetName];
    for (var i = 0; i < NUM_KEYS.length; i++) { cur[NUM_KEYS[i]] = p0[NUM_KEYS[i]]; tgt[NUM_KEYS[i]] = p0[NUM_KEYS[i]]; }
    cur.theme = tgt.theme = (o.theme === 'white') ? 1 : 0;

    var canvas = null, gl = null, prog = null, buf = null, U = {}, debugEl = null, fallbackEl = null;
    var container = null, isBody = true, restoreStyles = null;
    var rafLoop = 0, rafOnce = 0, running = false, paused = false, destroyed = false, lost = false;
    var lastTick = 0, lastDraw = 0, pulseV = 0, frozen = num(o.freeze) ? o.freeze : null;
    var frameInterval = 1000 / clamp(o.fps, 1, 120);
    var scale = clamp(o.scale, 0.1, 2);
    var slowFrames = 0, emaInterval = 0, debugAt = 0, fpsCount = 0, fpsAt = 0;
    var t0 = localMidnight();
    var timeOrigin = (root.performance && root.performance.timeOrigin) ? root.performance.timeOrigin : Date.now() - (root.performance ? root.performance.now() : 0);
    var mqReduce = null, ro = null, mo = null;
    var staticMode = o.mode === 'static';
    var colorsLin = null;
    var resolveReady;
    var safeA = new Float32Array(32), safeB = new Float32Array(32), safeNA = 0, safeNB = 0, safeT = 1;
    var protectTarget = o.protect || null, recheckTimer = 0;

    var ctl = {
      version: VERSION,
      canvas: null,
      ready: new Promise(function (res) { resolveReady = res; }),
      stats: { frames: 0, fps: 0, width: 0, height: 0, scale: scale, mode: o.mode, preset: presetName, theme: o.theme === 'white' ? 'white' : 'navy' },
      set: set,
      pulse: pulse,
      pause: pause,
      resume: resume,
      freeze: freeze,
      protect: protect,
      state: state,
      render: requestRender,
      destroy: destroy,
      presets: PRESETS
    };
    root.EnergyField.current = ctl;

    if (o.mode === 'off') {
      resolveReady(ctl);
      return ctl;
    }

    if (doc.body) init();
    else doc.addEventListener('DOMContentLoaded', init, { once: true });
    return ctl;

    // ---------------- init ----------------
    function init() {
      if (destroyed) return;
      container = o.container ? (typeof o.container === 'string' ? doc.querySelector(o.container) : o.container) : doc.body;
      if (!container) { warnOnce('container', 'container が見つからないので body に置きます'); container = doc.body; }
      isBody = container === doc.body;

      canvas = doc.createElement('canvas');
      canvas.className = o.className;
      canvas.setAttribute('aria-hidden', 'true');
      var st = canvas.style;
      st.position = isBody ? 'fixed' : 'absolute';
      st.left = '0'; st.top = '0'; st.width = '100%'; st.height = '100%';
      st.zIndex = String(o.zIndex);
      st.pointerEvents = 'none';
      st.display = 'block';
      if (!isBody) {
        var cs = root.getComputedStyle(container);
        restoreStyles = { position: container.style.position, isolation: container.style.isolation };
        if (cs.position === 'static') container.style.position = 'relative';
        container.style.isolation = 'isolate';
      }
      container.insertBefore(canvas, container.firstChild);
      ctl.canvas = canvas;
      doc.documentElement.classList.add('energy-field-on');

      if (o.respectReducedMotion && root.matchMedia) {
        mqReduce = root.matchMedia('(prefers-reduced-motion: reduce)');
        if (mqReduce.matches) staticMode = true;
        if (mqReduce.addEventListener) mqReduce.addEventListener('change', onReduceChange);
      }

      readColors();
      if (!initGL()) {
        useFallback();
      }

      if (o.observe) {
        syncFromAttributes();
        mo = new MutationObserver(syncFromAttributes);
        mo.observe(doc.documentElement, { attributes: true, attributeFilter: ['data-energy', 'data-energy-theme'] });
      }
      root.addEventListener('energyfield', onEvent);
      doc.addEventListener('visibilitychange', onVisibility);
      if (isBody) root.addEventListener('resize', resize);
      else if (root.ResizeObserver) { ro = new ResizeObserver(resize); ro.observe(container); }
      else root.addEventListener('resize', resize);

      if (o.debug) {
        debugEl = doc.createElement('div');
        debugEl.style.cssText = 'position:fixed;left:8px;bottom:8px;z-index:2147483647;font:12px/1.4 ui-monospace,Menlo,monospace;color:#9fe;background:rgba(0,0,0,.55);padding:4px 8px;border-radius:4px;pointer-events:none';
        doc.body.appendChild(debugEl);
      }

      resize();
      if (protectTarget) updateSafe(true);
      if (gl) start();
    }

    function readColors() {
      var css = null;
      try { css = root.getComputedStyle(doc.documentElement); } catch (e) { css = null; }
      var given = o.colors || {};
      var out = {};
      for (var key in DEFAULT_COLORS) {
        var v = given[key];
        if (!v && css) { var c = css.getPropertyValue(CSS_VARS[key]); if (c && c.trim()) v = c.trim(); }
        out[key] = hexToLinear(v || DEFAULT_COLORS[key], DEFAULT_COLORS[key]);
      }
      out.absBlue = absorption(out.blue);
      out.absCyan = absorption(out.cyan);
      out.absViolet = absorption(out.violet);
      colorsLin = out;
    }

    function compile(type, src) {
      var sh = gl.createShader(type);
      gl.shaderSource(sh, src);
      gl.compileShader(sh);
      if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
        warnOnce('compile', 'シェーダーのコンパイルに失敗: ' + gl.getShaderInfoLog(sh));
        gl.deleteShader(sh);
        return null;
      }
      return sh;
    }

    function initGL() {
      var attrs = { alpha: false, antialias: false, depth: false, stencil: false, premultipliedAlpha: false, preserveDrawingBuffer: false, powerPreference: 'low-power' };
      if (!gl) {
        try { gl = canvas.getContext('webgl', attrs) || canvas.getContext('experimental-webgl', attrs); } catch (e) { gl = null; }
        if (!gl) return false;
        canvas.addEventListener('webglcontextlost', onContextLost, false);
        canvas.addEventListener('webglcontextrestored', onContextRestored, false);
      }
      var vs = compile(gl.VERTEX_SHADER, VERT);
      var fs = compile(gl.FRAGMENT_SHADER, FRAG);
      if (!vs || !fs) return false;
      prog = gl.createProgram();
      gl.attachShader(prog, vs);
      gl.attachShader(prog, fs);
      gl.bindAttribLocation(prog, 0, 'aPos');
      gl.linkProgram(prog);
      gl.deleteShader(vs);
      gl.deleteShader(fs);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
        warnOnce('link', 'シェーダーのリンクに失敗: ' + gl.getProgramInfoLog(prog));
        return false;
      }
      gl.useProgram(prog);
      buf = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
      gl.enableVertexAttribArray(0);
      gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
      for (var i = 0; i < UNIFORMS.length; i++) U[UNIFORMS[i]] = gl.getUniformLocation(prog, UNIFORMS[i]);
      gl.disable(gl.DEPTH_TEST);
      gl.disable(gl.BLEND);
      uploadColors();
      uploadSafe();
      gl.uniform1f(U.uSeed, num(o.seed) ? o.seed : 0);
      gl.viewport(0, 0, canvas.width, canvas.height);
      return true;
    }

    function uploadColors() {
      if (!gl || !prog || !colorsLin) return;
      var c = colorsLin;
      gl.uniform3f(U.uNavyTop, c.navyTop[0], c.navyTop[1], c.navyTop[2]);
      gl.uniform3f(U.uNavyBottom, c.navyBottom[0], c.navyBottom[1], c.navyBottom[2]);
      gl.uniform3f(U.uWhiteTop, c.whiteTop[0], c.whiteTop[1], c.whiteTop[2]);
      gl.uniform3f(U.uWhiteBottom, c.whiteBottom[0], c.whiteBottom[1], c.whiteBottom[2]);
      gl.uniform3f(U.uDeep, c.deep[0], c.deep[1], c.deep[2]);
      gl.uniform3f(U.uBlue, c.blue[0], c.blue[1], c.blue[2]);
      gl.uniform3f(U.uCyan, c.cyan[0], c.cyan[1], c.cyan[2]);
      gl.uniform3f(U.uViolet, c.violet[0], c.violet[1], c.violet[2]);
      gl.uniform3f(U.uAbsBlue, c.absBlue[0], c.absBlue[1], c.absBlue[2]);
      gl.uniform3f(U.uAbsCyan, c.absCyan[0], c.absCyan[1], c.absCyan[2]);
      gl.uniform3f(U.uAbsViolet, c.absViolet[0], c.absViolet[1], c.absViolet[2]);
    }

    function releaseGL() {
      if (!gl) return;
      if (buf) gl.deleteBuffer(buf);
      if (prog) gl.deleteProgram(prog);
      buf = null; prog = null;
    }

    // WebGL が使えない環境では CSS のグラデーションで代用する (動かない)
    function useFallback() {
      releaseGL();
      if (canvas && canvas.parentNode) canvas.parentNode.removeChild(canvas);
      fallbackEl = doc.createElement('div');
      fallbackEl.className = o.className + ' energy-field--fallback';
      fallbackEl.setAttribute('aria-hidden', 'true');
      fallbackEl.style.cssText = canvas.style.cssText;
      container.insertBefore(fallbackEl, container.firstChild);
      canvas = null; gl = null;
      ctl.canvas = null;
      ctl.stats.mode = 'fallback';
      paintFallback();
      resolveReady(ctl);
    }

    function paintFallback() {
      if (!fallbackEl) return;
      var white = tgt.theme > 0.5;
      var a = clamp(tgt.intensity, 0, 1);
      var px = (tgt.x * 100).toFixed(1) + '% ' + (tgt.y * 100).toFixed(1) + '%';
      var size = (tgt.radius * 160).toFixed(0) + 'vh';
      fallbackEl.style.background = white
        ? 'radial-gradient(' + size + ' circle at ' + px + ', rgba(47,107,255,' + (0.16 * a).toFixed(3) + '), rgba(124,92,255,' + (0.06 * a).toFixed(3) + ') 45%, transparent 70%), linear-gradient(#FFFFFF, #F2F5FB)'
        : 'radial-gradient(' + size + ' circle at ' + px + ', rgba(120,170,255,' + (0.42 * a).toFixed(3) + '), rgba(47,107,255,' + (0.22 * a).toFixed(3) + ') 30%, rgba(26,60,158,' + (0.12 * a).toFixed(3) + ') 55%, transparent 75%), linear-gradient(#0B1736, #050B1F)';
    }

    // ---------------- state ----------------
    function set(next, opts) {
      if (destroyed || !next) return ctl;
      if (typeof next === 'string') next = { preset: next };
      if (next.preset != null) {
        presetName = resolvePresetName(next.preset);
        var p = PRESETS[presetName];
        for (var i = 0; i < NUM_KEYS.length; i++) tgt[NUM_KEYS[i]] = p[NUM_KEYS[i]];
        ctl.stats.preset = presetName;
      }
      if (next.theme != null) {
        tgt.theme = (next.theme === 'white' || next.theme === 1) ? 1 : 0;
        ctl.stats.theme = tgt.theme ? 'white' : 'navy';
      }
      for (var j = 0; j < NUM_KEYS.length; j++) {
        var key = NUM_KEYS[j];
        if (num(next[key])) tgt[key] = next[key];
      }
      tgt.intensity = clamp(tgt.intensity, 0, 1.5);
      tgt.cap = clamp(tgt.cap, 0.01, 1);
      tgt.floor = clamp(tgt.floor, 0, 0.99);
      tgt.radius = clamp(tgt.radius, 0.02, 3);
      if (next.colors) { o.colors = next.colors; readColors(); uploadColors(); }
      var instant = (opts && opts.instant) || frozen !== null || staticMode;
      if (instant) snap();
      if (next.protect !== undefined) protectTarget = next.protect;
      if (protectTarget) { updateSafe(instant); scheduleRecheck(); }
      if (fallbackEl) paintFallback();
      wake();
      return ctl;
    }

    // ---------------- 文字を守る範囲 ----------------
    function protect(target) {
      if (target !== undefined) protectTarget = target;
      updateSafe(frozen !== null || staticMode);
      scheduleRecheck();
      wake();
      return ctl;
    }

    // 出だしのアニメーションで文字が動くことがあるので、少し後にもう一度測る
    function scheduleRecheck() {
      if (recheckTimer) root.clearTimeout(recheckTimer);
      if (!protectTarget || destroyed) return;
      recheckTimer = root.setTimeout(function () { recheckTimer = 0; updateSafe(false); wake(); }, 700);
    }

    function textRects(el, out) {
      var walker = doc.createTreeWalker(el, 4 /* NodeFilter.SHOW_TEXT */, null);
      var range = doc.createRange();
      var n;
      while ((n = walker.nextNode())) {
        if (!/\S/.test(n.nodeValue)) continue;
        var parent = n.parentElement;
        if (!parent) continue;
        var cs = root.getComputedStyle(parent);
        if (cs.visibility === 'hidden' || cs.display === 'none') continue;
        range.selectNodeContents(n);
        var rs = range.getClientRects();
        for (var i = 0; i < rs.length; i++) {
          if (rs[i].width > 1 && rs[i].height > 1) out.push([rs[i].left, rs[i].top, rs[i].right, rs[i].bottom]);
        }
      }
    }

    function collect(target) {
      var items = [];
      if (typeof target === 'string') items = Array.prototype.slice.call(doc.querySelectorAll(target));
      else if (target && target.nodeType === 1) items = [target];
      else if (target && typeof target.length === 'number') items = Array.prototype.slice.call(target);
      var out = [];
      for (var i = 0; i < items.length; i++) {
        var it = items[i];
        if (it && it.nodeType === 1) textRects(it, out);
        else if (it && num(it.left) && num(it.top)) {
          out.push([it.left, it.top, num(it.right) ? it.right : it.left + it.width, num(it.bottom) ? it.bottom : it.top + it.height]);
        }
      }
      return out;
    }

    function union(a, b) { return [Math.min(a[0], b[0]), Math.min(a[1], b[1]), Math.max(a[2], b[2]), Math.max(a[3], b[3])]; }
    function area(a) { return Math.max(0, a[2] - a[0]) * Math.max(0, a[3] - a[1]); }
    function near(a, b) {
      var g = 0.6 * Math.min(a[3] - a[1], b[3] - b[1]);
      return a[0] - g <= b[2] && b[0] - g <= a[2] && a[1] - g <= b[3] && b[1] - g <= a[3];
    }

    // 同じ段落の行をまとめ、多すぎるときは増える面積が小さい組から合わせて 8 個以内にする
    function mergeRects(list) {
      var changed = true, i, j;
      while (changed) {
        changed = false;
        for (i = 0; i < list.length && !changed; i++) {
          for (j = i + 1; j < list.length; j++) {
            if (near(list[i], list[j])) { list[i] = union(list[i], list[j]); list.splice(j, 1); changed = true; break; }
          }
        }
      }
      while (list.length > 8) {
        var best = Infinity, bi = 0, bj = 1;
        for (i = 0; i < list.length; i++) {
          for (j = i + 1; j < list.length; j++) {
            var cost = area(union(list[i], list[j])) - area(list[i]) - area(list[j]);
            if (cost < best) { best = cost; bi = i; bj = j; }
          }
        }
        list[bi] = union(list[bi], list[bj]);
        list.splice(bj, 1);
      }
      return list;
    }

    function updateSafe(instant) {
      if (!canvas && !fallbackEl) return;
      var el = canvas || fallbackEl;
      var cr = el.getBoundingClientRect();
      if (!cr.width || !cr.height) return;
      var list = protectTarget ? mergeRects(collect(protectTarget)) : [];
      var pad = 0.012 * cr.height;
      var next = new Float32Array(32);
      for (var i = 0; i < list.length; i++) {
        var r = list[i];
        next[i * 4] = (r[0] - pad - cr.left) / cr.width;
        next[i * 4 + 1] = 1 - (r[3] + pad - cr.top) / cr.height;
        next[i * 4 + 2] = (r[2] + pad - cr.left) / cr.width;
        next[i * 4 + 3] = 1 - (r[1] - pad - cr.top) / cr.height;
      }
      var same = list.length === safeNB;
      for (var k = 0; same && k < list.length * 4; k++) if (Math.abs(next[k] - safeB[k]) > 1e-4) same = false;
      if (same) return;
      if (instant) {
        safeNA = 0;
        safeT = 1;
      } else {
        safeA.set(safeB);
        safeNA = safeNB;
        safeT = 0;
      }
      safeB.set(next);
      safeNB = list.length;
      uploadSafe();
    }

    function uploadSafe() {
      if (!gl || !prog) return;
      gl.uniform4fv(U.uSafeA, safeA);
      gl.uniform4fv(U.uSafeB, safeB);
      gl.uniform1f(U.uSafeNA, safeNA);
      gl.uniform1f(U.uSafeNB, safeNB);
      gl.uniform1f(U.uSafeCap, clamp(o.safeCap, 0.005, 1));
      gl.uniform1f(U.uSafeFloor, clamp(o.safeFloor, 0, 0.99));
      gl.uniform1f(U.uFeather, 0.06);
    }

    function snap() {
      for (var i = 0; i < NUM_KEYS.length; i++) cur[NUM_KEYS[i]] = tgt[NUM_KEYS[i]];
      cur.theme = tgt.theme;
      safeT = 1;
    }

    function pulse(amount) {
      pulseV = Math.min(0.5, pulseV + (num(amount) ? amount : 0.25));
      wake();
      return ctl;
    }

    function freeze(t) {
      frozen = num(t) ? t : null;
      if (frozen !== null) snap();
      wake();
      return ctl;
    }

    // いまの値 (検証・調整用)
    function state() {
      var out = { preset: presetName, running: running, paused: paused, still: isStill(), protectedAreas: safeNB };
      for (var i = 0; i < NUM_KEYS.length; i++) out[NUM_KEYS[i]] = cur[NUM_KEYS[i]];
      out.theme = cur.theme;
      return out;
    }

    function pause() { paused = true; stop(); return ctl; }
    function resume() { paused = false; wake(); return ctl; }

    function syncFromAttributes() {
      var ds = doc.documentElement.dataset;
      var next = {};
      var any = false;
      if (ds.energy) { next.preset = ds.energy; any = true; }
      if (ds.energyTheme) { next.theme = ds.energyTheme; any = true; }
      if (any) set(next);
    }

    function onEvent(e) { if (e && e.detail) set(e.detail, e.detail); }

    function onReduceChange() {
      staticMode = (mqReduce && mqReduce.matches) || o.mode === 'static';
      if (staticMode) snap();
      wake();
    }

    function onVisibility() {
      if (doc.hidden) stop();
      else wake();
    }

    function onContextLost(e) {
      e.preventDefault();
      lost = true;
      stop();
      buf = null; prog = null;
    }

    function onContextRestored() {
      lost = false;
      if (initGL()) { resize(); wake(); }
    }

    // ---------------- loop ----------------
    function isStill() {
      // 止まった絵で良い状態 (静止モード、時間停止、または完全に消えている)
      if (staticMode || frozen !== null) return true;
      if (tgt.intensity > 0 || tgt.aurora > 0 || pulseV > 0.0005 || safeT < 1) return false;
      if (Math.abs(cur.theme - tgt.theme) > 1e-4) return false;
      // シェーダーは 0.002 以下を描かないので、ここまで下がれば絵は動かない
      return cur.intensity <= 0.002 && cur.aurora <= 0.002;
    }

    function wake() {
      if (destroyed || paused || lost || !gl || (doc.hidden && !isStill())) return;
      if (isStill()) { requestRender(); return; }
      start();
    }

    function start() {
      if (running || destroyed || paused || lost || !gl) return;
      if (isStill()) { requestRender(); return; }
      if (rafOnce) { root.cancelAnimationFrame(rafOnce); rafOnce = 0; }
      running = true;
      lastTick = 0;
      lastDraw = 0;
      rafLoop = root.requestAnimationFrame(frame);
    }

    function stop() {
      running = false;
      if (rafLoop) { root.cancelAnimationFrame(rafLoop); rafLoop = 0; }
      if (rafOnce) { root.cancelAnimationFrame(rafOnce); rafOnce = 0; }
    }

    function requestRender() {
      if (destroyed || lost || !gl || running || rafOnce) return;
      rafOnce = root.requestAnimationFrame(renderOnce);
    }

    function renderOnce(now) {
      rafOnce = 0;
      if (destroyed || lost || !gl) return;
      snapIfStill();
      draw(currentTime(now));
      if (!isStill()) start();
    }

    function snapIfStill() { if (staticMode || frozen !== null) snap(); }

    function frame(now) {
      rafLoop = 0;
      if (!running) return;
      rafLoop = root.requestAnimationFrame(frame);
      if (lastDraw && now - lastDraw < frameInterval - 1.5) return;
      var dt = lastTick ? (now - lastTick) / 1000 : 0;
      if (dt > 0.1) dt = 0.1;
      lastTick = now;
      if (lastDraw) trackQuality(now - lastDraw);
      lastDraw = now;
      step(dt);
      draw(currentTime(now));
      if (isStill()) { snap(); stop(); }
    }

    function currentTime(now) {
      if (frozen !== null) return frozen;
      return (timeOrigin + now - t0) / 1000;
    }

    // duration 秒でおよそ 95% 目標に近づく指数イーズ
    function ease(key, dt, duration) {
      cur[key] += (tgt[key] - cur[key]) * (1 - Math.exp(-3 * dt / duration));
    }

    function step(dt) {
      if (dt <= 0) return;
      var tf = Math.max(0.05, o.fadeDuration), tm = Math.max(0.05, o.moveDuration), tt = Math.max(0.02, o.themeDuration);
      ease('intensity', dt, tf);
      ease('cap', dt, tf);
      ease('floor', dt, tf);
      ease('aurora', dt, tf);
      ease('particles', dt, tf);
      ease('x', dt, tm);
      ease('y', dt, tm);
      ease('radius', dt, tm);
      cur.theme += (tgt.theme - cur.theme) * (1 - Math.exp(-3 * dt / tt));
      if (Math.abs(cur.theme - tgt.theme) < 1e-3) cur.theme = tgt.theme;
      pulseV *= Math.exp(-dt / 1.1);
      if (pulseV < 0.0005) pulseV = 0;
      if (safeT < 1) safeT = Math.min(1, safeT + dt / Math.max(0.05, o.protectFade));
    }

    function draw(t) {
      if (!gl || !prog) return;
      var breath = 0.5 + 0.5 * (0.62 * Math.sin(TAU * t / 26) + 0.38 * Math.sin(TAU * t / 37 + 1.7));
      var ax = cur.x + 0.012 * Math.sin(TAU * t / 53 + 0.4);
      var ay = cur.y + 0.010 * Math.sin(TAU * t / 71 + 1.9);
      gl.uniform2f(U.uRes, canvas.width, canvas.height);
      gl.uniform1f(U.uTime, t);
      gl.uniform1f(U.uRot, (t * 0.022) % TAU);
      gl.uniform1f(U.uTwT, t % (200 * Math.PI));
      gl.uniform2f(U.uAnchor, ax, 1 - ay);
      gl.uniform1f(U.uRadius, cur.radius * (1 + 0.06 * (breath - 0.5)));
      gl.uniform1f(U.uIntensity, cur.intensity + pulseV);
      gl.uniform1f(U.uBreath, breath);
      gl.uniform1f(U.uTheme, cur.theme);
      gl.uniform1f(U.uCap, cur.cap);
      gl.uniform1f(U.uFloor, cur.floor);
      gl.uniform1f(U.uAurora, cur.aurora);
      gl.uniform1f(U.uParticles, cur.particles);
      gl.uniform1f(U.uSafeT, safeT * safeT * (3 - 2 * safeT));
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      ctl.stats.frames++;
      if (ctl.stats.frames === 1) resolveReady(ctl);
      countFps();
    }

    function countFps() {
      var now = root.performance ? root.performance.now() : Date.now();
      fpsCount++;
      if (!fpsAt) fpsAt = now;
      if (now - fpsAt >= 1000) {
        ctl.stats.fps = Math.round(fpsCount * 1000 / (now - fpsAt));
        fpsCount = 0;
        fpsAt = now;
      }
      if (debugEl && now - debugAt > 500) {
        debugAt = now;
        debugEl.textContent = 'energy ' + ctl.stats.fps + 'fps ' + canvas.width + 'x' + canvas.height + ' ' + presetName + ' I=' + cur.intensity.toFixed(2) + (cur.theme > 0.5 ? ' white' : ' navy');
      }
    }

    // 描画が目標の 1.6 倍以上遅い状態が続いたら解像度を下げる (上げ直しはしない)
    function trackQuality(interval) {
      if (!o.autoQuality || frozen !== null) return;
      if (interval > 500) return;
      emaInterval = emaInterval ? emaInterval * 0.9 + interval * 0.1 : interval;
      if (emaInterval > frameInterval * 1.6) slowFrames++;
      else slowFrames = 0;
      if (slowFrames > 90 && scale > 0.26) {
        scale = Math.max(0.25, scale * 0.8);
        slowFrames = 0;
        emaInterval = 0;
        ctl.stats.scale = scale;
        warnOnce('quality:' + scale.toFixed(2), '描画が重いので解像度を ' + Math.round(scale * 100) + '% に下げました');
        resize();
      }
    }

    function resize() {
      if (!canvas) return;
      var w = isBody ? root.innerWidth : container.clientWidth;
      var h = isBody ? root.innerHeight : container.clientHeight;
      if (!w || !h) return;
      var W = Math.max(2, Math.round(w * scale));
      var H = Math.max(2, Math.round(h * scale));
      if (W * H > o.maxPixels) {
        var f = Math.sqrt(o.maxPixels / (W * H));
        W = Math.max(2, Math.round(W * f));
        H = Math.max(2, Math.round(H * f));
      }
      if (canvas.width !== W || canvas.height !== H) {
        canvas.width = W;
        canvas.height = H;
      }
      ctl.stats.width = W;
      ctl.stats.height = H;
      if (protectTarget) updateSafe(true);
      if (gl) {
        gl.viewport(0, 0, W, H);
        if (!running) requestRender();
      }
    }

    function destroy() {
      if (destroyed) return;
      destroyed = true;
      stop();
      if (recheckTimer) root.clearTimeout(recheckTimer);
      if (mo) mo.disconnect();
      if (ro) ro.disconnect();
      if (mqReduce && mqReduce.removeEventListener) mqReduce.removeEventListener('change', onReduceChange);
      root.removeEventListener('energyfield', onEvent);
      root.removeEventListener('resize', resize);
      doc.removeEventListener('visibilitychange', onVisibility);
      if (canvas) {
        canvas.removeEventListener('webglcontextlost', onContextLost, false);
        canvas.removeEventListener('webglcontextrestored', onContextRestored, false);
      }
      releaseGL();
      if (gl) {
        var ext = gl.getExtension('WEBGL_lose_context');
        if (ext) ext.loseContext();
      }
      gl = null;
      if (canvas && canvas.parentNode) canvas.parentNode.removeChild(canvas);
      if (fallbackEl && fallbackEl.parentNode) fallbackEl.parentNode.removeChild(fallbackEl);
      if (debugEl && debugEl.parentNode) debugEl.parentNode.removeChild(debugEl);
      if (restoreStyles && container) {
        container.style.position = restoreStyles.position;
        container.style.isolation = restoreStyles.isolation;
      }
      doc.documentElement.classList.remove('energy-field-on');
      if (root.EnergyField.current === ctl) root.EnergyField.current = null;
    }
  }

  // ------------------------------------------------------------------
  // コントラスト比 (WCAG)。資料側の検品にも使える。
  // ------------------------------------------------------------------
  function contrast(hexA, hexB) {
    var a = hexToLinear(hexA, '#000000'), b = hexToLinear(hexB, '#000000');
    var la = 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2];
    var lb = 0.2126 * b[0] + 0.7152 * b[1] + 0.0722 * b[2];
    var hi = Math.max(la, lb), lo = Math.min(la, lb);
    return (hi + 0.05) / (lo + 0.05);
  }

  // 画面の種類ごとに「どこに重なっても下回らないコントラスト」を返す
  function guarantee(presetName, textHex) {
    var p = PRESETS[resolvePresetName(presetName)];
    var t = hexToLinear(textHex, '#FFFFFF');
    var lt = 0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2];
    return {
      navy: (Math.max(lt, p.cap) + 0.05) / (Math.min(lt, p.cap) + 0.05),
      white: (Math.max(lt, p.floor) + 0.05) / (Math.min(lt, p.floor) + 0.05)
    };
  }

  root.EnergyField = {
    version: VERSION,
    mount: mount,
    presets: PRESETS,
    aliases: ALIASES,
    contrast: contrast,
    guarantee: guarantee,
    current: null
  };
})(typeof window !== 'undefined' ? window : this);
