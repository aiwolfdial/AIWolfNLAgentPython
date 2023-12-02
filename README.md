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
## 予選について
予選は例年通り運営の提供する`host: "160.16.83.206"`,`port: 10001`の対戦リモートサーバに接続して頂くことでゲームが実行可能です。

## Agent 1体を使用して実行する場合
1. `res/config.iniを`以下の説明に合わせて設定を変更してください

`[connection] host_flag`: tureの場合にゲームサーバの待ち受けを行います。 falseの場合はゲームサーバへの接続を行います。 予選の際は`host_flag = false`にしてください。

`[connection-client] host:` 接続を行うサーバのipを記述してください

`[connection-client] port:` 接続を行うサーバのポートを記述してください

`[game] num:` 連続実行するゲームの回数を記述してください

`[agent] name1:` エージェントの名前を記述してください
> name1 には英数字を使用してください。

・例
```
[connection]
host_flag = false
buffer = 2048

(中略)

[connection-client]
; local sever settings
host = localhost
port = 10001
; remote sever settings
; host = 160.16.83.206
; port = 10001

(中略)

[game]
num = 1

[agent]
name1 = kanolab1

```
2. サーバプログラム実行後、```python3 main.py```で動作します。


<br>

## Agent 複数体を同時に使用して実行する場合
1. `res/config.iniを`以下の説明に合わせて設定を変更してください
`[connection] host_flag`: tureの場合にゲームサーバの待ち受けを行います。 falseの場合はゲームサーバへの接続を行います。 予選の際は`host_flag = false`にしてください。

`[connection-client] host:` 接続を行うサーバのipを記述してください

`[connection-client] port:` 接続を行うサーバのポートを記述してください

`[game] num:` 連続実行するゲームの回数を記述してください

`[agent] name1~5:` エージェントの名前を記述してください
> name には他のエージェントと重複しない名前（英数字）を使用してください。

・例
```
[connection]
host_flag = false
buffer = 2048

(中略)

[connection-client]
; local sever settings
host = localhost
port = 10001
; remote sever settings
; host = 160.16.83.206
; port = 10001

(中略)

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

2.サーバプログラム実行後、```python3 multiprocess.py```で動作します。


## 本戦について
予期せぬプログラムの実行エラーや日程調整の兼ね合いにより、本戦では運営が対戦用リモートサーバを提供するのではなく、参加者の方々にゲームサーバの待ち受けをして頂き運営がそこに接続をする形で開催することに致しました。

## 環境構築について
本プログラムを使用し、仮想環境として`venv`を使用する想定で手順を記載します。また、後述するコマンドを実行するosは`linux`を想定しています。
別の環境でゲームに参加する場合はご自身で適切な設定を行ってください。

### clone後1度実行して頂く必要のあるコマンド
```
$ python3 -m venv venv	# 仮想環境の作成
$ . venv/bin/activate	# 仮想環境の有効化
$ pip install -r res/requirements.txt	# ライブラリのインストール
```

## res/config.iniの設定
`res/config.ini`を以下の説明に合わせて設定を変更してください

`[connection] host_flag`: tureの場合にゲームサーバの待ち受けを行います。 falseの場合はゲームサーバへの接続を行います。 本戦の際は`host_flag = true`にしてください。

`[connection-server] ip`: 待ち受けを行うアドレスを指定します。通常`0.0.0.0`で問題ないはずです。

`[connection-server] port`: 各エージェントが待ち受けるポートを指定してください

```
[connection]
host_flag = true	; true: hosting,  false: guest
buffer = 2048

[connection-server]
ip = 0.0.0.0		; Please write down the address where you would like to wait.
port1 = 50000		; Please write the port that Agent[01] is listening on
port2 = 50001		; Please write the port that Agent[02] is listening on
port3 = 50002		; Please write the port that Agent[03] is listening on
port4 = 50003		; Please write the port that Agent[04] is listening on
port5 = 50004		; Please write the port that Agent[05] is listening on
```

## 運営にグローバルIP、待ち受けポートを伝える
運営が接続を行う都合上、`グローバルIP`、`ポート`の2つが必要です。以下の内容を伝えて下さい。

### グローバルIP
以下のコマンドを実行し、その内容を教えてください
```
$ python3 check_gpi.py
```

### 待ち受けポート
`res/config.ini`に記載した待ち受けポートを参加するエージェントの数分教えてください

## プログラムの実行
以下の`2.`と同じです。

[Agent 複数体を同時に使用して実行する場合](#agent-複数体を同時に使用して実行する場合)