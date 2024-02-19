# AIWolfNLAgentPython
A sample python code of an AIWolf Contest's agent for Natural Language Division.
The server code is [AIWolfNLGameServer](https://github.com/aiwolfdial/AIWolfNLGameServer)

人狼知能大会自然言語部門向けのPythonサンプルエージェントコードと、エージェントをリモート待ち受け状態にするリモートラッパーのコードです。
人狼知能自然言語部門2024国内大会については https://sites.google.com/view/aiwolfdial2024jp に説明があります。先にお読みください。
対戦接続システムのコードは [AIWolfNLGameServer](https://github.com/aiwolfdial/AIWolfNLGameServer) です。
英語の説明の後に、同じ内容で日本語の説明があります。

# Overview
Starting this year, to address unexpected program execution errors and scheduling difficulties encountered in the past, we've decided to shift the tournament format. Instead of organizers providing a dedicated match server for participants to connect their own five agents, we're asking participants to host the match server themselves. Organizers will then connect to these servers remotely.
For specifics, participants will be required to establish an SSH connection with a Linux server provided by the organizers. Simultaneously, they'll set up a remote forward to host the match server, allowing the organizers to connect to it.

## Regarding Registration for Participation
Due to the requirement for participants to establish an SSH connection to the server provided by the organizers this year, we will need everyone's public keys. Therefore, when registering, please either attach your public key or include it in the body of the registration email.

Once registered, the organizers will provide the IP address and port number. Please write the provided details into the res/ssh-config file.

## About Setting Up the Environment
Here are the steps assuming the use of the venv as a virtual environment. The commands mentioned below are intended for the linux operating system. If participating in the game from a different environment, please configure the settings accordingly on your own

### The command that needs to be executed once after cloning
```
$ python3 -m venv venv	# Creating a virtual environment
$ . venv/bin/activate	# Activating the virtual environment
$ pip install -r res/requirements.txt	# Installing libraries
```

## Explanation of settings in `res/config.ini`
The settings are configured as follows by default, but please modify them according to your own needs.

### [connection]
`host_flag`: When set to true, it initiates the game server to listen for connections. When false, it connects to the game server. Set `host_flag = true` when expecting the provided game server to host.
`ssh_flag`: When true, it allows the program to initiate an SSH connection to the server provided by the organizers. When false, it uses a TCP connection as in the previous year's setup.
`buffer`: The buffer size used for sending and receiving data with the match server.

### [ssh-server]
`config_path`: Path to the file containing SSH connection settings. By default, it's set as `res/ssh-config`, but specifying the path based on the configuration written in the SSH config file is also acceptable.
`host_name`: Used to identify which settings from the file containing SSH connection configurations should be utilized. It should match the `Host` in the SSH config described later.
`ssh_agent_flag`: When set to true, it utilizes ssh-agent during SSH connections. This setting is primarily for those who have the program placed on a remote server or similar setups and want to establish an SSH connection to the match server from there. When false, ssh-agent isn't used. In this case, make sure to specify the path to the private key in the `IdentityFile` field in the subsequent SSH config. This setting is mainly for those wishing to connect to the match server from their local environment.

### [tcp-client]
`host`: This represents the connection method used until last year. Set it by default if the match server is to be accessed via SSH, as used in the `execute.sh` mentioned later. When `ssh_flag=false` and `host_flag=false`, it operates as a TCP client to connect to the match server.

### [game]
`num`: The number of consecutive games to be played.

### [agent]
`num`: The number of agents participating in the game.
`name*`: The name of the *th agent.

```
[connection]
host_flag = true
ssh_flag = true
buffer = 2048

[ssh-server]
config_path = ./res/ssh-config
host_name = aiwolf-server
ssh_agent_flag = true
timeout = 200

[tcp-client]
; local sever settings
host = localhost
port = 10001

[game]
num = 1

[agent]
num = 5
name1 = kanolab1
```

## Explanation of the settings in res/ssh-config.
Here, you'll describe SSH connection settings. Following the typical format for SSH config, please write it in `~/.ssh/config` rather than `res/ssh-config`. Alternatively, you can specify `config_path=~/.ssh/config` in `res/config.ini`

`Host`: connection name. Please set it the same as host_name in `res/config.ini`
`User`: username used for SSH connections. This will be provided by the organizer after registration.
`IdentityFile`:This is primarily used when `ssh_flag = false` in `res/config.ini`. It is the path to the private key
`RemoteForward [remote_port1] localhost:[local_port1]`: This is the configuration for remote forwarding to the server provided by the organizer. It forwards the [remote_port*] of the organizer's server and the [local_port*] of all participants. Each agent uses one port to communicate with the game server. Regarding remote_port*, please specify the port designated by the organizer after registration.
```
Host aiwolf-server
HostName [対戦サーバのipアドレス]
User [user name]
IdentityFile ~/.ssh/id_rsa
RemoteForward [remote_port1] localhost:[local_port1]
RemoteForward [remote_port2] localhost:[local_port2]
RemoteForward [remote_port3] localhost:[local_port3]
RemoteForward [remote_port4] localhost:[local_port4]
RemoteForward [remote_port5] localhost:[local_port5]
```

## Self-play metho
1. Configure `res/config.ini` as follows:
	```
	[connection]
	host_flag = true
	ssh_flag = false

	(...)
	
	[tcp-server]
	ip = localhost
	port1 = 50000		; The listening port of Agent[01].
	port2 = 50001		; The listening port of Agent[02].
	port3 = 50002		; The listening port of Agent[03].
	port4 = 50003		; The listening port of Agent[04].
	port5 = 50004		; The listening port of Agent[05].

	(...)

	[game]
	num = 2				; Number of consecutive game plays

	[agent]
	num = 5				; The number of agents.
	name1 = kanolab1	; The name of Agent[01].
	name2 = kanolab2	; The name of Agent[02].
	name3 = kanolab3	; The name of Agent[03].
	name4 = kanolab4	; The name of Agent[04].
	name5 = kanolab5	; The name of Agent[05].
	```
1. Execute the program with the following command.
	```
	$ python3 multiprocess.py
	```
1. Launch the battle program.\
	The battle program is set up for [AIWolfNLGameServer](https://github.com/aiwolfdial/AIWolfNLGameServer).
## How to confirm execution
Here, we'll explain how participants can verify if their systems are set up to host the match server.**In the future, due to potential changes related to logs and other aspects, please check this section frequently for any updates.**

### For those connecting from locations where the private key is not directly stored, such as remote servers.
"In this case, the connection method involves using ssh-agent. First, execute the following command in your local environment. Replace [private_key] with the corresponding private key for the public key provided during registration.
```
$ eval `ssh-agent`
$ ssh-add ~/.ssh/[private_key]
```

Next, please access your own remote server or similar by adding the -A option as follows
```
$ ssh -A [host name]
```

The rest will be the same as `for those 'connecting to the match server from their local environment`.

### For those connecting to the match server from their local environmen

1. Please configure the settings in `res/config.ini`
1. Please configure the settings in `res/ssh-config`.
1. Finally, please execute the following command.
```
$ sh execute.sh
```


# 概要
このリポジトリにはエージェントのサンプルPython実装と、エージェントを運営側の固定IPを用いてリモート待ち受け状態にするコードが含まれています。
エージェントは各自のサーバ・マシンで実行いただきます。そのため、エージェントの実装詳細は実装言語を含め、自由です。

対戦の際は、5体のエージェントを固定IP/ポートにてリモート待ち受け状態にし、対戦接続システムを実行することでリモート対戦を行います。
固定IP/ポートをご自身で用意できる方は自前でテストいただくこともできますが、予選提出の際は必ず下記の公式運営サーバに登録し公式運営サーバ経由で実行、ログの保存をしてください。
その際は、運営が提供するLinuxサーバにSSH接続をしたうえでリモートフォワードし、ご自身のエージェントの固定IP待ち受けを実現します。
つまり、参加者はインターネット（SSH)接続可能な任意のマシンで、このリポジトリのコードを実行すればよいことになります。

※2023年までは主催者が提供する対戦サーバに自身のエージェント5体を接続して頂くことで対戦を自動実行していましたが、予期せぬプログラムの実行エラーや日程調整の兼ね合いが困難なことなどを鑑み、本年度からは参加者の方々に対戦サーバの待ち受けをして頂き主催者がそこに接続をする形で開催することに致しました。

## サンプルエージェントコード
`全エージェント共通`の動作には`player/agent.py` が呼び出されますので、`talk`,`vote`関数をカスタマイズしてお使いください。

`村人専用`の動作には`player/agent.py`を継承した`player/villager.py`が呼び出されますので、`talk`,`vote`関数をカスタマイズしてお使いください。

`占い師専用`の動作には`player/agent.py`を継承した`player/seer.py`が呼び出されますので、`divine`関数や`talk`,`vote`関数をカスタマイズしてお使いください。

`狂人専用`の動作には`player/agent.py`を継承した`player/possessed.py`が呼び出されますので、`talk`,`vote`関数をカスタマイズしてお使いください。

`人狼専用`の動作には`player/agent.py`を継承した`player/werewolf.py`が呼び出されますので、`attack`関数や`talk`,`vote`関数をカスタマイズしてお使いください。

## 参加登録について
公式運営サーバにssh接続するため、参加登録の際には公開鍵を添付してください。
登録後、主催者からユーザ名、固定IPとポート番号を通知しますので、提供された内容を`res/ssh-config`に記述してください

## 環境構築について
本プログラムを使用し、仮想環境として`venv`を使用する想定で手順を記載します。また、後述するコマンドを実行するosは`linux`を想定しています。
別の環境でゲームに参加する場合はご自身で適切な設定を行ってください。

### clone後1度実行して頂く必要のあるコマンド
```
$ python3 -m venv venv	# 仮想環境の作成
$ . venv/bin/activate	# 仮想環境の有効化
$ pip install -r res/requirements.txt	# ライブラリのインストール
```

## res/config.iniの設定の説明
デフォルトで以下の説明のように設定されていますが、ご自身の用途に合わせて設定を変更してください。

### [connection]
※過去のシステムとの互換性設定のため、変更の必要はありません。
`host_flag`: trueの場合に対戦接続の待ち受けを行います。 falseの場合はゲームサーバへの接続を行います。運営が提供する対戦接続システムの待ち受けを行う際は `host_flag = true`にして下さい。

`ssh_flag`: trueの場合に運営が提供するサーバへSSH接続をプログラムから行います。 falseの場合はSSH接続ではなく2023年以前のようにTCPコネクションを行います。

`buffer`: 対戦サーバとの送受信の際に利用されるバッファサイズです。

### [ssh-server]
`config_path`:後述するSSH接続の設定を書いたファイルのパスです。\
デフォルトでは`res/ssh-config`となっていますが、sshのconfigに書かれた方はそのパスを指定されても問題ありません。

`host_name`:SSH接続の設定を書いたファイルからどのホストに対する設定を使用するか識別する際に使用します。\
後述する`res/ssh-config`の`Host`と同じであれば問題ありません。

`ssh_agent_flag`:\
`false`(デフォルト):場合はssh-agentを使用しません。主にローカル環境等、プログラムを実行する環境で`秘密鍵が~/.ssh/等に置いてある方向け`です。後述する`res/ssh-config`で`IdentityFile`にご自身の秘密鍵のパスを書くようにしてください。ローカル環境から直接主催者が提供するサーバへSSH接続を行いたい方向けの設定です。\
`true`:ssh-agentを使用します。主に、ローカル環境からではなくご自身のリモートサーバ等にプログラムがおいてあるため、プログラムを実行する環境で`秘密鍵を~/.ssh/等に置けない環境の方向け`です。一度ローカルからご自身のリモートサーバへ接続し、そこからさらに主催者が提供するサーバへSSH接続を行いたい方向けの設定です。\
[踏み台サーバを経由する等、秘密鍵を参照することができない場所から接続を行う方向け](#踏み台サーバを経由する等、秘密鍵を参照することができない場所から接続を行う方向け)を参考にご自身のリモートサーバ等に接続し、プログラムを実行してください。こちらの場合は`res/ssh-config`で`IdentityFile`に**パスを記述せず**プログラムを実行してください。

### [tcp-client]
※過去のシステムとの互換性設定のため、変更の必要はありません。

`host`:2023年までの接続方式です。後述する`execute.sh`で使用しているため対戦サーバにSSHで接続される場合はデフォルトで設定をしてください。 

`ssh_flag=false`かつ`host_flag=false`の時に対戦サーバに接続するTCPクライアントとして動作します。

### [game]
`num`:連続で行うゲームの回数です。

### [agent]
`num`:ゲームに参加するエージェントの人数です。
`name*`:*番目のエージェントの名前です。

```
[connection]
host_flag = true
ssh_flag = true
buffer = 2048

[ssh-server]
config_path = ./res/ssh-config
host_name = aiwolf-server
ssh_agent_flag = true
timeout = 200

[tcp-client]
; local sever settings
host = localhost
port = 10001

[game]
num = 1

[agent]
num = 5
name1 = kanolab1
```

## res/ssh-configの設定の説明
ここではSSH接続の設定を記述します。一般的なsshのconfigの記述方式に従っているため、`res/ssh-config`ではなく、`~/.ssh/config`に記述していただき、`res/config.ini`で`config_path=~/.ssh/config`として頂くことも可能です。

`Host`:接続名です。`res/config.ini`の`host_name`と同じにしてください

`User`:SSH接続を行う際のユーザ名です。こちらは参加登録後、運営から提供します。

`IdentityFile`:`res/config.ini`で`ssh_flag = false`の場合に主に使用します。秘密鍵のパスです。

`RemoteForward [remote_port1] localhost:[local_port1]`: 運営が提供するするサーバに対するリモートフォワードの設定です。運営が提供するサーバの[remote_port*]と参加者の皆様の[local_port*]をフォワーディングします。この1ポートを1エージェントが使用し、対戦接続システムと通信を行います。`remote_port*`に関しては参加登録後、運営が指定するポートを指定してください。


```
Host aiwolf-server
HostName [対戦サーバのipアドレス]
User [user name]
IdentityFile ~/.ssh/id_rsa
RemoteForward [remote_port1] localhost:[local_port1]
RemoteForward [remote_port2] localhost:[local_port2]
RemoteForward [remote_port3] localhost:[local_port3]
RemoteForward [remote_port4] localhost:[local_port4]
RemoteForward [remote_port5] localhost:[local_port5]
```

## 自己対戦方法
1. `res/config.ini`を以下のように設定する
	```
	[connection]
	host_flag = true
	ssh_flag = false

	(...)
	
	[tcp-server]
	ip = localhost
	port1 = 50000		; Agent[01]の待ち受けポート
	port2 = 50001		; Agent[02]の待ち受けポート
	port3 = 50002		; Agent[03]の待ち受けポート
	port4 = 50003		; Agent[04]の待ち受けポート
	port5 = 50004		; Agent[05]の待ち受けポート

	(...)

	[game]
	num = 2				; 連続ゲーム回数

	[agent]
	num = 5				; Agentの数
	name1 = kanolab1	; Agent[01]の名前
	name2 = kanolab2	; Agent[02]の名前
	name3 = kanolab3	; Agent[03]の名前
	name4 = kanolab4	; Agent[04]の名前
	name5 = kanolab5	; Agent[05]の名前
	```
1. 以下のコマンドでプログラムを実行する
	```
	$ python3 multiprocess.py
	```
1. 対戦プログラムを起動する\
	対戦プログラムは[AIWolfNLGameServer](https://github.com/aiwolfdial/AIWolfNLGameServer)に用意してあります。

## 主催者が提供するサーバでの実行確認方法
ここでは参加者の方々に対戦サーバの待ち受けができているか確認する方法を説明します。

1. `res/config.ini`の設定を行ってください。
	以下の値は変更を行わないでください。
	```	
	[game]
	num = 1
	```
1. `res/ssh-config`の設定を行ってください。
1. 最後にエージェントのプログラムを実行してください
	```
	$ python3 multiprocess.py
	```
1. エージェントが待ち受けているポート番号を運営が提供するするサーバの対戦プログラムに伝える。
	[AIWolfPreliminaryRun](https://github.com/aiwolfdial/AIWolfPreliminaryRun)の内容に従ってAIWolfPreliminaryRunのプログラムを実行してください。


## 一部の方向けの情報
### 踏み台サーバを経由する等、秘密鍵を参照することができない場所から接続を行う方向け
この場合の接続方法はssh-agentを使用する方法となります。

1. まずはローカルの環境で以下のコマンドを実行してください。`[秘密鍵]`の部分は参加登録の際に頂いた公開鍵に対応する秘密鍵を指定してください。
	```
	$ eval `ssh-agent`
	$ ssh-add ~/.ssh/[秘密鍵]
	```
2. 次に以下のように`-A`オプションを付与してご自身のリモートサーバ等にアクセスしてください
	```
	$ ssh -A [host name]
	```
3. `./res/config.ini`の一部を以下に合わせてください
	```
	[ssh-server]
	ssh_agent_flag = true
	```
4. プログラムを実行してください。
	```
	$ python3 multiprocess.py
	```