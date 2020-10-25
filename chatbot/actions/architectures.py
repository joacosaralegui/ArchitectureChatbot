from scipy.spatial import distance

req_index = {
    'availability':0,
    'fault_tolerance':1,
    'maintainability':2,
    'performance':3,
    'scalability':4,
    'security':5,
    'usability':6,
    'portability':7,
    'interoperability':8,
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

class Architecture:
    def __init__(self, name, vector):
        self.name = name
        self.vector = vector

    def distance(self, other_vector):
        value = 0
        for i in range(len(self.vector)):
            if self.vector[i] == -1 and other_vector[i] == 0 or self.vector[i] == 0 and other_vector[i] == -1:
                continue
            else:
                value += abs(self.vector[i]-other_vector[i])
        return value
        #return distance.euclidean(self.vector, other_vector)

    def analysis(self, other_vector):
        text = ""
        pros = []
        cons = []
        for i in range(len(self.vector)):
            if self.vector[i] == -1 and other_vector[i] == 1:
                cons.append(i)
            elif self.vector[i] == 1 and other_vector[i] == 1:
                pros.append(i)
        
        if len(pros) > 0:
            text = "\nCoincidencias: (aquellos requerimientos que son importantes para tu proyecto y son fomentados por la arquitectura).\n" 
        else:
            text = "\nEsta arquitectura no presenta beneficios en relación a tus necesidades.\n" 
        for p in pros:
            text += "-" + req_index[p] + "\n"
        
        if len(cons) > 0:
            text += "\nDesventajas: (aquellos requerimientos que son importantes para tu proyecto y son perjudicados por esta arquitectura).\n" 
        else:
            text += "\nEsta arquitectura no presenta desventajas graves en relación a tus necesidades.\n" 
        for c in cons:
            text += "-" + req_index[c] + "\n"

        return text
        
#disponibilidad tolerancia a fallos mantenibilidad performance escalabilidad seguridad usabilidad 
architectures = []
architectures.append(Architecture("Layers",(0,1,-1,-1,1,0,1,1,0)))
architectures.append(Architecture("Broker",(0,0,0,-1,1,0,1,1,1)))
architectures.append(Architecture("Model-View-Controller",(0,0,1,-1,-1,0,1,-1,0)))
architectures.append(Architecture("Client-Server",(0,0,1,-1,-1,-1,0,1,0)))
architectures.append(Architecture("Pipes and filters",(0,0,1,1,0,1,-1,1,-1)))
architectures.append(Architecture("Peer to Peer",(1,0,0,-1,1,-1,0,1,1)))