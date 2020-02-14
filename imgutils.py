import cv2
import numpy as np

def resize_cut(srcimg, dstsize):
	dstheight, dstwidth = dstsize
	img = srcimg
	imgheight, imgwidth = img.shape[:2]
	sc = max(dstheight/imgheight, dstwidth/imgwidth)
	imgsize = (int(np.ceil(imgheight*sc)), int(np.ceil(imgwidth*sc)))
	img = cv2.resize(img, (imgsize[1], imgsize[0]))
	imgheight, imgwidth = img.shape[:2]
	imgcut = (int((imgheight-dstheight)/2), int((imgwidth-dstwidth)/2))
	imgcuttop, imgcutleft = imgcut
	imgcutbottom, imgcutright = (imgcuttop + dstheight, imgcutleft + dstwidth)
	img = img[imgcuttop:imgcutbottom, imgcutleft:imgcutright, :]
	return img
