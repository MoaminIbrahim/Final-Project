from tkinter import *
from tkinter import filedialog
from tkinter import font
import sys
import traceback
from backend import *
from tkinter import messagebox
import time


## initiallizing a variable for opened file name and selected text
global openedName
openedName = False
global selected
selected = False


## conecting to the server
comm = chatComm("86.36.46.10", 15112)
comm.startConnection()

## Login screen class 
class loginScreen():
    def __init__(self,wnd,comm):
## initializing the properties 
        self.scr = wnd
        self.scr.configure(bg = "#17202A")
        self.user = comm
        self.scr.title("Login")
        self.scr.geometry("200x200")
        userlbl = Label(self.scr,text="Username",bg = "#17202A",fg = "#EAECEE")
        self.username = Entry(self.scr,insertbackground="white",bg = "#17202A", fg = "#EAECEE")
        userlbl.pack()
        self.username.pack()
        passlbl = Label(self.scr,text="Password",bg = "#17202A", fg = "#EAECEE")
        self.password = Entry(self.scr,show = "*",insertbackground="white",bg = "#17202A",fg = "#EAECEE")
        passlbl.pack()
        self.password.pack()
        log = Button(self.scr,text="Login",bg = "#17202A",fg = "#EAECEE",command = lambda  : self.login())
        log.pack()
        
## this function Attempts to login creates the Main screen instance if successful or else close the window
        
    def login(self):
        username = self.username.get()
        password = self.password.get()
        if self.user.login(username,password):
            main = MainScreen(self.user,username)
            self.scr.destroy()
        else :
            messagebox.showinfo("login failed","wrong username or password")
          
####------------------------------------------------------------------------------------------------------------------------------------------------------
####------------------------------------------------------------------------------------------------------------------------------------------------------
                 

## this is the mainscreen class that takes a user and a username as parameters   
class MainScreen():
    def __init__(self,user,username):
## innitializing the properties of the main screen
        self.scr = Tk()
        self.scr.configure(bg = "#17202A")
        self.user = user
        self.ongoing = False
## innitializing the list of ongoing chats
        self.currentConvos = []
        self.username = username
        self.title = self.scr.title("main screen")
        AllUsers = Label(self.scr,text = "All Users",bg = "#17202A", fg = "#EAECEE")
        AllUsers.grid(row = 0 , column = 0)
        Friends = Label(self.scr,text = "Your Friends",bg = "#17202A",fg = "#EAECEE")
        Friends.grid(row = 0, column = 1)
        Req = Label(self.scr,text = "Pending Requests",bg = "#17202A", fg = "#EAECEE")
        Req.grid(row = 0, column =2)
        sesh = Label(self.scr,text = "Current Sessions",bg = "#17202A",fg = "#EAECEE")
        sesh.grid(row = 0 , column = 3)
        self.UserList = Listbox(self.scr,height = 15,bg = "#17202A", fg = "#EAECEE")
        self.UserList.grid(row = 2 , column = 0)
        self.FriendList = Listbox(self.scr,height = 15,bg = "#17202A",fg = "#EAECEE")
        self.FriendList.grid(row = 2 , column = 1)
        self.Requests = Listbox(self.scr,height = 15,bg = "#17202A",fg = "#EAECEE")
        self.Requests.grid(row = 2 , column = 2)
        self.currentsesh = Listbox(self.scr,height = 15,bg = "#17202A",fg = "#EAECEE")
        self.currentsesh.grid(row = 2 , column = 3)
        SendReq = Button(self.scr,text = "Send Request",bg = "#17202A", fg = "#EAECEE",command = lambda : self.sendRequest())
        SendReq.grid(row= 22, column =0)
        chat = Button(self.scr,text = "Send Session Request",bg = "#17202A",fg = "#EAECEE",command =  lambda : self.currentConvoCheck())
        chat.grid(row= 22, column =1)
        privsesh = Button(self.scr,text = "Private Session",bg = "#17202A",fg = "#EAECEE",command = lambda : codeScreen("PS",self.user,"PS",None,self))
        privsesh.grid(row = 22, column = 3)
        Accept = Button(self.scr,text = "Accept Friend Request",bg = "#17202A", fg = "#EAECEE",command =  lambda : self.AcceptReq())
        Accept.grid(row= 22, column =2)
