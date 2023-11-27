from flask import Flask, render_template, redirect, url_for, request, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "djfljdfljfnkjsfhjfshjkfjfjfhjdhfdjhdfu"

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    database="crud-flask",
    password="root",
)

cursor = conexao.cursor()

class Usuario:
    def __init__(self, id, nome, contacto, endereco, email):
        self.id = id
        self.nome = nome
        self.contacto = contacto
        self.endereco = endereco
        self.email = email

@app.route('/')
def index():
    query = "SELECT * FROM usuarios"
    cursor.execute(query)
    dados_usuarios = [Usuario(*row) for row in cursor.fetchall()]
    return render_template('index.html', data=dados_usuarios)

@app.route('/create', methods=['GET', 'POST'])
def create_data():
    if request.method == 'POST':
        nome = request.form['nome']
        contacto = request.form['contacto']
        endereco = request.form['endereco']
        email = request.form['email']

        query = "INSERT INTO usuarios (nome, contacto, endereco, email) VALUES (%s, %s, %s, %s)"
        values = (nome, contacto, endereco, email)

        cursor.execute(query, values)
        conexao.commit()

        flash("Usuário cadastrado com sucesso!")

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/update/<int:id>')
def edit_data(id):
    query = "SELECT * FROM usuarios WHERE id = %s"
    cursor.execute(query, (id,))
    dados_usuario = Usuario(*cursor.fetchone())
    return render_template('update.html', data=dados_usuario)

@app.route('/process_update', methods=['POST'])
def process_update():
    id = request.form.get('id')
    nome = request.form['nome']
    contacto = request.form['contacto']
    endereco = request.form['endereco']
    email = request.form['email']

    query = "UPDATE usuarios SET nome = %s, contacto = %s, endereco = %s, email = %s WHERE id = %s"
    values = (nome, contacto, endereco, email, id)

    cursor.execute(query, values)
    conexao.commit()

    flash('Usuário actualizado com sucesso!')

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    query = "DELETE FROM usuarios WHERE id = %s"
    cursor.execute(query, (id,))
    conexao.commit()

    flash('Usuário eliminado com sucesso!')

    return redirect(url_for('index'))

if __name__ == '__main__':


    app.run(debug=True)

