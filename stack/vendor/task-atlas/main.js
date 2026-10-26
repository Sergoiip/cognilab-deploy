/* Task Atlas — lienzo infinito para tareas de TaskNotes (una nota = una tarea).
   Conexión padre→hijo = el hijo lista al padre en su frontmatter `projects`. */
const { Plugin, ItemView, Modal, Menu, Notice, Setting, PluginSettingTab, FuzzySuggestModal, debounce } = require('obsidian');

const VIEW = 'task-atlas';
const SVGNS = 'http://www.w3.org/2000/svg';
const STATUSES = [
  { id: 'in-progress', label: 'En progreso', color: '#3b82f6' },
  { id: 'open', label: 'Abierta', color: '#9aa0a6' },
  { id: 'done', label: 'Hecha', color: '#22c55e' },
];
const PRIOS = [
  { id: 'high', label: 'Alta', color: '#ef4444' },
  { id: 'normal', label: 'Normal', color: '#f59e0b' },
  { id: 'low', label: 'Baja', color: '#22c55e' },
  { id: 'none', label: 'Sin prioridad', color: '#888888' },
];
const stColor = (s) => (STATUSES.find((x) => x.id === s) || STATUSES[1]).color;
const prColor = (p) => (PRIOS.find((x) => x.id === p) || PRIOS[3]).color;
const NW = 250, GX = 320, GY = 112;

