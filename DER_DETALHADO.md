# 🗄️ Diagrama Entidade-Relacionamento (DER) - SGHSS

## Visão Geral

Este é o Diagrama Entidade-Relacionamento do Sistema de Gestão de Saúde e Segurança em Telemedicina (SGHSS).

---

## 📊 Estrutura das Tabelas

### 👥 Tabela: `usuarios`
**Propósito:** Armazenar todos os usuários do sistema

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| `id` | INT | PK, Auto-increment | Identificador único |
| `nome` | VARCHAR(255) | NOT NULL | Nome completo do usuário |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | Email único para login |
| `senha` | VARCHAR(255) | NOT NULL | Senha com hash bcrypt |
| `tipo` | ENUM | NOT NULL, DEFAULT='paciente' | admin, medico, paciente, secretaria |
| `ativo` | BOOLEAN | DEFAULT=TRUE | Status ativo/inativo |
| `criado_em` | TIMESTAMP | DEFAULT=NOW() | Data de criação |
| `atualizado_em` | TIMESTAMP | ON UPDATE NOW() | Data da última atualização |

**Índices:**
- `idx_email` (email)
- `idx_tipo` (tipo)
- `idx_ativo` (ativo)

---

### 🏥 Tabela: `pacientes`
**Propósito:** Armazenar informações específicas de pacientes
**Relacionamento:** 1:1 com `usuarios` (via FK usuario_id)

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| `id` | INT | PK, Auto-increment | Identificador único |
| `usuario_id` | INT | FK, UNIQUE, NOT NULL | Referência a usuarios.id |
| `cpf` | VARCHAR(14) | UNIQUE, NOT NULL | CPF do paciente |
| `data_nascimento` | DATE | NULL | Data de nascimento |
| `telefone` | VARCHAR(20) | NULL | Telefone de contato |
| `endereco` | VARCHAR(500) | NULL | Endereço completo |
| `cidade` | VARCHAR(100) | NULL | Cidade |
| `estado` | VARCHAR(2) | NULL | Estado (UF) |
| `cep` | VARCHAR(9) | NULL | CEP |
| `condicoes_medicas` | TEXT | NULL | Histórico de condições |
| `alergias` | TEXT | NULL | Alergias conhecidas |
| `criado_em` | TIMESTAMP | DEFAULT=NOW() | Data de criação |
| `atualizado_em` | TIMESTAMP | ON UPDATE NOW() | Data da última atualização |

**Índices:**
- `idx_cpf` (cpf)
- `idx_usuario_id` (usuario_id)

**Foreign Keys:**
- `fk_pacientes_usuarios`: usuario_id → usuarios.id (ON DELETE CASCADE)

---

### 👨‍⚕️ Tabela: `profissionais`
**Propósito:** Armazenar informações de médicos e profissionais de saúde
**Relacionamento:** 1:1 com `usuarios` (via FK usuario_id)

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| `id` | INT | PK, Auto-increment | Identificador único |
| `usuario_id` | INT | FK, UNIQUE, NOT NULL | Referência a usuarios.id |
| `crm` | VARCHAR(20) | UNIQUE, NOT NULL | CRM do profissional |
| `especialidade` | VARCHAR(100) | NOT NULL | Especialidade (ex: Cardiologia) |
| `telefone_comercial` | VARCHAR(20) | NULL | Telefone do consultório |
| `endereco_consultorio` | VARCHAR(500) | NULL | Endereço do consultório |
| `cidade` | VARCHAR(100) | NULL | Cidade |
| `estado` | VARCHAR(2) | NULL | Estado (UF) |
| `cep` | VARCHAR(9) | NULL | CEP |
| `horario_inicio` | TIME | NULL | Hora de início do atendimento |
| `horario_fim` | TIME | NULL | Hora de término do atendimento |
| `dias_atendimento` | VARCHAR(100) | NULL | Dias da semana (ex: Segunda a Sexta) |
| `biografia` | TEXT | NULL | Biografia profissional |
| `criado_em` | TIMESTAMP | DEFAULT=NOW() | Data de criação |
| `atualizado_em` | TIMESTAMP | ON UPDATE NOW() | Data da última atualização |

**Índices:**
- `idx_crm` (crm)
- `idx_especialidade` (especialidade)
- `idx_usuario_id` (usuario_id)

**Foreign Keys:**
- `fk_profissionais_usuarios`: usuario_id → usuarios.id (ON DELETE CASCADE)

---

