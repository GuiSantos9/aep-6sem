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
    <p class="card-address">📍 ${esc(addr)}</p>
    <div class="card-footer">
      <span class="card-date">📅 ${formatDate(d.criado_em)}</span>
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

function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden');
  document.getElementById('denuncia-form').reset();
  document.getElementById('form-error').classList.add('hidden');
  document.getElementById('status-group').style.display = 'none';
  state.editingId = null;
}

function openCreate() {
  state.editingId = null;
  document.getElementById('modal-title').textContent = 'Nova Denúncia';
  document.getElementById('btn-submit').textContent  = 'Criar';
  document.getElementById('status-group').style.display = 'none';
  document.getElementById('denuncia-form').reset();
  openModal();
}

function openEdit(d) {
  state.editingId = d.id;
  document.getElementById('modal-title').textContent = 'Editar Denúncia';
  document.getElementById('btn-submit').textContent  = 'Salvar';
  document.getElementById('status-group').style.display = '';

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
  ['numero', 'complemento', 'cep'].forEach(k => {
    if (!data[k]) delete data[k];
  });

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
  state.deletingId = null;
}

async function handleDelete() {
  const btn = document.getElementById('confirm-delete');
  btn.disabled = true;
  btn.textContent = 'Excluindo...';
  try {
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

document.getElementById('btn-buscar').addEventListener('click', () => {
  state.tipo       = document.getElementById('filter-tipo').value;
  state.prioridade = document.getElementById('filter-prioridade').value;
  state.page = 0;
  loadList();
});

// buscar ao pressionar Enter nos filtros
['filter-tipo', 'filter-prioridade'].forEach(id => {
  document.getElementById(id).addEventListener('change', () => {
    state.tipo       = document.getElementById('filter-tipo').value;
    state.prioridade = document.getElementById('filter-prioridade').value;
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

// fechar com Escape
document.addEventListener('keydown', e => {
  if (e.key !== 'Escape') return;
  if (!document.getElementById('confirm-overlay').classList.contains('hidden')) { closeConfirm(); return; }
  if (!document.getElementById('modal-overlay').classList.contains('hidden'))   { closeModal();   return; }
});

/* ── Init ────────────────────────────────────────────── */
checkHealth();
loadList();
