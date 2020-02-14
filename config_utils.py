import re

__conf_keys = [
	"acceptfmts",
	"piecesize",
	"outputsize",
	"randomn"
]

def read_conf_file(filepath, append_from={}):
	conf_dict = {}
	for k in append_from:
		conf_dict[k] = append_from[k]
	with open(filepath, "r") as file:
		lines = file.read().split("\n")
	for line in lines:
		line = re.sub(r"#.*$", "", line)
		line = line.split("=")
		if len(line) > 1:
			conf_dict[line[0].strip()] = "".join(line[1:]).strip()
	return conf_dict

def read_conf_opts(append_from={}):
	import sys
	conf_dict = {}
	for k in append_from:
		conf_dict[k] = append_from[k]
	# for match in re.finditer(r"--(\w+)\=(\S+)"):
	for phrase in sys.argv[1:]:
		match = re.match(r"^--(\w+)\=(.+)$", phrase)
		if match is not None:
			conf_dict[match.group(1)] = match.group(2).strip()
	return conf_dict

def parse_bytesize(readable_bytesize):
	if readable_bytesize[-1] in [str(x) for x in range(10)]:
		return int(readable_bytesize)
	unit = readable_bytesize[-1].upper()
	mult_dict = {
		"B": 1,
		"K": 1024,
		"M": 1024 * 1024,
		"G": 1024 * 1024 * 1024,
		"T": 1024 * 1024 * 1024 * 1024
	}
	return int(readable_bytesize[:-1]) * mult_dict[unit]
