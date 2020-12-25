from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob
from datetime import datetime
from pathlib import Path
import random

Builder.load_file('design.kv')

with open("users.json") as file:
    users = json.load(file)
            
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        if uname == '' or pword == '':
             self.ids.login_wrong.text = "Please type a username or password"

        elif uname in users and users[uname]['password'] == pword:
            self.manager.current = 'login_screen_success'
        else:
            print('fail')
            self.ids.login_wrong.text = "Wrong username or password"

    def forgot_pass(self):
        self.manager.current = "forgot_pass_screen"


class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        if len(uname) < 3 or len(pword) < 5:
            print('PLEASE TYPE USERNAME OR PASSWORD AGAIN.\nUsername must be at least characters.\nPasswords must be at least 5 characters.')

        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users, file)

        self.manager.current = "sign_up_screen_success"


class SignUpScreenSuccess(Screen):
    def back_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    previous_line = 'placeholder'

    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")
        available_feelings = [Path(filename).stem for filename 
                                in available_feelings]
        
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()

            myline = random.choice(quotes)

            while myline == self.previous_line:
                myline = random.choice(quotes)

            self.previous_line = myline
            self.ids.quote.text = myline

        else:
            self.ids.quote.text = "Sorry, that feeling isn't supported yet. Please try something else"


class ForgotPassScreen(Screen):
    print('ran') 

    def forgot_pass_success(self, username, new_password): 
        print(username, new_password)
        with open('users.json') as f:
            data = json.load(f)
        for i, key in enumerate(data.keys()):
            print(data.keys())
            if username == key:
                print('done', i)
                break
            else:
                print('failed')



class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