### 💊 Tabela: `medicamentos`
**Propósito:** Catálogo de medicamentos disponíveis
**Relacionamento:** N:1 com `prescricoes` (prescricoes.medicamento_id)

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| `id` | INT | PK, Auto-increment | Identificador único |
| `nome` | VARCHAR(255) | NOT NULL | Nome do medicamento |
| `principio_ativo` | VARCHAR(255) | NOT NULL | Substância ativa principal |
| `fabricante` | VARCHAR(255) | NULL | Fabricante/Laboratório |
| `dosagem` | VARCHAR(100) | NULL | Dosagem apresentada |
| `forma_farmaceutica` | VARCHAR(100) | NULL | Forma (Comprimido, Cápsula, etc) |
| `lote` | VARCHAR(50) | NULL | Número do lote |
| `validade` | DATE | NULL | Data de validade |
| `preco` | DECIMAL(10,2) | NULL | Preço unitário |
| `estoque` | INT | DEFAULT=0 | Quantidade em estoque |
| `descricao` | TEXT | NULL | Descrição/indicações |
| `contraindicacoes` | TEXT | NULL | Contraindicações conhecidas |
| `criado_em` | TIMESTAMP | DEFAULT=NOW() | Data de criação |
| `atualizado_em` | TIMESTAMP | ON UPDATE NOW() | Data da última atualização |

**Índices:**
- `idx_nome` (nome)
- `idx_principio_ativo` (principio_ativo)
- `idx_lote` (lote)

---

### 📅 Tabela: `consultas`
**Propósito:** Armazenar agendamentos e registros de consultas
**Relacionamento:** 
- N:1 com `pacientes` (paciente_id)
- N:1 com `profissionais` (profissional_id)

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| `id` | INT | PK, Auto-increment | Identificador único |
| `paciente_id` | INT | FK, NOT NULL | Referência a pacientes.id |
| `profissional_id` | INT | FK, NOT NULL | Referência a profissionais.id |
| `tipo` | ENUM | NOT NULL, DEFAULT='presencial' | presencial ou telemedicina |
| `data_hora` | DATETIME | NOT NULL | Data e hora da consulta |
| `duracao_minutos` | INT | DEFAULT=30 | Duração em minutos |
| `motivo_consulta` | VARCHAR(500) | NULL | Motivo/queixa principal |
| `sintomas` | TEXT | NULL | Sintomas relatados |
| `diagnostico` | TEXT | NULL | Diagnóstico do profissional |
| `observacoes` | TEXT | NULL | Observações adicionais |
| `link_video` | VARCHAR(500) | NULL | Link da videoconferência (telemedicina) |
| `status` | ENUM | NOT NULL, DEFAULT='agendada' | agendada, realizada, cancelada, nao_compareceu |
| `criado_em` | TIMESTAMP | DEFAULT=NOW() | Data de criação |
| `atualizado_em` | TIMESTAMP | ON UPDATE NOW() | Data da última atualização |

**Índices:**
- `idx_paciente_id` (paciente_id)
- `idx_profissional_id` (profissional_id)
- `idx_data_hora` (data_hora)
- `idx_status` (status)
- `idx_tipo` (tipo)

**Foreign Keys:**
- `fk_consultas_pacientes`: paciente_id → pacientes.id (ON DELETE CASCADE)
- `fk_consultas_profissionais`: profissional_id → profissionais.id (ON DELETE CASCADE)

---

### 📋 Tabela: `prescricoes`
**Propósito:** Armazenar prescrições de medicamentos
**Relacionamento:**
- N:1 com `consultas` (consulta_id)
- N:1 com `medicamentos` (medicamento_id)
- N:1 com `profissionais` (profissional_id)

| Campo | Tipo | Restrições | Descrição |
|-------|------|-----------|-----------|
| `id` | INT | PK, Auto-increment | Identificador único |
| `consulta_id` | INT | FK, NOT NULL | Referência a consultas.id |
| `medicamento_id` | INT | FK, NOT NULL | Referência a medicamentos.id |
| `profissional_id` | INT | FK, NOT NULL | Referência a profissionais.id |
| `dosagem` | VARCHAR(100) | NOT NULL | Como tomar (ex: 500mg) |
| `frequencia` | VARCHAR(100) | NOT NULL | Frequência (ex: 3x ao dia) |
| `duracao_dias` | INT | NOT NULL | Duração em dias |
| `data_inicio` | DATE | NOT NULL | Data de início |
| `data_fim` | DATE | NOT NULL | Data de término |
| `instrucoes_uso` | TEXT | NULL | Instruções especiais |
| `observacoes` | TEXT | NULL | Observações importantes |
| `ativa` | BOOLEAN | DEFAULT=TRUE | Status da prescrição |
| `criado_em` | TIMESTAMP | DEFAULT=NOW() | Data de criação |
| `atualizado_em` | TIMESTAMP | ON UPDATE NOW() | Data da última atualização |

**Índices:**
- `idx_consulta_id` (consulta_id)
- `idx_medicamento_id` (medicamento_id)
- `idx_profissional_id` (profissional_id)
- `idx_ativa` (ativa)
- `idx_data_inicio` (data_inicio)

**Foreign Keys:**
- `fk_prescricoes_consultas`: consulta_id → consultas.id (ON DELETE CASCADE)
- `fk_prescricoes_medicamentos`: medicamento_id → medicamentos.id (ON DELETE RESTRICT)
- `fk_prescricoes_profissionais`: profissional_id → profissionais.id (ON DELETE RESTRICT)

---

## 🔗 Relacionamentos Entre Tabelas