## filling the users,friends, requests Lists
        self.fillUsers()
        self.fillFriends()
        self.fillRequests()
## updating the Requests and friend lists periodically
        self.updateRequests(self.Requests.get(0,END),self.Requests,self.user.getRequests())
        self.updateFriendList(self.FriendList.get(0,END),self.FriendList,self.user.getFriends())
## start being alert for chats from remote users
        self.messageManager2()
        
####----------------------Methods------------------------------------------------------------------------
## the next 3 functions fill the request friend and users lists
    def fillRequests(self):    
        requests = self.user.getRequests()
        for req in requests :
            self.Requests.insert(END, req)
    
    def fillFriends(self):
        friends = self.user.getFriends()
        for friend in friends :
            self.FriendList.insert(END,friend)
            
    def fillUsers(self):
        users = self.user.getUsers()
        for user in users :
            self.UserList.insert(END, user)
## the next two functions update the friends list and requests list every second           
    def updateFriendList(self,oldFriends,FriendsBox,NewFriends):
        for i in NewFriends :
            if i not in oldFriends:
                FriendsBox.insert(END,i)
        FriendsBox.after(1000,lambda oldFriends = FriendsBox.get(0,END),FriendsBox = FriendsBox , NewFriends = self.user.getFriends():
                         self.updateFriendList(oldFriends,FriendsBox,NewFriends))

    def updateRequests(self,penReq,reqBox,newReq):
        for i in newReq:
            if i not in penReq :
                reqBox.insert(END,i)
        self.Requests.after(1000,lambda  penReq = reqBox.get(0,END),reqBox = self.Requests , newReq = self.user.getRequests():
                     self.updateRequests(penReq,reqBox,newReq))
        
## this function is called in the case of the user pressing the start chat button
## it checks whether theres an already open chat window with the selected user and opens a chat window if there isnt        
    def currentConvoCheck(self):
            if self.FriendList.curselection() == ():
                self.info("Select a friend from the list","Code session start failed")
            else:
                if self.FriendList.get(self.FriendList.curselection()) not in self.currentConvos :
                    self.user.sendMessage(self.FriendList.get(self.FriendList.curselection()),"seshReq")
                else:
                    self.info("session already in progress","Code session start failed")

## this function connects every interaction to its specified function or tasks 
    def messageManager2(self):
        messages = self.user.getMail()[0]
        for (u,m) in messages:
            if u not in self.currentConvos:
                msg = m.split("#")
                if msg[0] == "seshReq":
                    msgb = self.askq(u+" invites you to a coding session","Session Request")
                    if msgb == "yes":
                        self.user.sendMessage(u,"seshReqReply#yes")
                        self.currentConvos.append(u)
                        self.currentsesh.insert(END,u)
                        self.base = 2
                        window = codeScreen(u,self.user,self.username,None,self)
                    if msgb == "no":
                        self.user.sendMessage(u,"seshReqReply#no")
                elif msg[0] == "seshReqReply" :
                    if msg[1] == "yes":
                        self.info(u+" has accepted your session request","accepted seesion request")
                        self.currentConvos.append(u)
                        self.currentsesh.insert(END,u)
                        self.base = 1
                        window = codeScreen(u,self.user,self.username,None,self)
                    elif msg[1] == "no":
                        self.info(u+" has declined your session request","declined session request")

        self.scr.after(100,lambda:self.messageManager2())
                    
## this function opens a dialog without the root window popping outside
    def info(self,message, title):
        root = Tk()
        root.overrideredirect(1)
        root.withdraw()
        messagebox.showinfo(title, message)
        root.destroy()
    def askq(self,message, title):
        root = Tk()
        root.overrideredirect(1)
        root.withdraw()
        msgq = messagebox.askquestion(title, message)
        root.destroy()
        return msgq
##this function sends a request and show a mesage box
    def sendRequest(self):
        if self.UserList.curselection() == ():
            self.info("Select a user from the list","Request status")
        else :
            self.user.sendFriendRequest(self.UserList.get(self.UserList.curselection()))
            self.info("Request to "+self.UserList.get(self.UserList.curselection())+" sent succesflly","Request status")
