# 📌 Funcionamento do Sistema

O sistema permite que usuários autenticados cadastrem ocorrências, consultem registros existentes e abram chamados para os órgãos ou instituições responsáveis.

---

### 🔐 1. Autenticação (Login)

Para acessar as funcionalidades, o usuário deve validar suas credenciais:

1. Inserir **usuário** e **senha**.
2. O sistema valida o cadastro e a correspondência da senha.
3. Se os dados forem válidos, o acesso é liberado.

---

### 📝 2. Cadastro de Denúncias

Após o login, uma nova denúncia pode ser registrada preenchendo os seguintes campos:

| Campo | Descrição |
| :--- | :--- |
| **Descrição** | Detalhes completos da ocorrência |
| **Tipo** | Categoria do registro |
| **Endereço** | Local exato do ocorrido |
| **Telefone** | Contato do denunciante/responsável |
| **Prioridade** | `🔴 Alta` \| `🟡 Média` \| `🟢 Baixa` |

---

### 🔎 3. Consulta e Listagem

O módulo de visualização permite gerenciar as denúncias registradas:

* **Busca direta:** Localização rápida de registros específicos.
* **Ordenação por prioridade:** Filtro decrescente (`Alta` ➔ `Média` ➔ `Baixa`) para agilizar o atendimento de casos urgentes.

---

### 📞 4. Abertura de Chamados

Permite encaminhar uma denúncia ativa para a entidade competente:

1. **Selecionar a denúncia** desejada na listagem.
2. **Escolher o órgão/instituição** responsável pelo atendimento.
3. **Inserir a justificativa** técnica do encaminhamento.
4. **Confirmar:** O chamado é gerado e vinculado diretamente à denúncia.

---

### 🔄 Fluxo Operacional

```text
[ LOGIN ]
   ├── Informar usuário e senha
   └── Validação de credenciais
           │
           ▼
[ CADASTRAR DENÚNCIA ]
   ├── Dados: Descrição, Tipo, Endereço, Telefone
   └── Definir Prioridade (Alta / Média / Baixa)
           │
           ▼
[ EXIBIR DENÚNCIAS ]
   ├── Buscar registros
   └── Ordenar por nível de prioridade
           │
           ▼
[ ABRIR CHAMADO ]
   ├── Selecionar denúncia
   ├── Vincular órgão/instituição
   └── Adicionar justificativa
