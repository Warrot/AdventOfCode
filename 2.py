import re
from typing import List
import math

filepath = "/home/warrot/projects/advent_of_coding/data/2.txt"

Red, Green, Blue = int, int, int

def load_file(file):
    with open(file, 'r') as file:
        for line in file:
            yield line

def get_game_index(game):
    return int(re.findall(r"Game (\d*)", game)[0])

def parse_single_game(game):
    """
    Pare the raw game string and return the individual results as a list of lists in fixed RGB values
    """
    # Parse the cubes
    draws = game.split(': ')[-1]
    draws = draws.split('; ')
    for draw in draws:
        yield parse_single_drawing(draw)

def parse_single_drawing(draw) -> List:
    """
    Return the amount of cubes drawn in a drawing in the shape
    """
    blue = re.findall(r"(\d*) blue", draw)
    green = re.findall(r"(\d*) green", draw)
    red = re.findall(r"(\d*) red", draw)
    draw = map(lambda x: x[0] if x else '0', [red, green, blue])
    draw_content = [int(val) for val in draw]
    return draw_content


def run_2_1():
    """
    Determine is the game is valid based on a preset number of cubes available and a series of games
    where multiple cases of cubes are drawn
    """
    total = 0
    reference = [13, 14, 15]  # R G B
    for game in load_file(filepath):
        # Add index to total
        index = get_game_index(game)
        total += index
        game_content = parse_single_game(game)
        for draw in game_content:
            # Determine if the draw is valid
            res = [max(val[0] - val[1], 0) for val in zip(reference, draw)]
            if not all(res):
                total -= index
                break
    return total


def run_2_2():
    """
    Determine the fewest number of each color cube a given game could have been played with
    and calculate the power (r*b*g) of that game. Finally sum all the powers and return that value.
    """
    total = 0
    for game in load_file(filepath):
        # Add index to total
        game_content = parse_single_game(game)

        # Set default values for draw
        rgb = [0, 0, 0]
        for draw in game_content:
            # Use values from new draw if they are higher than existing values
            rgb = list(map(max, zip(rgb, draw)))
        
        # Calculate power
        total += math.prod(rgb)
    
    return total


def find_possible_games():
    """First iteration of problem 2_1"""
    # Set total
    total = 0
    # Set reference to be one higher than reported values
    reference = [13, 14, 15]  # R G B

    # Load and iterate over data
    for line in load_file(filepath):
        # Parse the cubes
        index = int(re.findall(r"Game (\d*)", line)[0])
        total += index
        games = line.split(': ')[-1]
        games = games.split('; ')
        for game in games:

            blue = re.findall(r"(\d*) blue", game) 
            green = re.findall(r"(\d*) green", game)
            red = re.findall(r"(\d*) red", game)
            game = map(lambda x: x[0] if x else '0', [red, green, blue])
            game = [int(val) for val in game]

            # Calculate if the game was possible
            res = [max(val[0] - val[1], 0) for val in zip(reference, game)]
            if not all(res):
                # print(f"{index=}, {blue=}, {green=}, {red=}")
                total -= index
                break
    return total

if __name__ == "__main__":
    print(run_2_2())
    

