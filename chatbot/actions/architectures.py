req_index = {
    'availability':0,
    'fault_tolerance':1,
    'maintainability':2,
    'performance':3,
    'scalability':4,
    'security':5,
    'usability':6
}

class Architecture:
    def __init__(self, name, vector):
        self.name = name
        self.vector = vector

#disponibilidad tolerancia a fallos mantenibilidad performance escalabilidad seguridad usabilidad 
architectures = []
architectures.append(Architecture("Layers",(0,1,-1,-1,1,0,1)))
architectures.append(Architecture("Broker",(0,0,0,-1,1,0,1)))
architectures.append(Architecture("Model-View-Controler",(0,0,1,-1,-1,0,1)))
architectures.append(Architecture("Cliente-Serivor",(0,0,1,-1,-1,-1,0)))
architectures.append(Architecture("Pipes and filters",(0,0,1,-1,0,0,0)))
architectures.append(Architecture("Peer to Peer",(1,0,0,0,0,-1,0)))
architectures.append(Architecture("Monolith",(-1,0,-1,1,0,1,-1)))
"""
architectures.append(Architecture("Layers",(0,1,0,0,1,0,1)))
architectures.append(Architecture("Broker",(0,0,0,0,1,0,1)))
architectures.append(Architecture("Model-View-Controler",(0,0,1,0,0,0,1)))
architectures.append(Architecture("Cliente-Servidor",(0,0,1,0,1,0,0)))
architectures.append(Architecture("Pipes and filters",(0,0,1,1,0,1,0)))
architectures.append(Architecture("Peer to Peer",(1,1,0,0,0,0,0)))
architectures.append(Architecture("Monolith",(0,0,0,1,0,1,0)))
"""
