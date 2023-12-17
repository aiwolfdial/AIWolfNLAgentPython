# AIWolfNLAgentPython
A sample python code of an AIWolf Contest's agent for Natural Language Division.
The server code is https://github.com/aiwolfdial/RandomTalkAgent

人狼知能大会自然言語部門向けのPythonサンプルエージェントコードです。
対戦サーバのコードは https://github.com/aiwolfdial/RandomTalkAgent です。
英語の説明の後に、同じ内容で日本語の説明があります。

# Usage

## Run a Single Agent 
1. Please fill `host` ,`port` ,`name1`, `game` in `res/config.ini`.
host and port should be set to specified locations of the contest server, or your own server if any.
name1 should be a unique name within other agents.
game specifies the number of consecutive games to be played.

・例
```
[connection]
host = localhost
port = 10000
buffer = 2048

[game]
num = 1

[agent]
name1 = kanolab1
```
2.After running the server program, execute ```python3 main.py```.


<br>

## Run Mutiple Agents 
1. Please fill `host` , `port`, `num` (number of agents), `game` (number of consecutive matches), num lines of `name`s in config.ini.

・例
```
[connection]
host = localhost
port = 10000
buffer = 2048

[game]
num = 1

[agent]
num = 5
name1 = kanolab1
name2 = kanolab2
name3 = kanolab3
name4 = kanolab4
name5 = kanolab5
```

2.After running the server program, execute ```python3 multiprocess.py```.

# 使いかた
昨年度までは主催者が提供する対戦サーバに自身のエージェント5体を接続して頂くことで対戦を自動実行していましたが、予期せぬプログラムの実行エラーや日程調整の兼ね合いが困難なことなどを鑑み、本年度からは参加者の方々に対戦サーバの待ち受けをして頂き主催者がそこに接続をする形で開催することに致しました。
具体的な方法については後述しますが、主催者が提供するLinuxサーバとSSH接続をして頂き、同時にリモートフォワードして頂く形で対戦サーバの待ち受けをして頂きます。

## 参加登録について
本年度から主催者が提供するサーバにSSH接続を行って頂く関係で、参加者の皆様の公開鍵が必要となります。
そのため参加登録の際には、公開鍵を添付いただくか、公開鍵を本文にお願いします。

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
`host_flag`: trueの場合にゲームサーバの待ち受けを行います。 falseの場合はゲームサーバへの接続を行います。主催者が提供するゲームサーバの待ち受けを行う際は `host_flag = true`にして下さい。
`ssh_flag`: trueの場合に主催者が提供するサーバへSSH接続をプログラムから行います。 falseの場合はSSH接続ではなく昨年度までのようにTCPコネクションを行います。
`buffer`: 対戦サーバとの送受信の際に利用されるバッファサイズです。

### [ssh-server]
`config_path`:後述するSSH接続の設定を書いたファイルのパスです。デフォルトでは`res/ssh-config`となっていますが、sshのconfigに書かれた方はそのパスを指定されても問題ありません。
`host_name`:SSH接続の設定を書いたファイルからどのホストに対する設定を使用するか識別する際に使用します。後述するsshのconfigの`Host`と同じであれば問題ありません。
`ssh_agent_flag`:trueの場合SSH接続を行う際にssh-agentを使用します。主に、ローカル環境からではなくリモートサーバ等にプログラムがおいてあり、そこから対戦サーバにSSH接続を行いたい方向けの設定です。falseの場合はssh-agentを使用しないので、後述するsshのconfigで`IdentityFile`に秘密鍵のパスを書くようにしてください。主にローカル環境から対戦サーバに接続を行いたい方向けです。

### [tcp-client]
`host`:昨年度までの接続方式です。後述する`execute.sh`で使用しているため対戦サーバにSSHで接続される場合はデフォルトで設定をしてください。 `ssh_flag=false`かつ`host_flag=false`の時に対戦サーバに接続するTCPクライアントとして動作します。

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
```

## res/ssh-configの設定の説明
ここではSSH接続の設定を記述します。一般的なsshのconfigの記述方式に従っているため、`res/ssh-config`ではなく、`~/.ssh/config`に記述していただき、`res/config.ini`で`config_path=~/.ssh/config`として頂くことも可能です。
`Host`:接続名です。`res/config.ini`の`host_name`と同じにしてください
`User`:SSH接続を行う際のユーザ名です。こちらは参加登録後、主催者から提供します。
`IdentityFile`:`res/config.ini`で`ssh_flag = false`の場合に主に使用します。秘密鍵のパスです。
`RemoteForward [remote_port1] localhost:[local_port1]`: 主催者が提供するするサーバに対するリモートフォワードの設定です。主催者が提供するするサーバの[remote_port*]と参加者の皆様の[local_port*]をフォワーディングします。この1ポートを1エージェントが使用し、対戦サーバと通信を行います。`remote_port*`に関しては参加登録後、主催者が指定するポートを指定してください。

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

## 実行確認方法
ここでは参加者の方々に対戦サーバの待ち受けができているか確認する方法を説明します。**今後、log等の関係でこの部分は変更が行われる可能性が高いため、頻繁にご確認ください**

### リモートサーバ等、秘密鍵に直接置いていない場所から接続を行う方向け
この場合の接続方法はss-agentを使用する方法となります。
まずはローカルの環境で以下のコマンドを実行してください。`[秘密鍵]`の部分は参加登録の際に頂いた公開鍵に対応する秘密鍵を指定してください。
```
$ eval `ssh-agent`
$ ssh-add ~/.ssh/[秘密鍵]
```

次に以下のように`-A`オプションを付与してご自身のリモートサーバ等にアクセスしてください
```
$ ssh -A [host name]
```

後は`ローカル環境から対戦サーバへ接続を行う方向け`と同じとなります。

### ローカル環境から対戦サーバへ接続を行う方向け

1. `res/config.ini`の設定を行ってください。
1. `res/ssh-config`の設定を行ってください。

最後に以下のコマンドを実行してください
```
$ sh execute.sh
```