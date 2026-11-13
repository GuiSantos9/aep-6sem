'use strict';

/* ── Config ──────────────────────────────────────────── */
const BASE_URL = 'http://localhost:8000';

/* ── Helpers de apresentação ─────────────────────────── */
const TIPO_LABEL = {
  banco_dividido:          'Banco Dividido',
  espigao_metalico:        'Espigão Metálico',
  inclinacao_de_superficie:'Inclinação de Superfície',
  retirada_de_assento:     'Retirada de Assento',
  barreira_fisica:         'Barreira Física',
  emissao_sonora:          'Emissão Sonora',
  aspersor_de_agua:        'Aspersor de Água',
  outro:                   'Outro',
};

const PRIORIDADE_LABEL = {
  baixa:   'Baixa',
  media:   'Média',
  alta:    'Alta',
  urgente: 'Urgente',
};

const STATUS_LABEL = {
  registrada:  'Registrada',
  em_analise:  'Em Análise',
  encaminhada: 'Encaminhada',
  resolvida:   'Resolvida',
  arquivada:   'Arquivada',
};

function formatDate(iso) {
  if (!iso) return '';
  return new Date(iso).toLocaleDateString('pt-BR', {
    day: '2-digit', month: 'short', year: 'numeric',
  });
}

/* ── Estado da aplicação ─────────────────────────────── */
const state = {
  page:       0,
  limit:      12,
  total:      0,
  tipo:       '',
  prioridade: '',
  local:      '',
  locais:     [],
  editingId:  null,
  deletingId: null,
};

/* ── API ─────────────────────────────────────────────── */
const api = {
  async request(method, path, body) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body !== undefined) opts.body = JSON.stringify(body);
    const res = await fetch(BASE_URL + path, opts);
    if (res.status === 204) return null;
    const data = await res.json();
    if (!res.ok) {
      const msg = data?.detail
        ? (Array.isArray(data.detail)
            ? data.detail.map(e => e.msg).join('; ')
            : data.detail)
        : `Erro ${res.status}`;
      throw new Error(msg);
    }
    return data;
  },

  health:    ()             => api.request('GET', '/health'),
  list:      (params)       => api.request('GET', `/denuncias?${new URLSearchParams(params)}`),
  create:    (payload)      => api.request('POST', '/denuncias', payload),
  update:    (id, payload)  => api.request('PATCH', `/denuncias/${id}`, payload),
  delete:    (id)           => api.request('DELETE', `/denuncias/${id}`),

  listLocais:    ()          => api.request('GET', '/locais'),
  createLocal:   (payload)   => api.request('POST', '/locais', payload),
  deleteLocal:   (id)        => api.request('DELETE', `/locais/${id}`),
  denunciasDoLocal: (id)     => api.request('GET', `/locais/${id}/denuncias`),
};

/* ── Toast ───────────────────────────────────────────── */
let toastTimer;
function showToast(msg, type = 'ok') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = `toast toast-${type}`;
  el.classList.remove('hidden');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.add('hidden'), 3000);
}

/* ── Health check ────────────────────────────────────── */
async function checkHealth() {
  const el = document.getElementById('health-badge');
  try {
    await api.health();
    el.textContent = '⬤ online';
    el.className = 'health-badge health-ok';
  } catch {
    el.textContent = '⬤ offline';
    el.className = 'health-badge health-error';
  }
}

/* ── Render lista ────────────────────────────────────── */
function renderList(items, total) {
  const grid    = document.getElementById('denuncia-grid');
  const empty   = document.getElementById('empty-state');
  const summary = document.getElementById('list-summary');
  const pag     = document.getElementById('pagination');

  grid.innerHTML = '';

  if (items.length === 0) {
    empty.classList.remove('hidden');
    summary.textContent = '';
    pag.classList.add('hidden');
    return;
  }

  empty.classList.add('hidden');

  const from = state.page * state.limit + 1;
  const to   = Math.min(state.page * state.limit + items.length, total);
  summary.textContent = `Exibindo ${from}–${to} de ${total} denúncia${total !== 1 ? 's' : ''}`;

  items.forEach(d => grid.appendChild(buildCard(d)));

  renderPagination(total);
}

