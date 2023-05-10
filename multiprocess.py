import multiprocessing
import lib
import main

if __name__ == "__main__":
    config_path = "./res/config.ini"
    
    inifile = lib.util.check_config(config_path=config_path)
    inifile.read(config_path,"UTF-8")

    agent_num = int(inifile.get("agent","num"))

    print("agent_num:" + str(agent_num))

    for i in range(agent_num):
        process = multiprocessing.Process(name="p" + str(i+1), target=main.main, args=(config_path, inifile.get("agent","name" + str(i+1))))
        process.start()