#Imports
import numpy as np

from architectures import architectures

def grounding(values,number):  
	# create numpy array   
	lst = np.asarray(values) 
	# fetch idx of value closest to "number"
	idx = (np.abs(lst - number)).argmin() 
	# return -1,0,1 instead of 0,1,2
	return idx - 1 


#Obtener un vector normalizado
def get_normalized_vector(vector):
	# normalized vector
	normalized_vector = []

	# obtengo el promedio, minimo y maximo
	average = np.average(vector)
	min_value = min(vector)
	max_value = max(vector)

	# Queremos que los valores tomen su valor de acuerdo a cual de estos tres estan mas cerca
	rounding_values = [min_value, average, max_value]

	# guardar el grouding
	for number in vector:
		normalized_vector.append(grounding(rounding_values, number))

	return normalized_vector 


def get_closer_architecture(vector):
	# calculate all distances for each arch
	distances = [(arch.distance(vector), arch) for arch in architectures]
	# sort by distance
	distances = sorted(distances, key=lambda x: x[0])
	
	print(distances)
	# last_d holds the distance value of the last architecture loaded, start with first value to ensure that is loaded
	last_d = distances[0][0]
	# if the distances between the architecture and the next is lower to this then they are close enough
	treshold = 1

	# Load all who are closer between than treshold
	archs = []
	for d, arch in distances:
		if abs(last_d-d) < treshold:
			archs.append(arch)
			last_d = d

	return archs

if __name__=="__main__":
	v = (0,0,1,0,5,0,4,0,3)
	v = get_normalized_vector(v)
	match=get_closer_architecture(v)
	for arch in match:
		print("Arquitectura sugerida: " + arch.name)
		print(arch.analysis(v))
		print("********************\n")
