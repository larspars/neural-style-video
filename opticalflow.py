import cv2
import numpy as np
import time
import argparse

def blend(img1, img2, alpha):
    if not isinstance(alpha, float):
    	alpha = np.dstack((alpha, alpha, alpha))
    return ((1-alpha)*img1) + (alpha*img2)


parser = argparse.ArgumentParser()
parser.add_argument('--input_1', type=str, required=True)
parser.add_argument('--input_1_styled', type=str, required=True)
parser.add_argument('--input_2', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--alpha', type=float, default=0.2)
parser.add_argument('--flowblend', type=bool, default=False)
args = parser.parse_args()

start = time.time()
img1       = cv2.imread(args.input_1, cv2.IMREAD_GRAYSCALE)
img1styled = cv2.imread(args.input_1_styled, cv2.IMREAD_COLOR)
img1styled = cv2.resize(img1styled, (img1.shape[1], img1.shape[0]))
img2       = cv2.imread(args.input_2, cv2.IMREAD_GRAYSCALE)
img2color  = cv2.imread(args.input_2, cv2.IMREAD_COLOR)

flow = cv2.calcOpticalFlowFarneback(img1, img2, 0.5, 3, 15, 3, 5, 1.2, 0)


ys = range(flow.shape[0])
xs = range(flow.shape[1])
mapping = flow.copy()
for y in ys:
    mapping[y, :, 0] = xs - flow[y, :, 0]
for x in xs:
    mapping[:, x, 1] = ys - flow[:, x, 1]
#dst[x,y] = src[mapping[x,y]], in other words
#mapping[x,y] gives the indexes in src from which to get pixel (x,y) in dst

alpha = args.alpha
if args.flowblend:
    indices = np.indices((img1.shape[1], img1.shape[0])).swapaxes(0,2)
 	#- find the amount of flow/movement into each pixel
 	#- clip to [0, 1]
 	#- scale to [0, alpha] 
    xymovements = indices - mapping
    movements = np.sqrt(np.sum(xymovements ** 2, axis = 2)) #pythagorean theorem
    movements = np.max(np.abs(xymovements), axis = 2) #pythagorean theorem
    cv2.imwrite('img1alpha.jpg', np.clip(movements, 0, 1) * 255)
    alpha = np.clip(movements, 0, 1) * alpha 

img1morphedstyled = cv2.remap(img1styled, mapping, None, cv2.INTER_CUBIC)

img2blend = blend(img2color, img1morphedstyled, alpha)

cv2.imwrite(args.output, img2blend)


dur = time.time() - start
print(dur)