const pad = (n) => String(n).padStart(2, '0');
function today() { const d = new Date(); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`; }
function isoNow() {
  const d = new Date(), o = -d.getTimezoneOffset(), s = o >= 0 ? '+' : '-';
  return `${today()}T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}.${String(d.getMilliseconds()).padStart(3, '0')}${s}${pad(Math.floor(Math.abs(o) / 60))}:${pad(Math.abs(o) % 60)}`;
}
function flat(v) { return Array.isArray(v) ? v.flatMap(flat) : v == null ? [] : [v]; }
// projects puede venir como ["[[A]]"] o, si no tiene comillas, como [[["A"]]]
function projectLinks(v) {
  const out = [];
  const walk = (x, depth) => {
    if (Array.isArray(x)) {
      if (depth >= 1 && x.length === 1 && Array.isArray(x[0]) && typeof x[0][0] === 'string') { out.push(`[[${x[0][0]}]]`); return; }
      x.forEach((y) => walk(y, depth + 1));
    } else if (typeof x === 'string') out.push(x);
  };
  walk(v, 0);
  return out;
}
function parseLink(s) { const m = /\[\[([^\]|#]+)/.exec(s); return m ? m[1].trim() : null; }
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

class AddModal extends Modal {
  constructor(app, opts, onSubmit) { super(app); this.opts = opts; this.onSubmit = onSubmit; }
  onOpen() {
    const { contentEl } = this;
    contentEl.createEl('h3', { text: this.opts.title });
    const input = contentEl.createEl('input', { type: 'text', placeholder: this.opts.placeholder || 'Escribe aquí…' });
    input.style.width = '100%';
    const row = contentEl.createDiv({ cls: 'tka-modal-row' });
    let sel = null, date = null;
    if (this.opts.options) { sel = row.createEl('select'); this.opts.options.forEach(([v, l]) => sel.createEl('option', { value: v, text: l })); }
    if (this.opts.date) { date = row.createEl('input', { type: 'date' }); date.value = today(); }
    const btn = row.createEl('button', { text: 'Añadir', cls: 'mod-cta' });
    const go = () => { const t = input.value.trim(); if (!t) return; this.close(); this.onSubmit(t, sel && sel.value, date && date.value); };
    btn.onclick = go; input.addEventListener('keydown', (e) => { if (e.key === 'Enter') go(); });
    setTimeout(() => input.focus(), 30);
  }
  onClose() { this.contentEl.empty(); }
}
class NotePicker extends FuzzySuggestModal {
  constructor(app, onPick) { super(app); this.onPick = onPick; this.setPlaceholder('Buscar nota clave para enlazar…'); }
  getItems() { return this.app.vault.getMarkdownFiles().filter((f) => !f.path.startsWith('TaskNotes/') && !f.path.startsWith('daily/')); }
  getItemText(f) { return f.path.replace(/\.md$/, ''); }
  onChooseItem(f) { this.onPick(f); }
}
class NewTaskModal extends Modal {
  constructor(app, opts, onSubmit) { super(app); this.opts = opts; this.onSubmit = onSubmit; }
  onOpen() {
    const { contentEl } = this;
    contentEl.createEl('h3', { text: this.opts.parentTitle ? `Nueva tarea  ←  ${this.opts.parentTitle}` : 'Nueva tarea' });
    const input = contentEl.createEl('input', { type: 'text', placeholder: 'Título de la tarea…' });
    input.style.width = '100%';
    const row = contentEl.createDiv({ cls: 'tka-modal-row' });
    const sel = row.createEl('select');
    PRIOS.slice(0, 3).forEach((p) => sel.createEl('option', { value: p.id, text: 'Prioridad: ' + p.label }));
    sel.value = 'normal';
    const date = row.createEl('input', { type: 'date' });
    date.value = today();
    const btn = row.createEl('button', { text: 'Crear', cls: 'mod-cta' });
    const go = () => {
      const t = input.value.trim();
      if (!t) return;
      this.close();
      this.onSubmit(t, sel.value, date.value);
    };
    btn.onclick = go;
    input.addEventListener('keydown', (e) => { if (e.key === 'Enter') go(); });
    setTimeout(() => input.focus(), 30);
  }
  onClose() { this.contentEl.empty(); }
}

class TaskSpaceView extends ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
    this.model = { nodes: new Map(), edges: [] };
    this.els = new Map();
    this.sel = new Set();
    this.dragging = false;
    this.q = '';
    this.refreshSoon = debounce(() => { if (!this.dragging) this.refresh(); }, 350, true);
  }
  getViewType() { return VIEW; }
  getDisplayText() { return 'Task Atlas'; }
  getIcon() { return 'network'; }
  get D() { return this.plugin.data; }
  get S() { return this.plugin.data.settings; }

  async onOpen() {
    const root = this.contentEl;
    root.empty();
    root.addClass('tka-root');
    this.side = root.createDiv('tka-side');
    this.stage = root.createDiv('tka-stage');
    this.world = this.stage.createDiv('tka-world');
    this.svg = document.createElementNS(SVGNS, 'svg');
    this.svg.classList.add('tka-edges');
    const defs = document.createElementNS(SVGNS, 'defs');
    defs.innerHTML = '<marker id="tka-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="tka-arrow-p"/></marker>';
    this.svg.appendChild(defs);
    this.edgeG = document.createElementNS(SVGNS, 'g');
    this.svg.appendChild(this.edgeG);
    this.world.appendChild(this.svg);
    this.layer = this.world.createDiv('tka-layer');
    this.buildTools();
    this.bindStage();
    const ev = this.app.metadataCache, vt = this.app.vault;
    this.registerEvent(ev.on('changed', () => this.refreshSoon()));
    this.registerEvent(vt.on('create', () => this.refreshSoon()));
    this.registerEvent(vt.on('delete', () => this.refreshSoon()));
    this.registerEvent(vt.on('rename', (f, old) => {
      if (this.D.pos[old]) { this.D.pos[f.path] = this.D.pos[old]; delete this.D.pos[old]; this.plugin.saveSoon(); }
      this.refreshSoon();
    }));
    this.applyView();
    this.refresh(true);
  }
  async onClose() { this.plugin.saveSoon.cancel && this.plugin.saveSoon.cancel(); await this.plugin.saveData(this.D); }

  // ---------- modelo ----------
  buildRoadmapModel() {
    const MC = this.app.metadataCache, folder = this.S.tasksFolder.replace(/\/+$/, ''), mf = (this.S.metasFolder || 'Roadmap/Metas').replace(/\/+$/, '');
    const fmOf = (f) => (MC.getFileCache(f) || {}).frontmatter || {};
    const nodes = new Map(), edges = [], all = this.app.vault.getMarkdownFiles();
    const link = (v, from) => { const l = parseLink(flat(v)[0] || ''); return l && MC.getFirstLinkpathDest(l, from); };
    for (const f of all) {
      if (!f.path.startsWith(mf + '/') || f.path.includes('/archivo/')) continue;
      const fm = fmOf(f); if (fm.type !== 'meta' && fm.type !== 'norte') continue;
      if (fm.type === 'norte' && this.S.scope === 'habitos') continue;
      nodes.set(f.path, { path: f.path, file: f, type: fm.type, title: fm.nombre || f.basename, status: 'note', priority: 'none', color: fm.color || null, medida: flat(fm.medida), hoy: fm.hoy || '', resultado: fm.resultado || '', fase: fm.fase || '', faseNum: Number(fm.faseNum) || 9, fecha: fm.fecha || '', responsable: fm.responsable || '', orden: Number(fm.orden) || 99 });
    }
    const HB = this.S.scope === 'habitos';
    const tasks = all.filter((f) => f.path.startsWith(folder + '/') && fmOf(f).meta && ((fmOf(f).tipo === 'habito') === HB) && (HB || fmOf(f).clave === true));
    for (const f of tasks) {
      const fm = fmOf(f), md = link(fm.meta, f.path);
      if (!md || !nodes.has(md.path)) continue;
      let st = fm.status || 'open'; if (st === 'none') st = 'idea';
      nodes.set(f.path, { path: f.path, file: f, type: 'task', title: fm.title || f.basename, status: st, priority: fm.priority || 'none', due: fm.due || null, scheduled: fm.scheduled || null, responsable: fm.responsable || '', meta: md.path, habito: fm.habito || '', medida: flat(fm.medida) });
    }
    const hasOut = new Set();
    for (const f of tasks) {
      if (!nodes.has(f.path)) continue;
      for (const l of flat(fmOf(f).depende_de)) {
        const lp = parseLink(String(l)), d = lp && MC.getFirstLinkpathDest(lp, f.path);
        if (d && nodes.has(d.path) && d.path !== f.path) { edges.push({ from: d.path, to: f.path, kind: 'dep' }); hasOut.add(d.path); }
      }
    }
    for (const n of [...nodes.values()]) {
      if (n.type === 'task' && !hasOut.has(n.path)) edges.push({ from: n.path, to: n.meta, kind: 'goal' });
      if (n.type === 'meta') { const nd = link(fmOf(n.file).alimenta, n.path); if (nd && nodes.has(nd.path)) edges.push({ from: n.path, to: nd.path, kind: 'feed' }); }
    }
    const inc = new Map();
    edges.filter((e) => e.kind === 'dep').forEach((e) => { if (!inc.has(e.to)) inc.set(e.to, []); inc.get(e.to).push(e.from); });
    for (const n of nodes.values()) {
      if (n.type !== 'task') continue;
      n.blocked = (inc.get(n.path) || []).some((d) => (nodes.get(d) || {}).status !== 'done');
      n.ready = !n.blocked && (n.status === 'open' || n.status === 'in-progress');
      n.waits = (inc.get(n.path) || []).filter((d) => (nodes.get(d) || {}).status !== 'done').length;
    }
    for (const m of nodes.values()) {
      if (m.type !== 'meta') continue;
      const ts = [...nodes.values()].filter((t) => t.type === 'task' && t.meta === m.path && t.status !== 'idea');
      m.total = ts.length; m.done = ts.filter((t) => t.status === 'done').length;
      m.ideas = [...nodes.values()].filter((t) => t.type === 'task' && t.meta === m.path && t.status === 'idea').length;
    }
    if (HB) for (const m of [...nodes.values()]) if (m.type === 'meta' && !m.total) nodes.delete(m.path);
    this.model = { nodes, edges };
  }
  habitsLayout() {
    const nodes = this.vis(), pos = this.D.pos, COLW = 276, RH = 80, HW = 320, GAP = 28;
    const metas = [...nodes.values()].filter((n) => n.type === 'meta').sort((a, b) => a.faseNum - b.faseNum);
    const FR = ['diario', 'semanal', 'mensual'];
    const metaX = HW + 3 * COLW + 30; let y = 0;
    for (const m of metas) {
      const ts = [...nodes.values()].filter((t) => t.type === 'task' && t.meta === m.path);
      const cols = FR.map((f) => ts.filter((t) => t.habito === f).sort((a, b) => a.title.localeCompare(b.title)));
      const stack = Math.max(1, ...cols.map((c) => c.length)), inner = Math.max(stack * RH, 300), h = inner + 56;
      cols.forEach((arr, ci) => arr.forEach((t, i) => { pos[t.path] = { x: HW + ci * COLW, y: y + 38 + i * RH }; }));
      pos[m.path] = { x: metaX, y: y + 28 + inner / 2 - 60 };
      (this.D['lanes_' + this.S.scope] = this.D['lanes_' + this.S.scope] || {})[m.path] = { x: -18, y, w: metaX + 280 + 54, h };
      y += h + GAP;
    }
  }
  buildOpsModel() {
    const folder = this.S.tasksFolder.replace(/\/+$/, ''), CL = this.S.scope === 'clientes', FIELD = CL ? 'cliente' : 'area';
    const af = (CL ? (this.S.clientesFolder || 'Clientes/Vista Task Atlas') : (this.S.areasFolder || 'Operaciones/Áreas')).replace(/\/+$/, '');
    const nodes = new Map(), edges = [], MC = this.app.metadataCache;
    const fmOf = (f) => (MC.getFileCache(f) || {}).frontmatter || {};
    const addNote = (dest, type) => {
      if (nodes.has(dest.path)) return nodes.get(dest.path);
      const fm = fmOf(dest);
      const n = { path: dest.path, file: dest, type, title: fm.nombre || dest.basename, status: 'note', priority: 'none', color: fm.color || null, responsable: fm.responsable || '', tipo: fm.tipo || '', orden: Number(fm.orden) || 99 };
      nodes.set(dest.path, n);
      if (type !== 'hub') {
        const hl = parseLink(flat(fm.padre)[0] || '');
        const hd = hl && MC.getFirstLinkpathDest(hl, dest.path);
        if (hd) { const ht = fmOf(hd).type; addNote(hd, ht === 'hub' || ht === 'cliente' ? ht : 'area'); edges.push({ from: hd.path, to: dest.path }); }
      }
      return n;
    };
    for (const f of this.app.vault.getMarkdownFiles()) if (f.path.startsWith(af + '/') && ['area', 'cliente'].includes(fmOf(f).type)) addNote(f, fmOf(f).type);
    const files = this.app.vault.getMarkdownFiles().filter((f) => f.path.startsWith(folder + '/') && fmOf(f)[FIELD]);
    for (const f of files) {
      const fm = fmOf(f);
      let st = fm.status || 'open'; if (st === 'none') st = 'open';
      nodes.set(f.path, { path: f.path, file: f, type: 'task', title: fm.title || f.basename, status: st, priority: fm.priority || 'none', due: fm.due || null, scheduled: fm.scheduled || null, responsable: fm.responsable || '' });
    }
    for (const f of files) {
      const fm = fmOf(f);
      const al = parseLink(flat(fm[FIELD])[0] || ''), ad = al && MC.getFirstLinkpathDest(al, f.path);
      if (ad) { addNote(ad, CL ? 'cliente' : 'area'); edges.push({ from: ad.path, to: f.path }); }
      for (const l of projectLinks(fm.projects)) {
        const lp = parseLink(l); if (!lp) continue;
        const dest = MC.getFirstLinkpathDest(lp, f.path);
        if (dest && dest.path !== f.path && nodes.has(dest.path) && nodes.get(dest.path).type === 'task') edges.push({ from: dest.path, to: f.path });
      }
    }
    edges.sort((a, b) => ((nodes.get(a.to) || {}).orden || 0) - ((nodes.get(b.to) || {}).orden || 0));
    this.model = { nodes, edges };
  }
  buildModel() {
    const folder = this.S.tasksFolder.replace(/\/+$/, '');
    const nodes = new Map(), edges = [];
    if (this.rm()) this.buildRoadmapModel();
    else if (this.S.scope === 'operaciones' || this.S.scope === 'clientes') this.buildOpsModel();
    else {
    const files = this.app.vault.getMarkdownFiles().filter((f) => f.path.startsWith(folder + '/'));
    for (const f of files) {
      const fm = (this.app.metadataCache.getFileCache(f) || {}).frontmatter || {};
      let st = fm.status || 'open'; if (st === 'none') st = 'open';
      nodes.set(f.path, {
        path: f.path, file: f, type: 'task', title: fm.title || f.basename, status: st,
        priority: fm.priority || 'none', due: fm.due || null, scheduled: fm.scheduled || null,
      });
    }
    for (const f of files) {
      const fm = (this.app.metadataCache.getFileCache(f) || {}).frontmatter || {};
      for (const l of projectLinks(fm.projects)) {
        const lp = parseLink(l); if (!lp) continue;
        const dest = this.app.metadataCache.getFirstLinkpathDest(lp, f.path);
        if (!dest || dest.path === f.path) continue;
        if (!nodes.has(dest.path)) {
          nodes.set(dest.path, { path: dest.path, file: dest, type: 'note', title: dest.basename, status: 'note', priority: 'none' });
        }
        edges.push({ from: dest.path, to: f.path });
      }
    }
    this.model = { nodes, edges };
    }
    const { nodes: nodes2, edges: edges2 } = this.model;
    this.children = new Map(); this.parents = new Map();
    for (const e of edges2) {
      if (!this.children.has(e.from)) this.children.set(e.from, []);
      if (!this.parents.has(e.to)) this.parents.set(e.to, []);
      this.children.get(e.from).push(e.to); this.parents.get(e.to).push(e.from);
    }
    this.allowed = null;
    if (this.S.filter && nodes2.has(this.S.filter)) { this.allowed = this.descendants(this.S.filter); this.allowed.add(this.S.filter); }
    else if (this.S.filter) this.S.filter = '';
  }
  isVisible(n) {
    if (!n) return false;
    if (this.allowed && !this.allowed.has(n.path)) return false;
    if (n.path === this.S.filter) return true;
    if (n.type === 'area' || n.type === 'hub' || n.type === 'cliente' || n.type === 'meta' || n.type === 'norte') return true;
    if (n.type === 'note') return this.S.showNotes;
    return !(this.S.hideDone && n.status === 'done');
  }
  descendants(p) {
    const seen = new Set(), st = [p];
    while (st.length) { const c = st.pop(); for (const k of this.children.get(c) || []) if (!seen.has(k)) { seen.add(k); st.push(k); } }
    return seen;
  }

  // ---------- layout ----------
  vis() { return new Map([...this.model.nodes].filter(([p, n]) => this.isVisible(n))); }
  laneOf(p, nodes) {
    if (this.rm()) { const n0 = this.model.nodes.get(p); return !n0 || n0.type === 'norte' ? '__none' : n0.type === 'meta' ? p : n0.meta; }
    if (this.S.scope === 'operaciones' || this.S.scope === 'clientes') {
      const n0 = this.model.nodes.get(p);
      if (!n0 || n0.type === 'hub') return '__none';
      let c = p, g = 0;
      for (;;) {
        const pa0 = (this.parents.get(c) || []).map((q) => this.model.nodes.get(q)).find((q) => q && nodes.has(q.path));
        if (!pa0 || g++ > 20) return c;
        if (pa0.type === 'hub') return c;
        c = pa0.path;
      }
    }
    let c = p, g = 0;
    for (;;) { const pa = (this.parents.get(c) || []).find((q) => nodes.has(q)); if (!pa || g++ > 50) break; c = pa; }
    const has = (this.children.get(c) || []).some((q) => nodes.has(q));
    return has || c !== p ? c : '__none';
  }
  rm() { return this.S.scope === 'roadmap' || this.S.scope === 'habitos'; }
  scoped() { return this.S.scope === 'operaciones' || this.S.scope === 'clientes'; }
  boardLayout() {
    const nodes = this.vis(), pos = this.D.pos;
    const RH = 84, CW = NW + 46, TOP = 150;
    const rank = (n) => ({ 'in-progress': 0, open: 1, done: 2 }[n.status] ?? 1);
    const pr = { high: 0, normal: 1, low: 2, none: 3 };
    const dd = (n) => String(n.due || n.scheduled || '9999').slice(0, 10);
    const cmpT = (a, b) => rank(a) - rank(b) || (pr[a.priority] ?? 3) - (pr[b.priority] ?? 3) || dd(a).localeCompare(dd(b)) || a.title.localeCompare(b.title);
    const kidsOf = (p) => {
      const k = (this.children.get(p) || []).map((c) => nodes.get(c)).filter(Boolean);
      return [...k.filter((c) => c.type !== 'task').sort((a, b) => (a.orden || 99) - (b.orden || 99)), ...k.filter((c) => c.type === 'task').sort(cmpT)];
    };
    const visPar = (n) => (this.parents.get(n.path) || []).map((q) => nodes.get(q)).filter(Boolean);
    const tops = [...nodes.values()].filter((n) => n.type === 'area' && visPar(n).every((q) => q.type === 'hub')).sort((a, b) => (a.orden || 99) - (b.orden || 99));
    const placed = new Set();
    let maxCol = 0;
    tops.forEach((t, i) => {
      let y = TOP; const x0 = i * CW;
      const put = (n, dx) => {
        if (placed.has(n.path)) return; placed.add(n.path);
        if (n.type === 'cliente') y += 14;
        pos[n.path] = { x: x0 + dx, y }; y += RH;
        for (const c of kidsOf(n.path)) put(c, n.type === 'area' || (n.type === 'area' && c.type === 'cliente') ? 0 : dx + 14);
      };
      put(t, 0); maxCol = i + 1;
    });
    let y = TOP, x0 = maxCol * CW;
    for (const n of nodes.values()) if (n.type !== 'hub' && !placed.has(n.path)) { pos[n.path] = { x: x0, y }; y += RH; placed.add(n.path); }
    if (y > TOP) maxCol++;
    for (const n of nodes.values()) if (n.type === 'hub') pos[n.path] = { x: Math.max(0, (maxCol - 1) * CW / 2), y: 0 };
  }
  roadmapLayout() {
    const nodes = this.vis(), pos = this.D.pos, ch = this.children;
    const HW = 320, COLW = 276, RH = 80, MW = 280, GAP = 28, ROWS = 3;
    const metas = [...nodes.values()].filter((n) => n.type === 'meta').sort((a, b) => a.faseNum - b.faseNum || a.orden - b.orden);
    const norte = [...nodes.values()].find((n) => n.type === 'norte');
    const memo = new Map();
    const dist = (p, mp) => {
      if (memo.has(p)) return memo.get(p);
      memo.set(p, 0);
      const ks = (ch.get(p) || []).filter((c) => nodes.has(c) && (nodes.get(c).meta === mp));
      const d = ks.length ? 1 + Math.max(...ks.map((c) => dist(c, mp))) : 0;
      memo.set(p, d); return d;
    };
    const rank = (n) => ({ 'in-progress': 0, open: 1, idea: 3, done: 2 }[n.status] ?? 1);
    const pr = { high: 0, normal: 1, low: 2, none: 3 };
    const lanes = []; let maxSub = 1;
    for (const m of metas) {
      const ts = [...nodes.values()].filter((n) => n.type === 'task' && n.meta === m.path);
      const cols = new Map();
      for (const t of ts) { const d = dist(t.path, m.path); if (!cols.has(d)) cols.set(d, []); cols.get(d).push(t); }
      let sub = 0;
      for (const arr of cols.values()) sub += Math.ceil(arr.length / ROWS);
      maxSub = Math.max(maxSub, sub);
      lanes.push({ m, cols });
    }
    const metaX = HW + maxSub * COLW + 30;
    let y = 0, lastFase = null;
    for (const L of lanes) {
      const maxStack = Math.max(1, ...[...L.cols.values()].map((a) => Math.min(ROWS, a.length)));
      const inner = Math.max(maxStack * RH, 300), h = inner + 56;
      if (lastFase != null && L.m.faseNum !== lastFase) y += 30;
      lastFase = L.m.faseNum;
      let xr = metaX;
      for (const d of [...L.cols.keys()].sort((a, b) => a - b)) {
        const arr = L.cols.get(d).sort((a, b) => rank(a) - rank(b) || (pr[a.priority] ?? 3) - (pr[b.priority] ?? 3) || a.title.localeCompare(b.title));
        const nsub = Math.ceil(arr.length / ROWS), per = Math.ceil(arr.length / nsub);
        for (let sidx = 0; sidx < nsub; sidx++) {
          xr -= COLW;
          const part = arr.slice(sidx * per, (sidx + 1) * per), off = (inner - part.length * RH) / 2;
          part.forEach((t, i) => { pos[t.path] = { x: xr, y: y + 38 + off + i * RH }; });
        }
      }
      pos[L.m.path] = { x: metaX, y: y + 28 + inner / 2 - 60 };
      (this.D['lanes_' + this.S.scope] = this.D['lanes_' + this.S.scope] || {})[L.m.path] = { x: -18, y, w: metaX + MW + 54, h };
      y += h + GAP;
    }
    if (norte) pos[norte.path] = { x: metaX + MW + 140, y: Math.max(0, y / 2 - 70) };
  }
  fullLayout() {
    if (this.S.scope === 'roadmap') return this.roadmapLayout();
    if (this.S.scope === 'habitos') return this.habitsLayout();
    if (this.scoped() && this.S.layout === 'tree') return this.boardLayout();
    const nodes = this.vis(), pos = {};
    if (!nodes.size) return;
    const ch = (p) => (this.children.get(p) || []).filter((c) => nodes.has(c));
    const pa = (p) => (this.parents.get(p) || []).filter((c) => nodes.has(c));
    if (this.S.layout === 'time') {
      const day = (n) => { const d = n.due || n.scheduled; const t = d ? Date.parse(String(d).slice(0, 10)) : NaN; return isNaN(t) ? null : Math.round(t / 864e5); };
      const dated = [...nodes.values()].map(day).filter((x) => x != null), min = dated.length ? Math.min(...dated) : 0;
      const lanes = new Map();
      for (const n of nodes.values()) { const k = this.laneOf(n.path, nodes); if (!lanes.has(k)) lanes.set(k, []); lanes.get(k).push(n); }
      const keys = [...lanes.keys()].sort((a, b) => (a === '__none') - (b === '__none'));
      let y = 0;
      for (const k of keys) {
        const rows = [];
        const items = lanes.get(k).map((n) => ({ n, d: day(n) })).sort((a, b) => (a.d ?? -1e9) - (b.d ?? -1e9));
        for (const it of items) {
          const x = it.d == null ? -GX : (it.d - min) * 90;
          let r = rows.findIndex((end) => end <= x); if (r < 0) { r = rows.length; rows.push(0); }
          rows[r] = x + NW + 24; pos[it.n.path] = { x, y: y + r * GY };
        }
        y += rows.length * GY + 90;
      }
    } else {
      const placed = new Set(); let row = 0;
      const place = (p, depth) => {
        placed.add(p);
        const kids = ch(p).filter((c) => !placed.has(c));
        if (!kids.length) { pos[p] = { x: depth * GX, y: row * GY }; row++; return pos[p].y; }
        pos[p] = { x: depth * GX, y: 0 };
        const ys = kids.map((c) => place(c, depth + 1));
        pos[p].y = (Math.min(...ys) + Math.max(...ys)) / 2;
        return pos[p].y;
      };
      const connected = [...nodes.keys()].filter((p) => ch(p).length || pa(p).length);
      connected.filter((p) => !pa(p).length).forEach((p) => { if (!placed.has(p)) { place(p, 0); row += 0.6; } });
      connected.forEach((p) => { if (!placed.has(p)) place(p, 0); });
      const iso = [...nodes.values()].filter((n) => !connected.includes(n.path))
        .sort((a, b) => (a.status === 'done') - (b.status === 'done') || a.title.localeCompare(b.title));
      const y0 = (row + 1) * GY + 60;
      iso.forEach((n, i) => { pos[n.path] = { x: (i % 5) * GX, y: y0 + Math.floor(i / 5) * GY }; });
    }
    Object.assign(this.D.pos, pos);
  }
  ensurePositions() {
    const P = this.D.pos, nodes = [...this.model.nodes.keys()];
    const missing = nodes.filter((p) => !P[p]);
    if (!missing.length) return;
    if (missing.length === nodes.length || this.rm() || (this.scoped() && this.S.layout === 'tree')) { this.fullLayout(); this.plugin.saveSoon(); return; }
    const ys = nodes.filter((p) => P[p]).map((p) => P[p].y);
    let freeY = Math.max(...ys) + GY * 1.4, free = 0;
    for (const p of missing) {
      const par = (this.parents.get(p) || []).find((q) => P[q]);
      if (par) {
        const sib = (this.children.get(par) || []).filter((c) => P[c]);
        const y = sib.length ? Math.max(...sib.map((c) => P[c].y)) + GY : P[par].y;
        P[p] = { x: P[par].x + GX, y };
      } else { P[p] = { x: (free % 5) * GX, y: freeY + Math.floor(free / 5) * GY }; free++; }
    }
    this.plugin.saveSoon();
  }

  // ---------- render ----------
  refresh(fit) {
    this.buildModel();
    this.contentEl.toggleClass('is-roadmap', this.rm()); if (this.legend) this.legend.toggle(this.rm());
    this.ensurePositions();
    this.renderNodes();
    this.drawEdges();
    this.fillFilter();
    this.renderSide();
    if (fit && !this.D.fitted) { this.fit(); this.D.fitted = true; }
  }
  renderNodes() {
    this.layer.empty(); this.els = new Map();
    const q = this.q.toLowerCase();
    for (const n of this.model.nodes.values()) {
      if (!this.isVisible(n)) continue;
      const el = this.layer.createDiv({ cls: `tka-node tka-${n.type === 'meta' ? 'metacard' : n.type} tka-st-${n.status}` });
      el.dataset.path = n.path;
      el.style.width = (n.type === 'meta' ? 280 : n.type === 'norte' ? 340 : n.type === 'task' && this.rm() ? 236 : NW) + 'px';
      if (this.rm() && n.type === 'task') { if (n.ready) el.addClass('is-ready'); if (n.blocked) el.addClass('is-blocked'); }
      if (n.type === 'task') {
        const chk = el.createDiv('tka-chk');
        chk.style.setProperty('--c', stColor(n.status));
        chk.setText(n.status === 'done' ? '✓' : '');
        chk.addEventListener('click', (e) => { e.stopPropagation(); this.setStatus(n.path, n.status === 'done' ? 'open' : 'done'); });
      } else el.createDiv({ cls: 'tka-ico', text: n.type === 'norte' ? '⭐' : n.type === 'meta' ? '🎯' : n.type === 'hub' ? '🧭' : n.type === 'area' ? '🗂️' : n.type === 'cliente' ? '👤' : '📄' });
      if (n.color) el.style.setProperty('--ac', n.color);
      const body = el.createDiv('tka-body');
      body.createDiv({ cls: 'tka-title', text: n.title });
      if (n.type === 'task') {
        const meta = body.createDiv('tka-meta');
        const dot = meta.createSpan('tka-dot'); dot.style.background = prColor(n.priority);
        const d = n.due || n.scheduled;
        if (d) { const s = meta.createSpan({ text: String(d).slice(0, 10) }); if (n.due && String(n.due).slice(0, 10) < today() && n.status !== 'done') s.addClass('tka-late'); }
        meta.createSpan({ text: n.status === 'idea' ? 'Idea' : STATUSES.find((s) => s.id === n.status)?.label || n.status });
        if (this.S.scope === 'habitos') { meta.createSpan({ cls: 'tka-tag-ready', text: '↻ ' + n.habito }); if (n.responsable) meta.createSpan({ text: '· ' + n.responsable }); } else if (this.rm()) { if (n.ready) meta.createSpan({ cls: 'tka-tag-ready', text: '▶ siguiente' }); else if (n.blocked) meta.createSpan({ cls: 'tka-tag-blocked', text: `🔒 espera ${n.waits}` }); if (n.responsable) meta.createSpan({ text: '· ' + n.responsable }); }
      } else if (n.type === 'meta' || n.type === 'norte') {
        body.createDiv({ cls: 'tka-meta', text: n.type === 'norte' ? (n.fase || 'Fase 3') : (this.S.scope === 'habitos' ? `${n.total} hábitos` : `${n.done}/${n.total} pasos`) + (n.responsable ? ' · ' + n.responsable : '') });
        if (n.resultado) body.createDiv({ cls: 'tka-res', text: n.resultado });
        (n.type === 'norte' ? (n.medida || []) : (n.medida || []).slice(0, 1)).forEach((x) => body.createDiv({ cls: 'tka-res tka-med', text: '📏 ' + x }));
      } else if (n.type === 'area' || n.type === 'cliente') {
        const ds = [...this.descendants(n.path)].map((c) => this.model.nodes.get(c)).filter((c) => c && c.type === 'task' && c.status !== 'done');
        const late = ds.filter((c) => c.due && String(c.due).slice(0, 10) < today()).length;
        const who = n.type === 'cliente' ? (n.tipo || '—') : (n.responsable || '—');
        body.createDiv({ cls: 'tka-meta', text: `${who} · ${ds.length} abiertas · ${ds.filter((c) => c.priority === 'high').length} altas` + (late ? ` · ${late} vencidas` : '') });
      } else if (n.type === 'hub') body.createDiv({ cls: 'tka-meta', text: (this.S.scope === 'clientes' ? 'Clientes · cómo trabajamos' : 'Big Picture · Operaciones') });
      else body.createDiv({ cls: 'tka-meta', text: n.path.split('/').slice(0, -1).join('/') });
      const open = el.createDiv({ cls: 'tka-open', text: '↗' });
      open.addEventListener('click', (e) => { e.stopPropagation(); this.app.workspace.getLeaf('tab').openFile(n.file); });
      el.createDiv('tka-port');
      if (this.sel.has(n.path)) el.addClass('is-sel');
      if (q && !n.title.toLowerCase().includes(q)) el.addClass('is-dim');
      this.els.set(n.path, el);
      this.placeEl(n.path);
    }
    this.drawLanes();
    this.bindNodes();
  }
  roadmapRects() {
    const out = new Map();
    for (const [p, n] of this.model.nodes) {
      if (n.type !== 'meta' || !this.els.has(p)) continue;
      if (this.D['lanes_' + this.S.scope] && this.D['lanes_' + this.S.scope][p]) { out.set(p, this.D['lanes_' + this.S.scope][p]); continue; }
      const mine = [...this.model.nodes.values()].filter((t) => (t.meta === p || t.path === p) && this.els.has(t.path) && this.D.pos[t.path]);
      let y0 = 1e9, y1 = -1e9, xm = 0;
      mine.forEach((t) => { const q = this.D.pos[t.path], z = this.size(t.path); y0 = Math.min(y0, q.y); y1 = Math.max(y1, q.y + z.h); if (t.path === p) xm = q.x + z.w; });
      const hh = 330;
      y1 = Math.max(y1, y0 + hh - 20);
      out.set(p, { x: -18, y: y0 - 38, w: xm + 36, h: y1 - y0 + 66 });
    }
    return out;
  }
  drawRoadmapLanes() {
    this.layer.querySelectorAll('.tka-lane').forEach((e) => e.remove());
    this.laneRects = this.roadmapRects();
    for (const [mp, r] of this.laneRects) {
      const m = this.model.nodes.get(mp); if (!m) continue;
      const el = createDiv({ cls: 'tka-lane tka-rlane' });
      el.style.cssText = `left:${r.x}px;top:${r.y}px;width:${r.w}px;height:${r.h}px;--lc:${m.color || '#39ff14'}`;
      const hd = el.createDiv('tka-rl-head');
      hd.createDiv({ cls: 'tka-rl-fase', text: m.fase });
      hd.createDiv({ cls: 'tka-rl-title', text: m.title });
      if (m.resultado) hd.createDiv({ cls: 'tka-rl-res', text: '🎯 ' + m.resultado });
      (m.medida || []).forEach((x) => hd.createDiv({ cls: 'tka-rl-med', text: '📏 ' + x }));
      if (m.hoy) hd.createDiv({ cls: 'tka-rl-hoy', text: m.hoy });
      const pct = m.total ? Math.round(100 * m.done / m.total) : 0;
      if (this.S.scope === 'habitos') { hd.createDiv({ cls: 'tka-rl-cnt', text: `${m.total} hábitos que sostienen esta meta` }); this.layer.insertBefore(el, this.layer.firstChild); continue; }
      const bar = hd.createDiv('tka-rl-bar'); bar.createDiv('tka-rl-fill').style.width = pct + '%';
      hd.createDiv({ cls: 'tka-rl-cnt', text: `${m.done}/${m.total} pasos · ${pct}%` + (m.ideas ? ` · ${m.ideas} ideas` : '') + (m.fecha && !/^fijar/i.test(m.fecha) ? ` · meta ${m.fecha}` : '') });
      this.layer.insertBefore(el, this.layer.firstChild);
    }
  }
  drawLanes() {
    if (this.rm()) return this.drawRoadmapLanes();
    this.layer.querySelectorAll('.tka-lane').forEach((e) => e.remove());
    if (!this.S.lanes) return;
    const nodes = new Map([...this.els.keys()].map((p) => [p, this.model.nodes.get(p)]));
    const groups = new Map();
    for (const p of nodes.keys()) { const k = this.laneOf(p, nodes); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(p); }
    const pal = ['#39ff14', '#f59e0b', '#3b82f6', '#a855f7', '#06b6d4', '#ef4444', '#eab308'];
    let i = 0;
    for (const [k, ps] of groups) {
      if (k === '__none' && this.scoped()) continue;
      const kn = this.model.nodes.get(k), c = k === '__none' ? '#888888' : (kn && kn.color) || pal[i++ % pal.length];
      let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      ps.forEach((p) => { const q = this.D.pos[p], z = this.size(p); if (!q) return; x0 = Math.min(x0, q.x); y0 = Math.min(y0, q.y); x1 = Math.max(x1, q.x + z.w); y1 = Math.max(y1, q.y + z.h); });
      if (x0 > x1) continue;
      const el = createDiv({ cls: 'tka-lane' });
      el.style.cssText = `left:${x0 - 22}px;top:${y0 - 40}px;width:${x1 - x0 + 44}px;height:${y1 - y0 + 62}px;--lc:${c}`;
      el.createDiv({ cls: 'tka-lane-t', text: k === '__none' ? (this.S.scope === 'operaciones' ? 'Big Picture' : this.S.scope === 'clientes' ? 'Clientes' : 'Sin proyecto') : this.model.nodes.get(k).title });
      this.layer.insertBefore(el, this.layer.firstChild);
    }
  }
  placeEl(p) { const el = this.els.get(p), pos = this.D.pos[p]; if (el && pos) el.style.transform = `translate(${pos.x}px,${pos.y}px)`; }
  size(p) { const el = this.els.get(p); return { w: el ? el.offsetWidth : NW, h: el ? el.offsetHeight : 60 }; }
  bez(a, b) { const dx = Math.max(50, Math.abs(b.x - a.x) / 2); return `M${a.x} ${a.y} C${a.x + dx} ${a.y},${b.x - dx} ${b.y},${b.x} ${b.y}`; }
  drawEdges() {
    this.edgeG.replaceChildren();
    for (const e of this.model.edges) {
      if (!this.els.has(e.from) || !this.els.has(e.to)) continue;
      const fn = this.model.nodes.get(e.from), tn = this.model.nodes.get(e.to);
      if (this.scoped() && fn.type !== 'hub' && !(fn.type === 'task' && tn.type === 'task')) continue;
      const pf = this.D.pos[e.from], pt = this.D.pos[e.to], sf = this.size(e.from), st = this.size(e.to);
      let d;
      if (fn.type === 'hub') { const a = { x: pf.x + sf.w / 2, y: pf.y + sf.h }, b = { x: pt.x + st.w / 2, y: pt.y - 30 }, my = (a.y + b.y) / 2; d = `M${a.x} ${a.y} C${a.x} ${my},${b.x} ${my},${b.x} ${b.y}`; }
      else d = this.bez({ x: pf.x + sf.w, y: pf.y + sf.h / 2 }, { x: pt.x, y: pt.y + st.h / 2 });
      const vis = document.createElementNS(SVGNS, 'path');
      vis.setAttribute('d', d); vis.setAttribute('marker-end', 'url(#tka-arrow)'); vis.classList.add('tka-edge'); if (e.kind) vis.classList.add('tka-edge-' + e.kind);
      if (this.chain ? (this.chain.has(e.from) && this.chain.has(e.to)) : (this.sel.has(e.from) || this.sel.has(e.to))) vis.classList.add('is-hot');
      else if (this.chain) vis.classList.add('is-faded');
      const hit = document.createElementNS(SVGNS, 'path');
      hit.setAttribute('d', d); hit.classList.add('tka-edge-hit');
      hit.addEventListener('contextmenu', (ev) => {
        ev.preventDefault();
        new Menu().addItem((i) => i.setTitle('Eliminar conexión').setIcon('trash').onClick(() => this.unlink(e.from, e.to))).showAtMouseEvent(ev);
      });
      this.edgeG.appendChild(vis); this.edgeG.appendChild(hit);
    }
  }
  renderSide() {
    const s = this.side; s.empty();
    const head = s.createDiv('tka-side-head');
    head.createEl('b', { text: 'Tareas' });
    const inp = head.createEl('input', { type: 'text', placeholder: 'Buscar…' });
    inp.value = this.q;
    inp.addEventListener('input', () => {
      this.q = inp.value; const q = this.q.toLowerCase();
      this.els.forEach((el, p) => el.toggleClass('is-dim', !!q && !this.model.nodes.get(p).title.toLowerCase().includes(q)));
      this.fillSide(list);
    });
    if (this.rm() && this.sel.size === 1) this.detail(s);
    else if (this.rm()) s.createDiv({ cls: 'tka-hint', text: 'Haz clic en un paso clave para ver cómo se descompone: hábitos, tareas, subtareas y notas.' });
    const list = s.createDiv('tka-side-list');
    this.fillSide(list);
  }
  detail(s) {
    const p = [...this.sel][0], n = this.model.nodes.get(p); if (!n) return;
    const box = s.createDiv('tka-detail');
    const hd = box.createDiv('tka-pl-head');
    hd.createDiv({ cls: 'tka-pl-t', text: n.title });
    const chips = hd.createDiv('tka-pl-chips');
    if (n.type === 'task') {
      const st = n.status === 'idea' ? 'Idea' : (STATUSES.find((x) => x.id === n.status) || {}).label || n.status;
      chips.createSpan({ cls: 'tka-chip', text: st });
      if (n.responsable) chips.createSpan({ cls: 'tka-chip', text: n.responsable });
      if (n.ready) chips.createSpan({ cls: 'tka-chip is-go', text: '▶ siguiente' });
      else if (n.blocked) chips.createSpan({ cls: 'tka-chip is-lock', text: '🔒 espera ' + n.waits });
      const m = this.model.nodes.get(n.meta); if (m) hd.createDiv({ cls: 'tka-pl-sub', text: '🎯 Aporta a: ' + m.title });
    } else if (n.type === 'meta') (n.medida || []).forEach((x) => hd.createDiv({ cls: 'tka-pl-sub', text: '📏 ' + x }));
    const ob = hd.createEl('button', { text: '↗ Abrir la nota', cls: 'tka-obtn' }); ob.addEventListener('click', () => this.app.workspace.getLeaf('tab').openFile(n.file));
    if (n.type === 'task' && this.S.scope === 'roadmap') this.planPanel(box, n);
    const sec = (label, ids) => {
      if (!ids.length) return;
      box.createDiv({ cls: 'tka-detail-h', text: label });
      ids.forEach((id) => { const m = this.model.nodes.get(id); if (!m) return; const it = box.createDiv({ cls: 'tka-item', text: (m.status === 'done' ? '✓ ' : m.type === 'meta' ? '🎯 ' : m.type === 'norte' ? '⭐ ' : '○ ') + m.title }); it.addEventListener('click', () => this.focusNode(id)); });
    };
    sec('⬅ Depende de (hay que cerrar antes)', this.parents.get(p) || []);
    sec('➡ Al cerrarla desbloquea', this.children.get(p) || []);
    if (n.type === 'meta') sec('Pasos de esta meta', [...this.model.nodes.values()].filter((t) => t.meta === p).map((t) => t.path));
  }
  plan(n) {
    const MC = this.app.metadataCache, folder = this.S.tasksFolder.replace(/\/+$/, '');
    const fmOf = (f) => (MC.getFileCache(f) || {}).frontmatter || {};
    const tgt = (v, from) => { const l = parseLink(String(flat(v)[0] || '')); return l && MC.getFirstLinkpathDest(l, from); };
    const fm = fmOf(n.file);
    const kids = this.app.vault.getMarkdownFiles().filter((f) => f.path.startsWith(folder + '/') && f.path !== n.path).map((f) => ({ f, fm: fmOf(f) })).filter((o) => o.fm.paso && (tgt(o.fm.paso, o.f.path) || {}).path === n.path);
    const ORD = { diario: 0, semanal: 1, mensual: 2 };
    const hab = kids.filter((o) => o.fm.tipo === 'habito').sort((a, b) => (ORD[a.fm.habito] ?? 3) - (ORD[b.fm.habito] ?? 3));
    const ses = kids.filter((o) => o.fm.tipo === 'sesion');
    const acts = kids.filter((o) => o.fm.tipo !== 'habito' && o.fm.tipo !== 'sesion');
    const notas = flat(fm.notas).map((v) => ({ v, d: tgt([v], n.path) }));
    const seen = new Set(notas.filter((x) => x.d).map((x) => x.d.path)), rel = [];
    const rl = MC.resolvedLinks || {};
    const skip = (q) => q.startsWith(folder + '/') || q.startsWith('Roadmap/') || q.startsWith('daily/') || q.startsWith('Canvas/') || q === n.path;
    const add = (q) => { if (seen.has(q) || skip(q)) return; const f = this.app.vault.getAbstractFileByPath(q); if (f && f.extension === 'md') { seen.add(q); rel.push(f); } };
    Object.keys(rl[n.path] || {}).forEach(add);
    for (const [src, t] of Object.entries(rl)) if (t[n.path]) add(src);
    return { fm, med: flat(fm.medida), hab, ses, acts, notas, rel };
  }
  planPanel(box, n) {
    const open = (f) => this.app.workspace.getLeaf('tab').openFile(f);
    const MC = this.app.metadataCache;
    const pl = this.plan(n);
    const section = (icon, title, count, onAdd, build, isOpen = true) => {
      const sec = box.createDiv('tka-pl-sec' + (isOpen ? ' is-open' : ''));
      const h = sec.createDiv('tka-pl-sh');
      h.createSpan({ cls: 'tka-pl-caret', text: '▸' }); h.createSpan({ cls: 'tka-pl-st', text: icon + ' ' + title }); h.createSpan({ cls: 'tka-pl-n', text: String(count) });
      if (onAdd) { const a = h.createSpan({ cls: 'tka-pl-add', text: '＋' }); a.title = 'Añadir'; a.addEventListener('click', (e) => { e.stopPropagation(); onAdd(); }); }
      const body = sec.createDiv('tka-pl-sb');
      h.addEventListener('click', () => sec.toggleClass('is-open', !sec.hasClass('is-open')));
      if (!count) body.createDiv({ cls: 'tka-pl-empty', text: 'Nada aún. Usa ＋ para añadir.' }); else build(body);
      return sec;
    };
    const row = (body, o) => {
      const it = body.createDiv({ cls: 'tka-pl-row' + (o.done ? ' is-done' : '') });
      if (o.check) { const c = it.createSpan({ cls: 'tka-cb', text: o.done ? '☑' : '☐' }); c.addEventListener('click', (e) => { e.stopPropagation(); o.check(); }); }
      if (o.pre) it.createSpan({ cls: 'tka-hf', text: o.pre });
      it.createSpan({ cls: 'tka-pl-tx', text: o.text });
      if (o.right) it.createSpan({ cls: 'tka-who', text: o.right });
      if (o.click) it.addEventListener('click', o.click);
      return it;
    };
    const clean = (t) => t.replace(/^(Hábito (diario|semanal|mensual)|Sesión de trabajo profundo) · /, '');
    const refresh = () => setTimeout(() => this.renderSide(), 700);
    const toggle = (f, done) => this.app.fileManager.processFrontMatter(f, (x) => { x.status = done ? 'open' : 'done'; x.dateModified = isoNow(); }).then(refresh);
    section('📏', 'Cómo se comprueba', pl.med.length, null, (b) => pl.med.forEach((x) => row(b, { text: x, pre: '◻' })));
    section('↻', 'Hábitos que lo sostienen', pl.hab.length, () => this.addToStep(n, 'habito'), (b) => pl.hab.forEach((o) => row(b, { pre: o.fm.habito || '', text: clean(o.f.basename), right: o.fm.responsable, click: () => open(o.f) })));
    section('🎯', 'Sesiones de trabajo profundo', pl.ses.length, () => this.addToStep(n, 'sesion'), (b) => pl.ses.forEach((o) => row(b, { check: () => toggle(o.f, o.fm.status === 'done'), done: o.fm.status === 'done', text: clean(o.f.basename), right: [o.fm.duracion, o.fm.scheduled && String(o.fm.scheduled).slice(5, 10)].filter(Boolean).join(' · '), click: () => open(o.f) })));
    section('⚡', 'Tareas y acciones', pl.acts.length, () => this.addToStep(n, 'accion'), (b) => pl.acts.forEach((o) => row(b, { check: () => toggle(o.f, o.fm.status === 'done'), done: o.fm.status === 'done', text: o.f.basename, right: o.fm.responsable, click: () => open(o.f) })));
    const lis = ((MC.getFileCache(n.file) || {}).listItems || []).filter((li) => li.task !== undefined);
    section('☑', 'Subtareas', lis.length, () => this.addToStep(n, 'subtarea'), (b) => {
      this.app.vault.cachedRead(n.file).then((txt) => {
        const lines = txt.split('\n');
        lis.forEach((li) => {
          const ln = li.position.start.line, done = li.task !== ' ';
          row(b, { done, text: (lines[ln] || '').replace(/^\s*- \[.\]\s*/, ''), check: async () => { await this.app.vault.process(n.file, (t) => { const L = t.split('\n'); L[ln] = done ? L[ln].replace(/- \[[xX]\]/, '- [ ]') : L[ln].replace('- [ ]', '- [x]'); return L.join('\n'); }); refresh(); } });
        });
      });
    });
    section('📚', 'Notas clave y wiki', pl.notas.length + pl.rel.length, () => new NotePicker(this.app, (f) => this.app.fileManager.processFrontMatter(n.file, (x) => { x.notas = flat(x.notas).concat('[[' + f.path.replace(/\.md$/, '') + ']]'); }).then(refresh)).open(), (b) => {
      pl.notas.forEach((x) => row(b, { pre: '📄', text: x.d ? x.d.basename : String(x.v), click: x.d ? () => open(x.d) : null }));
      pl.rel.forEach((f) => row(b, { pre: '↔', text: f.basename, right: 'enlazada', click: () => open(f) }));
    });
  }
  addToStep(n, kind) {
    const L = { habito: 'Nuevo hábito', sesion: 'Nueva sesión de trabajo profundo', accion: 'Nueva tarea o acción', subtarea: 'Nueva subtarea' };
    const options = kind === 'habito' ? [['diario', 'Diario'], ['semanal', 'Semanal'], ['mensual', 'Mensual']] : kind === 'sesion' ? [['60 min', '60 min'], ['90 min', '90 min'], ['120 min', '120 min']] : null;
    new AddModal(this.app, { title: L[kind] + '  ←  ' + n.title, options, date: kind === 'sesion' || kind === 'accion' }, async (text, opt, date) => {
      if (kind === 'subtarea') {
        await this.app.vault.process(n.file, (t) => {
          const Ls = t.split('\n'), i = Ls.findIndex((l) => /^## Subtareas\s*$/.test(l));
          if (i < 0) return t.replace(/\s*$/, '') + '\n\n## Subtareas\n- [ ] ' + text + '\n';
          let j = i + 1; while (j < Ls.length && !/^#{1,6} /.test(Ls[j]) && !/^\*/.test(Ls[j])) j++;
          while (j > i + 1 && Ls[j - 1].trim() === '') j--;
          Ls.splice(j, 0, '- [ ] ' + text); return Ls.join('\n');
        });
      } else {
        const folder = this.S.tasksFolder.replace(/\/+$/, '');
        const nm = (kind === 'habito' ? `Hábito ${opt} · ` : kind === 'sesion' ? 'Sesión de trabajo profundo · ' : '') + text;
        const base = nm.replace(/[\\/:*?"<>|#^\[\]]/g, '').replace(/\s+/g, ' ').trim().slice(0, 120);
        let path = `${folder}/${base}.md`, k = 2; while (this.app.vault.getAbstractFileByPath(path)) path = `${folder}/${base} ${k++}.md`;
        const fm = (this.app.metadataCache.getFileCache(n.file) || {}).frontmatter || {}, now = isoNow();
        const RR = { diario: 'FREQ=DAILY', semanal: 'FREQ=WEEKLY;BYDAY=MO', mensual: 'FREQ=MONTHLY;BYMONTHDAY=1' };
        const sd = date || today();
        let y = `---\nstatus: open\npriority: normal\nscheduled: ${sd}\n`;
        if (kind === 'habito') y += `recurrence: DTSTART:${sd.replace(/-/g, '')};${RR[opt]}\nrecurrence_anchor: scheduled\n`;
        const mt = flat(fm.meta)[0]; if (mt) y += `meta: ${JSON.stringify(String(mt))}\nprojects:\n  - ${JSON.stringify(String(mt))}\n`;
        y += `paso: "[[${n.file.basename}]]"\ntipo: ${kind === 'accion' ? 'accion' : kind}\n`;
        if (kind === 'habito') y += `habito: ${opt}\n`; if (kind === 'sesion') y += `duracion: ${opt}\n`;
        if (fm.responsable) y += `responsable: ${fm.responsable}\n`;
        y += `creadoPor: Task Atlas\ndateCreated: ${now}\ndateModified: ${now}\ntags:\n  - task\n---\n`;
        await this.app.vault.create(path, y);
      }
      setTimeout(() => this.renderSide(), 900);
    }).open();
  }
  fillSide(list) {
    list.empty();
    const q = this.q.toLowerCase();
    for (const st of STATUSES) {
      const items = [...this.model.nodes.values()].filter((n) => n.type === 'task' && this.isVisible(n) && n.status === st.id && (!q || n.title.toLowerCase().includes(q)));
      const g = list.createDiv('tka-group');
      const h = g.createDiv('tka-group-h');
      h.createSpan('tka-dot').style.background = st.color;
      h.createSpan({ text: `${st.label} · ${items.length}` });
      h.addEventListener('dragover', (e) => { e.preventDefault(); h.addClass('is-over'); });
      h.addEventListener('dragleave', () => h.removeClass('is-over'));
      h.addEventListener('drop', (e) => { e.preventDefault(); h.removeClass('is-over'); const p = e.dataTransfer.getData('text/plain'); if (p) this.setStatus(p, st.id); });
      items.sort((a, b) => a.title.localeCompare(b.title)).forEach((n) => {
        const it = g.createDiv({ cls: 'tka-item', text: n.title });
        it.draggable = true;
        it.addEventListener('dragstart', (e) => e.dataTransfer.setData('text/plain', n.path));
        it.addEventListener('click', () => this.focusNode(n.path));
      });
    }
  }
  buildTools() {
    const t = this.stage.createDiv('tka-tools');
    const b = (txt, fn, title) => { const x = t.createEl('button', { text: txt }); x.title = title || txt; x.onclick = fn; return x; };
    b('＋ Tarea', () => this.promptCreate(null, this.centerWorld()), 'Nueva tarea');
    this.filterSel = t.createEl('select'); this.filterSel.title = 'Filtrar por cliente / proyecto';
    this.filterSel.onchange = () => { this.S.filter = this.filterSel.value; this.plugin.saveSoon(); this.refresh(); this.reflow(); };
    const ls = t.createEl('select'); ls.title = 'Vista';
    [['tree', 'Vista: Árbol'], ['time', 'Vista: Línea de tiempo']].forEach(([v, l]) => ls.createEl('option', { value: v, text: l }));
    ls.value = this.S.layout; ls.onchange = () => { this.S.layout = ls.value; this.plugin.saveSoon(); this.reflow(); };
    const SCL = { roadmap: 'Vista: Roadmap (metas → pasos)', habitos: 'Vista: Hábitos', operaciones: 'Vista: Operaciones y Big Picture', clientes: 'Vista: Clientes', todo: 'Vista: Todo' };
    const sc = b(SCL[this.S.scope] || SCL.todo, () => { const o = ['roadmap', 'habitos', 'clientes', 'todo']; this.S.scope = o[(o.indexOf(this.S.scope) + 1) % 4]; this.S.filter = ''; sc.setText(SCL[this.S.scope]); this.plugin.saveSoon(); this.refresh(); this.reflow(); }, 'Cambiar entre Operaciones y Big Picture / Clientes / Todo');
    sc.toggleClass('is-on', true);
    b('Organizar', () => this.reflow(), 'Auto-layout');
    const ln = b('Carriles', () => { this.S.lanes = !this.S.lanes; ln.toggleClass('is-on', this.S.lanes); this.plugin.saveSoon(); this.drawLanes(); }, 'Agrupar por proyecto');
    ln.toggleClass('is-on', this.S.lanes);
    b('→ Canvas', () => this.plugin.exportCanvas(this), 'Exportar esta vista a un Canvas');
    b('Ajustar', () => this.fit(), 'Ver todo');
    this.legend = this.stage.createDiv('tka-legend');
    this.legend.innerHTML = '<span class="lg lg-dep">━▶ desbloquea</span><span class="lg lg-goal">┅▶ aporta a la meta</span><span class="lg lg-feed">━▶ meta alimenta la estrella</span><span class="lg lg-ready">▶ siguiente paso accionable</span><span class="lg lg-block">🔒 bloqueada por pasos previos</span><span class="lg lg-idea">◌ idea futura</span>';
    const hd = b('Ocultar hechas', () => { this.S.hideDone = !this.S.hideDone; hd.toggleClass('is-on', this.S.hideDone); this.plugin.saveSoon(); this.refresh(); });
    hd.toggleClass('is-on', this.S.hideDone);
    const nt = b('Notas enlazadas', () => { this.S.showNotes = !this.S.showNotes; nt.toggleClass('is-on', this.S.showNotes); this.plugin.saveSoon(); this.refresh(); });
    nt.toggleClass('is-on', this.S.showNotes);
  }

  reflow() { this.fullLayout(); this.plugin.saveSoon(); this.renderNodes(); this.drawEdges(); this.fit(); }
  fillFilter() {
    const sel = this.filterSel; if (!sel) return;
    sel.empty(); sel.createEl('option', { value: '', text: 'Todo' });
    [...this.model.nodes.values()].filter((n) => (this.children.get(n.path) || []).length)
      .sort((a, b) => a.title.localeCompare(b.title))
      .forEach((n) => sel.createEl('option', { value: n.path, text: (n.type === 'hub' ? '🧭 ' : n.type === 'area' ? '🗂️ ' : n.type === 'cliente' ? '👤 ' : n.type === 'note' ? '📄 ' : '✔ ') + n.title }));
    sel.value = this.S.filter || '';
  }

  // ---------- vista (pan/zoom) ----------
  applyView() {
    const v = this.D.view;
    this.world.style.transform = `translate(${v.x}px,${v.y}px) scale(${v.k})`;
    this.stage.style.backgroundPosition = `${v.x}px ${v.y}px`;
    this.stage.style.backgroundSize = `${24 * v.k}px ${24 * v.k}px`;
  }
  toWorld(cx, cy) { const r = this.stage.getBoundingClientRect(), v = this.D.view; return { x: (cx - r.left - v.x) / v.k, y: (cy - r.top - v.y) / v.k }; }
  centerWorld() { const r = this.stage.getBoundingClientRect(); return this.toWorld(r.left + r.width / 2, r.top + r.height / 2); }
  fit() {
    const ps = [...this.els.keys()].filter((p) => this.D.pos[p]);
    if (!ps.length) return;
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    ps.forEach((p) => { const q = this.D.pos[p], s = this.size(p); x0 = Math.min(x0, q.x); y0 = Math.min(y0, q.y); x1 = Math.max(x1, q.x + s.w); y1 = Math.max(y1, q.y + s.h); });
    if (this.rm() && this.laneRects) for (const r of this.laneRects.values()) { x0 = Math.min(x0, r.x); y0 = Math.min(y0, r.y); x1 = Math.max(x1, r.x + r.w); y1 = Math.max(y1, r.y + r.h); }
    const W = this.stage.clientWidth || 900, H = this.stage.clientHeight || 600, pad2 = 70;
    const k = clamp(Math.min(W / (x1 - x0 + pad2 * 2), H / (y1 - y0 + pad2 * 2)), 0.15, 1.2);
    this.D.view = { k, x: (W - (x1 - x0) * k) / 2 - x0 * k, y: (H - (y1 - y0) * k) / 2 - y0 * k };
    this.applyView(); this.plugin.saveSoon();
  }
  focusNode(p) {
    const q = this.D.pos[p]; if (!q || !this.els.has(p)) return;
    const s = this.size(p), v = this.D.view;
    v.x = this.stage.clientWidth / 2 - (q.x + s.w / 2) * v.k; v.y = this.stage.clientHeight / 2 - (q.y + s.h / 2) * v.k;
    this.sel = new Set([p]); this.paintSel(); this.applyView(); this.plugin.saveSoon();
  }
  paintSel() {
    this.chain = null;
    if (this.rm() && this.sel.size === 1) {
      const p = [...this.sel][0], c = new Set([p]);
      const walk = (m, dir) => { const st = [p]; const seen = new Set(); while (st.length) { const x = st.pop(); for (const k of (m.get(x) || [])) { if (seen.has(k)) continue; seen.add(k); c.add(k); const kn = this.model.nodes.get(k); if (kn && kn.type === 'task') st.push(k); else if (kn && kn.type === 'meta' && dir === 'down') st.push(k); } } };
      walk(this.parents, 'up'); walk(this.children, 'down'); this.chain = c;
    }
    this.els.forEach((el, p) => { el.toggleClass('is-sel', this.sel.has(p)); el.toggleClass('is-faded', !!this.chain && !this.chain.has(p)); });
    this.drawEdges();
    if (this.rm()) this.renderSide();
  }
  track(onMove, onUp) {
    const mv = (e) => onMove(e);
    const up = (e) => { document.removeEventListener('pointermove', mv); document.removeEventListener('pointerup', up); onUp && onUp(e); };
    document.addEventListener('pointermove', mv); document.addEventListener('pointerup', up);
  }

  // ---------- interacciones ----------
  bindStage() {
    this.stage.addEventListener('wheel', (e) => {
      e.preventDefault();
      const r = this.stage.getBoundingClientRect(), v = this.D.view, mx = e.clientX - r.left, my = e.clientY - r.top;
      const nk = clamp(v.k * Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0015)), 0.12, 2.5);
      v.x = mx - (mx - v.x) * (nk / v.k); v.y = my - (my - v.y) * (nk / v.k); v.k = nk;
      this.applyView(); this.plugin.saveSoon();
    }, { passive: false });
    this.stage.addEventListener('pointerdown', (e) => {
      if (e.target.closest('.tka-node,.tka-tools,.tka-edge-hit')) return;
      if (e.button !== 0 && e.button !== 1) return;
      if (!e.shiftKey && this.sel.size) { this.sel.clear(); this.paintSel(); }
      const v = this.D.view, sx = e.clientX, sy = e.clientY, ox = v.x, oy = v.y;
      this.stage.addClass('is-pan');
      this.track((ev) => { v.x = ox + ev.clientX - sx; v.y = oy + ev.clientY - sy; this.applyView(); },
        () => { this.stage.removeClass('is-pan'); this.plugin.saveSoon(); });
    });
    this.stage.addEventListener('dblclick', (e) => {
      if (e.target.closest('.tka-node,.tka-tools')) return;
      this.promptCreate(null, this.toWorld(e.clientX, e.clientY));
    });
  }
  bindNodes() {
    this.layer.onpointerdown = (e) => {
      const el = e.target.closest('.tka-node'); if (!el || e.button !== 0) return;
      const p = el.dataset.path;
      if (e.target.closest('.tka-port')) return this.startConnect(e, p);
      if (e.target.closest('.tka-chk,.tka-open')) return;
      this.startDrag(e, p);
    };
    this.layer.oncontextmenu = (e) => {
      const el = e.target.closest('.tka-node'); if (!el) return;
      e.preventDefault(); this.nodeMenu(e, el.dataset.path);
    };
  }
  startDrag(e, p) {
    if (e.shiftKey) { this.sel.has(p) ? this.sel.delete(p) : this.sel.add(p); }
    else if (!this.sel.has(p)) this.sel = new Set([p]);
    this.paintSel();
    const k = this.D.view.k, sx = e.clientX, sy = e.clientY;
    const orig = new Map([...this.sel].map((q) => [q, { ...this.D.pos[q] }]));
    let moved = false; this.dragging = true;
    this.track((ev) => {
      const dx = (ev.clientX - sx) / k, dy = (ev.clientY - sy) / k;
      if (!moved && Math.hypot(dx, dy) * k < 3) return;
      moved = true;
      orig.forEach((o, q) => { this.D.pos[q] = { x: o.x + dx, y: o.y + dy }; this.placeEl(q); });
      this.drawEdges();
    }, () => { this.dragging = false; if (moved) { this.plugin.saveSoon(); this.drawLanes(); } });
  }
  startConnect(e, p) {
    e.preventDefault(); e.stopPropagation();
    const q = this.D.pos[p], s = this.size(p), a = { x: q.x + s.w, y: q.y + s.h / 2 };
    const tmp = document.createElementNS(SVGNS, 'path'); tmp.classList.add('tka-tmp'); this.edgeG.appendChild(tmp);
    let hover = null; this.dragging = true;
    this.track((ev) => {
      tmp.setAttribute('d', this.bez(a, this.toWorld(ev.clientX, ev.clientY)));
      const t = document.elementFromPoint(ev.clientX, ev.clientY), n = t && t.closest('.tka-node');
      if (hover && hover !== n) hover.removeClass('is-target');
      hover = n && n.dataset.path !== p ? n : null; if (hover) hover.addClass('is-target');
    }, (ev) => {
      tmp.remove(); this.dragging = false; if (hover) hover.removeClass('is-target');
      const t = document.elementFromPoint(ev.clientX, ev.clientY), n = t && t.closest('.tka-node');
      if (n && n.dataset.path !== p) this.link(p, n.dataset.path);
      else if (!n && t && this.stage.contains(t) && !t.closest('.tka-tools')) this.promptCreate(p, this.toWorld(ev.clientX, ev.clientY));
    });
  }
  nodeMenu(e, p) {
    const n = this.model.nodes.get(p), m = new Menu();
    m.addItem((i) => i.setTitle('Abrir nota').setIcon('file-text').onClick(() => this.app.workspace.getLeaf('tab').openFile(n.file)));
    if (!(this.S.scope === 'roadmap' && n.type === 'task')) m.addItem((i) => i.setTitle('Nueva subtarea').setIcon('git-branch').onClick(() => {
      const q = this.D.pos[p], s = this.size(p); this.promptCreate(p, { x: q.x + GX, y: q.y + s.h + 20 });
    }));
    if (n.type === 'task' && this.S.scope === 'roadmap') {
      m.addItem((i) => i.setTitle('Ver plan del paso').setIcon('layout-list').onClick(() => { this.sel = new Set([p]); this.paintSel(); this.renderSide(); }));
      m.addSeparator();
      [['habito', '＋ Hábito', 'repeat'], ['sesion', '＋ Sesión de trabajo profundo', 'timer'], ['accion', '＋ Tarea o acción', 'check-square'], ['subtarea', '＋ Subtarea', 'list-checks']].forEach(([k, t, ic]) => m.addItem((i) => i.setTitle(t).setIcon(ic).onClick(() => this.addToStep(n, k))));
      const pl = this.plan(n);
      const links = [...pl.notas.filter((x) => x.d).map((x) => x.d), ...pl.rel].slice(0, 6);
      if (links.length) { m.addSeparator(); links.forEach((f) => m.addItem((i) => i.setTitle('📄 ' + f.basename).onClick(() => this.app.workspace.getLeaf('tab').openFile(f)))); }
      const items = [...pl.hab, ...pl.ses].slice(0, 6);
      if (items.length) { m.addSeparator(); items.forEach((o) => m.addItem((i) => i.setTitle((o.fm.tipo === 'sesion' ? '🎯 ' : '↻ ') + o.f.basename.replace(/^(Hábito \w+|Sesión de trabajo profundo) · /, '')).onClick(() => this.app.workspace.getLeaf('tab').openFile(o.f)))); }
    }
    if (n.type === 'task') {
      m.addSeparator();
      STATUSES.forEach((s) => m.addItem((i) => i.setTitle('Estado: ' + s.label).setChecked(n.status === s.id).onClick(() => this.setStatus(p, s.id))));
      m.addSeparator();
      PRIOS.forEach((s) => m.addItem((i) => i.setTitle('Prioridad: ' + s.label).setChecked(n.priority === s.id).onClick(() => this.setField(p, 'priority', s.id))));
      const pars = this.parents.get(p) || [];
      if (pars.length) { m.addSeparator(); m.addItem((i) => i.setTitle('Desconectar de padres').setIcon('unlink').onClick(() => pars.forEach((q) => this.unlink(q, p)))); }
    }
    m.showAtMouseEvent(e);
  }

  // ---------- escritura en el vault ----------
  async edit(p, fn) {
    const n = this.model.nodes.get(p); if (!n || n.type !== 'task') return;
    await this.app.fileManager.processFrontMatter(n.file, (fm) => { fn(fm); fm.dateModified = isoNow(); });
  }
  setStatus(p, st) {
    return this.edit(p, (fm) => { fm.status = st; if (st === 'done') fm.completedDate = today(); else delete fm.completedDate; });
  }
  setField(p, k, v) { return this.edit(p, (fm) => { fm[k] = v; }); }
  async link(parent, child) {
    const c = this.model.nodes.get(child), pn = this.model.nodes.get(parent);
    if (!c || c.type !== 'task') return new Notice('Las notas enlazadas solo pueden ser padres, no hijos.');
    if (pn && (pn.type === 'area' || pn.type === 'cliente')) { const lt0 = this.app.metadataCache.fileToLinktext(pn.file, c.file.path, true); const k0 = this.S.scope === 'clientes' ? 'cliente' : 'area'; if (pn.type === 'area' && this.S.scope === 'clientes') return new Notice('Las tareas cuelgan de un cliente, no del grupo.'); return this.edit(child, (fm) => { fm[k0] = `[[${lt0}]]`; }); }
    if (pn && pn.type === 'hub') return new Notice('Las tareas cuelgan de un área, no del hub.');
    if (this.descendants(child).has(parent)) return new Notice('Eso crearía un ciclo.');
    if ((this.children.get(parent) || []).includes(child)) return;
    const lt = this.app.metadataCache.fileToLinktext(pn.file, c.file.path, true);
    await this.edit(child, (fm) => { const arr = projectLinks(fm.projects); arr.push(`[[${lt}]]`); fm.projects = arr; });
  }
  async unlink(parent, child) {
    const c = this.model.nodes.get(child); if (!c) return;
    const par0 = this.model.nodes.get(parent);
    if (par0 && (par0.type === 'area' || par0.type === 'cliente')) return this.edit(child, (fm) => { delete fm[this.S.scope === 'clientes' ? 'cliente' : 'area']; });
    await this.edit(child, (fm) => {
      const keep = projectLinks(fm.projects).filter((l) => {
        const lp = parseLink(l), d = lp && this.app.metadataCache.getFirstLinkpathDest(lp, c.file.path);
        return !(d && d.path === parent);
      });
      if (keep.length) fm.projects = keep; else delete fm.projects;
    });
  }
  promptCreate(parent, at) {
    const pn = parent && this.model.nodes.get(parent);
    new NewTaskModal(this.app, { parentTitle: pn && pn.title }, async (title, prio, sched) => {
      const folder = this.S.tasksFolder.replace(/\/+$/, '');
      const base = title.replace(/[\\/:*?"<>|#^\[\]]/g, '').replace(/\s+/g, ' ').trim().slice(0, 120) || 'Tarea';
      let path = `${folder}/${base}.md`, i = 2;
      while (this.app.vault.getAbstractFileByPath(path)) path = `${folder}/${base} ${i++}.md`;
      const now = isoNow();
      let y = `---\nstatus: open\npriority: ${prio}\n`;
      if (sched) y += `scheduled: ${sched}\n`;
      if (pn && (pn.type === 'area' || pn.type === 'cliente')) y += `${this.S.scope === 'clientes' ? 'cliente' : 'area'}: \"[[${pn.file.basename}]]\"\n`;
      else if (pn) y += `projects:\n  - "[[${this.app.metadataCache.fileToLinktext(pn.file, path, true)}]]"\n`;
      y += `dateCreated: ${now}\ndateModified: ${now}\ntags:\n  - task\n---\n`;
      this.D.pos[path] = { x: at.x, y: at.y };
      await this.app.vault.create(path, y);
      this.plugin.saveSoon();
      setTimeout(() => this.refresh(), 400);
    }).open();
  }
}