function buildCard(d) {
  const card = document.createElement('article');
  card.className = 'card';
  card.dataset.id = d.id;

  const addr = [d.logradouro, d.numero, d.bairro, `${d.cidade}/${d.uf}`]
    .filter(Boolean).join(', ');

  card.innerHTML = `
    <div class="card-top">
      <h3 class="card-title">${esc(d.titulo)}</h3>
      <div class="card-actions">
        <button class="btn-icon" title="Editar" data-action="edit" data-id="${d.id}"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></button>
        <button class="btn-icon" title="Excluir" data-action="delete" data-id="${d.id}"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg></button>
      </div>
    </div>
    <div class="card-badges">
      <span class="badge badge-tipo">${esc(TIPO_LABEL[d.tipo] || d.tipo)}</span>
      <span class="badge badge-${d.prioridade}">${esc(PRIORIDADE_LABEL[d.prioridade] || d.prioridade)}</span>
      <span class="badge badge-${d.status}">${esc(STATUS_LABEL[d.status] || d.status)}</span>
    </div>
    <p class="card-descricao">${esc(d.descricao)}</p>
    <p class="card-address">${esc(addr)}</p>
    ${d.local_id ? `<p class="card-address">📍 ${esc(localNome(d.local_id))}</p>` : ''}
    <div class="card-footer">
      <span class="card-date">${(d.historico || []).length} registro(s) no histórico · ${formatDate(d.criado_em)}</span>
    </div>
  `;

  card.addEventListener('click', e => {
    const action = e.target.closest('[data-action]');
    if (!action) { openEdit(d); return; }
    e.stopPropagation();
    if (action.dataset.action === 'edit')   openEdit(d);
    if (action.dataset.action === 'delete') openConfirmDelete(d.id);
  });

  return card;
}

/* ── Paginação ───────────────────────────────────────── */
function renderPagination(total) {
  const pag       = document.getElementById('pagination');
  const totalPages = Math.ceil(total / state.limit);

  if (totalPages <= 1) { pag.classList.add('hidden'); return; }

  pag.classList.remove('hidden');
  pag.innerHTML = `
    <button class="btn btn-secondary" id="pg-prev" ${state.page === 0 ? 'disabled' : ''}>← Anterior</button>
    <span class="page-info">Página ${state.page + 1} de ${totalPages}</span>
    <button class="btn btn-secondary" id="pg-next" ${state.page >= totalPages - 1 ? 'disabled' : ''}>Próxima →</button>
  `;

  document.getElementById('pg-prev').addEventListener('click', () => { state.page--; loadList(); });
  document.getElementById('pg-next').addEventListener('click', () => { state.page++; loadList(); });
}

/* ── Carregamento ────────────────────────────────────── */
async function loadList() {
  const loading = document.getElementById('loading');
  const grid    = document.getElementById('denuncia-grid');
  loading.classList.remove('hidden');
  grid.innerHTML = '';

  const params = {
    limit:  state.limit,
    offset: state.page * state.limit,
  };
  if (state.tipo)       params.tipo       = state.tipo;
  if (state.prioridade) params.prioridade = state.prioridade;
  if (state.local)      params.local_id   = state.local;

  try {
    const data = await api.list(params);
    state.total = data.total;
    renderList(data.items, data.total);
  } catch (err) {
    showToast('Erro ao carregar denúncias: ' + err.message, 'error');
  } finally {
    loading.classList.add('hidden');
  }
}

/* ── Modal ───────────────────────────────────────────── */
function openModal() {
  document.getElementById('modal-overlay').classList.remove('hidden');
  document.getElementById('f-titulo').focus();
}

function renderHistorico(historico) {
  const group = document.getElementById('historico-group');
  const list  = document.getElementById('historico-list');
  list.innerHTML = '';
  if (!historico || historico.length === 0) { group.classList.add('hidden'); return; }
  historico.slice().reverse().forEach(h => {
    const li = document.createElement('li');
    const de = h.status_anterior
      ? `<span class="badge badge-${h.status_anterior}">${esc(STATUS_LABEL[h.status_anterior])}</span> →`
      : '';
    li.innerHTML = `
      <div class="timeline-status">${de}
        <span class="badge badge-${h.status_novo}">${esc(STATUS_LABEL[h.status_novo])}</span>
      </div>
      <p class="timeline-obs">${esc(h.observacao)}</p>
      <span class="timeline-date">${new Date(h.data + (h.data.endsWith('Z') ? '' : 'Z')).toLocaleString('pt-BR')}</span>`;
    list.appendChild(li);
  });
  group.classList.remove('hidden');
}

