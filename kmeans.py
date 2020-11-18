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