##this function accepts a request then deletes it from the requests list and adds it to friends  and show a mesage box
    def AcceptReq(self):
        if self.Requests.curselection() == ():
            self.info("Select a request from the list of requests","Request status")
        else:
            self.user.acceptFriendRequest(self.Requests.get(self.Requests.curselection()))
            self.info("Request from "+self.Requests.get(self.Requests.curselection())+" accepted succesflly","Request status")
            self.Requests.delete(self.Requests.curselection())

##this is the text editor clas
class codeScreen:
    def __init__(self,friend,user,username,file,main):
        self.root = Tk()
        self.main = main
        self.user = user
        self.username = username
        self.friend = friend
        self.file = file          
        self.my_frame = Frame(self.root)
        self.my_frame.grid(row = 0,column = 0,pady = 5)
        self.outpframe = Frame(self.root)
        self.outpframe.grid(row = 0 ,column = 1,pady = 5)
        ##scrollbar
        self.text_scroll = Scrollbar(self.my_frame)
        self.text_scroll.pack(side = RIGHT, fill = Y)
        self.hor_scroll = Scrollbar(self.my_frame,orient = "horizontal")
        self.hor_scroll.pack(side=BOTTOM,fill = X)
        ##code text widget
        self.myText = Text(self.my_frame, width = 100, height = 35,
                  selectbackground = "yellow",selectforeground = "black", undo = True,
                  yscrollcommand = self.text_scroll.set, wrap ="none",xscrollcommand = self.hor_scroll.set)
        self.myText.pack()
        self.text_scroll.config(command = self.myText.yview)
        self.hor_scroll.config(command = self.myText.xview)
        ##output scroll
        self.outp_scroll = Scrollbar(self.outpframe)
        self.outp_scroll.pack(side = RIGHT, fill = Y)
        self.outphor_scroll = Scrollbar(self.outpframe,orient = "horizontal")
        self.outphor_scroll.pack(side=BOTTOM,fill = X)
         ##outp text
        self.outp = Text(self.outpframe, width = 35, height = 35,
                  selectbackground = "yellow",selectforeground = "black", undo = True,
                  yscrollcommand = self.outp_scroll.set,xscrollcommand = self.outphor_scroll.set)
        self.outp.pack()
        if self.friend == "PS":
            self.root.title("Private Session")
        else:
            self.main.ongoing = True
            self.root.title(self.username+" Session with "+friend)
            self.checkText()
        ## create menu  
        self.menu = Menu(self.root)
        self.root.config(menu = self.menu)
        ## file menu
        self.fileMenu = Menu(self.menu, tearoff =False)
        self.menu.add_cascade(label = "File",menu = self.fileMenu)
        self.fileMenu.add_command(label = "New",command = lambda : self.newFile())
        self.fileMenu.add_command(label = "Open",command = lambda : self.openFile())
        self.fileMenu.add_command(label = "Save", command = lambda : self.saveFile())
        self.fileMenu.add_command(label = "Save As",command = lambda : self.saveAs())
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Exit",command = self.root.destroy)
        ##edit menu
        self.editMenu = Menu(self.menu,tearoff =False)
        self.menu.add_cascade(label = "Edit",menu = self.editMenu)
        self.editMenu.add_command(label = "Cut",command = lambda : self.cutText(False),accelerator = "(Ctrl+x)")
        self.editMenu.add_command(label = "Copy",command = lambda : self.copyText(False),accelerator = "(Ctrl+c)")
        self.editMenu.add_command(label = "Paste       ",command = lambda : self.pasteText(False),accelerator = "(Ctrl+v)")
        self.editMenu.add_separator()
        self.editMenu.add_command(label = "Undo",command = self.myText.edit_undo,accelerator = "(Ctrl+z)")
        self.editMenu.add_command(label = "Redo",command = self.myText.edit_redo,accelerator = "(Ctrl+y)")
        self.editMenu.add_separator()
        self.editMenu.add_command(label = "Select All",command = lambda: self.selectAll(),accelerator = "(Ctrl+a)")
        ##status bar
        self.statusbar = Label(self.root,text = "Ready        ",anchor = E)
        self.statusbar.grid(row = 1,column = 1)
        ##night mode
        self.optionsMenu = Menu(self.menu, tearoff =False)
        self.menu.add_cascade(label = "Options",menu = self.optionsMenu)
        self.optionsMenu.add_command(label = "Night Mode On",command = lambda: self.nightOn())
        self.optionsMenu.add_command(label = "Night Mode Off",command = lambda: self.nightOff())
        self.optionsMenu.add_separator()
        self.optionsMenu.add_command(label = "Run Module",command = lambda :self.run(False))
        self.cursor = self.myText.index(INSERT)
        self.checkCursor()
        self.messageManager()
        self.secondCurs = "0.0"
        self.root.protocol("WM_DELETE_WINDOW", lambda :self.onClosing())
        if self.file:
            self.myText.insert(END,file)
        ##edit bindings
        self.root.bind("<Key>",self.keys)
        self.myText.bind("<Tab>",self.keys)
