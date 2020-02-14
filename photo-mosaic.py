import sys
from photomosaic.mosaic import mosaic
import getopt

opts, args = getopt.getopt(sys.argv[1:], "t:i:o:", ["template=", "input=", "output="])
for o,a in opts:
	if o in ("-t", "--template"):
		template_path = a
	elif o in ("-i", "--input"):
		input_path = a
	elif o in ("-o", "--output"):
		output_path = a

mosaic(template_path, input_path, output_path)
