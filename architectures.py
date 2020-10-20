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

architectures = []
architectures.append(Architecture("Capas",(0,2,0,0,-1,0,1)))
architectures.append(Architecture("Broker",(1,1,1,0,2,3,0)))
architectures.append(Architecture("Server",(1,0,1,0,0,5,0)))
architectures.append(Architecture("Monolitico",(1,0,0,0,-1,2,1)))
architectures.append(Architecture("Pipes and filters",(1,1,0,5,0,0,0)))