## bind tab button        
        self.root.bind("<F5>",self.run)
        self.root.bind("<Control-Key-x>",self.cutText)
        self.root.bind("<Control-Key-c>",self.copyText)
        self.root.bind("<Control-Key-v>",self.pasteText)
        self.root.mainloop()
#### methods
##this function deals with thee event of exiting the session        
    def onClosing(self):
        if self.friend != "PS":
            self.user.sendMessage(self.friend,self.friend+"#SessionExit")
            self.main.currentConvos.remove(self.main.currentConvos[-1])
            self.main.currentsesh.delete(END)
            self.main.ongoing = False
            self.root.destroy()
        else:
            self.main.ongoing = False
            self.root.destroy()
## this function sends the inputs of the user to the other user
    def keys(self,e):
        key = e.keysym
        if self.friend == "PS":
            pass
        else:
            self.user.sendMessage(self.friend,"#key#"+key+"#"+self.cursor+"#"+str(time.time()))
## this function inserts the other users changes on the screen    
    def secondKeys(self,key,pos):
        speshChar = {"asciitilde":"~","exclam":"!","at":"@","numbersign":"#","dollar":"$","percent":"%","asciicircum":"^","ampersand":"&",
                     "asterisk":"*","parenleft":"(","parenright":")","underscore":"_","plus":"+","braceright":"}",
                     "braceleft":"{","colon":":","quotedbl":'"',"bar":"|","question":"?","greater":">","less":"<",
                     "quoteleft":"`","minus":"-","equal":"=","bracketright":"]","bracketleft":"[",
                     "backslash":"\\","quoteright":"'","semicolon":";","slash":"/","period":".","comma":",","Return":"\n","Tab":"                   "}
        if key in speshChar:
            self.myText.insert(pos,speshChar[key])
        elif key in [chr(i) for i in range(127)] :
            self.myText.insert(pos,key)
        elif key == "BackSpace":
            self.myText.delete(pos)
        elif key == "space":
            self.myText.insert(pos," ")
