import os
import config_utils

__conf_dict = config_utils.read_conf_opts(
		config_utils.read_conf_file(
			os.path.join(os.path.dirname(__file__), "config.conf")
		)
	)

acceptfmts = [x.strip() for x in __conf_dict["acceptfmts"].split(",")]
piecesize = tuple([int(x.strip()) for x in __conf_dict["piecesize"].split(",")])
outputsize = config_utils.parse_bytesize(__conf_dict["outputsize"])
randomn = int(__conf_dict["randomn"])
