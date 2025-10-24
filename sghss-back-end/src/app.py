from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from config import DB_CONFIG
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
app = Flask(__name__)

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
            access_token = create_access_token(identity=usuario["id"])
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