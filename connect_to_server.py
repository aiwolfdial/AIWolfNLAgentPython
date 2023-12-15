import lib
from lib.connection import TCPClient

if __name__ == "__main__":
	config_path = "./res/config.ini"
	inifile = lib.util.check_config(config_path=config_path)
	inifile.read(config_path,"UTF-8")
	client = TCPClient(inifile=inifile)

	