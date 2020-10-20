from scipy.spatial import distance

from architectures import architectures

def get_closer_architecture(vector):
    # (0,0,0,0,0,0,0)
    min_d = 100000000 # max_value
    min_arch = None

    for arch in architectures:
        d = distance.euclidean(vector, arch.vector)
        if d < min_d:
            min_d = d
            min_arch = arch

    return arch

if __name__=="__main__":
    print(get_closer_architecture((1,0,0,0,1,1,1)).name)