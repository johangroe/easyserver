import json
import requests

## push     {"req": "push", "username": "***", "client": "***", "data": [{tut-doc}, {tut-doc}] }                       -> {"resp": "check", "cmd": "push"}
## pull     {"req": "pull", "username": "***", "client": "***"}                                                        -> {"resp": "check, "data": [{doc}, {doc}], "cmd": "pull"}
## login    {"req": "login", "username": "***", "password": "***", "client": "***", "stayloggedin": "True/False"}      -> {"resp": "check", "cmd": "login"}
## logout   {"req": "logout", "username": "***", "client": "***"}                                                      -> {"resp": "check", "cmd": "logout"}
## new_user {"req": "new_user", "username": "***", "password": "***", "client": "***", "stayloggedin": "True/False"}   -> {"resp": "check", "cmd": "new_user"}
## del_user {"req": "del_user", "username": "***", "password": "***"}                                                  -> {"resp": "check", "cmd": "del_user"}
## test     {"req": "test"}                                                                                            -> {"resp": "check", "cmd": "test"}


def send(address, data) -> dict:
    payload = json.dumps(data)
    resp = requests.post(address, json = payload).json()
    return resp

#resp = send("http://127.0.0.1:5000/data/", {"req": "new_user", "username": "Johan2", "password": ".py2", "client": "win", "stayloggedin": "True"})
resp = send("http://127.0.0.1:5000/data/", {"req": "del_user", "username": "Johan3", "password": ".py3"})
#resp = send("https://moneyserver.jgroeger.repl.co/dataport/", {"req": "test"})
#resp = send("http://127.0.0.1:5000/data/", {"req": "pull", "username": "Johan", "client": "win"})
print(resp)