# API Quick Reference

Base URL: `http://localhost:5000/api`

**Headers Required:**
- `Content-Type: application/json`
- `Authorization: Bearer <token>` (exceto para `/auth/login`)

---

## Authentication

### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "senha": "password123"
}

Response (200):
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "id": 1,
    "nome": "John Doe",
    "email": "john@example.com",
    "tipo": "medico",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### Health Check
```
GET /auth/health

Response (200):
{
  "status": "success",
  "message": "Server is running",
  "data": {
    "status": "healthy"
  }
}
```

---

## Usuarios

### Criar Usuário
```
POST /usuarios
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@example.com",
  "senha": "senha123!",
  "tipo": "paciente"
}

Response (201):
{
  "status": "success",
  "message": "Usuario created successfully",
  "data": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@example.com",
    "tipo": "paciente"
  }
}
```

### Listar Usuários
```
GET /usuarios?page=1&per_page=20
Authorization: Bearer <token>

Response (200):
{
  "status": "success",
  "message": "Usuarios listed successfully",
  "data": [
    {
      "id": 1,
      "nome": "João Silva",
      "email": "joao@example.com",
      "tipo": "paciente"
    }
  ]
}
```

### Obter Usuário
```
GET /usuarios/1
Authorization: Bearer <token>

Response (200):
{
  "status": "success",
  "message": "Usuario retrieved successfully",
  "data": {...}
}
```

### Atualizar Usuário
```
PUT /usuarios/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "nome": "João Silva Updated",
  "email": "joao.updated@example.com",
  "tipo": "medico"
}

Response (200):
{
  "status": "success",
  "message": "Usuario updated successfully",
  "data": {...}
}
```

### Deletar Usuário
```
DELETE /usuarios/1
Authorization: Bearer <token>

Response (200):
{
  "status": "success",
  "message": "Usuario deleted successfully",
  "data": null
}
```

---

## Pacientes

### Criar Paciente
```
POST /pacientes
Authorization: Bearer <token>
Content-Type: application/json

{
  "nome": "Maria Santos",
  "email": "maria@example.com",
  "telefone": "11987654321",
  "cpf": "12345678901",
  "data_nascimento": "1990-01-15",
  "endereco": "Rua A, 123"
}

Response (201): {...}
```

### Listar Pacientes
```
GET /pacientes?page=1&per_page=20
Authorization: Bearer <token>

Response (200): {...}
```

### Obter Paciente
```
GET /pacientes/1
Authorization: Bearer <token>

Response (200): {...}
```

### Atualizar Paciente
```
PUT /pacientes/1
Authorization: Bearer <token>

{
  "nome": "Maria Santos Updated",
  "email": "maria.new@example.com",
  "telefone": "11987654322",
  "endereco": "Rua B, 456"
}

Response (200): {...}
```

### Deletar Paciente
```
DELETE /pacientes/1
Authorization: Bearer <token>

Response (200): {...}
```

---

## Profissionais

### Criar Profissional
```
POST /profissionais
Authorization: Bearer <token>

{
  "nome": "Dr. Carlos Silva",
  "email": "carlos@example.com",
  "telefone": "11998765432",
  "especialidade": "Cardiologia",
  "registro": "CRM123456789"
}

Response (201): {...}
```

### Listar Profissionais
```
GET /profissionais?page=1&per_page=20
Authorization: Bearer <token>

Response (200): {...}
```

### Obter Profissional
```
GET /profissionais/1
Authorization: Bearer <token>

Response (200): {...}
```

### Atualizar Profissional
```
PUT /profissionais/1
Authorization: Bearer <token>

{
  "nome": "Dr. Carlos Silva Updated",
  "especialidade": "Cardiologia e Pneumologia"
}

Response (200): {...}
```

### Deletar Profissional
```
DELETE /profissionais/1
Authorization: Bearer <token>

Response (200): {...}
```

---

## Consultas

