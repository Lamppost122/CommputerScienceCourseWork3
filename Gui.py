"""
Gui
This is the system that handles Gui
"""
import json
from tkinter import messagebox




import re,datetime,io,sys,os.path,os,smtplib,hashlib, uuid,ctypes
##from email.MIMEMultipart import MIMEMultipart
##from email.MIMEText import MIMEText
import tkinter as tk
from tkinter import font  as tkfont


CurrentUser = ""
AccessLevel = "Player"

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, Register,ProfileSetup,Home):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        frame.update()






class Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.Title = tk.Label(self, text="Please fill in your details", font=controller.title_font)
        self.loginButton = tk.Button(self, text="Login",command=lambda: controller.show_frame("Login") )
        self.registerButton = tk.Button(self, text="Register",command=lambda: self.register())
        self.lblUsername = tk.Label(self,text="Username: ")
        self.lblPassword = tk.Label(self,text="Password: ")
        self.lblConfirmUsername = tk.Label(self,text="Confirm Username: ")
        self.lblConfirmPassword = tk.Label(self,text="Confirm Password: ")
        self.lblEmail = tk.Label(self,text="Email: ")
        self.txtUsername = tk.Entry(self)
        self.txtConfirmUsername = tk.Entry(self)
        self.txtPassword = tk.Entry(self)
        self.txtConfirmPassword = tk.Entry(self)
        self.txtEmail = tk.Entry(self)
        self.lblAccessLevel = tk.Label(self,text = "Position: ")
        self.var = tk.StringVar()
        options = ["Player","Coach/Captin","Admin"]
        self.var.set(options[0])

        self.cmbAccessLevel = tk.OptionMenu(self, self.var,*options)


        self.txtUsername.grid(row=1,column = 1)
        self.txtConfirmUsername.grid(row=2,column = 1)
        self.txtPassword.grid(row=3,column = 1)
        self.txtConfirmPassword.grid(row=4,column = 1)
        self.txtEmail.grid(row=5,column = 1)
        self.loginButton.grid(row=7,column = 1)
        self.registerButton.grid(row=7,column = 0)
        self.lblUsername.grid(row=1,column = 0)
        self.lblConfirmUsername.grid(row=2,column = 0)
        self.lblPassword.grid(row=3,column = 0)
        self.lblConfirmPassword.grid(row=4,column = 0)
        self.lblEmail.grid(row=5,column = 0)
        self.Title.grid(row=0,column = 0,columnspan=2)
        self.lblAccessLevel.grid(row=6,column =0 )
        self.cmbAccessLevel.grid(row=6,column = 1)

    def register(self):
        username, password, confirmUsername, confirmPassword, Email, AccessLevel, ValidEmail = self.getRegisterData()
        self.addNewUser(username, password, confirmUsername, confirmPassword, Email, AccessLevel, ValidEmail)


    def getRegisterData(self):

        username =  self.txtUsername.get()
        confirmUsername = self.txtConfirmUsername.get()
        password = self.txtPassword.get()
        confirmPassword = self.txtConfirmPassword.get()
        Email = self.txtEmail.get()
        accessLevel = self.var.get()
        ValidEmail = False


        return username, password, confirmUsername, confirmPassword, Email, accessLevel, ValidEmail

    def addNewUser(self,username, password, confirmUsername, confirmPassword, Email, accessLevel, ValidEmail):

        data = {}
        users={}

        if username == confirmUsername and password == confirmPassword :
            with open('data.json', 'r') as fp:
                users = json.load(fp)
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
            userID = str(uuid.uuid4())
            data["Username"] = username
            data["Password"] = hashed_password
            data["Salt"] = salt
            data["Email"] = Email
            data["AccessLevel"] = accessLevel
            data["ValidEmail"] = ValidEmail
            users[userID] = data
            with open('data.json', 'w+') as fp:
                json.dump(users, fp)



class ProfileSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.lblFirstName= tk.Label(self,text=" First Name :")
        self.lblLastName= tk.Label(self,text=" Last Name :")
        self.lblPhoneNumber= tk.Label(self,text=" Phone Number :")
        self.lblAddress= tk.Label(self,text=" Address :")
        self.lblPostcode= tk.Label(self,text=" Postcode :")
        self.lblDateOfBirth= tk.Label(self,text=" Date of Birth :")
        self.txtFirstName = tk.Entry(self)
        self.txtLastName = tk.Entry(self)
        self.txtPhoneNumber = tk.Entry(self)
        self.txtAddress = tk.Entry(self)
        self.txtPostcode = tk.Entry(self)
        self.txtDateOfBirth = tk.Entry(self)


        self.SubmitButton= tk.Button(self, text="Submit",command=lambda: self.addNewPlayer(controller) )
        self.BackButton= tk.Button(self, text="Back",command=lambda: controller.show_frame("Login"))

        self.lblFirstName.grid(row=1,column=0)
        self.lblLastName.grid(row=2,column=0)
        self.lblPhoneNumber.grid(row=3,column=0)
        self.lblAddress.grid(row=4,column=0)
        self.lblPostcode.grid(row=5,column=0)
        self.lblDateOfBirth.grid(row=6,column=0)
        self.txtFirstName.grid(row=1,column=1)
        self.txtLastName.grid(row=2,column=1)
        self.txtPhoneNumber.grid(row=3,column=1)
        self.txtAddress.grid(row=4,column=1)
        self.txtPostcode.grid(row=5,column=1)
        self.txtDateOfBirth.grid(row=6,column=1)
        self.SubmitButton.grid(row=8,column=0,columnspan=2)
        self.BackButton.grid(row=9,column = 0,columnspan = 2)

    def getPlayerData(self):
        firstName = self.txtFirstName.get()
        lastName = self.txtLastName.get()
        phoneNumber = self.txtPhoneNumber.get()
        address = self.txtAddress.get()
        postCode = self.txtPostcode.get()
        DOB = self.txtDateOfBirth.get()



        return firstName , lastName, phoneNumber, address, postCode, DOB

    def addNewPlayer(self,controller):
        global CurrentUser
        firstName , lastName, phoneNumber, address, postCode, DOB = self.getPlayerData()

        data = {}
        players={}

        if self.validPlayerData(firstName , lastName, phoneNumber, address, postCode, DOB) == True :


            with open('players.json', 'r') as fp:
                    players = json.load(fp)
            data["First name"] = firstName
            data["Last name"] = lastName
            data["Phone number"] = phoneNumber
            data["Address"] = address
            data["Post code"] = postCode
            data["Date of Birth"] =DOB
            players[CurrentUser] = data
            print players
            print CurrentUser

            with open('players.json', 'w+') as fp:
                    json.dump(players, fp)

            controller.show_frame("Home")

    def validPlayerData(self,firstName,lastName,phoneNumber,Address,Postcode,dateOfBirth):
        valid = [self.validFirstName(firstName)
        ,self.validLastName(lastName)
        ,self.validPhoneNumber(phoneNumber)
        ,self.validAddress(Address)
        ,self.validPostcode(Postcode)
        ,self.validDateOfBirth(dateOfBirth)]
        for i in valid:
            if i == False :
                return False
        return True

    def validFirstName(self,firstName):
        if len(firstName) <30:
            return True
        else:
            messagebox.showinfo("",firstName +" is not a valid first name.")
            return False
    def validLastName(self,LastName):
        if len(LastName) <30:
            return True
        else:
            messagebox.showinfo("",LastName +" is not a valid Last name.")
            return False

    def validPhoneNumber(self,phoneNumber):
        if phoneNumber.isdigit() == True:
            if phoneNumber[0] == "0" :
                if len(phoneNumber) == 11 :
                    return True
        messagebox.showinfo("",phoneNumber +" is not a valid phone number.")
        return False
    def validAddress(self,address):
        if len(address) < 30:
            return True
        messagebox.showinfo("",address +" is not a valid address.")
        return False
    def validPostcode(self,postcode):

##        if re.match("^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$)",postcode) == False:
            return True
##          messagebox.showinfo(postcode +" is not a valid postcode.")
##        return False

    def validDateOfBirth(self,dateOfBirth):
##        try:
##            datetime.strptime(dateOfBirth, '%d/%m/%Y')
##        except ValueError:
##            messagebox.showinfo("",dateOfBirth +" is not a valid date of birth.")
##            return False
##        if datetime.now() - timedelta(days=2000) > datetime.strptime(dateOfBirth, '%d/%m/%Y'):
##            return True
##        messagebox.showinfo("",dateOfBirth +" is not a valid date of birth.")
##        return False
        return True



