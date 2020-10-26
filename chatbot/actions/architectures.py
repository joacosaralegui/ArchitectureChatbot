from scipy.spatial import distance
from actions import analysis

req_index = {
    'availability':0,
    'fault_tolerance':1,
    'maintainability':2,
    'performance':3,
    'scalability':4,
    'security':5,
    'usability':6,
    'portability':7,
    'interoperability':8   
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
       return analysis.analyze(self.vector,other_vector)        


#disponibilidad tolerancia a fallos mantenibilidad performance escalabilidad seguridad usabilidad 
architectures = []
architectures.append(Architecture("Layers",(0,1,-1,-1,1,0,1,1,0)))
architectures.append(Architecture("Broker",(0,0,0,-1,1,0,1,1,1)))
architectures.append(Architecture("Model-View-Controller",(0,0,1,-1,-1,0,1,-1,0)))
architectures.append(Architecture("Client-Server",(0,0,1,-1,-1,-1,0,1,0)))
architectures.append(Architecture("Pipes and filters",(0,0,1,1,0,1,-1,0,-1)))
architectures.append(Architecture("Peer to Peer",(1,0,0,-1,1,-1,0,1,1)))