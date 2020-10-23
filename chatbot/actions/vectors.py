#Imports
from scipy.spatial import distance
from sklearn.preprocessing import normalize
import numpy as np

from actions.architectures import architectures

#Obtener un vector normalizado
def get_normalized_vector(vector):
  data = vector
  data = normalize(data, axis=0, norm='max')
  return data
  
def get_closer_architecture(vector):
  v = np.array([vector])
  v = get_normalized_vector(v)
  
  # (0,0,0,0,0,0,0)
  min_d = 100000000 # max_value
  min_arch = None

  for arch in architectures:
    d = distance.euclidean(vector, arch.vector)
    if d < min_d:
      min_d = d
      min_arch = arch
  return min_arch

if __name__=="__main__":
  match=get_closer_architecture((0,0,14,0,-1,0,1))
  print(match.name)