function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden');
  document.getElementById('denuncia-form').reset();
  document.getElementById('form-error').classList.add('hidden');
  document.getElementById('status-group').style.display = 'none';
  document.getElementById('obs-group').style.display = 'none';
  document.getElementById('historico-group').classList.add('hidden');
  state.editingId = null;
}

function openCreate() {
  state.editingId = null;
  document.getElementById('modal-title').textContent = 'Nova Denúncia';
  document.getElementById('btn-submit').textContent  = 'Criar';
  document.getElementById('status-group').style.display = 'none';
  document.getElementById('obs-group').style.display = 'none';
  document.getElementById('historico-group').classList.add('hidden');
  document.getElementById('denuncia-form').reset();
  openModal();
}

function openEdit(d) {
  state.editingId = d.id;
  document.getElementById('modal-title').textContent = 'Editar Denúncia';
  document.getElementById('btn-submit').textContent  = 'Salvar';
  document.getElementById('status-group').style.display = '';
  document.getElementById('obs-group').style.display = '';

  const form = document.getElementById('denuncia-form');
  const set  = (name, val) => { if (form.elements[name]) form.elements[name].value = val ?? ''; };

  set('titulo',      d.titulo);
  set('tipo',        d.tipo);
  set('prioridade',  d.prioridade);
  set('status',      d.status);
  set('descricao',   d.descricao);
  set('logradouro',  d.logradouro);
  set('numero',      d.numero);
  set('complemento', d.complemento);
  set('bairro',      d.bairro);
  set('cidade',      d.cidade);
  set('uf',          d.uf);
  set('cep',         d.cep);
  set('local_id',    d.local_id);
  renderHistorico(d.historico);

  if (form.elements['evidencias']) {
    form.elements['evidencias'].value = (d.evidencias || []).join('\n');
  }

  openModal();
}

/* ── Submit formulário ───────────────────────────────── */
async function handleFormSubmit(e) {
  e.preventDefault();
  const form    = document.getElementById('denuncia-form');
  const errEl   = document.getElementById('form-error');
  const submitBtn = document.getElementById('btn-submit');

  errEl.classList.add('hidden');

  const data = Object.fromEntries(new FormData(form).entries());

  // evidências: string -> array de URLs
  const evidencias = (data.evidencias || '')
    .split('\n')
    .map(s => s.trim())
    .filter(Boolean);
  data.evidencias = evidencias;

  // campos opcionais vazios -> omitir
  ['numero', 'complemento', 'cep', 'observacao'].forEach(k => {
    if (!data[k]) delete data[k];
  });
  // local: vazio -> omitir na criação, desvincular (null) na edição
  if (!data.local_id) {
    if (state.editingId) data.local_id = null; else delete data.local_id;
  }
  if (!state.editingId) delete data.observacao;

  // em edição: enviar só campos alterados (todos presentes)
  submitBtn.disabled = true;
  submitBtn.textContent = 'Salvando...';

  try {
    if (state.editingId) {
      await api.update(state.editingId, data);
      showToast('Denúncia atualizada com sucesso.', 'ok');
    } else {
      await api.create(data);
      showToast('Denúncia criada com sucesso!', 'ok');
    }
    closeModal();
    state.page = 0;
    loadList();
  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.remove('hidden');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = state.editingId ? 'Salvar' : 'Criar';
  }
}

/* ── Exclusão ────────────────────────────────────────── */
function openConfirmDelete(id) {
  state.deletingId = id;
  document.getElementById('confirm-overlay').classList.remove('hidden');
}

function closeConfirm() {
  document.getElementById('confirm-overlay').classList.add('hidden');
  document.getElementById('confirm-text').textContent =
    'Tem certeza que deseja excluir esta denúncia? A ação não pode ser desfeita.';
  state.deletingId = null;
  state.deletingLocal = null;
}

