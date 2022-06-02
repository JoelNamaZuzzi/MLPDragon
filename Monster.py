import grpc
import random
import math
import numpy as np

import minecraft_pb2_grpc
from minecraft_pb2 import *
# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x):
    return np.tanh(x)
 
# derivative of our sigmoid function
def dsigmoid(x):
    return 1.0 - x**2     
     
class MLP:
    def __init__(self, *args):
        self.args = args
        n = len(args)
         
        self.layers = [np.ones(args[i] + (i==0)) for i in range(0, n)]
         
        self.weights = list()
        for i in range(n-1):
            R = np.random.random((self.layers[i].size, self.layers[i+1].size))
            self.weights.append((2*R-1)*0.20)
             
        self.m = [0 for i in range(len(self.weights))]
                      
    def update(self, inputs):
        self.layers[0][:-1] = inputs
         
        for i in range(1, len(self.layers)):
            self.layers[i] = sigmoid(np.dot(self.layers[i-1], self.weights[i-1])) 
             
        return self.layers[-1]
         
    def backPropagate(self, inputs, outputs, a=0.1, m=0.1):
         
        error = outputs - self.update(inputs)
        de = error*dsigmoid(self.layers[-1])
        deltas = list()
        deltas.append(de)
         
         
        for i in range(len(self.layers)-2, 0, -1):
 
            deh = np.dot(deltas[-1], self.weights[i].T) * dsigmoid(self.layers[i])
            deltas.append(deh)
             
        deltas.reverse()
         
        for i, j in enumerate(self.weights):
             
            layer = np.atleast_2d(self.layers[i])
            delta = np.atleast_2d(deltas[i])
             
            dw = np.dot(layer.T,delta)
            self.weights[i] += a*dw + m*self.m[i]
            self.m[i] = dw

class Individu:
    #Begin Individu
    def __init__(self,gene):
        self.gene=gene
        self.fit = 0

    def getGene(self):
        return self.gene
    def getFit(self):
        return self.fit
    #End Individu

def Fitness(ind):
    #Begin Fitness
    for i in (ind.gene):
        if (i>0.5):
            ind.fit +=1
    #print(ind.fit)
    #End Fitness

def Recomb(ind, indd):
    #Begin recomb
    BreakComb = 3
    parM=ind.gene
    parP=indd.gene
    ChildGene = []
    lenGeno=len(parM)
    for i in range(BreakComb):
        ChildGene.append(parM[i])
    #print("3 first ", ChildGene)
    for i in range (BreakComb, lenGeno):
        ChildGene.append(parP[i])
    #print("Child: ", ChildGene)
    Child = Individu(ChildGene)
    return Child
    #End recomb

def mutate(ind, mutationchance):
    newind=Individu(ind.gene)
    for gene in (ind.gene):
        actual = random.random()
        if actual < mutationchance:
            print ("mutate")
            if gene == 1 :
                gene = 0
            else :
                gene = 1
    return newind

def mutatePopulation (pop, mutationchance):
    newPop = []

    for ind in pop:
        newPop.append(mutate(ind, mutationchance))

    return newPop

def roulletteBiese(pop):
    pool = []
    selection = []

    for i in range(0, len(pop)):
        for y in range(pop[i].getFit()+1):
            pool.append(pop[i])

    for i in range(initnumber):
        s = random.randint(0,len(pool)-1)
        selection.append(pool.pop(s))

    return selection       

Generation = []
Pop = []
#individu number
initnumber = 40
#Genes number: 1: long. Queue, 2: Long. Cou, 3: Nb Pattes, 4: Long. Pattes, 5: Hauteur Piques dos, 6: Long. bouche, 7: Nb Dents, 8: Long. cornes
genenumber=8
#Generation Number
maxG=10
#Generation counter
g=0
#nb a garder par gen
nbBest = 10
for i in range (0, initnumber):
    ind=Individu([])
    for j in range (0,genenumber):
        ind.gene.append(random.random())

    #print(ind.gene)
    Pop.append(ind)
#print(Pop)
    
for i in Pop:
    Fitness(i)
    #print(i.fit)
