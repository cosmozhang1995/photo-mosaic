import os
import cv2
import numpy as np
from . import config as c
from .imgutils import resize_cut
import progressbar

# preprocess: Read the pieces in @srcdir, cut&resize them
# 			  into standard piece_size, and calculate some
# 			  properties for each piece.
# 			  If @output_path is specified, save the pre-
# 			  process results into @output_path as a MAT
# 			  file. (require scipy.io).
def preprocess(srcdir, output_path=None):
	filenames = os.listdir(srcdir)
	filenames = list(filter(lambda filename: filename.split(".")[-1].lower() in c.acceptfmts, filenames))
	nfiles = len(filenames)
	pieceheight, piecewidth = c.piecesize
	images = np.zeros((nfiles, pieceheight, piecewidth, 3), dtype=np.uint8)
	colors = np.zeros((nfiles, 3), dtype=np.double)
	prgbar = progressbar.ProgressBar(widgets=[
			"Preprocess:",
			progressbar.Percentage(),
			progressbar.Bar(),
			progressbar.Counter(format='%(value)d/%(max_value)d')
		] , max_value=nfiles)
	for i in range(nfiles):
		img = cv2.imread(os.path.join(srcdir, filenames[i]), cv2.IMREAD_COLOR).astype(np.uint8)
		img = resize_cut(img, c.piecesize)
		images[i,:,:,:] = img
		for j in range(3):
			colors[i,j] = np.mean(img[:,:,j])
		prgbar.update(i)
	prgbar.finish()
	images = {"images":images, "colors":colors, "filenames":filenames}
	if output_path is not None:
		from scipy.io import savemat
		savemat(os.path.join(c.datadir, "images.mat"), images)
	return images
