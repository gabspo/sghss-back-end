Instruções para integrar o Swagger UI (flasgger) na aplicação

1. Instale a dependência (ou adicione em requirements.txt):

```
flasgger==0.9.5
```

2. No `app.py` (ou dentro da função `create_app`), importe e inicialize o Swagger:

```python
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    # ... configuração da app ...
    Swagger(app, template_file='docs/openapi.yaml')
    return app

# ou, se usar app.py simples:
if __name__ == '__main__':
    app = create_app()
    Swagger(app, template_file='docs/openapi.yaml')
    app.run(host='0.0.0.0', port=5000)
```

3. Após iniciar a aplicação, a UI estará disponível em: `http://localhost:5000/apidocs`

Observação: o `template_file` aponta para `docs/openapi.yaml` que foi adicionado ao repositório.
