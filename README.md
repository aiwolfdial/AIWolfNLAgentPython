# AIWolfNLAgentPython
A sample python code of AIWolf NL agent

# 

# 使いかた

## Agent 1人で使用する場合
1. `res/client.ini`の `host` ,`port` ,`name1`を埋めてください

・例
```
[connection]
host = localhost
port = 10000
buffer = 2048

[agent]
name1 = kanolab1
```
2. サーバプログラム実行後、```python3 main.py```で動作します。


<br>

## Agent 複数人で使用する場合
1. client.iniの`host` ,`port` とエージェントの人数`num`、人数分の`name`を埋めてください

・例
```
[connection]
host = localhost
port = 10000
buffer = 2048

[agent]
num = 5
name1 = kanolab1
name2 = kanolab2
name3 = kanolab3
name4 = kanolab4
name5 = kanolab5
```

2.サーバプログラム実行後、```python3 multiprocess.py```で動作します。