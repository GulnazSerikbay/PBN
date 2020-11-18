from cv2 import *
import numpy as np
from PIL import Image

img = cv2.imread("house.webp")
img2 = img.reshape((-1,3))
print(img2)
img2 = np.float32(img2)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

k = 8
attempts = 10
ret, label, center = cv2.kmeans(img2,k,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
center = np.uint8(center)

res = center[label.flatten()]
res2 = res.reshape((img.shape))
cv2.imwrite('images/segmented.jpg', res2)

from cv2 import cv2


frame_im.save("images/outputim.png")

img = cv2.imread("images/outputim.png")
clusimg = img.reshape((-1,3))
clusimg = np.float32(img)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

k = P
attempts = 100
ret, label, center = cv2.kmeans(clusimg,k,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
center = np.uint8(center)

clustered = center[label.flatten()]
clustered = clustered.reshape((img.shape))
cv2.imwrite('images/outputmario.jpg', clustered)

clustered = Image.open("images/outputmario.jpg")
clustered.show()