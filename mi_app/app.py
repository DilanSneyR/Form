from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash'

# Crear la base de datos si no existe
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personas')
    registros = cursor.fetchall()
    conn.close()
    return render_template('index.html', registros=registros)

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO personas (nombre, correo) VALUES (?, ?)', (nombre, correo))
        conn.commit()
        conn.close()
        flash('¡Registro exitoso!')
        return redirect(url_for('formulario'))
    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)
