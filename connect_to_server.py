import lib
from lib.connection import TCPClient,SSHServer

def get_bind_port(inifile) -> map:
	parser = SSHServer(inifile=inifile,name=inifile.get("agent","name1"))
	parser.set_ssh_toolkit()
	parser.set_ssh_config()

	return parser

if __name__ == "__main__":
	config_path = "./res/config.ini"
	inifile = lib.util.check_config(config_path=config_path)
	inifile.read(config_path,"UTF-8")
	client = TCPClient(inifile=inifile)

	parser = get_bind_port(inifile=inifile)
	port_list = []

	for remote_foward in parser.config["remoteforward"]:
		parts = remote_foward.split()
		remote_port = parts[0]
		port_list.append(remote_port)
	
	client.connect()

	client.send(" ".join(port_list))

	client.close()