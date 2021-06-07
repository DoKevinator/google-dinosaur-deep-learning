# google-dinosaur-deep-learning
This is a project to learn how to use the NEAT genetic neural network to play the Google Chrome Dinosaur offline game. 

Main contributors:
- Kevin Do
- Jason Do

Original base dinosaur game: https://github.com/shivamshekhar/Chrome-T-Rex-Rush

We took this base game made for typical human play, and adapted it to work with the NEAT genetic machine learning algorithm. 
The AI is able to create a successful dinosaur within 50 generations of training, depending on how the mutations are seeded in the algorithm. It's able to run until failure due to the game speed being too fast for the dinosaur physics to keep up. 

This algorithm creates a bunch of dinosaurs that all compete against one another to be the strongest dino in the game (the one with the highest score). Survival of the fittest. Each generation carries it's traits from the previous generation's strongest dinos. Eventually, given enough generations, the dinosaurs will learn to play the game at superhuman levels. The NEAT algorithm simulates how evolution works in the real world. 

![screenshot](https://user-images.githubusercontent.com/4328910/120954102-46b49080-c703-11eb-8e96-4e4e86e1fe86.PNG)

![generation](https://user-images.githubusercontent.com/4328910/120954776-ca22b180-c704-11eb-8128-093952a8ae17.PNG)

In order to run this program, you will need:
- Python 3 or newer
- NEAT python
- pygame
- graphviz for python
- python pickle 

To run the base game that is playable by humans, run "python main.py".

To run the AI training model, run "python -u ai_model.py". The "-u" flag is used to print to console the generation and population information. Without the flag, the stdout is unflushed and there will be no console output. 

After training the AI, the model will generate a python pickle file containing the contents of the most "fit" neural network. This file is named "chad.p". This pickle file can be used an input to play the winning dinosaur against any randomized dino game. 


