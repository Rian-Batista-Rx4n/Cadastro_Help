from flask import redirect, request, render_template, flash, Flask
import json
import os
import mysql.connector

json_path = os.path.join(os.path.dirname(__file__), 'usuarios_help.json')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RX4NRX4N'

logado = False

@app.route("/")
def home():
    return render_template('login_help.html')

@app.route("/login_help", methods=["POST"])
def login_help():
    nome_completo = request.form.get('nome_completo')
    nome_apelido = request.form.get('nome_apelido')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    senha = request.form.get('senha')
    cep = request.form.get('cep')

    with open(json_path) as usuarios_help:
        usuarios = json.load(usuarios_help)

    for usuario in usuarios:
        if (
            usuario['nome_completo'] == nome_completo and
            usuario['nome_apelido'] == nome_apelido and
            usuario['cpf'] == cpf and
            usuario['email'] == email and
            usuario['senha'] == senha and
            usuario['cep'] == cep
        ):
            global logado
            logado = True
            return render_template("help_home.html")

    flash('Esse usuário não existe! Verifique os dados e tente novamente.')
    return redirect("/")


# Rota para exibir a página de cadastro (GET)
@app.route('/cadastro_help', methods=['GET'])
def cadastro_help_get():
    return render_template("cadastro_help.html")

# Rota para processar o formulário de cadastro (POST)
@app.route('/cadastro_help', methods=['POST'])
def cadastro_help_post():
    with open(json_path) as usuariosJson:
        usuarios = json.load(usuariosJson)

    nome_completo = request.form.get('nome_completo')
    nome_apelido = request.form.get('nome_apelido')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    senha = request.form.get('senha')
    cep = request.form.get('cep')

    for usuario in usuarios:
        if (
            usuario['nome_completo'] == nome_completo and
            usuario['cpf'] == cpf or
            usuario['email'] == email or
            usuario['cep'] == cep
        ):
            flash('Usuário já existe!')
            return redirect("/cadastro_help")  # Redireciona para o formulário

    novo_usuario = {
        "nome_completo": nome_completo,
        "nome_apelido": nome_apelido,
        "cpf": cpf,
        "email": email,
        "senha": senha,
        "cep": cep
    }

    usuarios.append(novo_usuario)

    with open(json_path, 'w') as gravarTemp:
        json.dump(usuarios, gravarTemp, indent=4)

    flash('Usuário cadastrado com sucesso! Faça login.')
    return redirect("/")  # Volta para a página de login

#MYSQL login-=-=-=-=-=--=-=-=-=-=-==-=-==-=-==-=-=-==-==-=-=-==-=-==-=-==-=-==-=-==-==-=-==-==-=-==-=-=-=-=
#MUDAR DEPOS
'''
@app.route("/login_help", methods=["POST"])
def login_help():
    nome_completo = request.form.get('nome_completo')
    nome_apelido = request.form.get('nome_apelido')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    senha = request.form.get('senha')
    cep = request.form.get('cep')

    #Comando novos
    conectar_mysql = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='') #se for de algum sevidor, colocar o caminho, database='Nome Do DB', depois passar o USUARIO e SENHAS do SQL
    if conectar_mysql.is_connected():
        cursor = conectar_mysql.cursor() # onde a linha está selecionado, para digitar o codigo
        cursor.execute('select * from usuario;') #codigo do SQL que deseja executar

        usuariosDB = cursor.fetchall #Selecionar todos os arquivos/dados do (cursor), e listar eles e salvar

    
    #Velhos
    for usuario in usuariosDB:
        
        #novos - para SQL!
        usuarioNome = str(usuario[1]) # pegar a 2º coluna do DB, por que a lista começa no 0, 0 = id, 1 = nome
        usuarioSenha = str(usuario[2])

        #modificar exemplo para os nomes do DB e HTML e PYTHON!!!!!!
        if (
            usuarioNome == nome_completo and
            usuarioSenha == senha
        ):
            global logado
            logado = True
            return render_template("help_home.html")

    flash('Esse usuário não existe! Verifique os dados e tente novamente.')
    return redirect("/")
'''
# CADASTRO MYSQL -=-=-=-=-=--=--=-=-=-=-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==--=-=-==--=
# Rota para exibir a página de cadastro (GET)
'''
@app.route('/cadastro_help', methods=['GET'])
def cadastro_help_get():
    return render_template("cadastro_help.html")

# Rota para processar o formulário de cadastro (POST)
@app.route('/cadastro_help', methods=['POST'])
def cadastro_help_post():
    nome_completo = request.form.get('nome_completo')
    nome_apelido = request.form.get('nome_apelido')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    senha = request.form.get('senha')
    cep = request.form.get('cep')

    #novos
    conectar_mysql = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='') #se for de algum sevidor, colocar o caminho, database='Nome Do DB', depois passar o USUARIO e SENHAS do SQL
    if conectar_mysql.is_connected():
        cursor = conectar_mysql.cursor() # onde a linha está selecionado, para digitar o codigo
        cursor.execute(f"insert into usuario values (default, {nome_completo}, {nome_apelido}, {cpf}, {email}, {senha}, {cep});") #codigo do SQL que deseja executar
    if conectar_mysql.is_connected(): #Vamos agora desconectar as coisas
        cursor.close()
        conectar_mysql.close()


    #velhos
    flash('Usuário cadastrado com sucesso! Faça login.')
    return redirect("/")  # Volta para a página de login
'''
    


# Lembrar de sempre deixar no final!
'''
if __name__ in "__main__":
    app.run(debug=True)
'''
#testar online via chatgpt foi ele quem ensionou
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
