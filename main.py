__author__ = 'Ryan Moreno'

import MySQLdb
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.carousel import Carousel
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
#import datetimefrom kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import (ObjectProperty, NumericProperty, OptionProperty,
                             BooleanProperty, StringProperty)
from kivy.resources import resource_add_path
from kivy.lang import Builder
import os.path

from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.window import Window
import time
import datetime
import sys
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.modalview import ModalView
from kivy.uix.listview import ListItemButton



pop1 = Popup(title='Empty Data', content=Label(text='Empty Username and/or Password'),size_hint=(None,None),size=(280,100))
pop2 = Popup(title='Login Failed', content=Label(text='Incorrect Username and/or Password'),size_hint=(None,None),size=(280,100))
pop3 = Popup(title='TextField empty', content=Label(text='Fields are all required'),size_hint=(None,None),size=(280,100))     
pop4 = Popup(title='Password Empty', content=Label(text='Password cannot be empty'),size_hint=(None,None),size=(280,100))
pop5 = Popup(title='Password Mismatch', content=Label(text='Retype Your Password'),size_hint=(None,None),size=(280,100))

class AppScreen(Screen):
    drivers = ObjectProperty()

class LoginForm(AppScreen):
    user = StringProperty()
    def driver_login(self,username,password):
        self.user = username
        print 'SUCCESSFULLY CONNECTED TO DATABASE!'
        if (self.txt_username.text=="" and self.txt_password.text==""):
            print pop1.title
            pop1.open()
        elif (query.execute("SELECT * FROM `register_account` WHERE `username` ='"+username+"' AND `password`='"+password+"'")):
            query.execute("UPDATE `register_account` SET `emergency_status`=' ' WHERE `username` = '"+username+"' ")
            print 'CONGRATULATIONS ' + username + '. You are succesfully logged in.'
            self.manager.current = 'mainwindow'
        else:
            db.commit()
            print pop2.title
            pop2.open()

class Admin(AppScreen):
    user = StringProperty()
    def admin_login(self,username,password):
        self.user_admin = username
        print 'SUCCESSFULLY CONNECTED TO DATABASE!'
        if (self.txt_username_admin.text=="" and self.txt_password_admin.text==""):
            print pop1.title
            pop1.open()
        elif (query.execute("SELECT * FROM `admin` WHERE `admin_user` ='"+username+"' AND `admin_pwd`='"+password+"'")):
            print 'CONGRATULATIONS ' + username + '. You are succesfully logged in.'
            self.manager.current = 'First'
        else:
            db.commit()
            print pop2.title
            pop2.open()

class First(AppScreen):
    user = StringProperty()
    def register_driver_form1(self,lastname,firstname,middlename,email,driver_password, driver_password_retype):
        self.user = email
        if (lastname=='' and middlename =='' and email =='' and driver_password =='' and driver_password_retype ==''):
            print pop3.title
            pop3.open()
        elif driver_password=='' and driver_password_retype=='':
            print pop4.title
            pop4.open()
        elif driver_password == driver_password_retype:
            query.execute("CALL registerform1('','"+lastname+"', '"+firstname+"', '"+middlename+"', '"+email+"', '"+driver_password+"')")
            print 'FORM 1 SUCCESSFULLY INSERTED'
            db.commit()
            self.manager.current = 'second'
        else:
            print pop5.title
            pop5.open()


class Second(AppScreen):
    def register_driver_form2(self,male,female,age,address,unitno,licenceno,username):
        if (age==''and address=='' and unitno==''):
            print pop3.title
            pop3.open()
        else:
            if (male.active == True):
                query.execute("CALL registerform2('"+male.text+"','"+age+"','"+address+"','"+unitno+"','"+licenceno+"','"+username+"')")
                print 'FORM 2 SUCCESSFULLY INSERTED'
                db.commit()
            else:
                query.execute("CALL registerform2('"+female.text+"','"+age+"','"+address+"','"+unitno+"','"+username+"')")
                print 'FORM 2 SUCCESSFULLY INSERTED'
                db.commit()
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    info = StringProperty()
    
    def dismiss_popup(self):
        self._popup.dismiss()
    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()
    def load(self, path, filename):
        print filename[0]
        self.info=filename[0]
        self.dismiss_popup()

class Third(AppScreen):
    def register_driver_form3(self,dir_location, username):
        query.execute("CALL registerform3('"+dir_location+"','"+username+"')")
        db.commit()
        print 'Third form succesful'

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class CustomLabel(Label):
	pass

class MainWindow(AppScreen):
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = ExitDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Exit Application", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        print filename[0]
        self.info=filename[0]
        self.dismiss_popup()

    def dismiss_popup1(self):
        self._popup.dismiss()

    def show_load1(self, username):
        content = LoadDialogInfo(load1=self.load1, cancel1=self.dismiss_popup)
        customer_username = username
        self._popup = Popup(title="Customer's Information - " + username, content=content, size_hint=(0.9, 0.9), height=30)
        query.execute("SELECT first_name,last_name,location_from,location_to from commuter where commuter.username = '"+username+"'")
        results = query.fetchall()
        db.commit()
        for row in results:
            content.firstname = row[0]
            content.lastname = row[1]
            content.locationfrom = row[2]
            content.locationto = row[3]
            print row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3] 
        self._popup.open()

    def load1(self, path, filename):
        print filename[0]
        self.info=filename[0]
        self.dismiss_popup()

    def exit_app(self):
        sys.exit()

    def send_emergency(self, user):
        currentlocation = 'Technological Institute of the Philippines,\n 938, Aurora Boulevard, Mangga, District III,\n Quezon City, Metro Manila, 1109, Philippines'
        query.execute("UPDATE `register_account` SET `emergency_status` = 'emergency', `current_location` = '"+currentlocation+"' WHERE username = '"+user+"'")
        db.commit()

