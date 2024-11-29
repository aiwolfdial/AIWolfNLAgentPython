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
- 村人: `player/villager.py` が呼び出されます。`talk`,`vote`関数をカスタマイズしてください
- 占い師: `player/seer.py` が呼び出されます。`divine`関数や`talk`,`vote`関数をカスタマイズしてください。
- 狂人: `player/possessed.py` が呼び出されます。`talk`,`vote`関数をカスタマイズしてください。
- 人狼: `player/werewolf.py` が呼び出されます。`attack`関数や`talk`,`vote`関数をカスタマイズしてください。

## 環境構築

> [!IMPORTANT]
> ライブラリのリファクタリングなどに伴い、コードの修正、破壊的変更を行いました。この対応により、現在のコードでは型エラーなどの警告の殆どを修正しました。  
> リファクタリング前のコードは、[v0.1.0](https://github.com/kano-lab/aiwolf-nlp-agent/tree/v0.1.0)をご参照ください。aiwolf-nlp-commonのバージョンはv0.2.2以下をご利用ください。

> [!IMPORTANT]
> Python 3.11以上が必要です。

```
git clone https://github.com/kano-lab/aiwolf-nlp-agent.git
cd aiwolf-nlp-agent
python -m venv .venv
source .venv/bin/activate
pip install .
cd src
```

> [!NOTE]
> aiwolf-nlp-commonとは、役職や接続方式に関するプログラムが定義されているPythonパッケージです。  
> 詳細については、https://github.com/kano-lab/aiwolf-nlp-common をご覧ください。

## 実行方法

### 自己対戦

事前に、ローカル内にゲームサーバを立ち上げる必要があります。  
[kano-lab/aiwolf-nlp-server](https://github.com/kano-lab/aiwolf-nlp-server) を参考にしてください。

```
cp res/config.ini.example res/config.ini
cp res/log.ini.example res/log.ini
python multi.py
```

### 主催者が提供するサーバでの自己対戦の実行

`res/config.ini` を主催者から提供された設定に変更してください。  

```
python multi.py
```

### 主催者が提供するサーバでの本戦の実行

`res/config.ini` を主催者から提供された設定に変更してください。  

```
chmod +x infinite.sh
./infinite.sh
```

## 設定 (config.ini)

### [websocket]

`url`: ゲームサーバのURLです。ローカル内のゲームサーバに接続する場合はデフォルト値で問題ありません。

### [connection]

`keep_connection`: game.num回のゲームを行ったあとにもう一度ゲームを行う場合は`true`にしてください。**本戦のみ`true`にしてください。**

### [game]

`num`: 連続でゲームを行う回数です。自己対戦の場合はデフォルト値で問題ありません。

### [agent]

`num`: 起動するエージェントの数です。自己対戦の場合はデフォルト値で問題ありません。  
`name*`: *番目のエージェントの名前です。基本的には参加登録時に登録した名前+数字で問題ありません。

```
[websocket]
url = ws://127.0.0.1:8080/ws

[connection]
keep_connection = false

[game]
num = 1

[agent]
num = 5
name1 = kanolab1
name2 = kanolab2
name3 = kanolab3
name4 = kanolab4
name5 = kanolab5

[path]
log_config = ./res/log.ini
random_talk = ./res/2019071_44011_AIWolfTalkLogs.txt
```

## ログの設定 (log.ini)

### [log]

`get_info`: ゲームサーバから取得したJsonをログに書き込むかどうかの設定です。  
`initialize`: Initializeリクエストの時にゲームサーバから取得したJsonをログに書き込むかどうかの設定です。  
`talk`: エージェントがゲームサーバに送信した`TALK`の内容ををログに書き込むかどうかの設定です。  
`vote`: エージェントがゲームサーバに送信した`VOTE`の内容ををログに書き込むかどうかの設定です。  
`divine`: エージェントがゲームサーバに送信した`DIVINE`の内容ををログに書き込むかどうかの設定です。  
`divine_result`: ゲームサーバから取得した占いの結果をログに書き込むかどうかの設定です。  
`attack`: エージェントがゲームサーバに送信した`ATTACK`の内容ををログに書き込むかどうかの設定です。  

### [path]

`output_dir`: エージェントのログを保存するパスの設定です。デフォルト値で問題ありません。
