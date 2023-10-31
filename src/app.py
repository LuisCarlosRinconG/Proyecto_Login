from flask import Flask, redirect, render_template, request, url_for
from config import *
from programa import Programa


con_bd = Conexion()

app = Flask(__name__)

@app.route('/admin')
def admin():
    programas = con_bd['Programas']
    ProgramasRegistrados=programas.find()
    return render_template('admin.html', programas = ProgramasRegistrados)

@app.route('/')
def index():
    programas = con_bd['Programas']
    ProgramasRegistrados=programas.find()
    return render_template('index.html', programas = ProgramasRegistrados)
    
@app.route('/login')
def login():
    return render_template('login.html')




@app.route('/guardar_programas', methods = ['POST'])
def agregarPrograma():
    programas = con_bd['Programas']
    nombre = request.form['nombre']
    titulo = request.form['titulo']
    nivelF= request.form['nivelF']
    metodologia = request.form['metodologia']
    creditos = request.form['creditos']
    duracionE = request.form['duracionE']
    mision = request.form['mision']
    vision = request.form['vision']

    if nombre and titulo and nivelF and metodologia and creditos and duracionE and mision and vision:
        programa = Programa(nombre, titulo, nivelF, metodologia, creditos, duracionE, mision, vision)
        #insert_one para crear un documento en Mongo
        programas.insert_one(programa.formato_doc())
        return redirect(url_for('admin'))
    else:
        return "Error"
    

@app.route('/eliminar_programa/<string:nombre_programa>')
def eliminar(nombre_programa):
    programas = con_bd['Programas']
    programas.delete_one({ 'nombre': nombre_programa})
    return redirect(url_for('admin'))

#Editar o actualizar el contenido 
@app.route('/editar_programa/<string:nombre_programa>', methods = ['POST'])
def editar(nombre_programa):
    programas = con_bd['Programas']
    nombre = request.form['nombre']
    titulo = request.form['titulo']
    nivelF= request.form['nivelF']
    metodologia = request.form['metodologia']
    creditos = request.form['creditos']
    duracionE = request.form['duracionE']
    mision = request.form['mision']
    vision = request.form['vision']
    if nombre and titulo and nivelF and metodologia and creditos and duracionE and mision and vision:
        programas.update_one({'nombre': nombre_programa}, 
                            {'$set': {'nombre' : nombre , 'titulo': titulo, 'nivelF': nivelF, 'metodologia': metodologia, 'creditos': creditos, 'duracionE': duracionE, 'mision': mision, 'vision': vision}}) # update_one() necesita de al menos dos parametros para funcionar
        return redirect(url_for('admin'))
    else:
        return "Error de actualización"


if __name__ == '__main__':
    app.run(debug = True, port = 2001)