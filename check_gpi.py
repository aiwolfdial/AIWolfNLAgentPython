import os
import paramiko

def read_config():
	config_file = os.path.expanduser('./res/ssh-config')
	ssh_config = paramiko.SSHConfig()
	ssh_config.parse(open(config_file, 'r'))
	return ssh_config.lookup("aiwolf")

if __name__ == "__main__":
	client = paramiko.SSHClient()

	agent = paramiko.Agent()
	agent_keys = agent.get_keys()

	if len(agent_keys) > 0:
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		config = read_config()
		print(config)
		client.connect(config["hostname"], username=config["user"], pkey=agent_keys[0])  # agent_keys[0] は最初の鍵を使用

		# コマンドの実行
		stdin, stdout, stderr = client.exec_command("ls /home")
		# コマンド実行結果を変数に格納
		cmd_result = ''
		cmd_err = ''
		for line in stdout:
			cmd_result += line

		for line in stderr:
			cmd_err += line

		# 実行結果を出力
		print(cmd_result)
		print("-------------")
		print(cmd_err)

		client.close()
	else:
		print("Not Found")