async function handleDelete() {
  const btn = document.getElementById('confirm-delete');
  btn.disabled = true;
  btn.textContent = 'Excluindo...';
  try {
    if (state.deletingLocal) {
      await api.deleteLocal(state.deletingLocal);
      showToast('Local excluído.', 'ok');
      closeConfirm();
      loadLocais();
      return;
    }
    await api.delete(state.deletingId);
    showToast('Denúncia excluída.', 'ok');
    closeConfirm();
    loadList();
  } catch (err) {
    showToast('Erro ao excluir: ' + err.message, 'error');
    closeConfirm();
  } finally {
    btn.disabled = false;
    btn.textContent = 'Excluir';
  }
}

/* ── Locais ──────────────────────────────────────────── */
function localNome(id) {
  const l = state.locais.find(x => x.id === id);
  return l ? l.nome : 'Local removido';
}

function fillLocalSelects() {
  const opts = state.locais.map(l => `<option value="${l.id}">${esc(l.nome)}</option>`).join('');
  const filtro = document.getElementById('filter-local');
  const form   = document.getElementById('f-local');
  const f = filtro.value, v = form.value;
  filtro.innerHTML = '<option value="">Todos os locais</option>' + opts;
  form.innerHTML   = '<option value="">Sem local vinculado</option>' + opts;
  filtro.value = f;
  form.value   = v;
}

async function loadLocais() {
  try {
    const data = await api.listLocais();
    state.locais = data.items;
    fillLocalSelects();
    renderLocais();
  } catch (err) {
    showToast('Erro ao carregar locais: ' + err.message, 'error');
  }
}

function renderLocais() {
  const grid  = document.getElementById('local-grid');
  const empty = document.getElementById('locais-empty');
  const sum   = document.getElementById('locais-summary');
  grid.innerHTML = '';
  empty.classList.toggle('hidden', state.locais.length > 0);
  const n = state.locais.length;
  sum.textContent = n ? `${n} local${n !== 1 ? 'is' : ''} cadastrado${n !== 1 ? 's' : ''}` : '';

  state.locais.forEach(l => {
    const card = document.createElement('article');
    card.className = 'card';
    card.innerHTML = `
      <div class="card-top">
        <h3 class="card-title">${esc(l.nome)}</h3>
        <div class="card-actions">
          <button class="btn-icon" title="Excluir" data-action="delete"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg></button>
        </div>
      </div>
      <p class="card-address">${esc([l.bairro, `${l.cidade}/${l.uf}`].join(', '))}</p>
      ${l.referencia ? `<p class="card-descricao">${esc(l.referencia)}</p>` : ''}
      <div class="card-footer"><span class="card-date">Clique para ver as denúncias · ${formatDate(l.criado_em)}</span></div>`;
    card.addEventListener('click', e => {
      if (e.target.closest('[data-action="delete"]')) { openConfirmDeleteLocal(l.id); return; }
      openLocalDenuncias(l);
    });
    grid.appendChild(card);
  });
}

async function openLocalDenuncias(l) {
  const body = document.getElementById('locdenuncias-body');
  document.getElementById('locdenuncias-title').textContent = `Denúncias — ${l.nome}`;
  body.innerHTML = '<p class="list-summary">Carregando...</p>';
  document.getElementById('locdenuncias-overlay').classList.remove('hidden');
  try {
    const data = await api.denunciasDoLocal(l.id);
    body.innerHTML = data.items.length
      ? data.items.map(d => `
          <div class="mini-row">
            <strong>${esc(d.titulo)}</strong>
            <div class="card-badges">
              <span class="badge badge-tipo">${esc(TIPO_LABEL[d.tipo] || d.tipo)}</span>
              <span class="badge badge-${d.prioridade}">${esc(PRIORIDADE_LABEL[d.prioridade])}</span>
              <span class="badge badge-${d.status}">${esc(STATUS_LABEL[d.status])}</span>
            </div>
          </div>`).join('')
      : '<p class="list-summary">Nenhuma denúncia vinculada a este local.</p>';
  } catch (err) {
    body.innerHTML = `<p class="form-error">${esc(err.message)}</p>`;
  }
}

function openLocalModal()  {
  document.getElementById('local-overlay').classList.remove('hidden');
  document.getElementById('l-nome').focus();
}
function closeLocalModal() {
  document.getElementById('local-overlay').classList.add('hidden');
  document.getElementById('local-form').reset();
  document.getElementById('local-error').classList.add('hidden');
}