#print(Pop[0].fit)
Generation.append(Pop)
#Access Individu gene and fit
#print(Generation[0][0].gene)
#print(Generation[0][0].fit)
#print(g)
while(g<maxG):
    g+=1
    Pop=Generation[g-1]
    NewPop=[]
    #print(Pop)

    select =  roulletteBiese(Pop)
    #CrossCombine in order and reversed
    for i in range(0,len(Pop),2):
        NewPop.append(Recomb(Pop[i],Pop[i+1]))
        NewPop.append(Recomb(Pop[i+1],Pop[i]))
        #print(NewPop)
        
    Pop=NewPop

    #Mutation
    Pop = mutatePopulation(Pop, mutationchance=0.05)
    #Fitness of New Gen
    for i in Pop:
        Fitness(i)
    Generation.append(Pop)

ToMLP = Generation[maxG][0]
#print(ToMLP.gene[0])
#Genes number: 0: long. Queue, 1: Long. Cou, 2: Nb Pattes, 3: Long. Pattes, 4: Hauteur Piques dos, 5: Long. bouche, 6: Nb Dents, 7: Long. cornes

pat = (((ToMLP.gene[0]), random.uniform(0.5, 1)),
       ((ToMLP.gene[1]), random.uniform(0.1, ToMLP.gene[0])),
       ((ToMLP.gene[2]), random.uniform(ToMLP.gene[0], 1)),
       ((ToMLP.gene[3]), random.uniform(ToMLP.gene[1], ToMLP.gene[0])),
       ((ToMLP.gene[4]), random.uniform(0.1, ToMLP.gene[0]/2.0)),
       ((ToMLP.gene[5]), random.uniform(0.1, ToMLP.gene[0])),
       ((ToMLP.gene[6]), random.uniform(0.1, ToMLP.gene[5])),
       ((ToMLP.gene[7]), random.uniform(0.1, ToMLP.gene[5])))

 
n = MLP(1, 4, 1)

for i in range(1000):
    for p in pat:
        n.backPropagate(p[0], p[1])
        
#decoding for minecraft
ForFinal = []
for p in pat:
    print (n.update(p[0]))
    ForFinal.append(n.update(p[0]))
   
#print(ForFinal[0][0])
ind=Individu([math.floor(ForFinal[0]*10), math.floor(ForFinal[1]*10), math.floor(ForFinal[2]*10), math.floor(ForFinal[3]*10), math.floor(ForFinal[4]*10), math.floor(ForFinal[5]*10), math.floor(ForFinal[6]*10), math.floor(ForFinal[7]*10)])
print(ind.gene)


#############################################################

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

client.fillCube(FillCubeRequest(  # Clear a working area
    cube=Cube(
        min=Point(x=-10, y=0, z=-10),
        max=Point(x=10, y=3, z=10)
    ),
    type=QUARTZ_BLOCK
))




client.fillCube(FillCubeRequest(  # Clear a working area
    cube=Cube(
        min=Point(x=-100, y=0, z=-100),
        max=Point(x=100, y=200, z=100)
    ),
    type=AIR
))

client.fillCube(FillCubeRequest(  # Clear a working area
    cube=Cube(
        min=Point(x=-100, y=0, z=-100),
        max=Point(x=100, y=3, z=100)
    ),
    type=154
))


def Horne(MaxH,X,Z):
    MaxL = ind.gene[7]
    
    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=1+X, y=MaxH, z=Z),
                    max=Point(x=1+X, y=MaxH+MaxL, z=Z+2)
                    ),
                    type=41
                ))

    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=1+X, y=MaxH+1+MaxL, z=Z+1),
                    max=Point(x=1+X, y=MaxH+1+MaxL, z=Z+1)
                    ),
                    type=41
                ))
    
    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=9+X, y=MaxH, z=Z),
                    max=Point(x=9+X, y=MaxH+MaxL, z=Z+2)
                    ),
                    type=41
                ))

    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=9+X, y=MaxH+1+MaxL, z=Z+1),
                    max=Point(x=9+X, y=MaxH+1+MaxL, z=Z+1)
                    ),
                    type=41
         ))

