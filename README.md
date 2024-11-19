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

## 環境構築

```
git clone https://github.com/aiwolfdial/AIWolfNLAgentPython/
cd AIWolfNLAgentPython
python -m venv .venv
source .venv/bin/activate
pip install .
```

> [!NOTE]
> aiwolf-nlp-commonとは、役職や接続方式に関するプログラムが定義されているPythonパッケージです。
> 詳細については、https://github.com/aiwolfdial/AIWolfNLPCommon をご覧ください。

## 実行方法

### 自己対戦

事前に、ローカル内にゲームサーバを立ち上げる必要があります。  
[kano-lab/aiwolf-nlp-server](https://github.com/kano-lab/aiwolf-nlp-server) を参考にしてください。

```
cp res/config.ini.sample res/config.ini
cp res/log.ini.sample res/log.ini
python multiprocess.py
```

### 主催者が提供するサーバでの自己対戦の実行

`res/config.ini` を主催者から提供された設定に変更してください。  

```
python multiprocess.py
```

### 主催者が提供するサーバでの本戦の実行

`res/config.ini` を主催者から提供された設定に変更してください。  

```
python multiprocess.py
```

## 設定

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
