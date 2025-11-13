# GUIA DE BOAS PRÁTICAS - SGHSS Backend

## 📋 Índice
1. [Estrutura de Código](#estrutura-de-código)
2. [Naming Conventions](#naming-conventions)
3. [Documentação](#documentação)
4. [Tratamento de Erros](#tratamento-de-erros)
5. [Testes](#testes)
6. [Segurança](#segurança)
7. [Performance](#performance)
8. [Git](#git)

---

## Estrutura de Código

### Imports
- Ordene imports em 3 grupos: stdlib, third-party, local
- Cada grupo separado por uma linha em branco

```python
# ✅ BOM
import os
from datetime import datetime
from typing import List, Optional

import flask
from flask_jwt_extended import jwt_required

from .models import Usuario
from .exceptions import ValidationError

# ❌ RUIM
from .models import Usuario
import os
from flask_jwt_extended import jwt_required
from .exceptions import ValidationError
import flask
from datetime import datetime
```

### Tamanho de Funções
- Máximo 30-40 linhas por função
- Se passar disso, quebre em funções menores
- Uma função, uma responsabilidade (Single Responsibility Principle)

```python
# ❌ RUIM - Função muito grande
def processar_usuario(dados):
    # Validação
    if not dados.get("nome"):
        return {"erro": "nome obrigatório"}
    
    # Hash de senha
    senha_hash = generate_password_hash(dados["senha"])
    
    # Salvar no BD
    try:
        conn = mysql.connector.connect(...)
        cursor = conn.cursor()
        cursor.execute(...)
        conn.commit()
    except Exception as e:
        return {"erro": str(e)}
    finally:
        cursor.close()
        conn.close()
    
    # Criar JWT
    token = create_access_token(...)
    
    # Retornar resposta
    return {"status": "ok", "token": token}

# ✅ BOM - Separado em funções pequenas
def processar_usuario(dados):
    usuario = usuario_service.criar_usuario(
        nome=dados.get("nome"),
        email=dados.get("email"),
        senha=dados.get("senha"),
        tipo=dados.get("tipo"),
    )
    token = create_access_token(identity=str(usuario.id))
    return {"usuario": usuario.to_dict(), "token": token}
```

### Linhas Longas
- Máximo 120 caracteres por linha
- Se precisar quebrar, indente logicamente

```python
# ❌ RUIM
resultado = db.execute("SELECT id, nome, email, telefone FROM usuarios WHERE tipo = %s AND criado_em > %s ORDER BY nome", (tipo, data))

# ✅ BOM
resultado = db.execute(
    """
    SELECT id, nome, email, telefone
    FROM usuarios
    WHERE tipo = %s AND criado_em > %s
    ORDER BY nome
    """,
    (tipo, data)
)
```

---

## Naming Conventions

### Variáveis e Funções
- Use `snake_case`
- Nomes descritivos, não abreviados

```python
# ❌ RUIM
u = Usuario("João", "jo@email.com")
def proc_usr(d):
    pass

def get_all():
    pass

# ✅ BOM
usuario = Usuario("João", "jo@email.com")
def processar_usuario(dados):
    pass

def listar_usuarios():
    pass
```

### Constantes
- Use `UPPER_SNAKE_CASE`

```python
# ❌ RUIM
max_tentativas = 5
timeout = 30

# ✅ BOM
MAX_TENTATIVAS = 5
TIMEOUT_SEGUNDOS = 30
```

### Classes
- Use `PascalCase`

```python
# ❌ RUIM
class usuario_service:
    pass

class database_manager:
    pass

# ✅ BOM
class UsuarioService:
    pass

class DatabaseManager:
    pass
```

### Arquivos
- Use `snake_case` para nomes de arquivo
- Se é um serviço, termine com `_service.py`
- Se é um modelo, use plural em `/models`

```
✅ BOM
src/services/usuario_service.py
src/services/paciente_service.py
src/routes/usuarios.py
src/models/__init__.py

❌ RUIM
src/Services/UsuarioService.py
src/routes/user.py
src/models.py
```

---

## Documentação

### Docstrings
- Toda função deve ter docstring
- Use format Google ou NumPy

```python
# ✅ BOM - Google style
def criar_usuario(nome: str, email: str, senha: str, tipo: str) -> Usuario:
    """
    Create a new user in the system.

    Args:
        nome: Full name of the user.
        email: Valid email address.
        senha: Password (minimum 6 characters).
        tipo: User type (admin, medico, paciente).

    Returns:
        Usuario: The created usuario object.

    Raises:
        ValidationError: If email format is invalid or password too weak.
        ConflictError: If email already registered.
        DatabaseError: If database operation fails.

    Example:
        >>> usuario = criar_usuario("João", "joao@email.com", "senha123", "paciente")
        >>> usuario.id
        1
    """
```

### Type Hints
- Use em todas as funções
- Especifique tipos de retorno

```python
# ❌ RUIM
def listar_usuarios(page, per_page):
    pass

# ✅ BOM
def listar_usuarios(page: int, per_page: int) -> List[Usuario]:
    pass

def obter_usuario_por_id(usuario_id: int) -> Optional[Usuario]:
    pass
```

### Comentários
- Use apenas para explicar **por que**, não **o que**
- Código limpo não precisa de muitos comentários

```python
# ❌ RUIM
# Incrementar contador
contador += 1

# ❌ RUIM (comentário óbvio)
# Validar email
Validator.validate_email(email)

# ✅ BOM (explicar lógica não óbvia)
# Email deve ser único no sistema por regulamento LGPD
if self._email_exists(email):
    raise ConflictError("Email already registered")
```

---

## Tratamento de Erros

### Use Exceções Customizadas
- Não use `Exception` genérica

```python
# ❌ RUIM
try:
    usuario = usuario_service.criar_usuario(...)
except Exception as e:
    return jsonify({"erro": str(e)})

# ✅ BOM
try:
    usuario = usuario_service.criar_usuario(...)
except ValidationError as e:
    return ResponseFormatter.error(message=e.message, status_code=400)
except ConflictError as e:
    return ResponseFormatter.error(message=e.message, status_code=409)
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    return ResponseFormatter.error(message="Internal server error", status_code=500)
```

### Sempre Log Erros
- Use logger, não print

```python
# ❌ RUIM
except Exception as e:
    print(f"Erro: {e}")
    return jsonify({"erro": str(e)})

# ✅ BOM
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return ResponseFormatter.error(message="Internal server error", status_code=500)
```

### Mensagens de Erro Úteis
- Use mensagens que ajudem a debugar

```python
# ❌ RUIM
raise ValidationError("Erro")
raise DatabaseError("Falhou")

# ✅ BOM
raise ValidationError("Email format is invalid. Expected format: user@domain.com")
raise DatabaseError("Failed to insert usuario in database: Duplicate entry")
```

---

## Testes

### Teste Unitário Básico

```python
import pytest
from unittest.mock import MagicMock

class TestUsuarioService:
    """Tests for UsuarioService."""

    @pytest.fixture
    def usuario_service(self):
        """Create UsuarioService instance."""
        service = UsuarioService()
        service.db_manager = MagicMock()  # Mock do banco
        return service

    def test_criar_usuario_success(self, usuario_service):
        """Test successful user creation."""
        # Arrange
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        usuario_service.db_manager.get_cursor.return_value.__enter__.return_value = (
            mock_cursor, MagicMock()
        )

        # Act
        usuario = usuario_service.criar_usuario(
            nome="João",
            email="joao@email.com",
            senha="senha123",
            tipo="paciente"
        )

        # Assert
        assert usuario.id == 1
        assert usuario.nome == "João"

    def test_criar_usuario_email_invalido(self, usuario_service):
        """Test user creation with invalid email."""
        with pytest.raises(ValidationError):
            usuario_service.criar_usuario(
                nome="João",
                email="email-invalido",
                senha="senha123",
                tipo="paciente"
            )
```

### Cobertura de Testes
- Mínimo 70%
- Critical paths: 100%

```bash
pytest --cov=src --cov-report=html
# Abrir htmlcov/index.html no navegador
```

---

## Segurança

### Senhas
- Sempre usar hash (werkzeug)
- Nunca armazenar em plain text

```python
# ❌ RUIM
usuario.senha = dados["senha"]  # Salvando em plain text!

# ✅ BOM
from werkzeug.security import generate_password_hash, check_password_hash

hash_senha = generate_password_hash(dados["senha"])
# Armazenar hash_senha no BD

# Para validar:
if check_password_hash(usuario.senha, senha_fornecida):
    # Válido
```

### Credenciais
- Nunca hardcode em código
- Sempre use variáveis de ambiente

```python
# ❌ RUIM
DB_PASSWORD = "Senha1704!"
JWT_SECRET = "ChaveSecreta"

# ✅ BOM
DB_PASSWORD = os.getenv("DB_PASSWORD")
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
```

### SQL Injection
- Sempre use prepared statements
- Nunca concatene strings SQL

```python
# ❌ RUIM - SQL Injection!
query = f"SELECT * FROM usuarios WHERE email = '{email}'"
cursor.execute(query)

# ✅ BOM
cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
```

### CORS
- Configure CORS apropriadamente em produção

```python
# ✅ BOM
from flask_cors import CORS

# Em desenvolvimento
if app.config["DEBUG"]:
    CORS(app)

# Em produção
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://seu-dominio.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "max_age": 3600
    }
})
```

---

## Performance

### Queries
- Use índices em BD
- Evite N+1 queries

```python
# ❌ RUIM - N+1 queries
usuarios = listar_usuarios()
for usuario in usuarios:
    email = obter_email(usuario.id)  # Query por usuário!

# ✅ BOM - Uma query
usuarios = listar_usuarios_com_emails()

# Ou usar JOIN no SQL
cursor.execute("""
    SELECT u.id, u.nome, e.email
    FROM usuarios u
    JOIN emails e ON u.id = e.usuario_id
""")
```

### Paginação
- Sempre paginar listas grandes

```python
# ✅ BOM
@app.route("/usuarios")
def listar_usuarios():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    
    usuarios = usuario_service.listar_usuarios(
        limite=per_page,
        offset=(page - 1) * per_page
    )
    
    return ResponseFormatter.paginated(...)
```

### Caching
- Use cache para queries pesadas

```python
from functools import lru_cache

# ✅ BOM
@lru_cache(maxsize=128)
def obter_tipo_usuario(tipo_id: int) -> str:
    # Query custosa, mas resultado será cacheado
    return tipo_service.obter_tipo(tipo_id)
```

---

## Git

### Commits
- Use mensagens descritivas
- Commits pequenos e atômicos

```bash
# ❌ RUIM
git commit -m "Corrigido"
git commit -m "Vários corrigidos"

# ✅ BOM
git commit -m "feat: add user registration endpoint"
git commit -m "fix: validate email format in usuario_service"
git commit -m "docs: update README with setup instructions"
```

### Padrão de Commit Message
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `refactor`: Refatoração sem mudança funcional
- `test`: Adicionar/atualizar testes
- `chore`: Tarefas build, dependencies

### Branch Naming
```
feature/user-authentication
bugfix/email-validation
docs/api-endpoints
```

### .gitignore
- Sempre versione `.env.example`, nunca `.env`
- Ignore `__pycache__`, `venv`, `.pyc`

---

## Checklist para Pull Request

- [ ] Código segue padrões de naming
- [ ] Funções têm docstrings
- [ ] Tipos estão especificados
- [ ] Testes foram escritos
- [ ] Cobertura >= 70%
- [ ] Nenhum hardcoded secrets
- [ ] Sem imports não utilizados
- [ ] Sem `print()` (usar logger)
- [ ] Mensagens de erro são úteis
- [ ] Performance foi considerada
- [ ] README foi atualizado (se necessário)

---

## Recursos Adicionais

- **PEP 8**: https://www.python.org/dev/peps/pep-0008/
- **PEP 257**: Docstring Conventions
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Security**: https://owasp.org/www-project-top-ten/

---

**Última atualização**: Novembro 2025
