# aiwolf-nlp-agent

人狼知能コンテスト2024冬季 国内大会（自然言語部門） のサンプルエージェントです。  

ローカル内での動作確認ならびに自己対戦するためのゲームサーバについては、[kano-lab/aiwolf-nlp-server](https://github.com/kano-lab/aiwolf-nlp-server) を参考にしてください。  
大会の詳細ならびに参加登録については、[AIWolfDial2024WinterJp](https://sites.google.com/view/aiwolfdial2024winterjp/) を参考にしてください。

大会参加者はエージェントを実装したうえで、ご自身の端末でエージェントを実行、大会運営が提供するゲームサーバに接続する必要があります。エージェントの実装については、実装言語を含め、制限はありません。  
自己対戦では、5体のエージェントをご自身の端末で実行し、大会運営が提供する自己対戦用のゲームサーバに接続しすることで、エージェント同士の対戦を行うことができます。

**全エージェント共通の動作**
`player/agent.py` が呼び出されます。  
`talk`関数: エージェントが発話する内容を返す関数です。  
`vote`関数: エージェントが投票するプレイヤーを返す関数です。

**役職別の動作**
- 村人: `player/villager.py` が呼び出されます。`talk`,`vote`関数をカスタマイズしてお使いください。
- 占い師: `player/seer.py` が呼び出されます。`divine`関数や`talk`,`vote`関数をカスタマイズしてお使いください。
- 狂人: `player/possessed.py` が呼び出されます。`talk`,`vote`関数をカスタマイズしてお使いください。
- 人狼: `player/werewolf.py` が呼び出されます。`attack`関数や`talk`,`vote`関数をカスタマイズしてお使いください。

## 実行方法

```
git clone https://github.com/aiwolfdial/AIWolfNLAgentPython/
cd AIWolfNLAgentPython
python -m venv .venv
source .venv/bin/activate
pip install .
```

### aiwolf-nlp-commonパッケージについて

役職や接続方式に関するプログラムが定義されているPythonパッケージです。  
詳細については、https://github.com/aiwolfdial/AIWolfNLPCommon をご覧ください。

## 自己対戦

1. `res/config.ini.sample`を`res/config.ini`に名前を変更してください。
1. 以下のコマンドを実行してください。
	```
	$ python multiprocess.py
	```
1. 対戦接続システムを起動してください。\
	対戦接続システムは、https://github.com/aiwolfdial/AIWolfNLPServer をご覧ください。

### 主催者が提供するサーバでの自己対戦の実行

> [!WARNING]
> 人狼知能コンテスト2024冬季国内大会から新しい対戦接続システムに置き換える予定であるため、以下の手順とは異なります。
> 新しい対戦接続システムについて決まり次第、こちらに記載します。

ここでは参加者の方々に対戦サーバの待ち受けができているか確認する方法を説明します。

1. `res/config.ini`の設定を行ってください。
	以下の値は変更を行わないでください。
	```	
	[game]
	num = 1
	```
1. エージェントのプログラムを実行してください
	```
	$ python multiprocess.py
	```

### 本戦での実行

> [!WARNING]
> 人狼知能コンテスト2024冬季国内大会から新しい対戦接続システムに置き換える予定であるため、以下の手順とは異なります。
> 新しい対戦接続システムについて決まり次第、こちらに記載します。

1. `res/config.ini`の設定を行ってください。
	以下の値は当日の運営の指示に従い設定してください。
	```	
	[game]
	num = ???

	[agent]
	num = ???
	```
1. エージェントプログラムの実行
	```
	$ python multiprocess.py
	```

## 設定

`res/config.ini.sample` を `res/config.ini` に名前を変更してください。  

### [connection]
`websocket`: WebSocketを使用して大戦サーバと通信を行うか設定します。
`buffer`: 対戦サーバとの送受信の際に利用されるバッファサイズです。  
`keep_connection`: **本戦の場合のみ** `true`にしてください。

### [game]

`num`: 連続で行うゲームの回数です。

### [agent]

`num`: ゲームに参加するエージェントの人数です。  
`name*`: *番目のエージェントの名前です。

```
[connection]
websocket = true
buffer = 2048
keep_connection = false

[websocket]
uri = 127.0.0.1:50000

[game]
num = 1

[agent]
num = 5
name1 = kanolab1


[filePath]
log_inifile = ./res/log.ini
random_talk = ./res/2019071_44011_AIWolfTalkLogs.txt
```

## ログの設定

`res/log.ini.sample` を `res/log.ini` に名前を変更してください。  

`storage_path`: エージェントのログを保存するパスの設定です

`get_info`\
`true`:ゲームサーバから取得したJsonをログに書き込みます。\
`false`:ログに書きません。

`initialize` = true\
`true`:initializeリクエストの時にゲームサーバから取得したJsonをログに書き込みます。\
`false`:ログに書きません。

`talk`\
`true`:エージェントがゲームサーバに送信した`TALK`の内容ををログに書き込みます。\
`false`:ログに書きません。

`vote`\
`true`:エージェントがゲームサーバに送信した`VOTE`の内容ををログに書き込みます。\
`false`:ログに書きません。

`divine`\
`true`:エージェントがゲームサーバに送信した`DIVINE`の内容ををログに書き込みます。\
`false`:ログに書きません。

`divine_result`\
`true`:ゲームサーバから取得した占いの結果をログに書き込みます。\
`false`:ログに書きません。

`attack`\
`true`:エージェントがゲームサーバに送信した`ATTACK`の内容ををログに書き込みます。\
`false`:ログに書きません。