def Teeth(MaxH,X,Z):
    MaxTeeth = ind.gene[6]
    for i in range(MaxTeeth):
        client.fillCube(FillCubeRequest(
                    cube=Cube(
                        min=Point(x=X+i*2, y=MaxH+2, z=Z),
                        max=Point(x=X+i*2, y=MaxH+2, z=Z)
                        ),
                        type=250
                    ))
        client.fillCube(FillCubeRequest(
                    cube=Cube(
                        min=Point(x=X+i, y=MaxH+3, z=Z),
                        max=Point(x=X+i, y=MaxH+3, z=Z)
                        ),
                        type=250
                    ))
    
    
    
def Mouth(MaxH,X,Z):
    
    MaxL = ind.gene[6]

    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=1+X, y=MaxH, z=Z-MaxL-2),
                    max=Point(x=9+X, y=MaxH+1, z=Z-1)
                    ),
                    type=151
                ))

    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=1+X, y=MaxH+4, z=Z-MaxL-2),
                    max=Point(x=9+X, y=MaxH+5, z=Z-1)
                    ),
                    type=151
                ))
    Teeth(MaxH,X+1,Z-MaxL-2)

def Eyes(MaxH,X,Z):
    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=2+X, y=MaxH, z=Z),
                    max=Point(x=3+X, y=MaxH, z=Z)
                    ),
                    type=179
                ))
    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=2+X, y=MaxH+1, z=Z),
                    max=Point(x=2+X, y=MaxH+1, z=Z)
                    ),
                    type=179
                ))

    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=1+X, y=MaxH, z=Z),
                    max=Point(x=1+X, y=MaxH+1, z=Z)
                    ),
                    type=250
                ))

    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=3+X, y=MaxH+1, z=Z),
                    max=Point(x=3+X, y=MaxH+1, z=Z)
                    ),
                    type=250
                ))
    
    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=4+X, y=MaxH, z=Z),
                    max=Point(x=4+X, y=MaxH, z=Z)
                    ),
                    type=250
                ))
    ###############################################
    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=7+X, y=MaxH, z=Z),
                    max=Point(x=8+X, y=MaxH, z=Z)
                    ),
                    type=179
                ))

    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=8+X, y=MaxH+1, z=Z),
                    max=Point(x=8+X, y=MaxH+1, z=Z)
                    ),
                    type=179
                ))
    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=9+X, y=MaxH, z=Z),
                    max=Point(x=9+X, y=MaxH+1, z=Z)
                    ),
                    type=250
                ))
    
    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=7+X, y=MaxH+1, z=Z),
                    max=Point(x=7+X, y=MaxH+1, z=Z)
                    ),
                    type=250
                ))
    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=6+X, y=MaxH, z=Z),
                    max=Point(x=6+X, y=MaxH, z=Z)
                    ),
                    type=250
                ))

def Wings(MaxH,X,MaxWings):
    for mw in range(MaxWings):
        for nb in range(0,2):
            for i in range(0,2):
                for j in range(5,7):
                    client.fillCube(FillCubeRequest(
                        cube=Cube(
                            min=Point(x=4*nb+X, y=j+MaxH, z=i+8+mw*12),
                            max=Point(x=4*nb+X, y=j+MaxH, z=i+8+mw*12)
                            ),
                            type=151
                        ))
                    
            for k in range(0,10):
                client.fillCube(FillCubeRequest(
                        cube=Cube(
                            min=Point(x=4*nb+X, y=j+k+MaxH, z=k+8+mw*12),
                            max=Point(x=4*nb+X, y=j+k+MaxH, z=k+8+mw*12)
                            ),
                            type=151
                        ))
                
            client.fillCube(FillCubeRequest(
                        cube=Cube(
                            min=Point(x=4*nb+X, y=j+k+MaxH, z=k+1+8+mw*12),
                            max=Point(x=4*nb+X, y=j+k+MaxH, z=k+2+8+mw*12)
                            ),
                            type=151
                        ))
            
            client.fillCube(FillCubeRequest(
                        cube=Cube(
                            min=Point(x=4*nb+X, y=j+k-1+MaxH, z=k+3+8+mw*12),
                            max=Point(x=4*nb+X, y=j+k-1+MaxH, z=k+3+8+mw*12)
                            ),
                            type=151
                        ))

        for nb in range(0,2):
                    
            for k in range(1,9):
                for l in range(0,5):
                    client.fillCube(FillCubeRequest(
                            cube=Cube(
                                min=Point(x=4*nb+X, y=j+k-1+MaxH, z=k+l+8+mw*12),
                                max=Point(x=4*nb+X, y=j+k-1+MaxH, z=k+l+8+mw*12)
                                ),
                                type=250
                            ))
                
            client.fillCube(FillCubeRequest(
                        cube=Cube(
                            min=Point(x=4*nb+X, y=j+k+MaxH, z=k+1+8+mw*12),
                            max=Point(x=4*nb+X, y=j+k+MaxH, z=k+3+8+mw*12)
                            ),
                            type=250
                        ))
