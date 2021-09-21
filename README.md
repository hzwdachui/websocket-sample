# websocket im sample
This is a im sample using websocket, including server and client, both of which work in the terminal.

## prerequesition
```python
pip3 install -r requirements.txt
```

# server
```python
# cd into a certain version  e.g. cd v1
python3 server.py
```

# client
```python
# cd into a certain version  e.g. cd v1
python3 client.py
```

# exception and errors
- exit normally
- exit abnormally
- launch connection failed
    - connection exists
    - server failed

# todo
- secure tsl
- handle closing and exception  \[doing\]
- use official websockets.broadcast
- customize port and host   \[check\]
    - config the server
- more uesr friendly input interface    \[check\]
- client reconnect

# input area
prompt_toolkit: https://python-prompt-toolkit.readthedocs.io/en/master/  
ref: https://github.com/zlqm/ws-ui

# PR
## lint your code
please use pylint to lint your code
```
crtl-k + f
```
## generate requirements
```python
pipreqs . --force
```