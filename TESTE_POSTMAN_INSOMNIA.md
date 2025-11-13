# 📮 GUIA DE TESTES COM POSTMAN/INSOMNIA

## Introdução

Este guia explica como testar todos os endpoints da API SGHSS usando **Postman** ou **Insomnia**.

---

## 🚀 PASSO 1: Importar a Collection

### Postman

1. Abra **Postman** (https://www.postman.com/)
2. Clique em **Collections** (lado esquerdo)
3. Clique em **Import**
4. Selecione **Upload Files**
5. Escolha `SGHSS-API.postman_collection.json`
6. Clique em **Import**

### Insomnia

1. Abra **Insomnia** (https://insomnia.rest/)
2. Clique em **Design** → **Create** → **Design Document**
3. Vá para **Code** → **Import**
4. Cole o conteúdo do arquivo JSON
5. Clique em **Import All**

---

## 🔧 PASSO 2: Configurar Variáveis de Ambiente

### Criar Arquivo Environment

**Postman:**

1. Clique em **Environments** (lado esquerdo)
2. Clique em **Create New Environment**
3. Nome: `SGHSS Development`
4. Adicione a variável:
   - **Key**: `token`
   - **Value**: (deixar vazio, será preenchido após login)
5. Salve

**Insomnia:**

1. Clique em **Manage Environments**
2. **Create New Environment**
3. Adicione:
```json
{
  "base_url": "http://localhost:5000",
  "token": ""
}
```

---

## ⚙️ PASSO 3: Preparar o Banco de Dados

### Executar o Script SQL

1. Abra **MySQL Workbench** ou **MySQL CLI**
2. Copie todo o conteúdo de `DATABASE_INIT.sql`
3. Execute no seu MySQL

```bash
# Via linha de comando
mysql -u root -p < DATABASE_INIT.sql
```

4. Verifique se as tabelas foram criadas:
```sql
USE sghss_db;
SHOW TABLES;
```

---

## 🚀 PASSO 4: Iniciar a API

### Terminal/PowerShell

```bash
# Navegar para o diretório
cd C:\Users\gabri\Desktop\sghss-refactored

# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências (primeira vez)
pip install -r requirements.txt

# Rodar a aplicação
python app.py
```

Você verá:
```
 * Running on http://127.0.0.1:5000
```

---

## 🧪 PASSO 5: Testar Endpoints

### 1️⃣ Health Check (Sem Autenticação)

**Endpoint**: `GET /api/auth/health`

```
GET http://localhost:5000/api/auth/health
```

**Resposta Esperada**:
```json
{
  "status": "success",
  "message": "API is running",
  "data": {
    "status": "healthy",
    "timestamp": "2025-11-13T10:30:00"
  }
}
```

---

### 2️⃣ Login (Obter Token)

**IMPORTANTE**: Este é o passo mais crítico! 🔐

**Endpoint**: `POST /api/auth/login`

```
POST http://localhost:5000/api/auth/login
Headers: Content-Type: application/json

Body:
{
  "email": "admin@sghss.com",
  "senha": "sua_senha_aqui"
}
```

⚠️ **PROBLEMA COMUM**: A senha que você inseriu no banco de dados precisa estar em hash!

**Solução 1: Usar a senha sem hash (para testes)**
- Modifique o script `DATABASE_INIT.sql` e adicione a senha com hash Python

**Solução 2: Gerar hash Python**
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash("seu_password_123"))
```

**Resposta Esperada**:
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "usuario_id": 1,
    "nome": "Admin Sistema",
    "email": "admin@sghss.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Salvar o Token**:
- Copie o valor do `token`
- Em Postman: Vá para **Environments** → `SGHSS Development` → Cole em `token`
- Em Insomnia: Faça igual

---

### 3️⃣ Testar CRUD de Usuários

#### Listar Usuários
```
GET http://localhost:5000/api/usuarios?page=1&per_page=10
Headers: 
  Authorization: Bearer {{token}}
```

#### Criar Usuário
```
POST http://localhost:5000/api/usuarios
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body:
{
  "nome": "João Silva",
  "email": "joao@example.com",
  "senha": "Senha123!@#",
  "tipo": "paciente"
}
```

#### Atualizar Usuário
```
PUT http://localhost:5000/api/usuarios/1
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body:
{
  "nome": "João Silva Atualizado"
}
```

#### Deletar Usuário
```
DELETE http://localhost:5000/api/usuarios/1
Headers:
  Authorization: Bearer {{token}}
```

---

### 4️⃣ Testar CRUD de Pacientes

#### Criar Paciente
```
POST http://localhost:5000/api/pacientes
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body:
{
  "usuario_id": 3,
  "cpf": "12345678901234",
  "data_nascimento": "1990-05-15",
  "telefone": "(11) 99876-5432",
  "endereco": "Avenida Paulista, 1000",
  "cidade": "São Paulo",
  "estado": "SP",
  "cep": "01311-100",
  "condicoes_medicas": "Nenhuma",
  "alergias": "Penicilina"
}
```

---

### 5️⃣ Testar CRUD de Profissionais

#### Criar Profissional
```
POST http://localhost:5000/api/profissionais
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body:
{
  "usuario_id": 2,
  "crm": "123456/SP",
  "especialidade": "Cardiologia",
  "telefone_comercial": "(11) 98765-4321",
  "endereco_consultorio": "Rua das Flores, 123",
  "cidade": "São Paulo",
  "estado": "SP",
  "cep": "01234-567",
  "horario_inicio": "08:00:00",
  "horario_fim": "18:00:00",
  "dias_atendimento": "Segunda a Sexta",
  "biografia": "Especialista em cardiologia com 10 anos de experiência"
}
```

---

### 6️⃣ Testar CRUD de Medicamentos

#### Criar Medicamento
```
POST http://localhost:5000/api/medicamentos
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body:
{
  "nome": "Dipirona 500mg",
  "principio_ativo": "Metamizol",
  "fabricante": "Blau",
  "dosagem": "500mg",
  "forma_farmaceutica": "Comprimido",
  "lote": "LT123456",
  "validade": "2026-12-31",
  "preco": 15.50,
  "estoque": 100,
  "descricao": "Analgésico e antipirético",
  "contraindicacoes": "Alergia ao metamizol"
}
```

#### Buscar Medicamento
```
GET http://localhost:5000/api/medicamentos/busca?busca=dipirona
Headers:
  Authorization: Bearer {{token}}
```

---

### 7️⃣ Testar CRUD de Consultas

#### Criar Consulta (Presencial)
```
POST http://localhost:5000/api/consultas
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body:
{
  "paciente_id": 1,
  "profissional_id": 1,
  "tipo": "presencial",
  "data_hora": "2025-11-20 14:30:00",
  "duracao_minutos": 30,
  "motivo_consulta": "Consulta de rotina",
  "sintomas": "Sem sintomas",
  "status": "agendada"
}
```

#### Criar Consulta (Telemedicina)
```
POST http://localhost:5000/api/consultas
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body:
{
  "paciente_id": 1,
  "profissional_id": 1,
  "tipo": "telemedicina",
  "data_hora": "2025-11-20 15:00:00",
  "duracao_minutos": 30,
  "motivo_consulta": "Consulta online",
  "link_video": "https://zoom.us/j/123456789",
  "status": "agendada"
}
```

#### Filtrar Consultas por Paciente
```
GET http://localhost:5000/api/consultas?paciente_id=1
Headers:
  Authorization: Bearer {{token}}
```

---

### 8️⃣ Testar CRUD de Prescrições

#### Criar Prescrição
```
POST http://localhost:5000/api/prescricoes
Headers:
  Content-Type: application/json
  Authorization: Bearer {{token}}

Body:
{
  "consulta_id": 1,
  "medicamento_id": 1,
  "profissional_id": 1,
  "dosagem": "500mg",
  "frequencia": "3x ao dia",
  "duracao_dias": 7,
  "data_inicio": "2025-11-13",
  "data_fim": "2025-11-20",
  "instrucoes_uso": "Tomar com água",
  "observacoes": "Não misturar com álcool",
  "ativa": true
}
```

#### Prescrições de uma Consulta
```
GET http://localhost:5000/api/prescricoes/consulta/1
Headers:
  Authorization: Bearer {{token}}
```

---

## ❌ Tratamento de Erros

### Erro 401 - Unauthorized
```json
{
  "status": "error",
  "message": "Missing or invalid token",
  "error_code": "INVALID_TOKEN"
}
```

**Solução**: Certifique-se que o token está correto e não expirou (5 horas)

### Erro 400 - Bad Request
```json
{
  "status": "error",
  "message": "Validation error",
  "error_code": "VALIDATION_ERROR",
  "details": "Email is invalid"
}
```

**Solução**: Verifique o formato do email, cpf, etc.

### Erro 404 - Not Found
```json
{
  "status": "error",
  "message": "Usuario not found",
  "error_code": "NOT_FOUND"
}
```

**Solução**: Verifique se o ID existe no banco de dados

### Erro 409 - Conflict
```json
{
  "status": "error",
  "message": "Email already registered",
  "error_code": "CONFLICT"
}
```

**Solução**: Use um email único que ainda não está cadastrado

---

## 📊 Checklist de Testes

- [ ] Health Check retorna 200
- [ ] Login retorna token válido
- [ ] CRUD Usuários funciona (Create, Read, Update, Delete)
- [ ] CRUD Pacientes funciona
- [ ] CRUD Profissionais funciona
- [ ] CRUD Medicamentos funciona
- [ ] CRUD Consultas funciona (presencial e telemedicina)
- [ ] CRUD Prescrições funciona
- [ ] Paginação funciona (page=1&per_page=10)
- [ ] Buscas funcionam (busca=termo)
- [ ] Filtros funcionam (paciente_id=1)
- [ ] Erros retornam status corretos (400, 401, 404, etc)

---

## 💡 Dicas Importantes

1. **Sempre use Authorization Bearer Token** em todas as rotas exceto login
2. **Respeite a ordem de testes**: Login → Criar Usuários → Criar Pacientes → etc
3. **Use dados realistas** para melhor validação
4. **Teste casos de erro** (email inválido, cpf duplicado, etc)
5. **Veja os logs** na aplicação para debug

---

## 🔗 Referências

- Documentação completa: `API_REFERENCE.md`
- Melhores práticas: `BEST_PRACTICES.md`
- Configuração: `SETUP.md`

**Bom teste!** 🎉
