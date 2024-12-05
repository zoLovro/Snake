import pygame as pg
import pickle

# Save only the high score
def save_highscore(highscore, file_name):
    try:
        with open(file_name, 'wb') as file:
            pickle.dump(highscore, file)
            print("High score saved successfully!")
    except IOError:
        print("Error: Unable to save high score.")

# Load the high score
def load_highscore(file_name):
    try:
        with open(file_name, 'rb') as file:
            highscore = pickle.load(file)
            print("High score loaded successfully!")
            return highscore
    except (IOError, pickle.UnpicklingError):
        print("Error: Unable to load high score.")
        return 0