async function handleLocalSubmit(e) {
  e.preventDefault();
  const errEl = document.getElementById('local-error');
  errEl.classList.add('hidden');
  const data = Object.fromEntries(new FormData(e.target).entries());
  if (!data.referencia) delete data.referencia;
  try {
    await api.createLocal(data);
    showToast('Local criado com sucesso!', 'ok');
    closeLocalModal();
    loadLocais();
  } catch (err) {
    errEl.textContent = err.message;
    errEl.classList.remove('hidden');
  }
}

function openConfirmDeleteLocal(id) {
  state.deletingLocal = id;
  document.getElementById('confirm-text').textContent =
    'Tem certeza que deseja excluir este local? Locais com denúncias vinculadas não podem ser excluídos.';
  document.getElementById('confirm-overlay').classList.remove('hidden');
}

function switchView(view) {
  ['denuncias', 'locais'].forEach(v => {
    document.getElementById(`view-${v}`).classList.toggle('hidden', v !== view);
    document.getElementById(`tab-${v}`).classList.toggle('active', v === view);
  });
}

/* ── Escape HTML ─────────────────────────────────────── */
function esc(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ── Event listeners ─────────────────────────────────── */
document.getElementById('btn-nova').addEventListener('click', openCreate);
document.getElementById('btn-cancel').addEventListener('click', closeModal);
document.getElementById('modal-close').addEventListener('click', closeModal);
document.getElementById('denuncia-form').addEventListener('submit', handleFormSubmit);

document.getElementById('btn-limpar').addEventListener('click', () => {
  document.getElementById('filter-tipo').value = '';
  document.getElementById('filter-prioridade').value = '';
  document.getElementById('filter-local').value = '';
  state.tipo       = '';
  state.prioridade = '';
  state.local      = '';
  state.page = 0;
  loadList();
});

// buscar ao pressionar Enter nos filtros
['filter-tipo', 'filter-prioridade', 'filter-local'].forEach(id => {
  document.getElementById(id).addEventListener('change', () => {
    state.tipo       = document.getElementById('filter-tipo').value;
    state.prioridade = document.getElementById('filter-prioridade').value;
    state.local      = document.getElementById('filter-local').value;
    state.page = 0;
    loadList();
  });
});

document.getElementById('confirm-cancel').addEventListener('click', closeConfirm);
document.getElementById('confirm-delete').addEventListener('click', handleDelete);

// fechar modais ao clicar fora
document.getElementById('modal-overlay').addEventListener('click', e => {
  if (e.target === e.currentTarget) closeModal();
});
document.getElementById('confirm-overlay').addEventListener('click', e => {
  if (e.target === e.currentTarget) closeConfirm();
});

document.getElementById('btn-novo-local').addEventListener('click', openLocalModal);
document.getElementById('local-cancel').addEventListener('click', closeLocalModal);
document.getElementById('local-close').addEventListener('click', closeLocalModal);
document.getElementById('local-form').addEventListener('submit', handleLocalSubmit);
document.getElementById('locdenuncias-close').addEventListener('click',
  () => document.getElementById('locdenuncias-overlay').classList.add('hidden'));
['local-overlay', 'locdenuncias-overlay'].forEach(id => {
  document.getElementById(id).addEventListener('click', e => {
    if (e.target === e.currentTarget) e.currentTarget.classList.add('hidden');
  });
});
document.querySelectorAll('.tab').forEach(t =>
  t.addEventListener('click', () => switchView(t.dataset.view)));

// fechar com Escape
document.addEventListener('keydown', e => {
  if (e.key !== 'Escape') return;
  for (const id of ['local-overlay', 'locdenuncias-overlay']) {
    const el = document.getElementById(id);
    if (!el.classList.contains('hidden')) { el.classList.add('hidden'); return; }
  }
  if (!document.getElementById('confirm-overlay').classList.contains('hidden')) { closeConfirm(); return; }
  if (!document.getElementById('modal-overlay').classList.contains('hidden'))   { closeModal();   return; }
});

/* ── Init ────────────────────────────────────────────── */
checkHealth();
loadLocais().then(loadList);
