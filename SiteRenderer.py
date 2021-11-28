"""
A small module, that can render (partly) custom webpages. It needs `DataProcessor` to figure out, if the
user is loggedin, has which username, gather personal data, etc.
"""
## by me, -johangroe

from flask import render_template
import DataProcessorServer as datapro
#import yaml

## enter your custom descriptions and names and stuff here:
## general stuff

#config = yaml.safe_load("config.yml")
#PROJ_NAME = config["PROJ_NAME"]
#print(config)

PROJ_NAME = "MoneyApp"
SUPPORT_MAIL_ADDRESS = "johan.groeger@gmail.com"

## homepage stuff
HOMEPAGE_TAB_TITLE = f"{PROJ_NAME} - Home"
## every item you enter is a new line.
HOMEPAGE_PROJ_DESCR = ["An app, that tracks on what stuff you have spent how much money.", "It can be used locally, but offers free cloud storage and sync too."]
## "None" hides the link
HOMEPAGE_LINK_DWNLD_ANDROID = "android_dload"
HOMEPAGE_LINK_DWNLD_IOS = "ios_dload"
HOMEPAGE_LINK_DWNLD_WIN = "win_dload"
HOMEPAGE_LINK_DWNLD_LINUX = "linux_dload"
HOMEPAGE_LINK_DWNLD_MACOS = "macos_dload"

## login page stuff
LOGIN_TAB_TITLE = f"{PROJ_NAME} - Login"

## register page stuff
REGISTER_TAB_TITLE = f"{PROJ_NAME} - Register"

## user page stuff
USER_TAB_TITLE = f"{PROJ_NAME} - Account"

## admin page stuff
ADMIN_TAB_TITLE = f"{PROJ_NAME} - Admin"


'''
SUPPORT_MAIL_ADDRESS = 

## homepage stuff
HOMEPAGE_TAB_TITLE = 
## every item you enter is a new line.
HOMEPAGE_PROJ_DESCR = 
## "None" hides the link
HOMEPAGE_LINK_DWNLD_ANDROID = 
HOMEPAGE_LINK_DWNLD_IOS = 
HOMEPAGE_LINK_DWNLD_WIN = 
HOMEPAGE_LINK_DWNLD_LINUX = 
HOMEPAGE_LINK_DWNLD_MACOS = 

## login page stuff
LOGIN_TAB_TITLE = 

## register page stuff
REGISTER_TAB_TITLE = 

## user page stuff
USER_TAB_TITLE = 

## admin page stuff
ADMIN_TAB_TITLE = 
'''


is_loggedin = False
is_adminloggedin = False
website_username = ""


class intern:
    def convert_to_jinja_list(list_to_convert):
        new_list_multiple = []
        for item in list_to_convert:
            new_list_single = []
            new_list_single.append(item)
            new_list_multiple.append(new_list_single)
        return new_list_multiple



def homepage(**kwargs):
    """
    Needs:

    ```loggedin```: is either ```True``` or ```False``` 

     ```username```: is either a string or ```None``` """
    for key, value in kwargs.items():
        if key == "loggedin":
            loggedin_value = value
        if key == "username":
            username_value = value

    homepage_proj_descr_list = intern.convert_to_jinja_list(HOMEPAGE_PROJ_DESCR)
    return render_template("homepage.html", tab_title = HOMEPAGE_TAB_TITLE, proj_name = PROJ_NAME, proj_descr = homepage_proj_descr_list, link_dload_android = HOMEPAGE_LINK_DWNLD_ANDROID, link_dload_ios = HOMEPAGE_LINK_DWNLD_IOS, link_dload_win = HOMEPAGE_LINK_DWNLD_WIN, link_dload_linux = HOMEPAGE_LINK_DWNLD_LINUX, link_dload_macos = HOMEPAGE_LINK_DWNLD_MACOS, support_mail = SUPPORT_MAIL_ADDRESS, user_loggedin = loggedin_value, user_name = username_value)


def account(**kwargs):
    mode = None
    username = None
    error = None
    username_to_register = ""
    question = ""
    answer = ""
    password1 = ""
    password2 = ""
    direct_login_bool = False
    direct_login = None


    for key, value in kwargs.items():
        if key == "mode":
            mode = value
        if key == "username":
            username = value
        if key == "error":
            error = value
        if key == "username_to_register":
            username_to_register = value
        if key == "question":
            question = value
        if key == "answer":
            answer = value
        if key == "password1":
            password1 = value
        if key == "password2":
            password2 = value
        if key == "direct_login":
            direct_login_bool = value
            
    if direct_login_bool == True:
        direct_login = "on"
    elif direct_login_bool == False:
        direct_login = None
    if mode == "login":
        return render_template("login.html", tab_title = LOGIN_TAB_TITLE, error = error, support_mail = SUPPORT_MAIL_ADDRESS, proj_name = PROJ_NAME)
    elif mode == "register":
        return render_template("register.html", tab_title = LOGIN_TAB_TITLE, error = error, support_mail = SUPPORT_MAIL_ADDRESS, proj_name = PROJ_NAME, username_to_register = username_to_register, question = question, answer = answer, password1 = password1, password2 = password2, direct_login = direct_login)
    elif mode == "account":
        return render_template("accountpage.html", tab_title = USER_TAB_TITLE, support_mail = SUPPORT_MAIL_ADDRESS, proj_name = PROJ_NAME)

    #return render_template("login_register_account.html", , mode = mode, username = username, error = error)


def register():
    return render_template("registerpage.html", tab_title = REGISTER_TAB_TITLE, support_mail = SUPPORT_MAIL_ADDRESS, proj_name = PROJ_NAME)


def accountpage():
    return render_template("userpage.html", tab_title = USER_TAB_TITLE, support_mail = SUPPORT_MAIL_ADDRESS, proj_name = PROJ_NAME)


def admin():
    return "this is the admin page :D"