import os
import cv2
import numpy as np
from . import config as c
from .imgutils import resize_cut
import random
import progressbar

# mosaic: Construct a mosaic version of the template image which
# 		  is specified by @template_image_path. The pieces used
# 		  for mosaic are specified by @inputs.
# 		  When @inputs is a MAT file, it's regarded as a file
# 		  storing the preprocessing results. Elsewise @inputs is
# 		  regarded as a directory that contains the original pi-
# 		  eces which are not preprocessed. @inputs can also be a
# 		  result dict of the preprocessing procedure.
# 		  If @output_path is specified, the mosaic result image
# 		  will be written into @output_path. The write-out image
# 		  format is determined by suffix of @output_path.
def mosaic(template_image_path, inputs, output_path=None):
	tplimg = cv2.imread(template_image_path, cv2.IMREAD_COLOR)
	if isinstance(inputs, dict):
		images = inputs
	elif os.path.isdir(inputs):
		from .preprocess import preprocess
		images = preprocess(inputs)
	elif inputs.isfile(inputs) and inputs.split(".")[-1].lower() == "mat":
		from scipy.io import loadmat
		images = loadmat(os.path.join(input_, "images.mat"))
	else:
		raise FileNotFoundError("%s doesn't exist or is not a directory" % inputs)
	colors = images["colors"]
	images = images["images"]
	nimgs = len(images)

	outputsize = c.outputsize
	tplheight, tplwidth = tplimg.shape[:2]
	hwr = tplheight / tplwidth
	tgtwidth = np.sqrt(outputsize / hwr)
	tgtheight = hwr * tgtwidth
	pieceheight, piecewidth = c.piecesize
	gridy, gridx = (int(np.round(tgtheight / pieceheight)), int(np.round(tgtwidth / piecewidth)))
	dstheight, dstwidth = (pieceheight * gridy, piecewidth * gridx)
	tplingrids = resize_cut(tplimg.astype(np.double), (gridy,gridx))
	dstimg = np.zeros([dstheight, dstwidth, 3], np.uint8)
	total = gridx * gridy
	cnt = 0

	prgbar = progressbar.ProgressBar(widgets=[
			"Mosaic:",
			progressbar.Percentage(),
			progressbar.Bar()
		] , max_value=total)
	for y in range(gridy):
		for x in range(gridx):
			dsttop = y * pieceheight
			dstbottom = dsttop + pieceheight
			dstleft = x * piecewidth
			dstright = dstleft + piecewidth
			pixel = tplingrids[y,x,:]
			distsqrs = np.sum(np.power(colors - pixel, 2), axis=1)
			itopn = np.argsort(distsqrs)[:c.randomn]
			isel = random.choice(itopn)
			dstimg[dsttop:dstbottom, dstleft:dstright, :] = images[isel,:,:,:]
			cnt += 1
			prgbar.update(cnt)
	prgbar.finish()

	if output_path is not None:
		cv2.imwrite(output_path, dstimg)

	return dstimg
