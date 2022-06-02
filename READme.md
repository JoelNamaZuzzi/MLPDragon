# MLPDragon
Creation of a Dragon with Game of Life and MLP

Hello,

We are a team of 4, Joël Zuzzi, Dorian Bazoin, Corentin Ciret & Quentin Fert and this is our project for EvoCraft 2022.

The goal of our project is to generate a Dragon with multiple parameters in order to obtain the best possible Dragon.

In order to obtain it, we use 2 Algorithm: Genetic Algorithm and MLP in order to have neuro evolution.

Summary:
1. The Dragon
2. Genetic Algorithm
3. MLP
4. Conclusion
5. Requirements
6. Video Link

1. The Dragon

The Dragon has 8 parameters that can vary:
1. Tail Length
2. Neck Length
3. Pair of Legs Number
4. Legs Length
5. Spike Heigth
6. Mouth Length
7. Teeths numbers
8. Horns Length

We manually created the different parts of the dragon (made a model of legs and such in minecraft to generate the beast proceduraly from the results) individually 
in order to multiply and put them together easily.
These 8 parameters will vary 
with the Genetic Algorithm and MLP in order to assemble & show the best dragon.

2. Genetic Algorithm

Our Genetic Algorithm is composed of individuals, which has 2 parameters, a gene list and a fit (initialized at 0). The genes are our dragon parameters.
And a generation List that just contains each generation of individuals (40 each).
We then make evolute our population (initialized at 10).

For the selection we use the roulette wheel, and for the combine we use the cross combine and we mutate our population with a chance of 0.05.
And then we do a fitness, we look each gene and if it's > 0.5 fitness gains 1.

3. MLP

Thirdly, the MLP, we begin by creating a patern with 1 entry and the target value oftenly depends on other values (for example we don't want to have the neck longer than the legs).

Then after the creation of the pattern we run the MLP where we specify him 1 entry, 4 hidden neurons and 1 output.

Then we BackPropagate 1000 times for each parameters in order to have a result close to the target values.

And then we update the results (meaning making the values nicier) and decode it for using it in minecraft by taking the first decimal as a value. 

Then we create an individual with the final values that will be taken for the Minecraft Generation.

The minecraft Generation simply consist in taking the values in the order we want to generate the blocs in Minecraft.

4. Conclusion

The code generates dragons as you can see in our video, the project was for us a pretty good introduction to genetic development,with the genetic algorithm and mostly the mlp, for the neuron part. 
With more time we probably would have made a better selection, fitness and combination. 
But for a first project in this domain our team is pretty much satisfied.

5. Requirements

In order to run the project, you just need the two files provided in the GIT + the following libraries:
Random
Math
Numpy

6. Video Link

https://youtu.be/n_RAMJMa_HQ

