from flask import Flask, jsonify, request, Response
import mysql.connector
import logging
from logging.handlers import RotatingFileHandler
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app)

# Conexão com o banco de dados MySQL
def conectar_banco():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abc123",  # Atualize com a sua senha do MySQL
            database="univesp"  # Nome do banco de dados
        )
        return db
    except mysql.connector.Error as err:
        app.logger.error(f"Erro ao conectar ao banco de dados: {str(err)}")
        abort(500, description="Erro ao conectar ao banco de dados.")

#API de teste para ver se esta funcionando
@app.route('/')
@limiter.limit("5 per minute")  # Limita a 5 requisições por minuto
def home():
    return "API funcionando!"

# API para validar login
@app.route('/api/validar_login', methods=['POST'])
@limiter.limit("5 per minute")  # Limita a 5 requisições por minuto
def validar_login_banco():
    data = request.json
    usuario = data.get('usuario')
    senha = data.get('senha')

    if usuario and senha:
        db = conectar_banco()
        cursor = db.cursor()
        cursor.execute("SELECT aut FROM tbLogin WHERE usuario = %s AND senha = %s", (usuario, senha))
        aut = cursor.fetchone()

        if aut:
            return jsonify({"status": True, "aut": aut[0]}), 200
        else:
            return jsonify({"status": False, "aut": 0}), 401
    return jsonify({"status": False, "aut": 0}), 400

# API para cadastro de usuário na tabela tbLogin
@app.route('/api/cadastro_usuario', methods=['POST'])
@limiter.limit("5 per minute")
def cadastro_usuario():
    data = request.json
    aut_usuario = data.get('aut_usuario')  # Verificação de permissão para cadastro
    usuario = data.get('usuario')
    senha = data.get('senha')
    aut = data.get('aut')

    if aut_usuario != 5:  # Somente usuários com "aut_usuario" 5 podem cadastrar
        return jsonify({"status": False, "message": "Permissão negada"}), 403

    if not usuario or not senha or not aut:
        return jsonify({"status": False, "message": "Todos os campos são obrigatórios"}), 400

    try:
        db = conectar_banco()
        cursor = db.cursor()

        # Inserir o novo usuário no banco de dados
        cursor.execute("INSERT INTO tbLogin (usuario, senha, aut) VALUES (%s, %s, %s)", (usuario, senha, aut))
        db.commit()

        return jsonify({"status": True}), 201

    except mysql.connector.Error as err:
        return jsonify({"status": False, "message": str(err)}), 500

    finally:
        db.close()

# API para atualização de dados de usuário na tabela tbLogin
@app.route('/api/update_usuario', methods=['PUT'])
@limiter.limit("5 per minute")
def update_usuario():
    data = request.json
    cod = data.get('cod')  # ID do usuário a ser atualizado
    usuario = data.get('usuario')
    senha = data.get('senha')
    aut = data.get('aut')

    if not cod or not usuario or not senha or not aut:
        return jsonify({"status": False, "message": "Todos os campos são obrigatórios"}), 400

    try:
        db = conectar_banco()
        cursor = db.cursor()

        # Atualizar o usuário no banco de dados
        cursor.execute("UPDATE tbLogin SET usuario = %s, senha = %s, aut = %s WHERE cod = %s", 
                       (usuario, senha, aut, cod))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"status": False, "message": "Usuário não encontrado"}), 404

        return jsonify({"status": True, "message": "Usuário atualizado com sucesso"}), 200

    except mysql.connector.Error as err:
        return jsonify({"status": False, "message": str(err)}), 500

    finally:
        db.close()

