import requests
import configparser
import socket
from lib import(
    util
)

class Server:

	def __init__(self, inifile:configparser.ConfigParser) -> None:
		self.gip = self.get_gip_addr()
		self.host_port = inifile.getint("connection","buffer")


	def get_gip_addr():
		res = requests.get('https://ifconfig.me')
		return res.text
	