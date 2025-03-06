from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import sqlite3
import datetime

app = Flask(__name__)

# Definindo a API com Swagger (Flask-RESTX)
api = Api(app, version='1.0', title='API de Ponto Eletrônico', description='Uma API para registro de ponto eletrônico')

# Definindo o modelo de dados para validação com o Swagger
ponto_model = api.model('Ponto', {
    'nome': fields.String(required=True, description='Nome do usuário'),
    'email': fields.String(required=True, description='E-mail do usuário'),
    'departamento': fields.String(required=True, description='Departamento do usuário'),
    'cargo': fields.String(required=True, description='Cargo do usuário'),
    'id': fields.String(required=True, description='ID único do usuário'),
    'tipo': fields.String(required=True, description='Tipo de ponto (entrada ou saída)', enum=['entrada', 'saida'])
})

# Função para conectar ao banco de dados SQLite
def get_db():
    conn = sqlite3.connect('pontos.db')  # Cria ou abre o banco de dados pontos.db
    conn.row_factory = sqlite3.Row  # Para acessar os dados como dicionários
    return conn

# Função para criar a tabela se não existir
def criar_tabela():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pontos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                departamento TEXT NOT NULL,
                cargo TEXT NOT NULL,
                id_usuario TEXT NOT NULL,
                tipo TEXT NOT NULL,
                hora TEXT NOT NULL
            )
        ''')
        conn.commit()

# Chama a função para criar a tabela quando o servidor for iniciado
criar_tabela()

# Rota para registrar o ponto de entrada ou saída
@api.route('/registrar_ponto')
class RegistrarPonto(Resource):
    @api.doc('Registrar Ponto')
    @api.expect(ponto_model)
    def post(self):
        dados = request.get_json()

        # Extraindo os dados do corpo da requisição
        nome = dados['nome']
        email = dados['email']
        departamento = dados['departamento']
        cargo = dados['cargo']
        id_usuario = dados['id']
        tipo = dados['tipo'].lower()

        # Validando o tipo (entrada ou saída)
        if tipo not in ['entrada', 'saida']:
            return {'error': "Tipo inválido. Use 'entrada' ou 'saida'."}, 400

        # Capturando a hora atual
        hora_atual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Salvando o ponto no banco de dados
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pontos (nome, email, departamento, cargo, id_usuario, tipo, hora)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nome, email, departamento, cargo, id_usuario, tipo, hora_atual))
            conn.commit()

        return {'mensagem': f"Ponto de {tipo} registrado com sucesso!"}, 201

# Rota para consultar todos os pontos registrados
@api.route('/consultar_pontos')
class ConsultarPontos(Resource):
    @api.doc('Consultar todos os pontos')
    def get(self):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM pontos')
            pontos = cursor.fetchall()

        pontos_lista = []
        for ponto in pontos:
            pontos_lista.append({
                'usuario': {
                    'nome': ponto['nome'],
                    'email': ponto['email'],
                    'departamento': ponto['departamento'],
                    'cargo': ponto['cargo'],
                    'id': ponto['id_usuario']
                },
                'tipo': ponto['tipo'],
                'hora': ponto['hora']
            })
        
        return {'pontos': pontos_lista}, 200

# Rota para consultar os pontos de um usuário específico
@api.route('/consultar_pontos/<id_usuario>')
class ConsultarPontosUsuario(Resource):
    @api.doc('Consultar pontos de um usuário específico')
    def get(self, id_usuario):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM pontos WHERE id_usuario = ?', (id_usuario,))
            pontos = cursor.fetchall()

        if not pontos:
            return {'mensagem': "Nenhum ponto encontrado para esse usuário."}, 404

        pontos_lista = []
        for ponto in pontos:
            pontos_lista.append({
                'usuario': {
                    'nome': ponto['nome'],
                    'email': ponto['email'],
                    'departamento': ponto['departamento'],
                    'cargo': ponto['cargo'],
                    'id': ponto['id_usuario']
                },
                'tipo': ponto['tipo'],
                'hora': ponto['hora']
            })
        
        return {'pontos': pontos_lista}, 200

# Rota para atualizar um ponto eletrônico (PUT)
@api.route('/atualizar_ponto/<int:ponto_id>')
class AtualizarPonto(Resource):
    @api.doc('Atualizar ponto eletrônico')
    @api.expect(ponto_model)
    def put(self, ponto_id):
        dados = request.get_json()

        nome = dados['nome']
        email = dados['email']
        departamento = dados['departamento']
        cargo = dados['cargo']
        id_usuario = dados['id']
        tipo = dados['tipo'].lower()

        # Validando o tipo (entrada ou saída)
        if tipo not in ['entrada', 'saida']:
            return {'error': "Tipo inválido. Use 'entrada' ou 'saida'."}, 400

        # Capturando a hora atual
       # hora_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hora_atual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE pontos 
                SET nome = ?, email = ?, departamento = ?, cargo = ?, id_usuario = ?, tipo = ?, hora = ?
                WHERE id = ?
            ''', (nome, email, departamento, cargo, id_usuario, tipo, hora_atual, ponto_id))
            conn.commit()

        return {'mensagem': 'Ponto atualizado com sucesso!'}, 200

# Rota para excluir um ponto eletrônico (DELETE)
@api.route('/deletar_ponto/<int:ponto_id>')
class DeletarPonto(Resource):
    @api.doc('Deletar ponto eletrônico')
    def delete(self, ponto_id):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM pontos WHERE id = ?', (ponto_id,))
            conn.commit()

        return {'mensagem': 'Ponto deletado com sucesso!'}, 200

# Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)
