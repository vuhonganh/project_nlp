# f = 292.84
# c1 = 161.09
# c2 = 128.56
# w = 44  # cube size in mm
import numpy as np

def estim_z(f1, f2, w, h, wi, hi):
	return 0.5 * (f1 * w / wi + f2 * h / hi)

def estim_xy(u1, v1, u2, v2, c1, c2, f1, f2, z):
	xc = 0.5 * (u1 + u2 - 2 * c1) * z / f1
	yc = 0.5 * (v1 + v2 - 2 * c2) * z / f2
	return xc, yc


def estim_center(u1, v1, u2, v2, w, h, f1=292.84, f2=292.84, c1=161.09, c2=128.56):
	wi = u2 - u1
	hi = v2 - v1
	zc = estim_z(f1, f2, w, h, wi, hi)
	xc, yc = estim_xy(u1, v1, u2, v2, c1, c2, f1, f2, zc)
	return xc, yc, zc


w = h = 4.4  # in cm
with open('note.txt', 'r') as f:
	for line in f:
		line = line.strip('\n')
		img_name, u1, v1, u2, v2 = line.split(',')
		u1 = int(u1); v1 = int(v1); u2 = int(u2); v2 = int(v2)
		xc, yc, zc = estim_center(u1, v1, u2, v2, w, h)		
		dist = np.sqrt(xc * xc + yc * yc + zc * zc)
		print(img_name, xc, yc, zc, dist)