# API para consultar todos os usuários (somente usuários com aut_usuario = 5)
@app.route('/api/consulta_usuarios', methods=['GET'])
@limiter.limit("5 per minute")
def consulta_usuarios():
    aut_usuario = request.args.get('aut_usuario', default=0, type=int)

    if aut_usuario != 5:  # Somente usuários com "aut_usuario" 5 podem consultar
        return jsonify({"status": False, "message": "Permissão negada"}), 403

    try:
        db = conectar_banco()
        cursor = db.cursor(dictionary=True)

        # Consultar todos os usuários
        cursor.execute("SELECT cod, usuario, senha, aut FROM tbLogin")
        result = cursor.fetchall()

        return jsonify(result), 200  # Retorna todos os usuários cadastrados

    except mysql.connector.Error as err:
        return jsonify({"status": False, "message": str(err)}), 500

    finally:
        db.close()

# API para cadastrar armazenamento
@app.route('/api/cadastro_armazenamento', methods=['POST'])
@limiter.limit("5 per minute")  # Limita a 5 requisições por minuto
def cadastro_armazenamento():
    data = request.json
    desc_local = data.get('desc_local')

    if not desc_local:
        return jsonify({"status": False}), 400

    try:
        db = conectar_banco()
        cursor = db.cursor()

        cursor.execute("INSERT INTO tbCadastroArmazenamento (desc_local) VALUES (%s)", (desc_local,))
        db.commit()

        return jsonify({"status": True}), 201  # Retorno de sucesso

    except mysql.connector.Error as err:
        return jsonify({"status": False}), 500

    finally:
        db.close()

# API para consultar armazenamento
@app.route('/api/consulta_armazenamento', methods=['GET'])
@limiter.limit("5 per minute")  # Limita a 5 requisições por minuto
def consulta_armazenamento():
    try:
        db = conectar_banco()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT cod, desc_local FROM tbCadastroArmazenamento")
        result = cursor.fetchall()

        return jsonify(result), 200  # Retorna todos os locais de armazenamento

    except mysql.connector.Error as err:
        return jsonify({"status": False, "message": str(err)}), 500

    finally:
        db.close()

# API para atualizar armazenamento
@app.route('/api/update_armazenamento', methods=['PUT'])
@limiter.limit("5 per minute")  # Limita a 5 requisições por minuto
def update_armazenamento():
    data = request.json
    cod = data.get('cod')
    desc_local = data.get('desc_local')

    if not cod or not desc_local:
        return jsonify({"status": False, "message": "Os campos 'cod' e 'desc_local' são obrigatórios"}), 400

    try:
        db = conectar_banco()
        cursor = db.cursor()

        # Atualiza o local de armazenamento
        cursor.execute("UPDATE tbCadastroArmazenamento SET desc_local = %s WHERE cod = %s", (desc_local, cod))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"status": False, "message": "Código do armazenamento não encontrado"}), 404
        
        return jsonify({"status": True, "message": "Armazenamento atualizado com sucesso"}), 200

    except mysql.connector.Error as err:
        return jsonify({"status": False, "message": str(err)}), 500

    finally:
        db.close()