## this function deals with the interactions between the users during the session
    def messageManager(self):
        messages = self.user.getMail()
        for (u,m) in messages[0]:
            if u == self.friend:
                msg = m.split("#")
                keys = {}
                lst = []
                for i in range(len(msg)):
                    if msg[i] == "key":
                        keys[msg[2]] = msg[3]+"#"+msg[4]
                        lst.append(float(msg[4]))
                if msg[0] == "newfile":
                    a = self.main.askq(u+" wants to open a new file","New file request")
                    if a == "yes":
                        self.user.sendMessage(u,"newfileReply#yes")
                        self.myText.delete("1.0",END)
                        self.root.title("New File - momenHub")
                        self.statusbar.config(text = "New File")
                    elif a == "no":
                        self.user.sendMessage(u,"newfileReply#no")
                elif msg[0] == "newfileReply":
                    if msg[1] == "yes":
                        self.myText.delete("1.0",END)
                        self.root.title("New File - momenHub")
                        self.statusbar.config(text = "New File")
                    else:
                        self.main.info(u+" has declined your new file request","file request denied")
                elif msg[0][:5] == "CHECK":
                    self.myText.delete("1.0",END)
                    self.myText.insert(END,msg[0][5:])
                elif msg[0][:3] == "RUN":
                    self.myText.delete("1.0",END)
                    self.myText.insert(END,msg[0][3:])
                    self.remoterun()  
                elif msg[1] == "cursor":
                    position = msg[2]
                    self.secondCurs = position
                    self.secondCursor(position)
                    
                elif msg[1] == "SessionExit":
                    msgb = self.main.askq(msg[0]+" has left the seesion\n would you like to switch to a private seesion?",
                                          msg[0]+" left the session")
                    if msgb == "yes":
                        file = self.myText.get("1.0","end-1c")
                        self.main.currentConvos.remove(self.main.currentConvos[-1])
                        self.main.currentsesh.delete(END)
                        self.root.destroy()
                        codeScreen("PS","PS","PS",file,self)
                    elif msgb == "no":
                        self.main.currentConvos.remove(self.main.currentConvos[-1])
                        self.main.currentsesh.delete(END)
                        self.root.destroy()
                else:
                    pass

                lst = sorted(lst)
                for n in lst:
                    for key in keys:
                        if str(n) in keys[key]:
                            self.secondKeys(key,keys[key].split("#")[0])
        for (u,f) in messages[1]:
            if u == self.friend:
                global openedName
                openedName = f
                name = f
                self.root.title(name)
                ## removing the C     
                self.statusbar.config(text = name)
                self.myText.delete("1.0",END)
                ## open file
                textFile = open(f,"r")
                content = textFile.read()
                self.myText.insert(END,content)
                textFile.close()
                
        self.myText.after(100,lambda:self.messageManager())
## new file    
    def newFile(self):
        global openedName
        openedName = False
        if self.friend == "PS":
            self.myText.delete("1.0",END)
            self.root.title("New File - momenHub")
            self.statusbar.config(text = "New File")
        else:
            self.user.sendMessage(self.friend,"newfile")
## open file
    def openFile(self):
        ## need to ask where to open
        textFile = filedialog.askopenfilename(title = "Open File", filetypes =(("Python Files","*.py"),("Text Files","*.txt")))
        if textFile:
        ## same as current convos        
            global openedName
            openedName = textFile
            name = textFile
            if self.friend != "PS":
                self.user.sendFile(self.friend,name)
            self.root.title(name)
            ## removing the C     
            self.statusbar.config(text = name)
            self.myText.delete("1.0",END)
            ## open file
            textFile = open(textFile,"r")
            content = textFile.read()
            self.myText.insert(END,content)
            textFile.close()
## save as     
    def saveAs(self):
        textFile = filedialog.asksaveasfilename(defaultextension = ".py",
            title = "Save File As",filetypes =(("Python Files","*.py"),("Text Files","*.txt")))
        if textFile :
            name = textFile
            self.root.title(name)
            self.statusbar.config(text = "Saved: "+name)
            textFile = open(textFile,"w")
            textFile.write(self.myText.get("1.0",END))
            textFile.close()
##save file            
    def saveFile(self):
        global openedName
        if openedName:
            textFile = open(openedName,"w")
            textFile.write(self.myText.get("1.0",END))
            textFile.close()
            self.statusbar.config(text = "Saved: "+openedName)
        else:
            self.saveAs()
## this functions maintanes the indenticality of the two users screens 
    def checkText(self):
        if self.main.base == 1:
            lines = self.myText.get("1.0","end-1c")
            self.user.sendMessage(self.friend,"CHECK"+lines)
            self.myText.after(5000,lambda :self.checkText())
        elif self.main.base == 2:
            lines = self.myText.get("1.0","end-1c")
            self.user.sendMessage(self.friend,"CHECK"+lines)
            self.myText.after(8000,lambda :self.checkText())
## cut text
    def cutText(self,e):
        global selected
        if e :
            selected = self.root.clipboard_get()
        else:
            if self.myText.selection_get():
                selected = self.myText.selection_get()
                self.myText.delete("sel.first","sel.last")
                self.root.clipboard_clear()
                self.root.clipboard_append(selected)
## copy text
    def copyText(self,e):
        global selected
        if e :
            selected = self.root.clipboard_get()
        else:
            if self.myText.selection_get():
                selected = self.myText.selection_get()
                self.root.clipboard_clear()
                self.root.clipboard_append(selected)

