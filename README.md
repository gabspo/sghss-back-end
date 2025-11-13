# SGHSS - Sistema de Gestão de Saúde e Segurança em Telemedicina

Sistema backend desenvolvido com Flask para gerenciar consultas, pacientes, profissionais de saúde e telemedicina.

## 📋 Estrutura do Projeto

```
sghss-back-end/
├── src/
│   ├── __init__.py           # Aplicação principal
│   ├── config/               # Configurações da aplicação
│   │   ├── settings.py       # Configurações por ambiente
│   │   ├── database.py       # Gerenciador de conexão com banco de dados
│   ├── models/               # Modelos de dados
│   ├── services/             # Lógica de negócio
│   │   ├── usuario_service.py
│   │   ├── paciente_service.py
│   │   └── ...
│   ├── routes/               # Rotas/Endpoints da API
│   │   ├── auth.py
│   │   ├── usuarios.py
│   │   ├── pacientes.py
│   │   └── ...
│   ├── utils/                # Utilitários
│   │   ├── logging.py        # Configuração de logs
│   │   ├── validators.py     # Validadores
│   │   └── response.py       # Formatadores de resposta
│   ├── exceptions/           # Exceções customizadas
│
├── tests/                    # Testes unitários e de integração
├── app.py                    # Ponto de entrada da aplicação
├── requirements.txt          # Dependências do projeto
├── .env.example              # Variáveis de ambiente (exemplo)
└── README.md                 # Este arquivo
```

## 🚀 Iniciando o Projeto

### 1. Instalação de Dependências

```bash
pip install -r requirements.txt
```

### 2. Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto, baseado em `.env.example`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_DATABASE=sghss_db
DB_PORT=3306

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-chave-secreta-segura

# JWT
JWT_SECRET_KEY=sua-chave-jwt-segura
JWT_ACCESS_TOKEN_EXPIRES=18000

# Application
APP_HOST=0.0.0.0
APP_PORT=5000
```

### 3. Inicializar Banco de Dados

```bash
# Criar tabelas no banco de dados
# (Adicione um script SQL com as tabelas necessárias)
```

### 4. Executar a Aplicação

```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

## 📚 Boas Práticas Implementadas

### 1. **Arquitetura em Camadas**
- **Config**: Gerenciamento de configurações e banco de dados
- **Models**: Definição de modelos de dados
- **Services**: Lógica de negócio isolada das rotas
- **Routes**: Endpoints da API
- **Utils**: Funções auxiliares reutilizáveis
- **Exceptions**: Exceções customizadas da aplicação

### 2. **Separação de Responsabilidades**
Cada camada tem uma responsabilidade bem definida:
- Rotas: Validação de entrada e formatação de resposta
- Services: Lógica de negócio e operações com banco de dados
- Utils: Funções auxiliares genéricas
- Exceptions: Tratamento de erros específicos

### 3. **Tratamento de Erros**
- Exceções customizadas para diferentes cenários
- Handlers globais de erros na aplicação
- Mensagens de erro consistentes e informativas

### 4. **Logging**
- Configuração centralizada de logs
- Logs em console e arquivo
- Rotação automática de arquivos de log

### 5. **Validação de Dados**
- Classe `Validator` com métodos reutilizáveis
- Validação de email, senha, telefone, data, etc.
- Validação de campos obrigatórios

### 6. **Segurança**
- Senhas com hash usando werkzeug
- JWT para autenticação
- Variáveis de ambiente para credenciais sensíveis
- Proteção com `@jwt_required()` em rotas

### 7. **Resposta Padronizada**
- Classe `ResponseFormatter` para formatar respostas
- Respostas de sucesso e erro consistentes
- Paginação integrada

### 8. **Gerenciamento de Banco de Dados**
- Classe `DatabaseManager` com context managers
- Conexões automáticas fechadas
- Tratamento de erros de conexão

### 9. **Documentação**
- Docstrings em todas as funções
- Type hints para melhor IDE support
- Comentários explicativos

### 10. **Configuração por Ambiente**
- Desenvolvimento, produção e teste
- Variáveis de ambiente para segurança
- Fácil switch entre ambientes

## 🔗 Endpoints da API

### Autenticação
- `POST /api/auth/login` - Login do usuário
- `GET /api/auth/health` - Health check

### Usuários
- `POST /api/usuarios` - Criar usuário
- `GET /api/usuarios` - Listar usuários
- `GET /api/usuarios/<id>` - Obter usuário
- `PUT /api/usuarios/<id>` - Atualizar usuário
- `DELETE /api/usuarios/<id>` - Deletar usuário

### Pacientes
- `POST /api/pacientes` - Criar paciente
- `GET /api/pacientes` - Listar pacientes
- `GET /api/pacientes/<id>` - Obter paciente
- `PUT /api/pacientes/<id>` - Atualizar paciente
- `DELETE /api/pacientes/<id>` - Deletar paciente

## 🧪 Testes

Execute os testes com:

```bash
pytest tests/
```

## 📝 Padrões de Codificação

- **Nomes de variáveis**: snake_case
- **Nomes de funções**: snake_case
- **Nomes de classes**: PascalCase
- **Constantes**: UPPER_SNAKE_CASE
- **Imports**: Organizados em ordem (stdlib, third-party, local)

## 🔒 Segurança

Sempre lembre-se de:
1. Nunca commitar arquivos `.env` com credenciais reais
2. Usar HTTPS em produção
3. Validar e sanitizar todas as entradas
4. Manter dependências atualizadas
5. Usar CORS apropriado para frontend

## 📦 Dependências Principais

- **Flask**: Framework web
- **Flask-JWT-Extended**: Autenticação JWT
- **mysql-connector-python**: Driver MySQL
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **Werkzeug**: Utilidades para segurança

## 🤝 Contribuindo

Ao adicionar novo código:
1. Siga os padrões estabelecidos
2. Adicione docstrings em todas as funções
3. Use type hints
4. Adicione testes unitários
5. Atualize a documentação

## 📄 Licença

MIT License

## ✉️ Contato

Para dúvidas ou sugestões, entre em contato com o time de desenvolvimento.
