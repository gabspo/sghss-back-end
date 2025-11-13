# GUIA DE SETUP DO PROJETO SGHSS

## Pré-requisitos

- Python 3.8+
- MySQL 5.7+ (ou servidor MySQL compatível)
- pip (gerenciador de pacotes Python)

## Passos de Instalação

### 1. Clonar ou Extrair o Projeto

```bash
# Se clonando do git
git clone https://github.com/seu-usuario/sghss-back-end.git
cd sghss-back-end

# Ou se tiver um arquivo ZIP
unzip sghss-back-end.zip
cd sghss-back-end
```

### 2. Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

```bash
# Copiar o arquivo de exemplo
cp .env.example .env

# Editar o arquivo .env com suas configurações
# Use seu editor preferido (VSCode, Sublime, etc)
```

**Exemplo de .env preenchido:**

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_DATABASE=sghss_db
DB_PORT=3306

FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-chave-secreta-super-segura-123

JWT_SECRET_KEY=sua-chave-jwt-segura-456
JWT_ACCESS_TOKEN_EXPIRES=18000

APP_HOST=0.0.0.0
APP_PORT=5000

LOG_LEVEL=INFO
```

### 5. Criar Banco de Dados

Execute os comandos SQL no MySQL:

```sql
-- Criar banco de dados
CREATE DATABASE sghss_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Selecionar banco de dados
USE sghss_db;

-- Criar tabelas
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'medico', 'paciente', 'secretaria') NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE pacientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE,
    endereco VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_cpf (cpf),
    INDEX idx_email (email)
);

CREATE TABLE profissionais (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    especialidade VARCHAR(100) NOT NULL,
    registro VARCHAR(100) UNIQUE NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_registro (registro)
);

CREATE TABLE consultas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    paciente_id INT NOT NULL,
    profissional_id INT,
    data DATETIME NOT NULL,
    motivo VARCHAR(255),
    observacoes TEXT,
    tipo_consulta ENUM('presencial', 'telemedicina') DEFAULT 'presencial',
    link_video VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (profissional_id) REFERENCES profissionais(id),
    INDEX idx_paciente (paciente_id),
    INDEX idx_data (data)
);

CREATE TABLE medicamentos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    dosagem VARCHAR(100),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nome (nome)
);

CREATE TABLE prescricoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    consulta_id INT NOT NULL,
    medicamento_id INT NOT NULL,
    duracao VARCHAR(100),
    instrucoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (consulta_id) REFERENCES consultas(id) ON DELETE CASCADE,
    FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id),
    INDEX idx_consulta (consulta_id)
);
```

### 6. Executar a Aplicação

```bash
# Método 1: Com Python direto
python app.py

# Método 2: Com Flask CLI
flask run

# Método 3: Com Gunicorn (produção)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

A aplicação estará disponível em: **http://localhost:5000**

## 🧪 Executar Testes

```bash
# Instalar pytest (se ainda não estiver instalado)
pip install pytest pytest-cov

# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src tests/

# Executar teste específico
pytest tests/test_example.py::TestValidator::test_validate_email_valid

# Modo verbose
pytest -v
```

## 🔍 Verificar Formato de Código

```bash
# Instalar ferramentas
pip install black pylint flake8

# Formatar código automaticamente
black src/

# Verificar estilo
flake8 src/

# Verificar com pylint
pylint src/
```

## 📊 Estrutura de Diretórios Criada

```
sghss-back-end/
├── src/
│   ├── __init__.py              # Aplicação principal (create_app)
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py          # Configurações por ambiente
│   │   └── database.py          # Gerenciador de BD
│   ├── models/
│   │   └── __init__.py          # Modelos de dados (dataclasses)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── usuario_service.py
│   │   ├── paciente_service.py
│   │   └── ...
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── usuarios.py
│   │   ├── pacientes.py
│   │   └── ...
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   ├── validators.py
│   │   └── response.py
│   └── exceptions/
│       └── __init__.py
├── tests/
│   ├── conftest.py
│   ├── test_example.py
│   └── ...
├── logs/                        # Arquivos de log (criado automaticamente)
├── app.py                       # Ponto de entrada
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── SETUP.md                    # Este arquivo
```

## 🚀 Próximos Passos

1. **Implementar serviços faltantes:**
   - ProfissionalService
   - ConsultaService
   - MedicamentoService
   - PrescricaoService

2. **Criar rotas faltantes:**
   - /api/profissionais
   - /api/consultas
   - /api/medicamentos
   - /api/prescricoes

3. **Adicionar autenticação:**
   - Proteção de rotas com JWT
   - Permissões por tipo de usuário

4. **Melhorias:**
   - Paginação em todas as listas
   - Filtros avançados
   - Busca
   - Relatórios

5. **Testes:**
   - Cobertura de 80%+ do código
   - Testes de integração
   - Testes de carga

## 🆘 Troubleshooting

### Erro de conexão com banco de dados

```
mysql.connector.errors.DatabaseError: 1045 (28000): Access denied for user 'root'@'localhost'
```

**Solução:** Verifique as credenciais no arquivo `.env`. Certifique-se de que o MySQL está rodando.

### Erro de porta já em uso

```
Address already in use
```

**Solução:** Mude a porta em `.env` ou finalize o processo que está usando a porta:

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Módulos não encontrados

```
ModuleNotFoundError: No module named 'flask'
```

**Solução:** Certifique-se de ter ativado o ambiente virtual e instalado as dependências:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

## 📞 Suporte

Para mais informações e suporte, consulte a documentação completa em `README.md`.
