import subprocess
import os
import json

with open("src/configs/cities.json", "r") as file:
    cities = json.load(file)

def midpoint(position, upper_bound=1.0, lower_bound=0.0):
    if lower_bound > upper_bound:
        raise ValueError("lower_bound must be less than upper_bound")
    else:
        return (lower_bound + upper_bound) / 2

for city in cities:
    try:
        print(f"City: {city['name']}, Position: {city['position']}")
    except KeyError:
        city['position'] = [0.5, 0.5]
        print(f"City: {city['name']}, Position: {city['position']}")

    game = subprocess.Popen(['python', 'src/game.py'])
    status = subprocess.Popen.poll(game)
    print(status)

    horizontal_change = input("Should the city move left or right? (l/r/n)")
    vertical_change = input("Should the city move up or down? (u/d/n)")

    horizontal_window = [0.0, 1.0]
    vertical_window = [0.0, 1.0]

    while horizontal_change != 'n' and vertical_change != 'n':
        if horizontal_change != 'n':
            if horizontal_change == "l":
                horizontal_window[1] = city['position'][0]
            elif horizontal_change == "r":
                horizontal_window[0] = city['position'][0]

            city['position'][0] = midpoint(horizontal_window[0], horizontal_window[1])


        if vertical_change != 'n':
            if vertical_change == "u":
                vertical_window[1] = city['position'][0]
            elif vertical_change == "d":
                vertical_window[0] = city['position'][0]

            city['position'][1] = midpoint(horizontal_window[0], horizontal_window[1])
            horizontal_change = input("Should the city move left or right? (l/r/n)")

        with open("src/configs/cities.json", "w") as file:
            json.dump(cities, file)

        subprocess.Popen.terminate(game)
        game = subprocess.Popen(['python', 'src/game.py'])

        horizontal_change = input("Should the city move left or right? (l/r/n)")
        vertical_change = input("Should the city move up or down? (u/d/n)")






