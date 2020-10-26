req_name = {
    0:'Disponibilidad',
    1:'Tolerancia a fallos',
    2:'Mantenibilidad',
    3:'Rendimiento',
    4:'Escalabilidad',
    5:'Seguridad',
    6:'Usabilidad',
    7:'Portabilidad',
    8:'Interoperabilidad'
}


class Analysis:
    def __init__(self, name, description, comparison):
        self.name = name
        self.description = description
        self.comparison = comparison
    
    def __str__(self):    
        return  name
    
    def compare(self, vector1, vector2):
        found = []
        for i in range(len(vector1)):
            if self.comparison(vector1[i],vector2[i]):
                found.append(i)
        
        text = ""
        if len(found) > 0:
            text += self.name + " (" + self.description + "):\n"
            for i in found: 
                text += "-" + req_name[i] + "\n"
        
        return text


# its important for both
def f1(a,b):
    return a == 1 and b == 1

# its important for b, a ignores
def f2(a,b):
    return a == 0 and b == 1

# its important for b, a attacks
def f3(a,b):
    return a == -1 and b == 1

# its not important for b, a improves
def f4(a,b):
    return a == 1 and b == 0

all_analysis = [
    Analysis("Coincidencias","la arquitectura esta alineada con las necesidades de tu proyecto en estos requerimientos",f1),
    Analysis("Pendientes","la arquitectura no mejora estos requerimientos que son importantes para tu proyecto",f2),
    Analysis("Desventajas","la arquitectura va en contra de estos requerimientos, que son importantes para tu proyecto",f3),
    Analysis("Extras","a pesar de que no son tan importantes para tu proyecto, la arquitectura provee benenficios en los siguientes requerimientos",f4)
] 

# given two vectors, return all analyisis and info between
def analyze(vector1, vector2):
    text = ""
    for analysis in all_analysis:
        text += analysis.compare(vector1, vector2)
     
    return text