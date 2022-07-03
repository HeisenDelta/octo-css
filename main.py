from asyncio.windows_events import NULL
from inspect import _void
import os
import json
import numpy as np
import scipy.interpolate
import cv2
from matplotlib import pyplot as plt
from PIL import Image as im
import random


def image_to_vector(IMG_NAME: str, IMG_EXTENSION: str) -> int:

    img = cv2.imread(f'{IMG_NAME}.{IMG_EXTENSION}', 0)
    edges = cv2.Canny(img, 50, 100)

    plt.imshow(edges, cmap = 'gray')
    plt.xticks([])
    plt.yticks([])

    seed = random.randrange(1000, 9999)

    pixel_data = im.fromarray(edges)
    pixel_data.save(f'{IMG_NAME}_{seed}.bmp')

    plt.show()

    return seed

def run_potrace(IMG_NAME: str, seed: int):

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    bmp_name = f'{IMG_NAME}_{seed}.bmp'

    if bmp_name not in files:
        # Error pillow did not generate a file

        print('No file to process exists')
        return

    # subprocess.Popen(['potrace ' + bmp_name, '-b geojson'])
    os.system(f'potrace {bmp_name} -b geojson')

def parse_json(IMG_NAME: str, seed: int):

    with open(f'{IMG_NAME}_{seed}.json', 'r') as fl:
        json_text = json.load(fl)

        for ucoord in json_text['features']:
            coords = ucoord['geometry']['coordinates'][0]

            for idx in range(0, len(coords) - 3, 3):
                base_string = '<path d="'
                fin_string = '" stroke="white" stroke-width="1" fill="none" />'

                base_string += f'M {coords[idx][0]} {coords[idx][1]} S {coords[idx + 1][0]} {coords[idx + 1][1]} {coords[idx + 2][0]} {coords[idx + 2][1]}' + fin_string
                print(base_string)

            break

        plt.show()


if __name__ == '__main__':

    IMG_NAME = 'test_image'
    IMG_EXTENSION = 'jpeg'

    seed = image_to_vector(IMG_NAME, IMG_EXTENSION)
    run_potrace(IMG_NAME, seed)
    parse_json(IMG_NAME, seed)