# API para cadastrar produto
@app.route('/api/cadastro_produto', methods=['POST'])
@limiter.limit("5 per minute")  # Limita a 5 requisições por minuto
def cadastro_produto():
    data = request.json
    required_fields = [
        'codArmaz', 'dscNome', 'fornecedor', 'qtdMaxima', 'estadoFisico', 'substancias',
        'numeroCas', 'concentracao', 'classsGHS', 'elemento1', 'elemento2', 'elemento3',
        'elemento4', 'elemento5', 'elemento6', 'elemento7', 'elemento8', 'elemento9',
        'advertencia', 'frasePerigo', 'frasePrecaucao'
    ]

    # Verificar se todos os campos obrigatórios estão presentes
    for field in required_fields:
        if field not in data:
            return jsonify({"status": False, "message": f"O campo '{field}' é obrigatório"}), 400

    try:
        db = conectar_banco()
        cursor = db.cursor()

        # Inserir o novo produto no banco de dados
        query = """
        INSERT INTO tbCadastroProdutos (codArmaz, dscNome, fornecedor, qtdMaxima, estadoFisico, substancias, numeroCas, 
                                         concentracao, classsGHS, elemento1, elemento2, elemento3, elemento4, elemento5, 
                                         elemento6, elemento7, elemento8, elemento9, advertencia, frasePerigo, frasePrecaucao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['codArmaz'], data['dscNome'], data['fornecedor'], data['qtdMaxima'], data['estadoFisico'],
            data['substancias'], data['numeroCas'], data['concentracao'], data['classsGHS'], data['elemento1'],
            data['elemento2'], data['elemento3'], data['elemento4'], data['elemento5'], data['elemento6'],
            data['elemento7'], data['elemento8'], data['elemento9'], data['advertencia'], data['frasePerigo'],
            data['frasePrecaucao']
        ))
        db.commit()

        return jsonify({"status": True}), 201  # Retorno de sucesso

    except mysql.connector.Error as err:
        return jsonify({"status": False, "message": str(err)}), 500

    finally:
        db.close()

# API para consultar produtos
@app.route('/api/consulta_produto', methods=['GET'])
@limiter.limit("5 per minute")  # Limita a 5 requisições por minuto
def consulta_produto():
    cod = request.args.get('cod', default=0, type=int)

    try:
        db = conectar_banco()
        cursor = db.cursor(dictionary=True)

        if cod == 0:
            # Consultar todos os produtos
            query = "SELECT * FROM tbCadastroProdutos"
            cursor.execute(query)
            result = cursor.fetchall()
        else:
            # Consultar produto específico
            query = "SELECT * FROM tbCadastroProdutos WHERE cod = %s"
            cursor.execute(query, (cod,))
            result = cursor.fetchone()

        if result:
            return jsonify(result), 200  # Retorna a lista de produtos ou o produto específico
        else:
            return jsonify({"status": False, "message": "Produto não encontrado"}), 404

    except mysql.connector.Error as err:
        return jsonify({"status": False, "message": str(err)}), 500

    finally:
        db.close()

# API para atualizar produto
@app.route('/api/update_produto', methods=['PUT'])
@limiter.limit("5 per minute")  # Limita a 5 requisições por minuto
def update_produto():
    data = request.json
    cod = data.get('cod')

    if not cod:
        return jsonify({"status": False, "message": "O campo 'cod' é obrigatório"}), 400

    try:
        db = conectar_banco()
        cursor = db.cursor()

        # Atualiza o produto
        query = """
        UPDATE tbCadastroProdutos SET 
            codArmaz = %s, dscNome = %s, fornecedor = %s, qtdMaxima = %s, estadoFisico = %s,
            substancias = %s, numeroCas = %s, concentracao = %s, classsGHS = %s,
            elemento1 = %s, elemento2 = %s, elemento3 = %s, elemento4 = %s, elemento5 = %s,
            elemento6 = %s, elemento7 = %s, elemento8 = %s, elemento9 = %s, advertencia = %s,
            frasePerigo = %s, frasePrecaucao = %s
        WHERE cod = %s
        """
        cursor.execute(query, (
            data['codArmaz'], data['dscNome'], data['fornecedor'], data['qtdMaxima'], data['estadoFisico'],
            data['substancias'], data['numeroCas'], data['concentracao'], data['classsGHS'], data['elemento1'],
            data['elemento2'], data['elemento3'], data['elemento4'], data['elemento5'], data['elemento6'],
            data['elemento7'], data['elemento8'], data['elemento9'], data['advertencia'], data['frasePerigo'],
            data['frasePrecaucao'], cod
        ))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"status": False, "message": "Produto não encontrado"}), 404
        
        return jsonify({"status": True, "message": "Produto atualizado com sucesso"}), 200

    except mysql.connector.Error as err:
        return jsonify({"status": False, "message": str(err)}), 500

    finally:
        db.close()

# Definindo o logger
if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=3000, debug=True)
