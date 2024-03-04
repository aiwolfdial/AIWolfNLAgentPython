import multiprocessing
import configparser
import main
import lib

def execute_game(inifile:configparser.ConfigParser, name:str):

    while inifile.getboolean("connection","keep_connection"):

        # connect to server or listen client
        if inifile.getboolean("connection","ssh_flag"):
            sock = lib.connection.SSHServer(inifile=inifile, name=name)
        else:
            sock = lib.connection.TCPServer(inifile=inifile, name=name) if inifile.getboolean("connection","host_flag") else lib.connection.TCPClient(inifile=inifile)
        
        sock.connect()

        received = None

        for _ in range(inifile.getint("game","num")):
            received = main.main(sock=sock, inifile=inifile, received=received, name=name)
        
        sock.close()

if __name__ == "__main__":
    config_path = "./res/config.ini"
    
    inifile = lib.util.check_config(config_path=config_path)
    inifile.read(config_path,"UTF-8")

    agent_num = int(inifile.get("agent","num"))

    print("agent_num:" + str(agent_num))
        
    for i in range(agent_num):
        process = multiprocessing.Process(name="p" + str(i+1), target=execute_game, args=(inifile, inifile.get("agent","name" + str(i+1))))
        process.start()