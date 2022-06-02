import grpc
import random

import minecraft_pb2_grpc
from minecraft_pb2 import *

material = ['STONE','GRASS','DIRT','COBBLESTONE','SNOW']

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

client.fillCube(FillCubeRequest(  # Clear a working area
    cube=Cube(
        min=Point(x=-30, y=0, z=-30),
        max=Point(x=30, y=3, z=30)
    ),
    type=GRASS
))


client.fillCube(FillCubeRequest(  # Clear a working area
    cube=Cube(
        min=Point(x=-10, y=0, z=-10),
        max=Point(x=10, y=3, z=10)
    ),
    type=QUARTZ_BLOCK
))

client.fillCube(FillCubeRequest(  # Clear a working area
    cube=Cube(
        min=Point(x=-15, y=4, z=-15),
        max=Point(x=15, y=15, z=15)
    ),
    type=AIR
))

def Fitness(l,y_m):
    #Détection Fitness
    tabfitness = [l]
    i=0
    for X in range(-8,8):
        for Z in range(-8,8):
            value =0
            for Y in range(4, y_m+2):
                block = client.readCube(Cube(
                    min=Point(x=X, y=Y - 1, z=Z),
                    max=Point(x=X, y=Y - 1, z=Z)
                ))
                if (block.blocks[0].type == 194):
                    tabfitness.append(value)
                    print("fitness de ", str(X), " ", str(Y-1), " ", str(Z), " = ", value, " type: ",block.blocks[0].type)
                value+=1
            value = 0

    for I in range(l-1):
        print(tabfitness[I]," ")


def Spawn():
    MaxX = random.randint(5,8)
    MaxY = random.randint(5,8)
    MinX = random.randint(-8,-5)
    MinY = random.randint(-8,-5)
    Up = 0
    Y_Max = random.randint(5,10)
    Jump = random.randint(2,3)
    Y_M = Y_Max

    for Y in range (4,Y_Max):
        RMaxY = MaxY - Up
        for X in reversed(range(MinX,MaxX)):
            for Z in range(MinY,RMaxY):
                random_block = random.choice(material)
                client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=X, y=Y, z=-Z),
                    max=Point(x=X, y=Y, z=-Z)
                    ),
                    type=STONE
                ))
            RMaxY = RMaxY -1
        Up = Up + Jump

    MaxX = random.randint(5,8)
    MaxY = random.randint(5,8)
    MinX = random.randint(-8,-5)
    MinY = random.randint(-8,-5)
    Up = 0
    Y_Max = random.randint(5,10)
    if(Y_M<Y_Max):
        Y_M=Y_Max
        
    Jump = random.randint(2,3)

    for Y in range (4,Y_Max):
        RMaxY = MaxY - Up
        for X in range(MinX,MaxX):
            for Z in range(MinY,RMaxY):
                random_block = random.choice(material)
                client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=X, y=Y, z=Z),
                    max=Point(x=X, y=Y, z=Z)
                    ),
                    type=STONE
                ))
            RMaxY = RMaxY -1
        Up = Up + Jump

    MaxIndividu = random.randint(10,15);

    for I in range(MaxIndividu):
        X_Rand = random.randint(-8,8)
        Z_Rand = random.randint(-8,8)
        client.fillCube(FillCubeRequest(
                cube=Cube(
                    min=Point(x=X_Rand, y=15, z=Z_Rand),
                    max=Point(x=X_Rand, y=15, z=Z_Rand)
                    ),
                    type=SAND
                ))
    Fitness(MaxIndividu,Y_M)

Spawn()
def Clear():
    
    for I in range(-11,11):
        for J in range(-11,11):
            client.fillCube(FillCubeRequest(
                    cube=Cube(
                        min=Point(x=I, y=4, z=J),
                        max=Point(x=I, y=4, z=J)
                        ),
                        type=AIR
                    ))


