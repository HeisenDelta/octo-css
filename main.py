import os
import json
from tkinter.tix import IMAGE
import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image as im
import random


def image_to_vector(IMG_NAME, IMG_EXTENSION):

    img = cv2.imread(f'{IMG_NAME}.{IMG_EXTENSION}', 0)
    edges = cv2.Canny(img, 50, 100)
    formatted_edges = (img > 0).astype(int)

    plt.imshow(edges, cmap = 'gray')
    plt.xticks([])
    plt.yticks([])

    seed = random.randrange(1000, 9999)

    pixel_data = im.fromarray(edges)
    pixel_data.save(f'{IMG_NAME}_{seed}.bmp')

    # print(edges[0][:100], '\n', formatted_edges[0][:100])

    plt.show()

    return seed

def run_potrace(IMG_NAME, seed):

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    bmp_name = f'{IMG_NAME}_{seed}.bmp'

    if bmp_name not in files:
        # Error pillow did not generate a file

        print('No file to process exists')
        return

    # subprocess.Popen(['potrace ' + bmp_name, '-b geojson'])
    os.system(f'potrace {bmp_name} -b geojson')

def parse_json(IMG_NAME, seed):

    with open(f'{IMG_NAME}_{seed}.json', 'r') as fl:
        json_text = json.load(fl)

        for ucoord in json_text['features']:
            coords = ucoord['geometry']['coordinates'][0]

            for x in coords: plt.plot(x[0], x[1], 'o', markersize = 0.1)

        plt.show()


if __name__ == '__main__':

    IMG_NAME = 'test_image'
    IMG_EXTENSION = 'jpeg'

    seed = image_to_vector(IMG_NAME, IMG_EXTENSION)
    run_potrace(IMG_NAME, seed)
    parse_json(IMG_NAME, seed)