class TaskSpaceSettings extends PluginSettingTab {
  constructor(app, plugin) { super(app, plugin); this.plugin = plugin; }
  display() {
    const el = this.containerEl; el.empty();
    new Setting(el).setName('Carpeta de tareas').setDesc('Donde TaskNotes guarda una nota por tarea.')
      .addText((t) => t.setValue(this.plugin.data.settings.tasksFolder).onChange((v) => { this.plugin.data.settings.tasksFolder = v.trim() || 'TaskNotes/Tasks'; this.plugin.saveSoon(); }));
    new Setting(el).setName('Alcance').setDesc('Operaciones: solo hub Big Picture → áreas → tareas con campo `area`. Todo: comportamiento anterior (por `projects`).')
      .addDropdown((d) => d.addOption('roadmap', 'Roadmap (metas → pasos)').addOption('habitos', 'Hábitos').addOption('operaciones', 'Operaciones por áreas').addOption('clientes', 'Clientes').addOption('todo', 'Todo').setValue(this.plugin.data.settings.scope).onChange((v) => { this.plugin.data.settings.scope = v; this.plugin.saveSoon(); }));
    new Setting(el).setName('Carpeta de metas').setDesc('Notas `type: meta|norte` del Roadmap. Las tareas se enlazan con `meta` y `depende_de`.')
      .addText((t) => t.setValue(this.plugin.data.settings.metasFolder).onChange((v) => { this.plugin.data.settings.metasFolder = v.trim() || 'Roadmap/Metas'; this.plugin.saveSoon(); }));
    new Setting(el).setName('Carpeta de áreas').setDesc('Notas con `type: area` (frontmatter: nombre, color, responsable, orden, padre).')
      .addText((t) => t.setValue(this.plugin.data.settings.areasFolder).onChange((v) => { this.plugin.data.settings.areasFolder = v.trim() || 'Operaciones/Áreas'; this.plugin.saveSoon(); }));
    new Setting(el).setName('Carpeta de la vista Clientes').setDesc('Hub, grupos y clientes (`type: area|cliente`). Las tareas se enlazan con el campo `cliente`.')
      .addText((t) => t.setValue(this.plugin.data.settings.clientesFolder).onChange((v) => { this.plugin.data.settings.clientesFolder = v.trim() || 'Clientes/Vista Task Atlas'; this.plugin.saveSoon(); }));
    new Setting(el).setName('Mostrar notas enlazadas').setDesc('Muestra como nodos las notas (Cadence, clientes…) a las que apuntan las tareas con `projects`.')
      .addToggle((t) => t.setValue(this.plugin.data.settings.showNotes).onChange((v) => { this.plugin.data.settings.showNotes = v; this.plugin.saveSoon(); }));
    new Setting(el).setName('Reiniciar posiciones').setDesc('Borra las posiciones guardadas; el próximo "Organizar" recalcula todo.')
      .addButton((b) => b.setButtonText('Reiniciar').onClick(async () => { this.plugin.data.pos = {}; this.plugin.data.fitted = false; await this.plugin.saveData(this.plugin.data); new Notice('Posiciones reiniciadas'); }));
  }
}

