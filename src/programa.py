class Programa:
    def __init__(self, nombre, titulo, nivelF,metodologia,creditos,duracionE,mision,vision):
        self.nombre = nombre
        self.titulo = titulo
        self.nivelF = nivelF
        self.metodologia = metodologia
        self.creditos = creditos
        self.duracionE = duracionE
        self.mision = mision
        self.vision = vision
    
    # Metodo para almacenar los documentos
    def formato_doc(self):
        return{
            'nombre': self.nombre,
            'titulo': self.titulo,
            'nivelF': self.nivelF,
            'metodologia': self.metodologia,
            'creditos': self.creditos,
            'duracionE': self.duracionE,
            'mision': self.mision,
            'vision': self.vision    
        }