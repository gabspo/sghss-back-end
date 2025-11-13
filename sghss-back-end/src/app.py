from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from config import DB_CONFIG
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
app = Flask(__name__)
from datetime import timedelta
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "Senha1704!"  # Chave secreta usada para assinar os tokens
jwt = JWTManager(app)

# Helper para conexão com o banco
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Rota de teste
@app.route("/ping")
def ping():
    return {"status": "ok", "message": "Servidor rodando!"}

@app.route("/teleconsulta", methods=["POST"])
@jwt_required()
def agendar_teleconsulta():
    dados = request.get_json()
    # salvar tipo_consulta = "telemedicina" e link_video

# Rota para criar usuário
@app.route("/usuarios", methods=["POST"])

def criar_usuario():
    data = request.json
    required_fields = ["nome", "email", "senha", "tipo"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "erro", "message": "Campos obrigatórios ausentes"}), 400

    senha_hash = generate_password_hash(data["senha"])
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, tipo)
            VALUES (%s, %s, %s, %s)
        """, (data["nome"], data["email"], senha_hash, data["tipo"]))
        conn.commit()
        return jsonify({"status": "ok", "message": "Usuário criado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

# Rota para listar usuários
@app.route("/usuarios", methods=["GET"])
@jwt_required()
def listar_usuarios():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, email, tipo FROM usuarios")
        usuarios = cursor.fetchall()
        return jsonify(usuarios)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

# Rota de login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nome, email, senha, tipo FROM usuarios
            WHERE email = %s
        """, (data["email"],))
        usuario = cursor.fetchone()
        if usuario and check_password_hash(usuario["senha"], data["senha"]):
            access_token = create_access_token(identity=str(usuario["id"]))
            del usuario["senha"]
            return jsonify({"status": "ok", "usuario": usuario, "token": access_token})
        else:
            return jsonify({"status": "erro", "message": "Credenciais inválidas"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()
@app.route("/usuarios/<int:id>", methods=["PUT"])
@jwt_required()
def editar_usuario(id):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios
            SET nome = %s, email = %s, tipo = %s
            WHERE id = %s
        """, (data["nome"], data["email"], data["tipo"], id))
        conn.commit()
        return jsonify({"status": "ok", "message": "Usuário atualizado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()
@app.route("/usuarios/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_usuario(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Usuário excluído com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/profissionais", methods=["POST"])
@jwt_required()
def cadastrar_profissional():
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO profissionais (nome, email, telefone, especialidade, registro)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            dados["nome"],
            dados["email"],
            dados["telefone"],
            dados["especialidade"],
            dados["registro"]
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Profissional cadastrado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/profissionais", methods=["GET"])
@jwt_required()
def listar_profissionais():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM profissionais")
        resultado = cursor.fetchall()
        return jsonify(resultado)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/profissionais/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_profissional(id):
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE profissionais
            SET nome=%s, email=%s, telefone=%s, especialidade=%s, registro=%s
            WHERE id=%s
        """, (
            dados["nome"],
            dados["email"],
            dados["telefone"],
            dados["especialidade"],
            dados["registro"],
            id
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Profissional atualizado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/profissionais/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_profissional(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM profissionais WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Profissional excluído com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/receitas", methods=["POST"])
@jwt_required()
def emitir_receita():
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO receitas (profissional_id, paciente_id, data_emissao, conteudo)
            VALUES (%s, %s, NOW(), %s)
        """, (
            dados["profissional_id"],
            dados["paciente_id"],
            dados["conteudo"]
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Receita emitida com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/receitas", methods=["GET"])
@jwt_required()
def listar_receitas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM receitas")
        resultado = cursor.fetchall()
        return jsonify(resultado)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/receitas/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_receita(id):
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE receitas
            SET profissional_id=%s, paciente_id=%s, conteudo=%s
            WHERE id=%s
        """, (
            dados["profissional_id"],
            dados["paciente_id"],
            dados["conteudo"],
            id
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Receita atualizada com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/receitas/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_receita(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM receitas WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Receita excluída com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/agendas", methods=["POST"])
@jwt_required()
def cadastrar_agenda():
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO agendas (profissional_id, data, status)
            VALUES (%s, %s, %s)
        """, (
            dados["profissional_id"],
            dados["data"],
            dados["status"]
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Horário cadastrado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/agendas", methods=["GET"])
@jwt_required()
def listar_agendas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agendas")
        resultado = cursor.fetchall()
        return jsonify(resultado)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/agendas/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_agenda(id):
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE agendas
            SET profissional_id=%s, data=%s, status=%s
            WHERE id=%s
        """, (
            dados["profissional_id"],
            dados["data"],
            dados["status"],
            id
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Horário atualizado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/agendas/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_agenda(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM agendas WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Horário excluído com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/exames", methods=["POST"])
@jwt_required()
def cadastrar_exame():
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO exames (paciente_id, tipo, data, resultado, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            dados["paciente_id"],
            dados["tipo"],
            dados["data"],
            dados["resultado"],
            dados["status"]
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Exame cadastrado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/exames", methods=["GET"])
@jwt_required()
def listar_exames():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM exames")
        resultado = cursor.fetchall()
        return jsonify(resultado)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/exames/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_exame(id):
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE exames
            SET paciente_id=%s, tipo=%s, data=%s, resultado=%s, status=%s
            WHERE id=%s
        """, (
            dados["paciente_id"],
            dados["tipo"],
            dados["data"],
            dados["resultado"],
            dados["status"],
            id
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Exame atualizado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/exames/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_exame(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM exames WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Exame excluído com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/prontuarios", methods=["POST"])
@jwt_required()
def criar_prontuario():
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO prontuarios (paciente_id, profissional_id, data, observacoes)
            VALUES (%s, %s, NOW(), %s)
        """, (
            dados["paciente_id"],
            dados["profissional_id"],
            dados["observacoes"]
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Prontuário criado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/prontuarios", methods=["GET"])
@jwt_required()
def listar_prontuarios():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prontuarios")
        resultado = cursor.fetchall()
        return jsonify(resultado)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/prontuarios/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_prontuario(id):
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE prontuarios
            SET paciente_id=%s, profissional_id=%s, observacoes=%s
            WHERE id=%s
        """, (
            dados["paciente_id"],
            dados["profissional_id"],
            dados["observacoes"],
            id
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Prontuário atualizado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/prontuarios/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_prontuario(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prontuarios WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Prontuário excluído com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/leitos", methods=["POST"])
@jwt_required()
def cadastrar_leito():
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leitos (numero, tipo, status, paciente_id)
            VALUES (%s, %s, %s, %s)
        """, (
            dados["numero"],
            dados["tipo"],
            dados["status"],
            dados.get("paciente_id")
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Leito cadastrado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/leitos", methods=["GET"])
@jwt_required()
def listar_leitos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM leitos")
        resultado = cursor.fetchall()
        return jsonify(resultado)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/leitos/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_leito(id):
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE leitos
            SET numero=%s, tipo=%s, status=%s, paciente_id=%s
            WHERE id=%s
        """, (
            dados["numero"],
            dados["tipo"],
            dados["status"],
            dados.get("paciente_id"),
            id
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Leito atualizado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/leitos/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_leito(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leitos WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Leito excluído com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/financeiros", methods=["POST"])
@jwt_required()
def registrar_financeiro():
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO financeiros (tipo, descricao, valor, data, categoria)
            VALUES (%s, %s, %s, NOW(), %s)
        """, (
            dados["tipo"],         # entrada ou saida
            dados["descricao"],
            dados["valor"],
            dados["categoria"]
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Movimentação registrada com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/financeiros", methods=["GET"])
@jwt_required()
def listar_financeiros():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM financeiros")
        resultado = cursor.fetchall()
        return jsonify(resultado)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/financeiros/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_financeiro(id):
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE financeiros
            SET tipo=%s, descricao=%s, valor=%s, categoria=%s
            WHERE id=%s
        """, (
            dados["tipo"],
            dados["descricao"],
            dados["valor"],
            dados["categoria"],
            id
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Movimentação atualizada com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/financeiros/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_financeiro(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM financeiros WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Movimentação excluída com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/suprimentos", methods=["POST"])
@jwt_required()
def cadastrar_suprimento():
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO suprimentos (nome, categoria, quantidade, unidade, validade, fornecedor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            dados["nome"],
            dados["categoria"],
            dados["quantidade"],
            dados["unidade"],
            dados["validade"],
            dados["fornecedor"]
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Suprimento cadastrado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/suprimentos", methods=["GET"])
@jwt_required()
def listar_suprimentos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM suprimentos")
        resultado = cursor.fetchall()
        return jsonify(resultado)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/suprimentos/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_suprimento(id):
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE suprimentos
            SET nome=%s, categoria=%s, quantidade=%s, unidade=%s, validade=%s, fornecedor=%s
            WHERE id=%s
        """, (
            dados["nome"],
            dados["categoria"],
            dados["quantidade"],
            dados["unidade"],
            dados["validade"],
            dados["fornecedor"],
            id
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Suprimento atualizado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/suprimentos/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_suprimento(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM suprimentos WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Suprimento excluído com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/auditoria", methods=["POST"])
@jwt_required()
def registrar_log():
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO auditoria (usuario, acao, recurso, data, detalhes)
            VALUES (%s, %s, %s, NOW(), %s)
        """, (
            dados["usuario"],
            dados["acao"],
            dados["recurso"],
            dados["detalhes"]
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Log registrado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/auditoria", methods=["GET"])
@jwt_required()
def listar_logs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM auditoria ORDER BY data DESC")
        resultado = cursor.fetchall()
        return jsonify(resultado)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/auditoria/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_log(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM auditoria WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Log excluído com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/teleconsultas", methods=["POST"])
@jwt_required()
def agendar_teleconsulta():
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO teleconsultas (paciente_id, profissional_id, data, link_video, status, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            dados["paciente_id"],
            dados["profissional_id"],
            dados["data"],
            dados["link_video"],
            "agendada",
            dados.get("observacoes", "")
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Teleconsulta agendada com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/teleconsultas", methods=["GET"])
@jwt_required()
def listar_teleconsultas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM teleconsultas ORDER BY data DESC")
        resultado = cursor.fetchall()
        return jsonify(resultado)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/teleconsultas/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_teleconsulta(id):
    dados = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE teleconsultas
            SET status=%s, observacoes=%s
            WHERE id=%s
        """, (
            dados["status"],
            dados["observacoes"],
            id
        ))
        conn.commit()
        return jsonify({"status": "ok", "message": "Teleconsulta atualizada com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/teleconsultas/<int:id>", methods=["DELETE"])
@jwt_required()
def cancelar_teleconsulta(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teleconsultas WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Teleconsulta cancelada com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

# Rota para criar paciente
@app.route("/pacientes", methods=["POST"])
@jwt_required()
def criar_paciente():
    data = request.json
    required_fields = ["nome", "cpf", "data_nascimento", "telefone", "email"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "erro", "message": "Campos obrigatórios ausentes"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pacientes (nome, cpf, data_nascimento, telefone, email)
            VALUES (%s, %s, %s, %s, %s)
        """, (data["nome"], data["cpf"], data["data_nascimento"], data["telefone"], data["email"]))
        conn.commit()
        return jsonify({"status": "ok", "message": "Paciente cadastrado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

# Rota para listar pacientes
@app.route("/pacientes", methods=["GET"])
@jwt_required()
def listar_pacientes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pacientes")
        pacientes = cursor.fetchall()
        return jsonify(pacientes)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()
@app.route("/pacientes/<int:id>", methods=["PUT"])
@jwt_required()
def editar_paciente(id):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pacientes
            SET nome = %s, cpf = %s, data_nascimento = %s, telefone = %s, email = %s
            WHERE id = %s
        """, (data["nome"], data["cpf"], data["data_nascimento"], data["telefone"], data["email"], id))
        conn.commit()
        return jsonify({"status": "ok", "message": "Paciente atualizado com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()
@app.route("/pacientes/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_paciente(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pacientes WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Paciente excluído com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/consultas", methods=["POST"])
@jwt_required()
def criar_consulta():
    data = request.json
    required_fields = ["paciente_id", "data", "motivo", "observacoes"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "erro", "message": "Campos obrigatórios ausentes"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO consultas (paciente_id, data, motivo, observacoes)
            VALUES (%s, %s, %s, %s)
        """, (data["paciente_id"], data["data"], data["motivo"], data["observacoes"]))
        conn.commit()
        return jsonify({"status": "ok", "message": "Consulta registrada com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/consultas/<int:id>", methods=["PUT"])
@jwt_required()
def editar_consulta(id):
    data = request.get_json()
    required_fields = ["data", "motivo", "observacoes"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "erro", "message": "Campos obrigatórios ausentes"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE consultas SET data=%s, motivo=%s, observacoes=%s WHERE id=%s
        """, (data["data"], data["motivo"], data["observacoes"], id))
        conn.commit()
        return jsonify({"status": "ok", "message": "Consulta atualizada com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/consultas/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_consulta(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consultas WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"status": "ok", "message": "Consulta excluída com sucesso!"})
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route("/consultas", methods=["GET"])
@jwt_required()
def listar_consultas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id, c.data, c.motivo, c.observacoes,
                   p.nome AS paciente_nome, p.id AS paciente_id
            FROM consultas c
            JOIN pacientes p ON c.paciente_id = p.id
            ORDER BY c.data DESC
        """)
        consultas = cursor.fetchall()
        return jsonify(consultas)
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()
@app.route("/consultas/<int:id>", methods=["GET"])
@jwt_required()
def consulta_por_id(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id, c.data, c.motivo, c.observacoes,
                   p.nome AS paciente_nome, p.id AS paciente_id
            FROM consultas c
            JOIN pacientes p ON c.paciente_id = p.id
            WHERE c.id = %s
        """, (id,))
        consulta = cursor.fetchone()
        if consulta:
            return jsonify(consulta)
        else:
            return jsonify({"status": "erro", "message": "Consulta não encontrada"}), 404
    except mysql.connector.Error as err:
        return jsonify({"status": "erro", "message": str(err)})
    finally:
        cursor.close()
        conn.close()


# Iniciar servidor
if __name__ == "__main__":
    app.run(debug=True)