### Criar Consulta
```
POST /consultas
Authorization: Bearer <token>

{
  "paciente_id": 1,
  "profissional_id": 1,
  "data": "2025-11-20 14:30:00",
  "motivo": "Checkup",
  "observacoes": "Paciente com histórico de hipertensão",
  "tipo_consulta": "presencial",
  "link_video": null
}

// Para telemedicina:
{
  "paciente_id": 1,
  "profissional_id": 1,
  "data": "2025-11-20 14:30:00",
  "motivo": "Consulta online",
  "tipo_consulta": "telemedicina",
  "link_video": "https://meet.google.com/..."
}

Response (201): {...}
```

### Listar Consultas
```
GET /consultas?page=1&per_page=20
GET /consultas?page=1&per_page=20&paciente_id=1  (filtrar por paciente)
Authorization: Bearer <token>

Response (200): {...}
```

### Obter Consulta
```
GET /consultas/1
Authorization: Bearer <token>

Response (200): {...}
```

### Atualizar Consulta
```
PUT /consultas/1
Authorization: Bearer <token>

{
  "data": "2025-11-21 14:30:00",
  "motivo": "Checkup completo",
  "observacoes": "Trazer exames anteriores"
}

Response (200): {...}
```

### Deletar Consulta
```
DELETE /consultas/1
Authorization: Bearer <token>

Response (200): {...}
```

---

## Medicamentos

### Criar Medicamento
```
POST /medicamentos
Authorization: Bearer <token>

{
  "nome": "Dipirona 500mg",
  "descricao": "Analgésico e antitérmico",
  "dosagem": "500mg"
}

Response (201): {...}
```

### Listar Medicamentos
```
GET /medicamentos?page=1&per_page=20
GET /medicamentos?page=1&per_page=20&busca=dipirona  (buscar por nome)
Authorization: Bearer <token>

Response (200): {...}
```

### Obter Medicamento
```
GET /medicamentos/1
Authorization: Bearer <token>

Response (200): {...}
```

### Atualizar Medicamento
```
PUT /medicamentos/1
Authorization: Bearer <token>

{
  "nome": "Dipirona 750mg",
  "dosagem": "750mg"
}

Response (200): {...}
```

### Deletar Medicamento
```
DELETE /medicamentos/1
Authorization: Bearer <token>

Response (200): {...}
```

---

## Prescrições

### Criar Prescrição
```
POST /prescricoes
Authorization: Bearer <token>

{
  "consulta_id": 1,
  "medicamento_id": 1,
  "duracao": "7 dias",
  "instrucoes": "Tomar 1 comprimido a cada 6 horas com alimento"
}

Response (201): {...}
```

### Listar Prescrições
```
GET /prescricoes?page=1&per_page=20
Authorization: Bearer <token>

Response (200): {...}
```

### Listar Prescrições por Consulta
```
GET /prescricoes/consulta/1?page=1&per_page=20
Authorization: Bearer <token>

Response (200): {...}
```

### Obter Prescrição
```
GET /prescricoes/1
Authorization: Bearer <token>

Response (200): {...}
```

### Atualizar Prescrição
```
PUT /prescricoes/1
Authorization: Bearer <token>

{
  "duracao": "14 dias",
  "instrucoes": "Tomar 2 comprimidos a cada 8 horas com alimento"
}

Response (200): {...}
```

### Deletar Prescrição
```
DELETE /prescricoes/1
Authorization: Bearer <token>

Response (200): {...}
```

---

## Códigos de Erro

| Status | Error Code | Descrição |
|--------|-----------|-----------|
| 400 | VALIDATION_ERROR | Dados inválidos |
| 401 | AUTH_ERROR | Credenciais inválidas |
| 403 | AUTHORIZATION_ERROR | Sem permissão |
| 404 | NOT_FOUND | Recurso não encontrado |
| 409 | CONFLICT | Conflito (ex: email existente) |
| 500 | INTERNAL_ERROR | Erro interno do servidor |

---

## Exemplo com cURL

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","senha":"password123"}'

# Obter token da resposta e usar em próximas requisições

# Listar pacientes
curl -X GET http://localhost:5000/api/pacientes \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."

# Criar novo paciente
curl -X POST http://localhost:5000/api/pacientes \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "nome":"Maria",
    "email":"maria@example.com",
    "telefone":"11987654321",
    "cpf":"12345678901"
  }'
```

---

**Última Atualização**: 13 de Novembro de 2025