class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        self.titleProfile = tk.Label(self,text="My Profile",font=controller.title_font)
        self.lblFirstName= tk.Label(self,text=" First Name :")
        self.lblLastName= tk.Label(self,text=" Last Name :")
        self.lblPhoneNumber= tk.Label(self,text=" Phone Number :")
        self.lblAddress= tk.Label(self,text=" Address :")
        self.lblPostcode= tk.Label(self,text=" Postcode :")
        self.lblDateOfBirth= tk.Label(self,text=" Date of Birth :")
        self.lblTeam = tk.Label(self,text=" Team :")






        self.titleProfile.grid(row = 0 ,column = 0 ,columnspan = 2)
        self.lblFirstName.grid(row=1,column=0)
        self.lblLastName.grid(row=2,column=0)
        self.lblPhoneNumber.grid(row=3,column=0)
        self.lblAddress.grid(row=4,column=0)
        self.lblPostcode.grid(row=5,column=0)
        self.lblDateOfBirth.grid(row=6,column=0)
        self.lblTeam.grid(row=7,column = 0 )
        self.on_show_frame()



    def on_show_frame(self):
        global CurrentUser


        with open('players.json', 'r') as fp:
                    player = json.load(fp)

        data = player[CurrentUser]
        self.lblDataFirstName= tk.Label(self,text ="User Data Not Found ")
        self.lblDataLastName= tk.Label(self,text="User Data Not Found ")
        self.lblDataPhoneNumber= tk.Label(self,text="User Data Not Found ")
        self.lblDataAddress= tk.Label(self,text="User Data Not Found ")
        self.lblDataPostcode= tk.Label(self,text="User Data Not Found ")
        self.lblDataDateOfBirth = tk.Label(self,text="User Data Not Found ")
        self.lblDataTeam = tk.Label(self,text=" Team :")

        self.lblDataFirstName.grid(row=1,column=1)
        self.lblDataLastName.grid(row=2,column=1)
        self.lblDataPhoneNumber.grid(row=3,column=1)
        self.lblDataAddress.grid(row=4,column=1)
        self.lblDataPostcode.grid(row=5,column=1)
        self.lblDataDateOfBirth.grid(row=6,column=1)
        self.lblDataTeam.grid(row=7,column = 1 )
        print data["First name"]
        self.lblDataFirstName.config(text = data["First name"])















class Login(tk.Frame,Home):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.Title = tk.Label(self, text="Please login to your account", font=controller.title_font).grid(row=0,column=0,columnspan=2)
        self.loginButton = tk.Button(self, text="Login",command= lambda:self.checkDetails(controller))
        self.loginButton.grid(row=4,column=1)
        self.registerButton = tk.Button(self, text="Register",command=lambda: controller.show_frame("Register")).grid(row=4,column=0)
        self.lblUsername = tk.Label(self,text="Username: ").grid(row=1,column=0)
        self.lblPassword = tk.Label(self,text="Password: ").grid(row=2,column=0)
        self.txtUsername = tk.Entry(self)
        self.txtUsername.grid(row=1,column = 1)
        self.txtPassword = tk.Entry(self)
        self.txtPassword.grid(row=2,column = 1)

    def checkDetails(self,controller):
        global CurrentUser, AccessLevel
        username = self.txtUsername.get()
        password = self.txtPassword.get()
        with open('data.json', 'r') as fp:
                users = json.load(fp)


        for j,i in enumerate(users ):
            if users[i]["Password"] == hashlib.sha512(password.encode('utf-8') + users[i]["Salt"].encode('utf-8')).hexdigest():

                if users[i]["ValidEmail"] == True :
                    CurrentUser = i
                    AccessLevel = users[i]["AccessLevel"]
                    Home.on_show_frame(self)

                    #controller.show_frame("Home")
                    break
                else :
                    self.ValidateEmail()

                    if users[i]["ValidEmail"] == True :
                        CurrentUser = i
                        AccessLevel = users[i]["AccessLevel"]
                        controller.show_frame("ProfileSetup")
                        break
                    else :
                        messagebox.showinfo("Messgae","You need to confirm your email")
                        break

            elif (j+1) == len(users):
                messagebox.showinfo("Messgae","Username or password incorrect")

    def ValidateEmail(self):
        userID = 0
        responce = True
        if responce == True :
            with open('data.json', 'r') as fp:
                users = json.load(fp)
            users[userID]["ValidEmail"] = True
            with open('data.json', 'w+') as fp:
                json.dump(users, fp)

    def loginSuccessfull(self,user):


        controller.show_frame("Home")











if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