class Driver(Carousel):
    name = StringProperty()
    unitno = StringProperty()
    licno= StringProperty()
    def driver_info(self, username):
        query.execute("SELECT * FROM `register_account` WHERE `username`='"+username+"'")
        results = query.fetchall()
        db.commit()
        for row in results:
            print row[1] + ', ' + row[2] +' ' + row[3] + ' ' + row[4] + ' ' + row[9]
            self.name = row[1] + ', ' + row[2] +' ' + row[3]
            self.unitno = row[9]
            self.licno = row[10]


class History(Carousel):
    def refresh(self,dname):
        query.execute("SELECT * FROM `commuter` WHERE `driver_username`='"+dname+"'")
        results = query.fetchall()
        db.commit()
        self.scrollview1.content_layout1.clear_widgets()
        for row in results:
            size_y = 100
            size_y = 100

            l = CustomLabel2(text=row[1] +'     ('+ row[8] + ' to '+ row[9] +') \n'+ 'FROM: ' + row[5] + '\nTO: ' + row[6], size_hint=(1.0, None), height=size_y, id=row[1], background_color=[1,1,1,0],font_size=25)
            
            self.scrollview1.content_layout1.add_widget(l) 

class Customer(Carousel):
    customer_container = ObjectProperty()
    def __init__(self, **kwargs):
        super(Customer, self).__init__(**kwargs)
        Clock.schedule_once(self.setup,2)
    def setup(self, dt):
        print 'SUCCESSFULLY CONNECTED TO DATABASE!'
        def make_run(*t):
            x=30
            if (x>5):
                query.execute("SELECT * FROM `commuter` WHERE `transact`='request'")
                results = query.fetchall()
                db.commit()
                numrows = int(query.rowcount)
                print numrows
                for row in results:
                    size_y = 100
                    if size_y < 20:
                        size_y = 20
                    l = CustomLabel1(text=row[1] + ': \nFROM: ' + row[5] + '\nTO ' + row[6], size_hint=(1.0, None), height=size_y, id=row[1], background_color=[0,0.349,0.953,1], font_size=25)
                    self.customer_username = row[1]
                    def remove_all(*t):
                        self.scrollview.content_layout.clear_widgets()
                    Clock.schedule_once(remove_all,1)
                    self.scrollview.content_layout.add_widget(l)  
                    
                if(numrows==0):
                    l1 = CustomLabel(text = 'There are no commuter request at this moment', font_size=25)
            Clock.schedule_once(make_run, 2)
        Clock.schedule_once(make_run,1)

class ScrollableContainer(ScrollView):
    pass

class ScrollableContainer1(ScrollView):
    pass

class LoadDialogInfo(FloatLayout):
    cancel1 = ObjectProperty(None)
    driver_username = StringProperty()
    lastname = StringProperty()
    firstname = StringProperty()
    locationfrom = StringProperty()
    locationto = StringProperty()
    l = LoginForm()
    driver_username = l.user

    def block_this_customer(self, lname, fname):
    	query.execute("CALL block_customer('"+lname+"','"+fname+"')")
    	self.cancel1()
    def done(self, lname, fname):
        display_time = time.strftime("%H : %M")
        query.execute("UPDATE `commuter` SET `transact` = 'done', time2 = '"+display_time+"' WHERE `last_name` = '"+lname+"' AND `first_name` = '"+fname+"'")

class ExitDialog(FloatLayout):
    cancel = ObjectProperty(None)
    def exit_app(self):
        sys.exit()

class CustomLabel1(Button):
    def execute(self, username):
        display_time = time.strftime("%H : %M")
        query.execute("CALL accept_request('"+username+"','"+driver_name+"','"+current_location+"', '"+latitude+"', '"+longhitude+"', '"+display_time+"')")
        customer_username = username
        print customer_username
        db.commit()
        print 'SUCCESSFULLY UPDATED THE DATABASE!--eto yon'
        m = MainWindow()
        m.show_load1(self.id)

class CustomLabel2(Button):
    pass

def locations_args_converter(index, data_item):
    city, country = data_item
    return {'location': (city, country)}

class LocationButton(ListItemButton):
    location = ListProperty()

class mainApp(App):
    
    def build(self):
        config = self.config
        self.title = "Parataxi - Driver"
        self.root = Builder.load_file('main.kv')
        return self.root
    add_location_form = ObjectProperty()
    def show_add_location_form(self):
        self.add_location_form = Customer_Information()
        self.add_location_form.open()


if __name__=='__main__':
    latitude = '14.626085'
    longhitude = '121.062519'
    driver_name = 'ryan'
    current_location = 'Technological Institute of the Philippines,\n 938, Aurora Boulevard, Mangga, District III,\n Quezon City, Metro Manila, 1109, Philippines'
    db = MySQLdb.connect(host="localhost",user="root",passwd="",db="parataxi")
    query = db.cursor()
    mainApp().run()
