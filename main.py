from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexao com o banco de dados
conn = sqlite3.connect('gestao_hospitalar.db')
cursor = conn.cursor()

# Criacao de tabela se nao existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pacientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        sexo TEXT,
        cpf TEXT UNIQUE,
        endereco TEXT,
        telefone TEXT              
    )
''')

conn.commit()  # Salvar
conn.close()  # Fechar

@app.route('/')
def index():
    conn = sqlite3.connect('gestao_hospitalar.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes')  # all
    pacientes = cursor.fetchall()
    conn.close()
    return render_template('index.html', pacientes=pacientes)

@app.route('/novo_paciente', methods=['GET', 'POST'])
def novo_paciente(): 
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        sexo = request.form['sexo']
        cpf = request.form['cpf']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        conn = sqlite3.connect('gestao_hospitalar.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pacientes (nome, idade, sexo, cpf, endereco, telefone)
            VALUES(?, ?, ?, ?, ?, ?)
        ''', (nome, idade, sexo, cpf, endereco, telefone))
        conn.commit()  # Salvar
        conn.close()  # Fechar
        return redirect(url_for('index'))
    return render_template('novo_paciente.html')

@app.route('/agendar/<int:paciente_id>', methods=['GET', 'POST'])
def agendar(paciente_id):
    if request.method == 'POST':
        data_hora = request.form['data_hora']
        descricao = request.form['descricao']
        conn.sqlite3.connect('gestao_hospitalar.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO consultas (paciente_id, data_hora, descricao)
            VALUES (?, ?, ?)
            ''', (paciente_id, data_hora, descricao))
        conn.commit() #salvar
        conn.close() #fechar
    return render_template('agendar.html')

@app.route('/limpar_paciente')
def limpar_paciente():
    conn = sqlite3.connect('gestao_hospitalar.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pacientes')
    conn.commit()  # Salvar
    conn.close()  # Fechar
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
