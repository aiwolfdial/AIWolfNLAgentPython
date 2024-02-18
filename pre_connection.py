import time
from sshtunnel import SSHTunnelForwarder
from lib import util
from lib.connection import SSHServer,TCPClient

if __name__ == "__main__":
	config_path = "./res/config.ini"
	inifile = util.check_config(config_path=config_path)
	inifile.read(config_path,"UTF-8")
	client = SSHServer(inifile=inifile,name=inifile.get("agent","name1"))
	config = client.read_ssh_config()

	port_list = []

	for remote_foward in config["remoteforward"]:
		parts = remote_foward.split()
		remote_port = parts[0]
		port_list.append(remote_port)

	server = SSHTunnelForwarder(
		config["hostname"],
		ssh_username=config["user"],
		local_bind_address=("localhost",10001),
		remote_bind_address=("localhost",10001),
		allow_agent=True,
	)

	server.start()
	
	try:
		client = TCPClient(inifile=inifile)
		client.connect()

		time.sleep(1)

		client.send(message=" ".join(port_list))
	except:
		print("ERROR")

	client.close()

	server.stop()
	server.close()