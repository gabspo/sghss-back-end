# SGHSS — Sistema de Gestão de Saúde e Segurança em Telemedicina

Resumo
-------
O repositório contém a implementação de um serviço backend desenvolvido em Python com o microframework Flask. O sistema provê APIs REST para gestão de pacientes, profissionais de saúde, agendamentos de consultas e funcionalidades iniciais de telemedicina.

Estrutura do repositório
------------------------
O projeto segue uma organização em camadas para separar responsabilidades. A árvore principal de diretórios é a seguinte:

```
sghss-back-end/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── settings.py
│   │   └── database.py
│   ├── models/
│   ├── services/
│   ├── routes/
│   ├── utils/
│   └── exceptions/
├── tests/
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

Instalação e execução
---------------------
1. Instalar dependências:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2. Configurar variáveis de ambiente: copiar o arquivo de exemplo e ajustar os valores conforme o ambiente.

```powershell
copy .env.example .env
```

Edite o `.env` para definir as informações de conexão com o banco de dados e chaves de segurança.

3. Inicializar o banco de dados:

Executar o script SQL disponível no repositório (`DATABASE_INIT.sql`) em uma instância MySQL apropriada para desenvolvimento.

4. Executar a aplicação:

```powershell
python app.py
```

Após a inicialização, a API estará disponível em `http://localhost:5000`.

Arquitetura e principais decisões de projeto
-------------------------------------------
- Aplicação configurada a partir de uma fábrica (`create_app`) para permitir múltiplos ambientes (desenvolvimento, teste, produção).
- Separação em camadas: rotas expõem endpoints HTTP; serviços encapsulam regras de negócio; modelos representam entidades e mapeamento com o banco.
- Autenticação baseada em tokens JWT para rotas que exigem autenticação.
- Configurações sensíveis são externalizadas via variáveis de ambiente.

Tratamento de erros e logging
-----------------------------
- A aplicação centraliza tratamento de exceções por meio de handlers específicos, retornando respostas HTTP padronizadas.
- Logging configurado para registrar eventos em console e em arquivos com rotação.

Qualidade e testes
------------------
- A base do projeto inclui exemplos de testes (pytest). Recomenda-se a execução periódica da suíte de testes durante o desenvolvimento e a integração de um pipeline de CI para automatizar validações.

Documentação da API
-------------------
- Uma especificação OpenAPI (3.0) para os principais endpoints foi adicionada em `docs/openapi.yaml`.
- Um mecanismo de documentação interativa (Swagger UI) pode ser ativado utilizando a biblioteca `flasgger` e apontando o template para `docs/openapi.yaml`.

Reprodutibilidade
-----------------
- Para reproduzir o ambiente de desenvolvimento recomenda-se o uso de contêineres (Docker) e de um arquivo `docker-compose` que inclua a aplicação e uma instância MariaDB/MySQL. Esse artefato não está incluído no repositório e pode ser adicionado conforme necessidade.

Segurança e conformidade
------------------------
- Senhas devem ser armazenadas de forma segura (hashing apropriado).
- Não versionar arquivos com segredos (`.env` contendo valores reais).
- Dados sensíveis (por exemplo, CPF ou prontuário) requerem políticas de proteção, pseudonimização e retenção compatíveis com a legislação aplicável.

Dependências principais
-----------------------
- Flask
- Flask-JWT-Extended
- mysql-connector-python
- python-dotenv

Execução de testes
------------------
Executar a suíte de testes com:

```powershell
pytest tests/
```

Padronização de código
----------------------
- Convenções de nomenclatura: `snake_case` para variáveis e funções; `PascalCase` para classes.
- Recomenda-se uso de ferramentas de lint (por exemplo, `flake8`) e de tipagem estática quando aplicável.

Contribuição
------------
Contribuições devem seguir as diretrizes de revisão e incluir testes que cobrem alterações funcionais relevantes. Atualize a documentação associada quando o comportamento da API for alterado.

Licença
-------
MIT License

Contato
-------
Removido conforme solicitado.