def Head(MaxH,X,Z):
    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=X, y=MaxH, z=Z),
                    max=Point(x=X+10, y=9+MaxH, z=Z+7)
                    ),
                    type=151
                ))
    Eyes(MaxH+6,X,Z)
    Mouth(MaxH,X,Z)
    Horne(MaxH+10,X,Z+3)

def Shell(MaxH,X,MaxShell):
    MaxHShell = ind.gene[5]
    for i in range(MaxShell):
        for j in range(2):
            client.fillCube(FillCubeRequest(
                        cube=Cube(
                            min=Point(x=X+j*2, y=MaxH, z=5+i*6),
                            max=Point(x=X+j*2, y=MaxH+1+MaxHShell, z=7+i*6)
                            ),
                            type=41
                        ))

            client.fillCube(FillCubeRequest(
                        cube=Cube(
                            min=Point(x=X+j*2, y=MaxH+2+MaxHShell, z=6+i*6),
                            max=Point(x=X+j*2, y=MaxH+2+MaxHShell, z=6+i*6)
                            ),
                            type=41
                      ))
    if(MaxShell==1):
        MaxWings = 1
    else:
        MaxWings = MaxShell/2
        
    Wings(MaxH-5,X-1,int(MaxWings))
def Tail(MaxH,X,Z):
    MaxLTail = ind.gene[0]
    
    client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=X-3, y=MaxH-1, z=Z),
                    max=Point(x=X-1, y=MaxH, z=Z+2+MaxLTail)
                    ),
                    type=151
              ))
def Neck(MaxH,X,Z):
    for i in range(ind.gene[1]):
        client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=X, y=MaxH+i*2, z=2-2*i),
                    max=Point(x=X+2, y=MaxH+2+i*2, z=4-2*i)
                    ),
                    type=151
              ))
    print(4-2*i)
    Head(MaxH+3+i*2,X-5,-3-2*i)
    
def Body(MaxH,X,Z):
    for i in range(ind.gene[1]):
        client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=X-4, y=MaxH-2, z=3),
                    max=Point(x=X, y=MaxH, z=Z)
                    ),
                    type=151
              ))
    
    if(ind.gene[1]>1):
        MaxShell = random.randint(1,ind.gene[3]*2)
        Shell(MaxH+1,X-3,MaxShell)
    Neck(MaxH,X-3,Z)
    
    Tail(MaxH,X,Z+1)

def Feet(MaxH,MaxFoot):

    for MF in range(MaxFoot):
        for NB in range(2):
            for nb in range(2):
                for k in range(1,3):
                    for l in range(4,6):
                        client.fillCube(FillCubeRequest(
                                    cube=Cube(
                                        min=Point(x=-15-nb*2-NB*8, y=l, z=k+MF*10),
                                        max=Point(x=-15-nb*2-NB*8, y=l, z=k+MF*10)
                                        ),
                                        type=250
                                    ))
                        k = k+1
                        
            client.fillCube(FillCubeRequest(
                    cube=Cube(
                         min=Point(x=-17-NB*8, y=4, z=3+MF*10),
                         max=Point(x=-15-NB*8, y=10+MaxH, z=4+MF*10)
                        ),
                        type=151
                ))
    Body(MaxH+10,-8-nb*2-NB*8,4+MF*10)
        
Feet(ind.gene[4],ind.gene[3])
