from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Conexion
from programa import Programa

con_bd = Conexion()

app = Flask(__name__)

# Configuración de la clave secreta para sesiones
app.secret_key = 'tu_clave_secreta'

@app.route('/admin')
def admin():
    if 'email' in session:
        programas = con_bd['Programas']
        ProgramasRegistrados = programas.find()
        return render_template('admin.html', programas=ProgramasRegistrados)
    else:
        return redirect(url_for('login'))

@app.route('/')
def index():
    programas = con_bd['Programas']
    ProgramasRegistrados = programas.find()
    return render_template('index.html', programas=ProgramasRegistrados)

# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    usuarios = con_bd['Usuarios']
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Consulta la base de datos para verificar las credenciales
        user_data = usuarios.find_one({'email': email, 'password': password})

        if user_data:
            # Almacenar el nombre de usuario en la sesión
            session['email'] = email
            return redirect(url_for('admin'))
        else:
            flash('Credenciales incorrectas. Inténtelo de nuevo.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Eliminar el nombre de usuario de la sesión al cerrar sesión
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/guardar_programas', methods=['POST'])
def agregarPrograma():
    if 'email' in session:  # Verificar si el usuario está autenticado
        programas = con_bd['Programas']
        nombre = request.form['nombre']
        titulo = request.form['titulo']
        nivelF = request.form['nivelF']
        metodologia = request.form['metodologia']
        creditos = request.form['creditos']
        duracionE = request.form['duracionE']
        mision = request.form['mision']
        vision = request.form['vision']

        if nombre and titulo and nivelF and metodologia and creditos and duracionE and mision and vision:
            programa = Programa(nombre, titulo, nivelF, metodologia, creditos, duracionE, mision, vision)
            # insert_one para crear un documento en Mongo
            programas.insert_one(programa.formato_doc())
            return redirect(url_for('admin'))
        else:
            return "Error"
    else:
        return redirect(url_for('login'))
    

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