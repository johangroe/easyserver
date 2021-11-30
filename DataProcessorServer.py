"""
A module to work between `Flask` and `TinyUtils` on a server to manage usernames, passwords, contents, requests & responses.
"""
## by me, -johangroe


## stdcmds:
#xx# push     {"req": "push", "username": "***", "client": "***", "data": [{tut-doc}, {tut-doc}] }
#xx# pull     {"req": "pull", "username": "***", "client": "***"}
#xx# login    {"req": "login", "username": "***", "password": "***", "client": "***", stayloggedin": "True/False"}
#xx# logout   {"req": "logout", "username": "***", "client": "***"}
#xx# new_user {"req": "new_user", "username": "***", "password": "***", "client": "***", "stayloggedin": "True/False"}
#xx# del_user {"req": "del_user", "username": "***", "password": "***"}
#xx# test     {"req": "test"}
## restart    {"req": "restart"}

## database-users       {"id": *, "table": "admin/user", "username": "***", "password": "***", "clients-loggedin-stayloggedin": {*client*: "True&True", *client*: "True&False"}}
## database-content     {"id": *, "table": "user, "username": "***", "data": "*data*"}
## database-cont-local  {"id": *, "table": *, *xyz*: *abc*, *123*: *789*}
import TinyUtils as tut

stdcmds = ["push", "pull", "login", "logout", "new_user", "del_user", "test"]
customcmds = []
USERDB = "users.json"
CONTENTDB = "data.json"

## smash every shit into here lol
def go(content):
    """
    Central function. Pass the received message, and it'll do all the work for you.
    """
    cmd = content.pop(list(content)[0])
    not_cmd = content

    print(cmd, not_cmd)
    resp = {}
    ## standard commands
    if cmd in stdcmds:
        ## content-commands
        if cmd == "push":
            resp = commands.push(not_cmd)

        elif cmd == "pull":
            resp = commands.pull(not_cmd)

        ## user-commands
        elif cmd == "login":
            resp = commands.login(not_cmd)
        
        elif cmd == "logout":
            resp = commands.logout(not_cmd)
        
        elif cmd == "new_user":
            resp = commands.new_user(not_cmd)
        
        elif cmd == "del_user":
            resp = commands.del_user(not_cmd)

        elif cmd == "test":
            resp = commands.test(not_cmd)
        
        tut.db.close()
    else:
        resp = {"resp":"Err: no such command"}
    
    resp["cmd"] = cmd

    return resp


def check_username_password(username, password):
    """
    Check if a username is existing and the password is valid.
    """
    name_found = False
    valid = False
    try:
        tut.db.close()
    except:
        pass
    tut.db.set(USERDB)
    content = tut.documents.get.by_field("username", username)
    if content != []:
        doc = content[0]
        if doc["password"] == password:
            valid = True
    else:
        valid = False
    return valid

def check_username_existing(username) -> bool:
    """Check if a username is existing."""
    username_found = False
    try:
        tut.db.close()
    except:
        pass
    tut.db.set(USERDB)
    content = tut.documents.get.by_field("username", username)
    if content != []:
        username_found = True
    return username_found


def check_client_loggedin(username, client) -> bool:
    client_loggedin = False
    clients = ["ios", "android", "win", "linux", "macos"]
    if client not in clients:
        return {"resp": "Err: no such client"}
    if check_username_existing(username) != True:
        return {"resp": "Err: name not found"}
    
    tut.db.set(USERDB)
    doc = tut.documents.get.by_field("username", username)[0]
    clients_loggedin = dict(doc["clients-loggedin-stayloggedin"])
    if client not in list(clients_loggedin):
        client_loggedin = False
        
    else:
        state = clients_loggedin[client]
        state = state.split("&")[0]
        if state == "True":
            client_loggedin = True
        elif state == "False":
            client_loggedin = False
        

    return client_loggedin


def check_session(session) -> set:
    """Gives back ```is-loggedin```, ```username```, ```stay-loggedin```, ```redirect-mode```"""
    try:
        waste = session["user_name"]
        ## session is existing       
        
    except:
        ## create new session
        session["user_loggedin"] = False
        session["user_stayloggedin"] = False
        session["user_name"] = None
        session["user_redirect_mode"] = "login"
    

    is_loggedin = session["user_loggedin"]
    username = session["user_name"]
    stayloggedin = session["user_stayloggedin"]
    redirect_mode = session["user_redirect_mode"]

    return is_loggedin, username, stayloggedin, redirect_mode