##paste text
    def pasteText(self,e):
        global selected
        if e:
            selected = self.root.clipboard_get()
        else:
            if selected:
                position = self.myText.index(INSERT)
                self.myText.insert(position,selected)
##select all
    def selectAll(self):
        self.myText.tag_add("sel","1.0",END)
##night mode on
    def nightOn(self):
        mainColor = "grey"
        secondColor = "#373737"
        self.root.config(bg = mainColor)
        text_color = "white"
        self.statusbar.config(bg = mainColor,fg = text_color)
        self.myText.config(bg = secondColor,insertbackground = "white",fg = "white")
        self.fileMenu.config(bg = mainColor,fg = text_color)
        self.editMenu.config(bg = mainColor,fg = text_color)
        self.optionsMenu.config(bg = mainColor,fg = text_color)
        ##OUTP
        self.outp.config(bg = secondColor,insertbackground = "white",fg = "white")
##night mode off
    def nightOff(self):
        mainColor = "SystemButtonFace"
        secondColor = "SystemButtonFace"
        self.root.config(bg = mainColor)
        text_color = "black"
        self.statusbar.config(bg = mainColor,fg = text_color)
        self.myText.config(bg = "white",fg = "black",insertbackground = "black")
        self.outp.config(bg = "white",fg = "black")
        self.fileMenu.config(bg = mainColor,fg = text_color)
        self.editMenu.config(bg = mainColor,fg = text_color)
        self.optionsMenu.config(bg = mainColor,fg = text_color)
## this function check if the cursor position changed
    def checkCursor(self):
        if self.friend != "PS":
            pos = self.myText.index(INSERT)
            if pos != self.cursor:
                self.cursor = self.myText.index(INSERT)
                self.user.sendMessage(self.friend,"#cursor#"+pos)
            self.myText.after(50,lambda:self.checkCursor())

## highlight where the cursor is from the second user
    def blink(self,hig,line,char):
        if self.friend != "PS":
            self.myText.tag_add(hig,line+"."+str(int(char)-1))
            if line+"."+str(int(char)) == self.secondCurs:
                self.myText.tag_config(hig, background="yellow", foreground="blue")
                self.myText.after(1000,lambda : self.myText.after(500,self.myText.tag_config(hig, background="white", foreground="black")
                                                                  ,self.myText.tag_delete(hig)))
## this function works with the blink function to highlight where the cursor is        
    def secondCursor(self,position):
        if self.friend != "PS":
            line = ""
            while position[0] != ".":
                   line+=position[0]
                   position = position[1:]
            char = position[1:]
            hig = self.myText.get(line+"."+str(int(char)-1))         
            self.blink(hig,line,char)
                
            self.myText.mark_set(INSERT, self.cursor)
## this function is for the case of the other user running the code
    def remoterun(self):
        lines = self.myText.get("1.0","end-1c")
        a = sys.stdout
        sys.stdout = open("file.txt","w")
        try :
            print("<<<<"+self.friend+" is running the code>>>>")
            exec(lines,{})
        except Exception as err:
            print("<<<<"+self.friend+" is running the code>>>>")
            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            print("%s at line %d : %s" % (error_class, line_number, detail))
        finally :
            sys.stdout = a
            file = open("file.txt","r")
            file.seek(0)
            output = "".join(file.readlines())
            if output:
                self.outp.config(state = NORMAL)
                self.outp.insert(END,output)
            file.close()
## this function runs the code from the user
    def run(self,e):
        lines = self.myText.get("1.0","end-1c")
        if self.friend != "PS":
            self.user.sendMessage(self.friend,"RUN"+lines)
        a = sys.stdout
        sys.stdout = open("file.txt","w")
        try :
            exec(lines,{})
        except Exception as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            print("%s at line %d : %s" % (error_class, line_number, detail))
        finally :
            sys.stdout = a
            file = open("file.txt","r")
            file.seek(0)
            output = "".join(file.readlines())
            if output:
                self.outp.config(state = NORMAL)
                self.outp.insert(END,output)
            file.close()   
## start the program
wnd = Tk()
loginScreen(wnd,comm)
wnd.mainloop()
