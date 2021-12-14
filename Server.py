from flask import Flask, request, render_template, redirect, session
import json

import DataProcessorServer as datapro
import SiteRenderer as renderer


## cookies / session:

## user_loggedin = bool
## user_stayloggedin = bool
## user_name = str
## redirect_mode = ["login", "register", "account"]


app = Flask(__name__)

app.secret_key = "9b82a4ca442f4ddc71a610a2d8e477b2"
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

## dataport: accept requests, send responses, just take commands and execute them mate
@app.route("/data/", methods = ["POST", "GET"])
def data_func(): 
    if request.method == "POST":
        jsondata = request.get_json()
        data = json.loads(jsondata)

        resp = datapro.go(data)

        return json.dumps(resp)
    
    elif request.method == "GET":
        return render_template("fake_not_found.html"), 404





## Homepage
@app.route("/", methods = ["GET", "POST"])
def home_func():
    session_loggedin, session_username, session_stayloggedin, session_redirect_mode = datapro.check_session(session)
    print(session)

    if request.method == "GET":
        return renderer.homepage(loggedin = session_loggedin, username = session_username)

    ## redirect to the account page, depending on which button was pressed
    elif request.method == "POST":
        redirect_site = request.form["origin"]
        if redirect_site == "homepage_login":
            session["user_redirect_mode"] = "login"
            return redirect("/account/", 302)

        elif redirect_site == "homepage_register":
            session["user_redirect_mode"] = "register"
            return redirect("/account/", 302)

        elif redirect_site == "homepage_account":
            session["user_redirect_mode"] = "account"
            return redirect("/account/", 302)
            
        elif redirect_site == "homepage_account_logout":
            datapro.clear_session(session)
            return redirect("/", 302)



## Loginpage, registerpage and accountpage in one
@app.route("/account/", methods = ["GET", "POST"])
def account_func():
    session_loggedin, session_username, session_stayloggedin, session_redirect_mode = datapro.check_session(session)

    if request.method == "GET":
        if session_loggedin == True:
            return renderer.account(mode = "account", username = session_username)

        is_error = None
        return renderer.account(mode = session_redirect_mode, username = session_username, error = is_error)


    elif request.method == "POST":
        is_error = None

        ## internes umschalten auf der account-seite
        if request.form["origin"] == "switch_to_register":
            return renderer.account(mode = "register", username = session_username, error = is_error)
        elif request.form["origin"] == "switch_to_login":
            return renderer.account(mode = "login", username = session_username, error = is_error)
        
        ## perform login
        elif request.form["origin"] == "login":
            
            ## load values from the form submitted
            username = str(request.form["username"])
            password = str(request.form["password"])
            if request.form.get("stayloggedin") == None:
                stayloggedin = False
            elif request.form.get("stayloggedin") == "on":
                stayloggedin = True

            print(f"Login-Stats: usrname:{username} pswrd:{password} stayloggedin:{stayloggedin}")

            ## catch that user has entered nothing
            if username == "" or password == "":
                return renderer.account(mode = "login", error = "invalid_login")
            

            else:
                valid = datapro.check_username_password(username, password)
                print("valid usrname and pswrd: " + str(valid))

                ## catch invalid password
                if valid == False:
                    return renderer.account(mode = "login", error = "invalid_login")
                
                
                elif valid == True:
                    if stayloggedin == True:
                        session.permanent = True
                    elif stayloggedin == False:
                        session.permanent = False

                    session["user_loggedin"] = True
                    session["user_stayloggedin"] = stayloggedin
                    session["user_name"] = username
                    session["user_redirect_mode"] = "account"
                    ## actualize session, reload page using new mode
                    return redirect("/account/", 302)


        ## perform signup
        elif request.form["origin"] == "register":
            
            ## load values from the form submitted
            username = str(request.form["username"])
            question = str(request.form.get("restoring_question"))
            answer = str(request.form["answer"])
            password1 = str(request.form["password1"])
            password2 = str(request.form["password2"])
            direct_login = False
            #print(request.form.get("direct_login"))
            
            if request.form.get("direct_login") == None:
                direct_login = False
            elif request.form.get("direct_login") == "on":
                direct_login = True

            print(f"{username}: {question}, {password1}, {password2}, {direct_login}")
            
            ## catch that user has entered nothing
            if username == "" or question == None or answer == "" or password1 == "" or password2 == "":
                return renderer.account(mode = "register", error = "invalid_data", username_to_register = username, question = question, answer = answer, password1 = password1, password2 = password2, direct_login = direct_login)
            
            ## catch that the username is already assigned
            elif datapro.check_username_existing(username) == True:
                return renderer.account(mode = "register", error = "username_already_assigned", username_to_register = username, question = question, answer = answer, password1 = password1, password2 = password2, direct_login = direct_login)
  
            ## catch two unidentical passwords
            elif password1 != password2:
                return renderer.account(mode = "register", error = "passwords_not_same", username_to_register = username, question = question, answer = answer, password1 = password1, password2 = password2, direct_login = direct_login)

            ## signup
            else:
                datapro.go({"req": "new_user", "username": username, "password": password1, "client": "web", "stayloggedin": "False"})
                if direct_login == True:
                    session["user_loggedin"] = True
                    session["user_stayloggedin"] = True
                    session["user_name"] = username
                    session["user_redirect_mode"] = "account"
                    
                    return redirect("/account/", 302)
                
                else:
                    session["user_redirect_mode"] = "login"
                    return redirect("/account/", 302)


        ## perform account data change
        elif request.form["origin"] == "account_change":
            new_username = str(request.form["username"])
            old_username = session["user_name"]

            password_old = str(request.form["password_old"])
            password_new1 = str(request.form["password_new1"])
            password_new2 = str(request.form["password_new2"])

            if new_username == "":
                ## fehler ungültiger nutzername
                pass

            if datapro.check_username_existing(new_username) == True:
                ## fehler nutzername bereits in nutzung
                pass
            
            if new_username != old_username:
                ## nutzernamen ändern
                pass

            if password_old != "" and password_new1 != "" and password_new2 != "":
                #if password_new1 != password_old
                
                if password_new1 == password_new2 and password_new1 != password_old:
                    ## passwort ändern
                    pass
                


            print("requested changes!!!")
            return redirect("/", 302)


        ## display final delete site
        elif request.form["origin"] == "account_delete":
            print("requested to delete account!!!")
            return renderer.account(mode = "account_delete", error = None)


        ## perform account deletion
        elif request.form["origin"] == "account_delete_final":
            username1 = session["user_name"]
            username2 = str(request.form["username"])
            password = str(request.form["password"])
            #print(username1, username2, password)
            if str(username1) == str(username2):
                if datapro.check_username_password(username2, password) == True:
                    print("account ready to delete")
                    datapro.go({"req": "del_user", "username": username2, "password": password})
                    datapro.clear_session(session)
                    return redirect("/", 302)
                else:
                    return renderer.account(mode = "account_delete", error = "invalid_data")
            else:
                return renderer.account(mode = "account_delete", error = "invalid_data")



## admin page
@app.route("/admin/")
def admin_func():
    #return render_template("fake_not_found.html")
    return renderer.admin()



@app.route("/test/", methods = ["GET", "POST"])
def test_func():
    return renderer.testpage()


if __name__ == "__main__":
    #app.run(host = "0.0.0.0", port = 5000)
    app.run(host = "127.0.0.1", port = 5000)