def clear_session(session):
    session["user_loggedin"] = False
    session["user_stayloggedin"] = False
    session["user_name"] = None
    session["user_redirect_mode"] = "login"



class commands:
    """
    All standard commands.
    """

    def push(content):
        if check_username_existing(content["username"]) != True:
            return {"resp": "Err: name not found"}
        if check_client_loggedin(content["username"], content["client"]) != True:
            return {"resp": "Err: client not logged in"}
        
        tut.db.set(CONTENTDB)
        new_doc = []

        for item in content["data"]:
            try:
                del item["id"]
                del item["table"]
            except:
                pass
            new_doc.append(item)
        
        try:
            doc = tut.documents.get.by_field("username", content["username"])[0]
            id = doc["id"]
            
            tut.documents.field.update(id, "data", "data", new_doc)
        except:
            tut.documents.new(new_doc, )
        return {"resp": "check"}
        


    def pull(content):
        if check_username_existing(content["username"]) != True:
            return {"resp": "Err: name not found"}
        if check_client_loggedin(content["username"], content["client"]) !=True:
            return {"resp": "Err: client not logged in"}
        
        tut.db.set(CONTENTDB)
        return_data = tut.documents.get.by_field("username", content["username"])
        for item in return_data:
            del item["id"]
            del item["table"]
        return {"resp": "check", "data": return_data}


    def login(content):
        if check_username_existing(content["username"]) != True:
            return {"resp": "Err: name not found"}
        if check_username_password(content["username"], content["password"]) != True:
            return {"resp": "Err: invalid pw or name"}
        
        clients = ["ios", "android", "win", "linux", "macos"]
        if content["client"] not in clients:
            return {"resp": "Err: no such client"}

        tut.db.set(USERDB)

        doc = tut.documents.get.by_field("username", content["username"])[0]
        id = doc["id"]
        client_loggedin_stay = doc["clients-loggedin-stayloggedin"]
        client_loggedin_stay[content["client"]] = str(True) + "&" + str(content["stayloggedin"])
        tut.documents.field.update(id, "clients-loggedin-stayloggedin", "clients-loggedin-stayloggedin", client_loggedin_stay)
        return {"resp": "check"}


    def logout(content):
        if check_username_existing(content["username"]) != True:
            return {"resp": "Err: name not found"}
        clients = ["ios", "android", "win", "linux", "macos"]
        if content["client"] not in clients:
            return {"resp": "Err: no such client"}

        tut.db.set(USERDB)

        doc = tut.documents.get.by_field("username", content["username"])[0]
        id = doc["id"]
        client_loggedin_stay = doc["clients-loggedin-stayloggedin"]
        client_loggedin_stay[content["client"]] = str(False) + "&" + str(False)
        tut.documents.field.update(id, "clients-loggedin-stayloggedin", "clients-loggedin-stayloggedin", client_loggedin_stay)
        return {"resp": "check"}


    def new_user(content):
        
        tut.db.set(USERDB)

        if check_username_existing(content["username"]) == True:
                return {"resp": "Err: name already assigned"}

        else:
            loggedin_staylogged = [True, bool(content["stayloggedin"])]
            
            tut.documents.new({"username": content["username"], "password": content["password"], "clients-loggedin-stayloggedin": {content["client"]: loggedin_staylogged}}, "user")
            
            tut.db.set(CONTENTDB)
            tut.documents.new({"username": content["username"], "data": ""}, "user")
            return {"resp": "check"}
            
        
    def del_user(content):

        tut.db.set(USERDB)

        if check_username_existing(content["username"]) != True:
            return {"resp": "Err: name not found"}

        doc = tut.documents.get.by_field("username", content["username"])[0]
        

        if content["password"] != doc["password"]:
            return {"resp": "Err: password incorrect"}
        else:
            id = doc["id"]
            tut.documents.delete(id)
            tut.db.set(CONTENTDB)
            doc = tut.documents.get.by_field("username", content["username"])[0]
            id = doc["id"]
            tut.documents.delete(id)
            return {"resp": "check"}


    def test(content):
        return {"resp": "check"}