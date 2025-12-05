""""
# File Name: generator.py
# Project: Procedural Terrain Generation
# Author: Angel Castillo
# Date Last Modified: December 04, 2025
# Version: 1.0
# Description: This Python program is a basic terrain generator that uses Perlin noise to simluate 
the kind of terrain generation used in games such as Minecraft, but on a much smaller scale. 
The program is meant to showcase how certain methods of linear algebra are used to accomplish this. 
This program was written as a part of a project for the course MTH3130: "Applied Methods in 
Linear Algebra" at MSU Denver in the Fall semester of 2025.

Required Libraries:
- Random (Allows for the generation of random numbers)
- NumPy (Provides support for arrays, matrices, and essential mathematical operations)
- Matplotlib (A plotting library to provide a visual result of the code)
- Perlin-Noise (Provides tools for generating Perlin noise, an essential aspect of terrain generation)
"""
import random
import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

# ***** TERRAIN GENERATION FUNCTION *****
def generateTerrain(width, height, seed):
    world = np.zeros((height, width))   # Creating new world, a 250 x 250 zero matrix 
    
    # --- PARAMETERS ---
    octaves = 4          # Number of noise layers
    persistence = 0.5    # How much each octave contributes, affects amplitude
    lacunarity = 2.0     # How much detail each octave adds, affects frequency
    scale = 50.0         # Essentially how "zoomed in/out" the map is
    
    # --- GENERATING PERLIN NOISE ---
    noiseGenerator = []
    for i in range(octaves):
        # Each noise layer has increasing frequency and decreasing amplitude
        freq = lacunarity ** i
        amp = persistence ** i
        # This is the Perlin noise generator itself:
        noiseGenerator.append((PerlinNoise(octaves=1, seed=seed + i), freq, amp))
    
    # --- USING fBm TO COMBINE NOISE LAYERS ---
    for y in range(height):
        for x in range(width):
            fBmValue = 0.0
            for noiseLayer, freq, amp in noiseGenerator:
                fBmValue += amp * noiseLayer([x * (freq / scale), y * (freq / scale)])
            world[y][x] = fBmValue
    
    return world

# ***** MAIN EXECUTION *****
userInput = input("Enter seed or press Enter for random: ").strip()    #Ask user to input seed

if userInput == "":
    SEED = random.randint(0, 2**32 - 1)         #Generates a random 32-bit seed when user inputs nothing
else:
    try:
        SEED = int(userInput)                  #Takes a seed inputed by user, 32-bit values only
    except ValueError:
        SEED = abs(hash(userInput)) % (2**32)  #If user input was not 32-bits, converts it into 32-bits

print(f"Seed: {SEED}")  #Displays the user's seed

WIDTH, HEIGHT = 250, 250    # Dimensions of the world

terrain = generateTerrain(WIDTH, HEIGHT, SEED)     #Begins generation using seed

# ***** MIN-MAX NORMALIZATION *****
# Normalizes the generated terrain to fit our predefined bounds
normalizedTerrain = (terrain - terrain.min()) / (terrain.max() - terrain.min())

# ***** VISUALIZATION *****
# This creates the map for us to see
plt.figure(figsize=(10, 8))
plt.imshow(normalizedTerrain, cmap='terrain')
plt.colorbar(label='Elevation')
plt.title(f'Seed: {SEED}')
plt.tight_layout()
plt.show()

#END