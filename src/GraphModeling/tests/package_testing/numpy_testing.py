import numpy as np

def main():
    x = np.zeros((5,5))
    x[0][1] = 1
    x[0][3] = 1
    x[1][2] = 1
    x[1][3] = 1
    x[1][4] = 1
    x[2][4] = 1
    x[3][4] = 1
    print(x)
    print(get_arcs(x))
    
def get_arcs(x):
    xnz = np.nonzero(x)
    arcs = []
    for i in range(0,len(xnz[0])):
        arcs.append([xnz[0][i],xnz[1][i]])
    return arcs

def get_seq(n):
    return [*range(n)]

if __name__ == "__main__":
    main()