```
usuarios (1) ←------ (1:1) ----→ pacientes (1)
    ↓
usuarios (1) ←------ (1:1) ----→ profissionais (1)
    
pacientes (1) ←------ (1:N) ----→ consultas (N)
profissionais (1) ←--(1:N) ----→ consultas (N)

consultas (1) ←------ (1:N) ----→ prescricoes (N)
medicamentos (1) ←----(N:1) ---→ prescricoes (N)
profissionais (1) ←---(N:1) ---→ prescricoes (N)
```

### Explicação dos Relacionamentos:

1. **USUARIOS ↔ PACIENTES (1:1)**
   - Cada usuário do tipo "paciente" tem exatamente um registro em pacientes
   - One-to-One: exclusivo

2. **USUARIOS ↔ PROFISSIONAIS (1:1)**
   - Cada usuário do tipo "medico" tem exatamente um registro em profissionais
   - One-to-One: exclusivo

3. **PACIENTES ↔ CONSULTAS (1:N)**
   - Um paciente pode ter múltiplas consultas
   - One-to-Many: um-para-muitos

4. **PROFISSIONAIS ↔ CONSULTAS (1:N)**
   - Um profissional pode atender múltiplas consultas
   - One-to-Many: um-para-muitos

5. **CONSULTAS ↔ PRESCRICOES (1:N)**
   - Uma consulta pode gerar múltiplas prescrições
   - One-to-Many: um-para-muitos

6. **MEDICAMENTOS ↔ PRESCRICOES (1:N)**
   - Um medicamento pode estar em múltiplas prescrições
   - One-to-Many: um-para-muitos

7. **PROFISSIONAIS ↔ PRESCRICOES (N:1)**
   - Uma prescrição é feita por um profissional
   - Many-to-One: muitos-para-um

---

## 📐 Cardinalidade

| Relacionamento | Tipo | Descrição |
|---|---|---|
| usuarios → pacientes | 1:1 | Um usuário é um paciente (opcional) |
| usuarios → profissionais | 1:1 | Um usuário é um profissional (opcional) |
| pacientes → consultas | 1:N | Um paciente tem múltiplas consultas |
| profissionais → consultas | 1:N | Um profissional realiza múltiplas consultas |
| consultas → prescricoes | 1:N | Uma consulta gera múltiplas prescrições |
| medicamentos → prescricoes | 1:N | Um medicamento está em múltiplas prescrições |

---

## 🔐 Integridade Referencial

### ON DELETE CASCADE
Aplicado quando:
- Uma linha pai é deletada
- Todas as linhas filhas associadas são **automaticamente deletadas**

**Usado em:**
- usuarios → pacientes (se delete usuário, deleta paciente)
- usuarios → profissionais (se delete usuário, deleta profissional)
- consultas → pacientes (se delete paciente, deleta consultas)
- consultas → profissionais (se delete profissional, deleta consultas)
- prescricoes → consultas (se delete consulta, deleta prescrições)

### ON DELETE RESTRICT
Aplicado quando:
- Uma linha pai **NÃO pode ser deletada** se tiver filhos
- Protege dados críticos

**Usado em:**
- prescricoes → medicamentos (medicamentos nunca podem ser deletados se em prescrição)
- prescricoes → profissionais (profissionais nunca podem ser deletados se em prescrição)

---

## 📝 Exemplo de Fluxo de Dados

```
1. Admin cria USUARIO do tipo "paciente"
   ↓
2. PACIENTE é criado com usuario_id
   ↓
3. Paciente se consulta com PROFISSIONAL
   ↓
4. CONSULTA é criada (paciente_id, profissional_id)
   ↓
5. Profissional prescreve MEDICAMENTO
   ↓
6. PRESCRIÇÃO é criada (consulta_id, medicamento_id, profissional_id)
   ↓
7. Paciente segue a prescrição
```

---

## 🔍 Queries Comuns

### Listar consultas de um paciente com prescrições
```sql
SELECT 
    c.id, c.data_hora, c.diagnostico,
    p.nome as medicamento, pr.dosagem, pr.frequencia
FROM consultas c
JOIN prescricoes pr ON c.id = pr.consulta_id
JOIN medicamentos p ON pr.medicamento_id = p.id
WHERE c.paciente_id = 1;
```

### Listar especialidades e profissionais
```sql
SELECT 
    especialidade, COUNT(*) as total_profissionais
FROM profissionais
GROUP BY especialidade;
```

### Medicamentos em estoque baixo
```sql
SELECT 
    nome, estoque, validade
FROM medicamentos
WHERE estoque < 10
ORDER BY estoque ASC;
```

---

## 📦 Estatísticas do Banco

| Item | Valor |
|------|-------|
| Total de Tabelas | 6 |
| Total de Colunas | 109 |
| Primary Keys | 6 |
| Foreign Keys | 7 |
| Índices | 15+ |
| Relacionamentos | 7 |

---

## 🎯 Próximos Passos

1. ✅ Executar `DATABASE_INIT.sql` para criar tabelas
2. ✅ Testar inserção de dados com API
3. ✅ Validar integridade referencial
4. ✅ Otimizar queries com índices
5. ✅ Implementar backup automático

---

**Gerado automaticamente** | Última atualização: 2025-11-24
