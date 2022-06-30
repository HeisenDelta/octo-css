import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('test_image.jpeg', 0)
edges = cv2.Canny(img, 50, 100)
formatted_edges = (img > 0).astype(int)

plt.imshow(edges, cmap = 'gray')
plt.xticks([])
plt.yticks([])

print(formatted_edges[0][:100])

plt.show()
