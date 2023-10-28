# Importar Flask y request 
from flask import Flask, redirect, render_template,request, url_for

# Crear la aplicación
app = Flask(__name__)

@app.route('/')
def index():    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5555)