module.exports = class TaskAtlas extends Plugin {
  async onload() {
    const d = (await this.loadData()) || {};
    this.data = Object.assign({ pos: {}, view: { x: 80, y: 80, k: 1 }, fitted: false }, d);
    this.data.settings = Object.assign({ tasksFolder: 'TaskNotes/Tasks', showNotes: true, hideDone: false, filter: '', layout: 'tree', lanes: true, scope: 'roadmap', metasFolder: 'Roadmap/Metas', areasFolder: 'Operaciones/Áreas', clientesFolder: 'Clientes/Vista Task Atlas' }, d.settings || {});
    if (!d.v08) { this.data.pos = {}; this.data.fitted = false; this.data.settings.filter = ''; this.data.settings.scope = 'roadmap'; this.data.v08 = true; }
    this.saveSoon = debounce(() => this.saveData(this.data), 600, true);
    this.registerView(VIEW, (leaf) => new TaskSpaceView(leaf, this));
    this.addRibbonIcon('network', 'Task Atlas', () => this.activate());
    this.addCommand({ id: 'open', name: 'Abrir Task Atlas', callback: () => this.activate() });
    this.addSettingTab(new TaskSpaceSettings(this.app, this));
  }
  async activate() {
    let leaf = this.app.workspace.getLeavesOfType(VIEW)[0];
    if (!leaf) { leaf = this.app.workspace.getLeaf('tab'); await leaf.setViewState({ type: VIEW, active: true }); }
    this.app.workspace.revealLeaf(leaf);
  }
  async exportCanvas(view) {
    view.buildModel();
    const nodes = view.vis(), ids = new Map(), cn = [], ce = [];
    let i = 0;
    for (const [p, n] of nodes) {
      const q = view.D.pos[p]; if (!q) continue;
      const id = 'n' + i++; ids.set(p, id);
      const color = n.status === 'done' ? '4' : n.status === 'in-progress' ? '5' : n.type === 'hub' ? '4' : n.type === 'area' ? '6' : n.type === 'cliente' ? '5' : n.type === 'note' ? '6' : n.priority === 'high' ? '1' : n.priority === 'normal' ? '3' : '0';
      cn.push({ id, type: 'file', file: p, x: Math.round(q.x * 1.15), y: Math.round(q.y * 1.15), width: 280, height: n.type === 'note' ? 100 : 90, color });
    }
    if (this.data.settings.lanes) {
      const groups = new Map();
      for (const p of ids.keys()) { const k = view.laneOf(p, nodes); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(p); }
      const gs = [];
      for (const [k, ps] of groups) {
        const bs = ps.map((p) => cn.find((c) => c.id === ids.get(p)));
        const x0 = Math.min(...bs.map((b) => b.x)), y0 = Math.min(...bs.map((b) => b.y)), x1 = Math.max(...bs.map((b) => b.x + b.width)), y1 = Math.max(...bs.map((b) => b.y + b.height));
        gs.push({ id: 'g' + gs.length, type: 'group', label: k === '__none' ? (this.data.settings.scope === 'operaciones' ? 'Big Picture' : this.data.settings.scope === 'clientes' ? 'Clientes' : 'Sin proyecto') : nodes.get(k).title, x: x0 - 30, y: y0 - 60, width: x1 - x0 + 60, height: y1 - y0 + 90 });
      }
      cn.unshift(...gs);
    }
    view.model.edges.forEach((e, j) => { if (ids.has(e.from) && ids.has(e.to)) ce.push({ id: 'e' + j, fromNode: ids.get(e.from), toNode: ids.get(e.to), fromSide: 'right', toSide: 'left', toEnd: 'arrow' }); });
    const path = 'Canvas/Task Atlas.canvas', text = JSON.stringify({ nodes: cn, edges: ce }, null, 1);
    if (!this.app.vault.getAbstractFileByPath('Canvas')) await this.app.vault.createFolder('Canvas');
    const ex = this.app.vault.getAbstractFileByPath(path);
    const f = ex ? (await this.app.vault.modify(ex, text), ex) : await this.app.vault.create(path, text);
    new Notice(`Exportado: ${cn.length} elementos → ${path}`);
    this.app.workspace.getLeaf('tab').openFile(f);
  }
  onunload() { this.app.workspace.detachLeavesOfType(VIEW); }
};
