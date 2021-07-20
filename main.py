import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QSvgWidget
from animated_toggle import AnimatedToggle
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

import sys, time, threading,os

import socket, errno
import mysql.connector, sqlite3
from win10toast_click import ToastNotifier
import sip 
from pygame import mixer
from mutagen.mp3 import MP3
import cv2
from PIL import Image


dirfile = os.environ['APPDATA']
if os.path.exists(f"{dirfile}\\Chat") == False :
        os.mkdir(f"{dirfile}\\Chat")
if os.path.exists(f"{dirfile}\\Chat\\imgFrind") == False :
        os.mkdir(f"{dirfile}\\Chat\\imgFrind")
if os.path.exists(f"{dirfile}\\Chat\\fileMessage") == False :
        os.mkdir(f"{dirfile}\\Chat\\fileMessage")
if os.path.exists(f"{dirfile}\\Chat\\tempData") == False :
        os.mkdir(f"{dirfile}\\Chat\\tempData")
dirfile = f"{dirfile}\\chat"
dirImage = f"{dirfile}\\imgFrind"
tempData = f"{dirfile}\\tempData"
fileMessagef =f"{dirfile}\\fileMessage"



Frind = []
_my_username = "Mohammad"
_myData = {}
_message = ""
_stateEnd = False
sendTo = ""
indexSendTo = 0
StateConnect = False
menuaction = 0
_LogOut = 0
_selectfrind= 0
_listShat = []
namefrindFileUpdate = ""
stateFileDownloade = False
fileDirCope = ""
notifi = ToastNotifier()
blockStat = 0
_startAnimation1 = False
_isStart = False
selectchate = False
indexchatShow = 0
mixer.init()
sliderChange = 0
sliderChangeStop = False
openMusic  = ''
nameplay = ''
startSund=False
ListSund = []
listVidoeShow = []

AddFrind = {}

class LoginScren(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("shate")

        
        self.setStyleSheet("""QMainWindow{background-image: url(img/main.svg);color:#fff;}QLable{color:#fff;}""")
        self.UI()
        self.show()
        threading.Thread(target=self.connectDB).start()
        self.dblite = sqlite3.connect(f"{dirfile}\\chat.db")
        self.curdblist = self.dblite.cursor()
        self.IMAGE = "img/gg.png"
        
        
    
    def connectDB(self):
        self.db = mysql.connector.connect(user='root', password='123456', host='localhost',port=3307, db="chat")
        self.curdb = self.db.cursor(buffered=True)
        print("connectDB")
    
        
    def UI(self):
        
        mainFrame = QFrame()
        mainFrame.setStyleSheet(u"""
                                     background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 0));
                                     
                                     """)
       
        mainFrame.resize(800,376)
        mainFrame.move(100,70)
        
        mainFrameLayout = QHBoxLayout()
        liftFrame = QFrame()
        liftFrame.setStyleSheet("background-color:#fff;")
        rightFrame = QFrame()

        
        liftFrameLayout = QVBoxLayout()
        rightFrameLayout = QVBoxLayout()
        liftFrameLayoutBottom = QHBoxLayout()
        
        usernamLable = QLabel("UserName")
        usernamLable.setStyleSheet("QLabel{color: #8c8c8c}")
        self.username = QLineEdit()
        self.username.setStyleSheet("QLineEdit{ border-radius:10px;background-color: #e6e6e6;border:2px solid rgb(255, 85, 255);color:#333333;}")
        self.username.setContentsMargins(5,0,10,0)
        self.username.setTextMargins(5,0,0,0)
        self.username.setMinimumHeight(25)
        passwordLable = QLabel("Password")
        passwordLable.setStyleSheet("QLabel{color: #8c8c8c}")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("QLineEdit{ border-radius:10px;background-color: #e6e6e6;border:2px solid rgb(255, 85, 255);color:#333333;}")
        self.password.setContentsMargins(5,0,10,0)
        self.password.setTextMargins(5,0,0,0)
        self.password.setMinimumHeight(25)
        self.Check = QCheckBox("One-time registration")
        self.Check.setStyleSheet(self.CheckStyal())
        
        self.spinnerLoginScreen = QSvgWidget("img/LoginScreen.svg")

        
        self.createAcont = QPushButton("Create Acount")
        self.createAcont.clicked.connect(self.CreateAcont)
        self.createAcont.setStyleSheet(self.createAcontStyal())
        self.login = QPushButton("Login")
        self.login.setStyleSheet(self.loginStyal())
        self.login.setMinimumHeight(20)
        self.login.setMinimumWidth(150)
        self.login.clicked.connect(self.getLogin)
        
        self.loginWrong = QLabel("The username or password is wrong")
        self.loginWrong.setStyleSheet("QLabel{color:#ff4d4d;}")
        self.loginWrong.hide()


        mainFrame.setContentsMargins(0,0,0,0)
        mainFrameLayout.setContentsMargins(0,0,0,0)
        liftFrameLayout.setContentsMargins(20,0,0,0)
        rightFrameLayout.setContentsMargins(0,0,0,0)
        liftFrameLayoutBottom.setContentsMargins(0,30,10,0)
        passwordLable.setContentsMargins(0,10,0,0)
        
        
        liftFrameLayoutBottom.addWidget(self.createAcont)
        liftFrameLayoutBottom.addWidget(self.login)

        liftFrameLayout.addStretch()
        liftFrameLayout.addWidget(usernamLable)
        liftFrameLayout.addWidget(self.username)
        liftFrameLayout.addWidget(passwordLable)
        liftFrameLayout.addWidget(self.password)
        liftFrameLayout.addWidget(self.Check)
        liftFrameLayout.addLayout(liftFrameLayoutBottom)
        liftFrameLayout.addWidget(self.loginWrong)
        liftFrameLayout.addStretch()
        
        rightFrameLayout.addWidget(self.spinnerLoginScreen)
        
        liftFrame.setLayout(liftFrameLayout)
        rightFrame.setLayout(rightFrameLayout)
        

        mainFrameLayout.addWidget(liftFrame,40)
        mainFrameLayout.addWidget(self.spinnerLoginScreen,60)
        mainFrameLayout.setSpacing(0)

        
        mainFrame.setLayout(mainFrameLayout)
        
        ####################################################################
        ####################################################################
        CreatemainLau = QVBoxLayout()
        
        CreatemainFrame = QFrame()
        CreatemainFrame.setStyleSheet(u"""
                                     QFrame{background-color:  #fff;
                                     }
                                     """)
       
        CreatemainFrame.resize(800,376)
        CreatemainFrame.move(100,70)
        
        CreatemainFrameLayout = QHBoxLayout()
        CreateliftFrame = QFrame()
        CreaterightFrame = QFrame()
        
        CreateliftFrameLayout = QVBoxLayout()
        CreaterightFrameLayout = QVBoxLayout()
        CreateliftFrameLayoutBottom = QHBoxLayout()
        CreatenamLable = QLabel("Name")
        CreatenamLable.setStyleSheet("QLabel{color: #8c8c8c}")
        self.Createname = QLineEdit()
        self.Createname.setStyleSheet("QLineEdit{ border-radius:10px;background-color: #e6e6e6;border:2px solid rgb(255, 85, 255);color:#333333;}")
        self.Createname.setContentsMargins(5,0,10,0)
        self.Createname.setTextMargins(5,0,0,0)
        self.Createname.setMinimumHeight(25)
        CreateusernamLable = QLabel("UserName")
        CreateusernamLable.setStyleSheet("QLabel{color: #8c8c8c}")
        self.Createusername = QLineEdit()
        self.Createusername.textChanged.connect(self.CreateusernameChanged)
        self.Createusername.setStyleSheet("QLineEdit{ border-radius:10px;background-color: #e6e6e6;border:2px solid rgb(255, 85, 255);color:#333333;}")
        self.Createusername.setContentsMargins(5,0,10,0)
        self.Createusername.setTextMargins(5,0,0,0)
        self.Createusername.setMinimumHeight(25)
        self.CreateusernameFound = QLabel("Username is already in use")
        self.CreateusernameFound.setStyleSheet("font-size:11px;color:#ff4d4d;")
        self.CreateusernameFound.hide()
        CreatepasswordLable = QLabel("Password")
        CreatepasswordLable.setStyleSheet("QLabel{color: #8c8c8c}")
        self.Createpassword = QLineEdit()
        self.Createpassword.setStyleSheet("QLineEdit{ border-radius:10px;background-color: #e6e6e6;border:2px solid rgb(255, 85, 255);color:#333333;}")
        self.Createpassword.setContentsMargins(5,0,10,0)
        self.Createpassword.setTextMargins(5,0,0,0)
        self.Createpassword.setMinimumHeight(25)
        self.Createpassword.setEchoMode(QLineEdit.Password)
        CreaterepasswordLable = QLabel("Confirm Password")
        CreaterepasswordLable.setStyleSheet("QLabel{color: #8c8c8c}")
        self.Createrepassword = QLineEdit()
        self.Createrepassword.setStyleSheet("QLineEdit{ border-radius:10px;background-color: #e6e6e6;border:2px solid rgb(255, 85, 255);color:#333333;}")
        self.Createrepassword.setContentsMargins(5,0,10,0)
        self.Createrepassword.setTextMargins(5,0,0,0)
        self.Createrepassword.setMinimumHeight(25)
        self.Createrepassword.setEchoMode(QLineEdit.Password)
        self.Createrepassword.textChanged.connect(self.CreaterepasswordChanged)

        
        self.spinnerSinginScreen = QSvgWidget("img/SinginScreen.svg")

 
        #####################################################
        self.addImage = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.addImage.sizePolicy().hasHeightForWidth())
        self.addImage.setSizePolicy(sizePolicy)
        self.addImage.setStyleSheet("""
                                    QPushButton{border-image: url('img/AddImage.png');
                                                border-radius: 25px;
                                                background-color: rgba(255, 255, 255,70);
                                                padding: 100px;
                                                }
                                    QPushButton:hover{background-color: #80dfff}
                                    """)
        #self.addImage.setMargin(20)
        self.addImage.setContentsMargins(20,20,20,20)
        #self.addImage.setMargi
       

        #self.addImage.setScaledContents(True)

        self.addImage.setFixedSize(55,55)
        self.addImage.clicked.connect(self.AddImage)
        
        addImageLayout = QHBoxLayout()
        addImageLayout.setAlignment(Qt.AlignCenter)
        
        addImageLayout.addWidget(self.addImage)
        
        #####################################################
        self.Createlogin = QPushButton("Login")
        self.Createlogin.clicked.connect(self._Createlogin)
        self.Createlogin.setStyleSheet(self.createAcontStyal())
        self.CreatecreateAcont = QPushButton("Create Acount")
        self.CreatecreateAcont.setStyleSheet(self.loginStyal())
        self.CreatecreateAcont.setMinimumHeight(20)
        self.CreatecreateAcont.setMinimumWidth(150)
        self.CreatecreateAcont.clicked.connect(self.getCreateAcount)
        
        
        CreatemainLau.setContentsMargins(0,0,0,0)
        CreatemainFrame.setContentsMargins(0,0,0,0)
        CreatemainFrameLayout.setContentsMargins(0,0,0,0)
        CreateliftFrameLayout.setContentsMargins(20,0,0,0)
        CreaterightFrameLayout.setContentsMargins(0,0,0,0)
        CreateliftFrameLayoutBottom.setContentsMargins(0,30,10,0)
        CreatepasswordLable.setContentsMargins(0,10,0,0)
        
        CreateliftFrameLayoutBottom.addWidget(self.Createlogin)
        CreateliftFrameLayoutBottom.addWidget(self.CreatecreateAcont)

        CreateliftFrameLayout.addStretch()
        CreateliftFrameLayout.addLayout(addImageLayout)
        CreateliftFrameLayout.addWidget(CreateusernamLable)
        CreateliftFrameLayout.addWidget(self.Createusername)#CreateusernameFound
        CreateliftFrameLayout.addWidget(self.CreateusernameFound)#CreateusernameFound
        CreateliftFrameLayout.addWidget(CreatenamLable)
        CreateliftFrameLayout.addWidget(self.Createname)     
        CreateliftFrameLayout.addWidget(CreatepasswordLable)
        CreateliftFrameLayout.addWidget(self.Createpassword)
        CreateliftFrameLayout.addWidget(CreaterepasswordLable)
        CreateliftFrameLayout.addWidget(self.Createrepassword)
        CreateliftFrameLayout.addLayout(CreateliftFrameLayoutBottom)
        CreateliftFrameLayout.addStretch()
        
        CreaterightFrameLayout.addWidget(self.spinnerSinginScreen,80)
        
        CreateliftFrame.setLayout(CreateliftFrameLayout)
        CreaterightFrame.setLayout(CreaterightFrameLayout)
        
        
        CreatemainFrameLayout.addWidget(CreateliftFrame,40)
        CreatemainFrameLayout.addWidget(self.spinnerSinginScreen,60)
        
        CreatemainFrame.setLayout(CreatemainFrameLayout)
        ####################################################################
        ####################################################################
        self.HH = QHBoxLayout()
        self.HH.setContentsMargins(50,50,50,50)
        self.Stack = QStackedWidget()
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        
        self.Stack.addWidget(mainFrame)
        self.Stack.addWidget(CreatemainFrame)
        self.Stack.setCurrentIndex(0)
        
        self.HH.addWidget(self.Stack)
        
        w = QWidget()
        w.setLayout(self.HH)
        w.setStyleSheet("QLable{color:#fff;}")
        self.setCentralWidget(w)
        
    def CreaterepasswordChanged(self,text):
        password = self.Createpassword.text()
        if password != text:
            self.Createrepassword.setStyleSheet("QLineEdit{ border-radius:10px;background-color: #e6e6e6;border:2px solid red;color:#333333;}")
        else:
            self.Createrepassword.setStyleSheet("QLineEdit{ border-radius:10px;background-color: #e6e6e6;border:2px solid rgb(255, 85, 255);color:#333333;}")
           
    def AddImage(self):
        file = "Sound Files (*.png *.jfif *.jpg) ;;All Files (*)"
        directory, ok = QFileDialog.getOpenFileName(self, "Add Image", "", file)
        if ok:
            print(directory)
            basename = os.path.basename(directory)
            namedir = os.path.dirname(directory)
            imgtype = basename.split(".")[-1]
            imgname =basename.split(f".{imgtype}")[0]
            print(imgtype)
            print(imgname)
            print(namedir+"/"+imgname+"."+imgtype)
            self.IMAGE = directory
            self.addImage.setStyleSheet("""
                                    border-image: url('{}');
                                                border-radius: 25px;
                                                background-color: rgba(255, 255, 255,70);
                                                padding: 100px;
                                                """.format(directory))
    def CreateusernameChanged(self, text):
        self.curdb.execute(f"SELECT username FROM user WHERE username='{text}'")
        frind = self.curdb.fetchall()
        print(frind)
        if frind != []:
            self.CreateusernameFound.show()
            self.CreateusernameFound.setText("Username is already in use")
            self.Createusername.setStyleSheet("QLineEdit{ border-radius:10px;background-color: #e6e6e6;border:2px solid red;color:#333333;}")
        else:
            self.CreateusernameFound.hide()
            self.CreateusernameFound.setText("")
            self.Createusername.setStyleSheet("QLineEdit{ border-radius:10px;background-color: #e6e6e6;border:2px solid rgb(255, 85, 255);color:#333333;}")
            
    
    def createAcontStyal(_):
        return"""
            QPushButton{
                color: #800080;
                background-color: #fff;
                border : 1px solid #fff;
            }
            QPushButton:hover{
                color: #0088cc;
                background-color: #fff;
                border : 1px solid #fff;
            }
    
    """ 
    def loginStyal(_):
        return"""
        QPushButton{
                color: #fff;
                background-color: rgb(55, 42, 111);
                border : 1px solid rgb(55, 42, 111);
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
        QPushButton:hover{
                color: #0088cc;
                background-color: #fff;
                border : 1px solid #fff;
            }
    """
    def CheckStyal(_):
        return"""
        QCheckBox{
                color:#8c8c8c;
                background-color:#fff;
            }
        QCheckBox:hover{
                color: rgb(55, 42, 111);
                background-color:#fff;
            }
    """
    def CreateAcont(self):
        self.Stack.setCurrentIndex(1)
    def _Createlogin(self):
        self.Stack.setCurrentIndex(0)
        
        
    def getLogin(self):
        global _my_username, Frind, _myData
        self.login.setText("Loading...")
        self.connectDB()
        username = self.username.text()
        password = self.password.text()
        print(f"{username}\n{password}")
        self.curdb.execute(f"SELECT username FROM user WHERE username='{username}' AND password='{password}';")
        state = self.curdb.fetchone()
        print(f"state :{state}")
        if state != [] and state != None:
            ############ clear Data sqlte
            self.curdblist.execute("DELETE FROM frind;")
            self.curdblist.execute("DELETE FROM messages;")
            self.curdblist.execute("DELETE FROM myData;")
            self.dblite.commit()
            
            self.curdb.execute(f"select * from user where username='{username}'")
            myData = self.curdb.fetchone()
            self.curdb.execute(f"select * from frind where username='{username}'")
            myFrind = self.curdb.fetchall()
            self.curdb.execute(f"select * from messages where username='{username}'")
            myChat = self.curdb.fetchall()
            print(f"myData: {myData}\n")        
            print(f"myFrind: {myFrind}\n")        
            # print(myChat)
            if  not self.Check.isChecked():
                self.curdblist.execute("INSERT INTO myData VALUES(?,?,?,?)",(myData[0],myData[1],myData[4],myData[2]))
            _my_username = myData[0]
            _myData = {"username":myData[0], "name":myData[1], "img":myData[2],"bio":myData[4]}
            print("\n\n0")
            if myFrind != []:
                Frind = []
                c1 = []
                for index, i in enumerate(myFrind):
                    try:
                        print(f"\n\n1 {i}")
                        self.curdb.execute(f"select name,image,bio,stateConnect from user where username='{i[1]}'")
                        Nameimage = self.curdb.fetchone()
                        print(f"\nNameimage:{Nameimage}\n")
                        # print(f"Nameimage[4] :{Nameimage[4]}")
                        c1.append(i[0])
                        _dirImage = dirImage.replace("\\","/")
                    
                        Frind.append({
                        i[1]:{"id":i[1],"name":Nameimage[0], "img":f"{_dirImage}/{Nameimage[1]}","bio":f"{Nameimage[2]}", "chat":[],"statechat":f"{Nameimage[3]}","block":f"{i[4]}"}
                        })
                    
                        self.curdb.execute(f"select state,message,time from messages where username='{username}' AND sendto='{i[1]}'")
                        chat = self.curdb.fetchall()
                        print("\n\n2")
                        for c in chat:
                            Frind[index][i[1]]["chat"].append(list(c))
                            if  not self.Check.isChecked():
                                self.curdblist.execute("INSERT INTO messages VALUES(?,?,?,?)",(i[1],c[0],c[1],c[2]))
                        print("\n\n3")
                        if  not self.Check.isChecked():
                            self.curdblist.execute("INSERT INTO frind VALUES(?,?,?,?,?,?)",(i[1],Nameimage[0],Nameimage[2],Nameimage[1],Nameimage[3],f"{i[4]}"))
                        self.dblite.commit()
                    except Exception as E:
                        print(f"\n\nE {E}")
            
           
            
            self.dblite.commit()
            
            _dirImage = dirImage.replace("\\","/")
            Image = _dirImage+"/"+username+".png"
            if not os.path.isfile(Image):
                print("not Image")
                self.HEADER_LENGTH = 10

                IP = "127.0.0.1"
                PORT = 1234
                
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    self.client_socket.connect((IP, PORT))
                except:
                    print("Error : CreateAcount")
                self.client_socket.setblocking(False)
                _username = username.encode('utf-8')
                username_header = f"{len(_username):<{self.HEADER_LENGTH}}".encode('utf-8')
                try:
                    self.client_socket.send(username_header + _username)
                except:
                    print(2)
                    return 
                
                message = username+"getImage"+username
                message = message.encode('utf-8')
                message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
                
                SendTo = sendTo.encode('utf-8')
                SendTo_header = f"{len(SendTo):<{self.HEADER_LENGTH}}".encode('utf-8')
                
                print(f"\n send message {message_header}\t { message } \t{SendTo_header }\t{ SendTo }")
                
                try:
                    self.client_socket.send(message_header + message +  SendTo_header + SendTo )    
                    threading.Thread(target=self.requestMessag).start()
                except:
                    print("Error getCreateAcount");
            else:
                print("\nImage\n")
            self.curdblist.execute("INSERT INTO stting (notifications)VALUES(?)",("1"))
            self.dblite.commit()
            self.window = WindowMain()
            self.close()
        else:
            self.loginWrong.show()
            self.username.setText("")
            self.password.setText("")
            self.login.setText("Login")
    def requestMessag(self):
        global StateConnect
        print("\n\nrequestMessag\n\n")
        while True:
            if _stateEnd == True:
                sys.exit()
            try:
            # Now we want to loop over received messages (there might be more than one) and print them
                while True:
                    if _stateEnd == True:
                        sys.exit()
                    # Receive our "header" containing username length, it's size is defined and constant
                    username_header = self.client_socket.recv(self.HEADER_LENGTH)

                    # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                    if not len(username_header):
                        print('Connection closed by the server')
                        sys.exit()

                    # Convert header to int value
                    username_length = int(username_header.decode('utf-8').strip())

                    # Receive and decode username
                    username = self.client_socket.recv(username_length).decode('utf-8')
                    print(f"\nusername:{username}")
                    try:
                        if username == "imagUser":
                            print("\nget imagUser 1\n")
                            imagUser_header = self.client_socket.recv(self.HEADER_LENGTH)
                            imagUser_length = int(imagUser_header.decode('utf-8').strip())
                            imagUser = self.client_socket.recv(imagUser_length).decode('utf-8')
                            print(f"imagUser : {imagUser}")
                            Img_header = self.client_socket.recv(self.HEADER_LENGTH)
                            Img_length = int(Img_header.decode('utf-8').strip())
                            _Img = self.client_socket.recv(Img_length)
                            # print(f"_Img :{_Img}")
                            
                            _dirImage = dirImage.replace("\\","/") 
                            Img = open(f"{_dirImage}/{imagUser}.png","wb")
                            Img.write(_Img)
                            Img.close()
                            
                            print(f"\n{_dirImage}/{imagUser}.png\n")
                            self.client_socket.close()
                            #self.getMessg.emit(["imagUser",f"{_dirImage}/{imagUser}.png"])
                            continue
                    except Exception as  E:
                        print(f"E : {E}")
                        continue
                    
                    

            except IOError as e:

                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    if _stateEnd:
                        sys.exit()
                    #self.errorConnect.emit()
                    return 
                continue
                

            except Exception as e:
                pass
            
            
    def getCreateAcount(self):
        _name = self.Createname.text()
        _username =self.Createusername.text()
        _password = self.Createpassword.text()
        _ConfirmPassword = self.Createrepassword.text()
        
        if _password =="" or _name == "" or _username == "" or _ConfirmPassword =="":
            QMessageBox.information(self,"CChat", "All fields must be filled out")
            return
        
        if self.CreateusernameFound.text() == "Username is already in use":
            QMessageBox.information(self,"CChat", "Username is already in use")
            return
        
        if len(_password) < 5:
            QMessageBox.information(self,"CChat", "Short password should be at least 6 characters long")
            return
        
        if _password != _ConfirmPassword:
            QMessageBox.information(self,"CChat", "Username is already in use")
            return
        
        
        
        _image = self.IMAGE
        basename = os.path.basename(_image)
        imgtype = basename.split(".")[-1]
        imgname =basename.split(f".{imgtype}")[0]
        print(imgtype)
        print(imgname)
        _dirImage = dirImage.replace("\\","/")
        
        
        imgbnry = open(_image,"rb")
        
        _imgbnry = open(f"{_dirImage}/{_username}.png", "wb")
        _imgbnry.write(imgbnry.read())
        _imgbnry.close()
        imgbnry.close()
        self.HEADER_LENGTH = 10

        IP = "127.0.0.1"
        PORT = 1234
        self.my_username = _username

        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((IP, PORT))
        except:
            print("Error : CreateAcount")
        self.client_socket.setblocking(False)
        username = _username.encode('utf-8')
        username_header = f"{len(username):<{self.HEADER_LENGTH}}".encode('utf-8')
        try:
            self.client_socket.send(username_header + username)
        except:
            print(2)
            return 
        
        message = "getCreateAcount".encode('utf-8')
        message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
        
        Username = _username.encode('utf-8')
        username_header = f"{len(Username):<{self.HEADER_LENGTH}}".encode('utf-8')
        
        Name = _name.encode('utf-8')
        name_header = f"{len(Name):<{self.HEADER_LENGTH}}".encode('utf-8')
        
        Password = _password.encode('utf-8')
        Password_header = f"{len(Password):<{self.HEADER_LENGTH}}".encode('utf-8')
        
        imgbnry = open(_image,"rb")
        Imag = imgbnry.read()
        Imag_header = f"{len(Imag):<{self.HEADER_LENGTH}}".encode('utf-8')
        imgbnry.close()
        try:
            self.client_socket.send(message_header + message +  username_header + Username +name_header + Name +Password_header + Password + Imag_header+ Imag)
        except:
            print("Error getCreateAcount");


        self.username.setText(_username)
        self.password.setText(_password)
        self.Stack.setCurrentIndex(0)
        self.getLogin()

    def closeEvent(self, _) :
        self.close()
        # sys.exit()


class Thread(QThread):
    getMessg = pyqtSignal(list)
    errorConnect = pyqtSignal()
    MessageThread= pyqtSignal(list)
    stateConnct= pyqtSignal(bool)
    slectFrindT = pyqtSignal(list)
    def __init__(self):
        global StateConnect
        super().__init__()
        
        
    
    def connect1(self):
        threading.Thread(target=self.connect).start()    
    def connect(self):  
        global StateConnect  
        self.HEADER_LENGTH = 10

        IP = "127.0.0.1"
        PORT = 1234
        self.my_username = _my_username

        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to a given ip and port
        #print(f"connect0.5 : {StateConnect}")
        if _stateEnd:
            sys.exit()
        try:
            self.client_socket.connect((IP, PORT))
        except:
            StateConnect = False
            self.stateConnct.emit(StateConnect)
            self.errorConnect.emit()
            return 
        StateConnect = True
        self.stateConnct.emit(StateConnect)
    
        

        # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
        self.client_socket.setblocking(False)

        # Prepare username and header and send them
        # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        username = self.my_username.encode('utf-8')
        username_header = f"{len(username):<{self.HEADER_LENGTH}}".encode('utf-8')
        try:
            self.client_socket.send(username_header + username)
        except:
            print(2)
            StateConnect = False
            self.stateConnct.emit(StateConnect)
            self.errorConnect.emit()
            return 

        
        threading.Thread(target=self.requestMessag).start()
        
    
    def run(self):
        
        # Wait for user to input a message
        message = f'{_message}'

        # If message is not empty - send it
        """ if dirfileNew != "":
                if os.path.isfile(dirfileNew):
                    message = "SendFile".encode('utf-8')
                    message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
                    
                    _nameImag =namefileNew.encode('utf-8')
                    nameImag_header = f"{len(_nameImag):<{self.HEADER_LENGTH}}".encode('utf-8')
                    
                    image = open(dirfileNew, "rb")
                    _image = image.read()
                    image.close()
                    image_header = f"{len(_image):<{self.HEADER_LENGTH}}".encode('utf-8')
                    
                    SendTo = sendTo.encode('utf-8')
                    SendTo_header = f"{len(SendTo):<{self.HEADER_LENGTH}}".encode('utf-8')
                    
                    self.client_socket.send(message_header + message +  SendTo_header + SendTo + nameImag_header + _nameImag + image_header +_image)
                return
        
            if dirfileNew != "":
                message = message.encode('utf-8')
                message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
                
                fileName = sendTo.encode('utf-8')
                fileName_header = f"{len(fileName):<{self.HEADER_LENGTH}}".encode('utf-8')
                
                SendTo = sendTo.encode('utf-8')
                SendTo_header = f"{len(SendTo):<{self.HEADER_LENGTH}}".encode('utf-8')
                
                print(f"\n send message {message_header}\t { message } \t{SendTo_header }\t{ SendTo }")
                self.client_socket.send(message_header + message +fileName_header+ fileName+  SendTo_header + SendTo )
                return
        """
        
        
        if message:
            
            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            message = message.encode('utf-8')
            message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
            
            SendTo = sendTo.encode('utf-8')
            SendTo_header = f"{len(SendTo):<{self.HEADER_LENGTH}}".encode('utf-8')
            
            print(f"\n send message {message_header}\t { message } \t{SendTo_header }\t{ SendTo }")
            self.client_socket.send(message_header + message +  SendTo_header + SendTo )
    
    def sendMessageFile(self,dirfileNew,namefileNew):
        threading.Thread(target=self._sendMessageFile, args=(dirfileNew,namefileNew)).start()
    
    def _sendMessageFile(self,dirfileNew,namefileNew):
        self.HEADER_LENGTH = 10
        if os.path.isfile(dirfileNew):
            message = "SendFile".encode('utf-8')
            message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
            
            _nameImag =namefileNew.encode('utf-8')
            nameImag_header = f"{len(_nameImag):<{self.HEADER_LENGTH}}".encode('utf-8')
            
            image = open(dirfileNew, "rb")
            _image = image.read()
            image.close()
            image_header = f"{len(_image):<{self.HEADER_LENGTH}}".encode('utf-8')
            
            SendTo = sendTo.encode('utf-8')
            SendTo_header = f"{len(SendTo):<{self.HEADER_LENGTH}}".encode('utf-8')
            
            self.client_socket.send(message_header + message +  SendTo_header + SendTo + nameImag_header + _nameImag + image_header +_image)
    
    def sendGitFile(self):
        threading.Thread(target=self._sendGitFile).start()
    def _sendGitFile(self):
        message = _message.encode('utf-8')
        message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
        
        SendTo = _my_username.encode('utf-8')
        SendTo_header = f"{len(SendTo):<{self.HEADER_LENGTH}}".encode('utf-8')
        
        print(f"\n send message {message_header}\t { message } \t{SendTo_header }\t{ SendTo }")
        self.client_socket.send(message_header + message +  SendTo_header + SendTo )
    
    def requestMessag1 (self):
       global _selectfrind
       print(f"\n\nrequestMessag1:\t{_selectfrind}\n\n")
       if _selectfrind == 2:
           print(f"\n\n_selectfrind:\t{_selectfrind}\n\n")
           _selectfrind = 0
           return
    def requestMessag(self):
        global StateConnect, _selectfrind, fileDirCope,AddFrind
        print("\n\nrequestMessag\n\n")
        while True:
            if _stateEnd == True:
                sys.exit()
            try:
            # Now we want to loop over received messages (there might be more than one) and print them
                while True:
                    if _selectfrind == 1:
                        return
                    if _stateEnd == True:
                        sys.exit()
                    # Receive our "header" containing username length, it's size is defined and constant
                    username_header = self.client_socket.recv(self.HEADER_LENGTH)
                    print(f"\nusername_header:{username_header}\n")
                    with open("temp.txt","a") as t:
                        t.write(f"username_header:{username_header}\n")
                    # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                    if not len(username_header):
                        print('Connection closed by the server')
                        sys.exit()

                    # Convert header to int value
                    username_length = int(username_header.decode('utf-8').strip())

                    # Receive and decode username
                    username = self.client_socket.recv(username_length).decode('utf-8')
                    print(f"\nusername:{username}")
                    
                    try:
                        if username == "getFile":
                            print("\nget getFile 1\n")
                            fileName_header = self.client_socket.recv(self.HEADER_LENGTH)
                            fileName_length = int(fileName_header.decode('utf-8').strip())
                            fileName = self.client_socket.recv(fileName_length).decode('utf-8')
                            print(f"getFile : {fileName}")
                            
                            file_header = self.client_socket.recv(self.HEADER_LENGTH)
                            file_length = int(file_header.decode('utf-8').strip())
                            _file = self.client_socket.recv(file_length)
                            
                            
                            print(f"file_length :{file_length}")
                            
                            _dirfile = fileMessagef.replace("\\","/")
                            try:
                                Img = open(f"{fileDirCope}","wb")
                                Img.write(_file)
                                Img.close()
                                fileDirCope = ''
                            except Exception as E:
                                print(E)
                            
                            print(f"\n{fileDirCope}\n")
                            self.getMessg.emit(["getFile",f"{_dirfile}/{fileName}",fileName])
                            continue
                    except Exception as E:
                        print("Erorr File recv ",E)
                    
                    try:
                        if username == "imagUser":
                            print("\nget imagUser 1\n")
                            imagUser_header = self.client_socket.recv(self.HEADER_LENGTH)
                            imagUser_length = int(imagUser_header.decode('utf-8').strip())
                            imagUser = self.client_socket.recv(imagUser_length).decode('utf-8')
                            print(f"imagUser : {imagUser}")
                            Img_header = self.client_socket.recv(self.HEADER_LENGTH)
                            Img_length = int(Img_header.decode('utf-8').strip())
                            _Img = self.client_socket.recv(Img_length)
                            
                            
                            _dirImage = dirImage.replace("\\","/") 
                            Img = open(f"{_dirImage}/{imagUser}.png","wb")
                            Img.write(_Img)
                            Img.close()
                            
                            self.getMessg.emit(["imagUser",f"{_dirImage}/{imagUser}.png"])
                            continue
                    except Exception as  E:
                        print(f"E : {E}")
                        continue
                    try:
                        if username == "getsearshImage":
                            print("\ngetsearshImage\n")
                            imagUser_header = self.client_socket.recv(self.HEADER_LENGTH)
                            imagUser_length = int(imagUser_header.decode('utf-8').strip())
                            imagUser = self.client_socket.recv(imagUser_length).decode('utf-8')
                            print(f"getsearshImage : {imagUser}")
                            Img_header = self.client_socket.recv(self.HEADER_LENGTH)
                            Img_length = int(Img_header.decode('utf-8').strip())
                            _Img = self.client_socket.recv(Img_length)
                            
                            _tempData = tempData.replace("\\","/") 
                            Img = open(f"{_tempData}/{imagUser}.png","wb")
                            Img.write(_Img)
                            AddFrind [imagUser] = _Img
                            Img.close()
                            
                            continue
                    except Exception as  E:
                        print(f"E : {E}")
                        continue
                    try:
                        if username == "SendFile":
                            print(f"\n\nSendFile\n\n")
                            print("_username_header")
                            _username_header = self.client_socket.recv(self.HEADER_LENGTH)
                            _username_length = int(_username_header.decode('utf-8').strip())
                            _username = self.client_socket.recv(_username_length).decode('utf-8')
                            
                            print("nameImag_header")
                            nameImag_header = self.client_socket.recv(self.HEADER_LENGTH)
                            nameImag_length = int(nameImag_header.decode('utf-8').strip())
                            nameImag = self.client_socket.recv(nameImag_length).decode('utf-8')
                            
                            print("image_header")
                            image_header = self.client_socket.recv(self.HEADER_LENGTH)
                            image_length = int(image_header.decode('utf-8').strip())
                            image = self.client_socket.recv(image_length)
                            
                            print("time_header")
                            time_header = self.client_socket.recv(self.HEADER_LENGTH)
                            time_length = int(time_header.decode('utf-8').strip())
                            time = self.client_socket.recv(time_length).decode('utf-8')
                            
                            
                            print("_fileMessagef")
                            if image != b'image':
                                _fileMessagef = fileMessagef.replace("\\","/")
                                with open(_fileMessagef+"/"+nameImag ,"wb") as F:
                                    F.write(image)
                            
                            
                                self.getMessg.emit(["SendFile",_username,time,nameImag,_fileMessagef+"/"+nameImag])
                                
                                continue
                            
                            self.getMessg.emit(["SendFile",_username,time,nameImag,""])
                            
                            continue
                    except Exception as E:
                        print(f"Erorr requst file message :{E}")
                        continue
                    # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                    print("\nget Message 1\n")
                    message_header = self.client_socket.recv(self.HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = self.client_socket.recv(message_length).decode('utf-8')

                    # Print message
                    print(f'{username} > {message}')
                    self.getMessg.emit([username,message])
                    

            except IOError as e:
                
                # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("\n\nIOError\n\n")
                    print('Reading error: {}'.format(str(e)))
                    if _stateEnd:
                        sys.exit()
                    StateConnect = False
                    self.stateConnct.emit(StateConnect)
                    self.errorConnect.emit()
                    return 
                continue

                # We just did not receive anything
                

            except Exception as e:
                print("\n\nException\n\n")
                pass

    def s(self):
        time.sleep(2)
        self.requestMessag()
        print("\n\nDen\n\n")
    def runrequestMessag(self):   
        threading.Thread(target=self.s).start()
    
    def run2(self):
        threading.Thread(target=self._run2).start()

    
    def _run2(self):
        global _selectfrind, selectchate
        
        print("\nThread2")
        self.dblite = sqlite3.connect(f"{dirfile}\\chat.db")
        self.curdblist = self.dblite.cursor()
        _selectfrind = 1
        for i in _listShat[::-1]:
            time.sleep(0.01)
            if "SendFile" in i[1] :
                nameImage = i[1].split("SendFile")[1]
                typeFile = nameImage.split(".")[-1]
                _isImag = ["png","jpg","jpeg","ico"]
                statsavefile = self.curdblist.execute("SELECT * from filemessages where filename=? ",(i[1],)).fetchone()
                if statsavefile == None:
                    self.curdblist.execute("INSERT INTO filemessages VALUES(?,?)",(f"{i[1]}",""))
                    self.dblite.commit()
                    statsavefile= [i[1],""]

                
                path = ""
                _fileMessagef = fileMessagef.replace("\\","/")
                if os.path.isfile(statsavefile[1]):
                    path = statsavefile[1].replace("\\","/")

                elif os.path.isfile(_fileMessagef+"/"+i[1]):
                    path = _fileMessagef+"/"+i[1]
                if typeFile in _isImag and path != "":
                    pixmap = QPixmap(path)
                    pixmap4 = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    
                    
                    i.append(pixmap4)
                    self.MessageThread.emit(i)
                    continue
            ##################################
            i.append("")
            self.MessageThread.emit(i)
        time.sleep(5)
        selectchate = False
        
        
        _selectfrind = 2
        print("\n\nFinsh show massage")
        time.sleep(0.01)
        self.MessageThread.emit(["minimumSizeMinueFrind"])
        time.sleep(1)
        self.runrequestMessag()
    
    
    def slectFrind(self,shat, key, index):
        threading.Thread(target=self._slectFrind, args=(shat, key, index)).start()
    
    def _slectFrind(self,shat, key, index):
        self.slectFrindT.emit([shat, key, index])
    def CloseClient(self):
        self.client_socket.close()
    
    
    def searshFrameImage(self, username, labelImage):
        threading.Thread(target=self.searshFrameImage1,args=(username,labelImage)).start()
        self.timarchacksearshFrame()
    
    def timarchacksearshFrame(self):
        print("\n timarchacksearshFrame")
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: not chacksearshFrame)
        self.timer.start(10000)
    def searshFrameImage1(self, username, labelImage):
        global chacksearshFrame
        print(username)
        message = _my_username+"getsearshImage"+username
        message = message.encode('utf-8')
        message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
        
        SendTo = sendTo.encode('utf-8')
        SendTo_header = f"{len(SendTo):<{self.HEADER_LENGTH}}".encode('utf-8')
        
        self.client_socket.send(message_header + message +  SendTo_header + SendTo)
        
        chacksearshFrame = True
        
        if username not in AddFrind:
           
            while chacksearshFrame:
                _tempData = tempData.replace("\\","/") 
                if os.path.isfile(f"{_tempData}/{username}.png") :
    
                    img =f"{_tempData}/{username}.png"
                    time.sleep(1)
                    labelImage.setStyleSheet("QLabel{border-image: url('"+img+"');border-radius: 20px; background-color: rgba(255, 255, 255,70);}")   
                    break
        else:
            _tempData = tempData.replace("\\","/") 
            if os.path.isfile(f"{_tempData}/{username}.png") :
                img =f"{_tempData}/{username}.png"
                time.sleep(1)
                if labelImage:
                    try:
                        labelImage.setStyleSheet("QLabel{border-image: url('"+img+"');border-radius: 20px; background-color: rgba(255, 255, 255,70);}")   
                    except Exception as E:
                        print(E)
     
class Thread1 (QThread):
    stateConnct= pyqtSignal(dict)
    animationCheck = pyqtSignal()
    getInfoDataUser = pyqtSignal()
    def __init__(self):
        super().__init__()
        
    def run(self):
        while True:
            time.sleep(1)
            self.db = mysql.connector.connect(user='root', password='123456', host='localhost',port=3307, db="chat")
            self.curdb = self.db.cursor()
            self.curdb.execute("SELECT stateConnect FROM user WHERE username='%s' "%(sendTo,))
            stateC = self.curdb.fetchone()
            self.curdb.execute("SELECT block FROM frind WHERE username='%s' and frinduser='%s' "%(sendTo,_my_username))
            block = self.curdb.fetchone()
            self.curdb.execute("SELECT block FROM frind WHERE username='%s' and frinduser='%s' "%(_my_username,sendTo))
            myblock = self.curdb.fetchone()
            self.db.close()
            if stateC != None and block != None and myblock != None:
                self.stateConnct.emit({"stateC":stateC[0],"block":int(block[0]),"myblock":int(myblock[0])})
            elif stateC != None:
                self.stateConnct.emit({"stateC":stateC[0],"block":int(0),"myblock":int(0)})

    def AnimationCheck(self):
        threading.Thread(target=self.AnimationCheck1).start() 
    def AnimationCheck1(self):
        time.sleep(0.2)
        self.animationCheck.emit()
    def GetInfoDataUser(self):
        threading.Thread(target=self._GetInfoDataUser).start() 
    def _GetInfoDataUser(self):
        self.getInfoDataUser.emit()

class messageLabel(QLabel):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()

class messageVideoLabel(QSvgWidget):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()


class WindowMain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("shate")
        self.resize(1150,600)
        
        self.dblite = sqlite3.connect(f"{dirfile}\\chat.db")
        self.curdblist = self.dblite.cursor()
        self.UI()
        self.animation11 = QPropertyAnimation(self.mainFrind, b"maximumWidth")
        self.show()
        threading.Thread(target=self.Connect).start()

        self.thread1 = Thread1()
        self.thread1.stateConnct.connect(self.stateConnectFrind)
        self.thread1.animationCheck.connect(self.mainFrindEnterProssor)
        self.thread1.getInfoDataUser.connect(self.FrindInfomainUI1)
        
        self.setStyleSheet("QWidget{background-color: rgb(29, 44, 58);}%s"%(self.styleScrollBar(),))

        threading.Thread(target=self.connectDB).start()
        
        self.UpDate()
        
       
    def Notifications(self, username, messag):
        print("Notifications")
        notifications =  self.curdblist.execute("SELECT notifications FROM stting").fetchone()
        if notifications != None:
            if notifications[0] == "0":
                return
        if self.isActiveWindow():
            print("\n\nisActiveWindow")
        else:
            print("\n\nNo isActiveWindow")
            
        _dirImage = dirImage.replace("\\","/")+f"/{username}.ico"
        if not os.path.isfile(_dirImage):
            from PIL import Image
            filename =  dirImage.replace("\\","/")+f"/{username}.png"
            try:
                img = Image.open(filename)
            except :
                img = Image.open("img/gg.png")
            img.save(_dirImage)
            img.close()
            
        x = lambda: notifi.show_toast(f"Send {username}", f" Message for you \n{messag}",icon_path=_dirImage, duration=10, threaded=True,callback_on_click=self.showWindow)
        x()
    def showWindow(self):
        print("showWindow")
        self.setFocus(True)
        self.activateWindow()
        if self.windowState() == Qt.WindowMinimized:
            # Window is minimised. Restore it.
            self.setWindowState(Qt.WindowActive)
        
    
    def connectDB(self):
        self.db = mysql.connector.connect(user='root', password='123456', host='localhost',port=3307, db="chat")
        self.curdb = self.db.cursor(buffered=True)
        threading.Thread(target=self.chackMessages).start()
        print("connectDB")
        
        
    def openFile(self,nameFile):
        print(nameFile)
        _fileMessagef = fileMessagef.replace("\\","/")
        if os.path.isfile(_fileMessagef+"/"+nameFile):
            os.startfile(_fileMessagef+"/"+nameFile)
        else:
            Dir = self.curdblist.execute("SELECT filedir from filemessages WHERE filename=?",(nameFile,)).fetchone()[0]
            if os.path.isfile(Dir):
                os.startfile(Dir)
        
    
    def openFolder (_,nameFile):
        _fileMessagef = os.path.dirname(nameFile)
        _fileMessagef = _fileMessagef.replace("/","\\")
        path = f'explorer.exe "{_fileMessagef}"'
        print(path)
        threading.Thread(target=lambda:os.system(path)).start()
    def Combochange(self,val, nameFile, dirFile,):
        print("val: ", val)
        

        if val == 0:
            self.openFile(nameFile)
        elif val == 1:
            self.openFolder(dirFile)
        elif val == 2:
            self.SaveFile(nameFile)
        try:
            self.combo.setCurrentIndex(-1)
            self.combo1.setCurrentIndex(-1)
        except:
            pass

            
    def SaveFile(self, nameFile, saveFile="" ):
        global namefrindFileUpdate, _message, fileDirCope
        if saveFile != '':
            saveFile.setStyleSheet("""
                                QPushButton{color:#fff;
                                background-image:url(img/loading.png);
                                background-repeat: no-repeat;
                                background-color: rgb(29, 44, 58);
                                background-position: center;
                                border:0px;
                                }
                                QPushButton:hover{background-color: #006699;border-radius: 9px;}
                                """)
            saveFile.setEnabled(False)
        namefrindFileUpdate = sendTo
        NameFile = nameFile.split("SendFile")[0]
        typ = NameFile.split(".")[-1]
        fileName,ok =  QFileDialog.getSaveFileName(None, 'Select a folder:', NameFile,f"*.{typ}")#, QFileDialog.ShowDirsOnly)
        print(fileName)
        if ok:
              
            _fileMessagef = fileMessagef.replace("\\","/")
            print(_fileMessagef+"/"+nameFile)
            if os.path.isfile(_fileMessagef+"/"+nameFile):
                with open(_fileMessagef+"/"+nameFile,"rb")as O:
                    o = O.read()
                    with open(fileName, "wb") as N:
                        N.write(o)
                        print(fileName)
                        self.curdblist.execute("INSERT INTO filemessages VALUES(?,?)",(f"{nameFile}",fileName))
                        self.dblite.commit()
            else:
                fileDirCope = fileName
                _message = _my_username+"getFile"+nameFile
                check = self.curdblist.execute("SELECT  * from filemessages WHERE filename=?",(nameFile,)).fetchone()
                if check:
                    self.curdblist.execute("UPDATE  filemessages SET filedir=? WHERE filename=?",(fileName,nameFile))
                    self.dblite.commit()
                else:
                    self.curdblist.execute("INSERT INTO filemessages VALUES(?,?)",(f"{nameFile}",fileName))
                    self.dblite.commit()
                self.thread.sendGitFile()
    
    def trans_paste(self,fg_img,bg_img,alpha=0.0,box=(1,0)):
        fg_img_trans = Image.new("RGBA",fg_img.size)
        fg_img_trans = Image.blend(fg_img_trans,fg_img,alpha)
        bg_img.paste(fg_img_trans,box,fg_img_trans)
        return bg_img
    def showVideo(self, path,time,chat):
        nameImage = chat.split("SendFile")[0]
        videoBoxV = QVBoxLayout()
        videoBoxH = QHBoxLayout()
        videoBoxV.setContentsMargins(0,0,0,0)
        videoBoxV.setSpacing(0)
        Frame = QFrame()
        Frame.setFixedSize(300,201)
        Frame.setStyleSheet(u"QFrame{\n"
                "background-color: rgb(29, 44, 58);\n"
                "color:rgb(255, 255, 255);\n"
                "border: 1px solid rgb(29, 44, 58) ;\n" #
                "padding: 1px;\n"
                "border-radius: 9px;}")
        
        
        nameVide = QLabel(nameImage)
        ##############################################
        cap= cv2.VideoCapture(path)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(f'{tempData}\\{chat}.png',frame)
            bg_img = Image.open(f'{tempData}\\{chat}.png')
            fg_img = Image.open("img/playVideo.png")
            p = self.trans_paste(fg_img,bg_img,1,(int(bg_img.size[0]/2),int(bg_img.size[1]/2)))
            p.save(f'{tempData}\\{chat}.png')
            pix = QPixmap(f'{tempData}\\{chat}.png')
            pixmap =  pix.scaled(300,150, Qt.KeepAspectRatio)
            showImage = messageLabel()
            showImage.setPixmap(pixmap)
        else:
            showImage = messageVideoLabel("img/showVideo.svg")
        showImage.setStyleSheet("QSvgWidget:hover{background-color:#263b59;})")
        
        showImage.setCursor(QCursor(Qt.PointingHandCursor))
        ##############################################
        
        timeVideo = QLabel(time)
        timeVideo.setStyleSheet("QLabel{font-size:10px;color:#999999;}")
        
        
        self.combo = QComboBox()
        self.combo.setPlaceholderText("--Select Country--")
        
        self.combo.addItems(["open","open Foldir", "Save"])
        self.combo.currentIndexChanged.connect(lambda val:self.Combochange(val ,chat, path))
        self.combo.setStyleSheet(
            """
            QComboBox::down-arrow {
                image: url(img/menu4.png); /* Set combobox button */
                border: 0px;
                
            }

            QComboBox::drop-down {
                width: 20px;  /* set the width of the drop down */
                border: 0px;
            }

            QComboBox {
                border: 0px;
                max-width: 600px;  /*width of whole box */
                background-color: rgb(29, 44, 58);
                color: rgb(29, 44, 58)
            }
            QComboBox::down-arrow:hover{
                image: url(img/menu4H.png); /* Set combobox button */
                border: 0px;
            }
            """
        )
        
        videoBoxH.setContentsMargins(0,0,0,0)
        videoBoxH.addWidget(nameVide,alignment=Qt.AlignLeft)
        videoBoxH.addWidget(self.combo,alignment=Qt.AlignRight)
        
        videoBoxV.addLayout(videoBoxH)
        videoBoxV.addWidget(showImage,stretch=70)
        videoBoxV.addWidget(timeVideo,alignment=Qt.AlignRight,stretch=10)
        Frame.setLayout(videoBoxV)
        showImage.clicked.connect(lambda: self.showVideo1(path, Frame,videoBoxV,videoBoxH,chat,nameImage,time))
        return Frame
    def showVideo1(self, path, Frame,videoBoxV,videoBoxH,chat,nameImage,time):
        try:
            if videoBoxH is not None:
                while videoBoxH.count():
                    item = videoBoxH.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        print(widget)
                        
                        widget.deleteLater()
                    else:
                        print("deleteLayout")
                        self.deleteLayout(item.layout())
                sip.delete(videoBoxH)
            if videoBoxV is not None:
                while videoBoxV.count():
                    item = videoBoxV.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        print(widget)
                        
                        widget.deleteLater()
                    else:
                        print("deleteLayout")
                        self.deleteLayout(item.layout())
                sip.delete(videoBoxV)
        except:
            pass

        ######################################
        nameVide = QLabel(nameImage)
        self.combo = QComboBox()
        self.combo.setPlaceholderText("--Select Country--")
        
        self.combo.addItems(["open","open Foldir", "Save"])
        self.combo.currentIndexChanged.connect(lambda val:self.Combochange(val ,chat, path))
        self.combo.setStyleSheet(
            """
            QComboBox::down-arrow {
                image: url(img/menu4.png); /* Set combobox button */
                border: 0px;
                
            }

            QComboBox::drop-down {
                width: 20px;  /* set the width of the drop down */
                border: 0px;
            }

            QComboBox {
                border: 0px;
                max-width: 600px;  /*width of whole box */
                background-color: rgb(29, 44, 58);
                color: rgb(29, 44, 58)
            }
            QComboBox::down-arrow:hover{
                image: url(img/menu4H.png); /* Set combobox button */
                border: 0px;
            }
            """
        )
        timeVideo = QLabel(time)
        timeVideo.setStyleSheet("QLabel{font-size:10px;color:#999999;padding:0px;}")
        timeVideo.setContentsMargins(0,0,0,0)
        timeVideo.setFixedHeight(12)
        ######################################
        Frame.setFixedSize(400,301)
        Frame.setStyleSheet(u"QFrame{\n"
                "background-color: rgb(29, 44, 58);\n"
                "color:rgb(255, 255, 255);\n"
                "border: 1px solid rgb(29, 44, 58) ;\n" #
                "padding: 1px;\n"
                "border-radius: 9px;}")
        


        videoBoxV = QVBoxLayout()
        Frame.setLayout(videoBoxV)
        videoBoxHTop = QHBoxLayout()
        videoBoxH  = QHBoxLayout()
        
        videoBoxV.setContentsMargins(0,0,0,0)
        videoBoxHTop.setContentsMargins(0,0,0,0)
        videoBoxH.setContentsMargins(0,0,0,0)
        videoBoxH.setSpacing(0)
        videoBoxHTop.addWidget(nameVide,alignment=Qt.AlignLeft)
        videoBoxHTop.addWidget(self.combo,alignment=Qt.AlignRight)
        videoBoxV.addLayout(videoBoxHTop,10)
        ############################
        mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videowidget = QVideoWidget()
        mediaPlayer.setVideoOutput(videowidget)
        mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        videoBoxV.addWidget(videowidget,70)
        videoBoxV.addStretch()
        
        mediaPlayer.positionChanged.connect(lambda position: self.position_changed(position,slider))
        mediaPlayer.durationChanged.connect(lambda duration: self.duration_changed(duration,slider))
        ######################################

        
        
        playBtn = QPushButton()
        
        playBtn.setIcon(QIcon(QPixmap("img/play.png").scaled(100,100)))
        playBtn.setIconSize(QSize(28, 28))
        playBtn.setStyleSheet("QPushButton{border:0px solid ;background-color:argb(0,0,0,0);}")
        playBtn.clicked.connect(lambda :self.play_video(mediaPlayer,playBtn))
        videoBoxH.addWidget(playBtn)
        # ######################################
        slider = QSlider(Qt.Horizontal)
        slider.setStyleSheet(self.QSliderStyle())
        slider.setRange(0,0)
        slider.sliderMoved.connect(lambda position: self.set_position(position,mediaPlayer))
        videoBoxH.addWidget(slider)
    
        listVidoeShow.append([self.play_video,mediaPlayer])
        
        videoBoxV.addLayout(videoBoxH,5)
        videoBoxV.addWidget(timeVideo,alignment= Qt.AlignRight,stretch=5)
        
        self.scrollarea.setCursor(QCursor(Qt.ArrowCursor))
        self.setCursor(QCursor(Qt.ArrowCursor))

    def play_video(self,mediaPlayer,playBtn):
        print("\n\nplay_video")
        for i in listVidoeShow:
            if mediaPlayer != i[1]:
                i[1].pause()
        if mediaPlayer.state() == QMediaPlayer.PlayingState:
            playBtn.setIcon(QIcon(QPixmap("img/play.png")))
            mediaPlayer.pause()

        else:
            playBtn.setIcon(QIcon(QPixmap("img/stop.png")))
            mediaPlayer.play() 
    def set_position(self, position,mediaPlayer):
        mediaPlayer.setPosition(position)    
    
    def position_changed(self, position,slider):
        try:
            slider.setValue(position)
        except:
            pass
    def duration_changed(self, duration,slider):
        slider.setRange(0, duration)
    
    
    def ShowAudioMessage(self,path,chat,time):
        global songLength,ListSund

        Frame = QFrame()
        Frame.setFixedSize(300,80)
        Frame.setStyleSheet(u"QFrame{\n"
                "background-color: rgb(29, 44, 58);\n"
                "color:rgb(255, 255, 255);\n"
                "border: 1px solid rgb(29, 44, 58) ;\n" #
                "padding: 1px;\n"
                "border-radius: 9px;}")
        HBoxLayout = QHBoxLayout()
        HBoxLayout.setContentsMargins(0,0,0,0)
        VBoxLayout = QVBoxLayout()
        VBoxLayout.setContentsMargins(0,0,0,0)
        ################################## name Audio ComboBox and Time
        namefile= chat.split("SendFile")[0]
        nameAudio = QLabel(namefile)
        self.combo = QComboBox()
        self.combo.setPlaceholderText("--Select Country--")
        
        self.combo.addItems(["open","open Foldir", "Save"])
        self.combo.currentIndexChanged.connect(lambda val:self.Combochange(val ,chat, path))
        self.combo.setStyleSheet(
            """
            QComboBox::down-arrow {
                image: url(img/menu4.png); /* Set combobox button */
                border: 0px;
                
            }

            QComboBox::drop-down {
                width: 20px;  /* set the width of the drop down */
                border: 0px;
            }

            QComboBox {
                border: 0px;
                max-width: 600px;  /*width of whole box */
                background-color: rgb(29, 44, 58);
                color: rgb(29, 44, 58)
            }
            QComboBox::down-arrow:hover{
                image: url(img/menu4H.png); /* Set combobox button */
                border: 0px;
            }
            """
        )
        timeAudio = QLabel(time)
        timeAudio.setStyleSheet("QLabel{font-size:10px;color:#999999;padding:0px;}")
        timeAudio.setContentsMargins(0,0,0,0)
        timeAudio.setFixedHeight(12)
        
        topLayout= QHBoxLayout()
        topLayout.setContentsMargins(0,0,0,0)
        topLayout.addWidget(nameAudio,alignment=Qt.AlignLeft)
        topLayout.addWidget(self.combo,alignment=Qt.AlignRight)
        VBoxLayout.addLayout(topLayout)
        # ############################## ProgressBar
        siderPlay = QSlider(Qt.Horizontal)
        siderPlay.setValue(0)
        siderPlay.setMinimum(0)
        siderPlay.setMaximum(100)
        siderPlay.setEnabled(False)
        

        siderPlay.setStyleSheet("""
                                QSlider{
                                    background-color:argb(0,0,0,0);
                                }
                                QSlider::groove:horizontal {
                                    border: 0px solid argb(0,0,0,0);
                                    height: 9px;

                                    border-radius: 2px;
                                    }

                                QSlider::handle:horizontal {
                                    width: 8px;
                                    height: 8px;
                                    background-image: url(img/slider.png)
                                    }

                                QSlider::add-page:qlineargradient {
                                    background: lightgrey;
                                    border-top-right-radius: 4px;
                                    border-bottom-right-radius: 4px;
                                    border-top-left-radius: 0px;
                                    border-bottom-left-radius: 0px;
                                    }

                                QSlider::sub-page:qlineargradient {
                                    background: blue;
                                    border-top-right-radius: 0px;
                                    border-bottom-right-radius: 0px;
                                    border-top-left-radius: 4px;
                                    border-bottom-left-radius: 4px;
                                    }
                                """)
        # #################################### Labels
        songTimerLabel = QLabel("0:00")
        songLentthLabel = QLabel("/ 0:00")
        songTimerLabel.setStyleSheet("color: #fff")
        songLentthLabel.setStyleSheet("color: #fff")
        
        
        # ############################### timer
        timer = QTimer()
        timer.setInterval(1000)
        
        # ############################### Buttons
        playButton = QToolButton()
        playButton.setIcon(QIcon("img/play.png"))
        playButton.setIconSize(QSize(48, 48))
        playButton.setToolTip("Play")
        playButton.setStyleSheet("QToolButton{background-color:rgb(29, 44, 58);border:1 void lightgrey;}")
        
        
        ################ add Wigdet
        HBoxLayout.addWidget(playButton) 
        HBoxLayout.addWidget(siderPlay) 
        HBoxLayout.addWidget(songTimerLabel) 
        HBoxLayout.addWidget(songLentthLabel)
        VBoxLayout.addLayout(HBoxLayout)
        
        VBoxLayout.addWidget(timeAudio,alignment=Qt.AlignRight)
        
        Frame.setLayout(VBoxLayout)
        #########################################
        mixer.music.set_volume(0.7)
        
        mixer.music.load(path)
        sound = MP3(path)
        songLength = sound.info.length
        songLength = round(songLength)
        sound = MP3(path)


        Min, sec = divmod(songLength, 60)
        if len(str(sec)) == 1:
            sec = f'0{sec}'
        if len(str(Min)) == 1:
            Min == f'0{Min}'
        songLentthLabel.setText(f"/ {Min}:{sec}")


        siderPlay.setValue(0)
        siderPlay.setMaximum(songLength)
        
        ListSund.append([self.StopSound,(playButton,timer,mixer)])
        timer.timeout.connect(lambda: self.updateSiderPlay(siderPlay,songTimerLabel,timer))
        playButton.clicked.connect(lambda: self.playSounds(path,siderPlay,songTimerLabel,playButton,timer,mixer))
        siderPlay.valueChanged.connect(lambda: self.SliderChange(path,siderPlay,songTimerLabel,playButton,mixer))
        return Frame
    def updateSiderPlay(self,siderPlay,songTimerLabel,timer):
        global count, songLength, sliderChange
        count += 1
        sliderChange = count
        siderPlay.setValue(count)
        songTimerLabel.setText(time.strftime("%M:%S", time.gmtime(count)))
        if count == songLength:
            timer.stop()
    def StopSound(self,playButton,timer,mixerr):
        global cuntprogre
        print("StopSound")
        timer.stop()
        playButton.setIcon(QIcon("img/play.png"))
        mixerr.music.pause()
    def PlaySound(self,playButton,timer,mixerr):
        global pause
        #################
        try :
            
            timer.start()
            playButton.setIcon(QIcon("img/stop.png"))
            mixerr.music.unpause()
            
            #################
            pause = False
        except:
            QMessageBox.information(self,"Music Player",f"Sorry, unexpected error, try again")   
    def playSounds(self,path,siderPlay,songTimerLabel,playButton,timer,mixerr):
        global songLength, nameplay,sliderChangeStop,startSund,count

        print(f"path:{path}\npath:{nameplay}")
        if nameplay != path and nameplay!= "":
            for i in ListSund:
                print(f"I:{i}")
                i[0](i[1][0],i[1][1],i[1][2])
              
        
        if sliderChangeStop == True:
            playButton.setToolTip("Stop")
            self.PlaySound(playButton,timer,mixerr)
            self.SliderChange(path,siderPlay,songTimerLabel,playButton,mixerr)
            sliderChangeStop = False
            
            return


        

        stat = playButton.toolTip()
        if path == nameplay:
            self.PlaySound(playButton,timer,mixerr)  
            if stat == "Stop":
                self.StopSound(playButton,timer,mixerr)
                playButton.setToolTip("Play")
                return
            else:
                playButton.setToolTip("Stop")
                count = siderPlay.value()
                if path == nameplay:
                    self.PlaySound(playButton,timer,mixerr)
                    return
        else:
            playButton.setToolTip("Stop")        
            

        
        try:

            startSund = True
            count = 0
            playButton.setIcon(QIcon("img/stop.png"))
            nameplay = str(path)
            
            siderPlay.setEnabled(True)
            mixerr.music.load(path)
            mixerr.music.play()

            timer.start()
                  
        except Exception as Error:
            print(Error)
    def SliderChange(self,path,siderPlay,songTimerLabel,playButton,mixerr):
        global sliderChange, count, sliderChangeStop,ind
        value = siderPlay.value()
        stat = playButton.toolTip()
        
        if stat == "Play":
            if sliderChange != value and sliderChange != value+1:
                pass
            sliderChangeStop = True
            count = value
            sliderChange = value
        
            songTimerLabel.setText(time.strftime("%M:%S", time.gmtime(count)))
            return
            
        if (stat == "Stop"  and sliderChange != value and sliderChange != value+1) or sliderChangeStop == True:
            mixerr.music.load(path)
            mixerr.music.play(0,value)
            count = value
            songTimerLabel.setText(time.strftime("%M:%S", time.gmtime(count)))
            sliderChangeStop = False

    def ShowImageMessage(self,time,chat,val, path,statsavefile, pixmap4):
        s = pixmap4.size()

        label = messageLabel()
        
        
        labelTime = QLabel(f"{time}")
        
        
        HCombo= QHBoxLayout()
        self.combo = QComboBox()
        self.combo.setPlaceholderText("--Select Country--")

        HCombo.addWidget(self.combo)
        HCombo.setAlignment(Qt.AlignRight)
        
        self.combo.addItems(["open","open Foldir", "Save"])
        self.combo.currentIndexChanged.connect(lambda val:self.Combochange(val ,chat, path))
        self.combo.setStyleSheet(
            """
            QComboBox::down-arrow {
                image: url(img/menu4.png); /* Set combobox button */
                border: 0px;
                
            }

            QComboBox::drop-down {
                width: 20px;  /* set the width of the drop down */
                border: 0px;
            }

            QComboBox {
                border: 0px;
                max-width: 600px;  /*width of whole box */
                background-color: rgb(29, 44, 58);
                color: rgb(29, 44, 58)
            }
            QComboBox::down-arrow:hover{
                image: url(img/menu4H.png); /* Set combobox button */
                border: 0px;
            }
            """
        )
        
        Frame = QFrame()
        Frame.setContentsMargins(0,0,0,0)
        VBox = QVBoxLayout()
        VBox.setContentsMargins(0,0,0,0)
        VBox.setSpacing(0)
        
        HBox = QHBoxLayout()
        HBox.setContentsMargins(0,0,0,0)
        HBox.setSpacing(0)
        
        VBox.addLayout(HCombo)
        VBox.addWidget(label)
        HBox.addWidget(labelTime)
        VBox.addLayout(HBox)
        if val == 0 :
            label.setAlignment(Qt.AlignRight)
            labelTime.setAlignment(Qt.AlignRight)
        else:
            label.setAlignment(Qt.AlignRight)
            labelTime.setAlignment(Qt.AlignRight)
        
        label.clicked.connect(  lambda:self.openFile(chat))
        label.mouseDoubleClickEvent = lambda _:self.openFolder(statsavefile[1])
        
        labelTime.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label.setPixmap(pixmap4)
        
        Frame.setStyleSheet(u"QFrame{\n"
                "background-color: rgb(29, 44, 58);\n"
                "color:rgb(255, 255, 255);\n"
                "border: 1px solid rgb(29, 44, 58) ;\n" #
                "padding: 1px;\n"
                "border-radius: 9px;}")
        labelTime.setStyleSheet("QLabel{font-size:10px;color:#999999;}")

            
        
            
        


        Frame.setLayout(VBox)
        Frame.setFixedSize(s)
        return Frame
    
    def ShowFileMessage(self,time,chat,val, path):
        NameFile = chat.split("SendFile")[0]
        label = QLabel(f"{NameFile}")
        
        
        labelTime = QLabel(f"{time}")
        

        
        HCombo= QHBoxLayout()
        self.combo1 = QComboBox()
        HCombo.addWidget(self.combo1)
        self.combo1.setPlaceholderText("--Select Country--")
        HCombo.setAlignment(Qt.AlignRight)
        
        self.combo1.addItems(["open","open Foldir", "Save"])
        self.combo1.currentIndexChanged.connect(lambda val:self.Combochange(val ,chat, path))
        self.combo1.setStyleSheet(
            """
            QComboBox::down-arrow {
                image: url(img/menu4.png); /* Set combobox button */
                border: 0px;
                
            }

            QComboBox::drop-down {
                width: 20px;  /* set the width of the drop down */
                border: 0px;
            }

            QComboBox {
                border: 0px;
                max-width: 600px;  /*width of whole box */
                background-color: rgb(29, 44, 58);
                color: rgb(29, 44, 58)
            }
            QComboBox::down-arrow:hover {
                image: url(img/menu4H.png); /* Set combobox button */
                border: 0px;
                
            }
            """
        )
        
        
        Frame = QFrame()
        Frame.setContentsMargins(0,0,0,0)
        VBox = QVBoxLayout()
        VBox.setContentsMargins(0,0,0,0)
        VBox.setSpacing(0)
        
        HBox = QHBoxLayout()
        HBox.setContentsMargins(0,0,0,0)
        
        
        if val == 0 :
            VBox.addLayout(HCombo)
            
            HBox.addWidget(label)
            VBox.addStretch()
            VBox.addStretch()
            VBox.addWidget(labelTime)
            
            HBox.addLayout(VBox)
            label.setAlignment(Qt.AlignCenter)
            VBox.setAlignment(Qt.AlignRight)
            labelTime.setAlignment(Qt.AlignRight)
            
        else:        
            VBox.addLayout(HCombo)
            VBox.addStretch()
            VBox.addWidget(labelTime)
            
            HBox.addWidget(label)
            HBox.addStretch()
            HBox.addLayout(VBox)
            
            
            label.setAlignment(Qt.AlignCenter)
            VBox.setAlignment(Qt.AlignLeft)
            labelTime.setAlignment(Qt.AlignLeft)
        
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        labelTime.setTextInteractionFlags(Qt.TextSelectableByMouse)
        Frame.setStyleSheet(u"QFrame{\n"
                "background-color: rgb(29, 44, 58);\n"
                "color:rgb(255, 255, 255);\n"
                "border: 1px solid rgb(29, 44, 58) ;\n" #
                "padding: 1px;\n"
                "border-radius: 9px;}")

        labelTime.setStyleSheet("QLabel{font-size:10px;color:#999999;}")

            
            
        Frame.setLayout(HBox)

        Frame.setFixedSize(400,60)
        return Frame
    
    def ShowFileDownloadMessage(self,time,chat,val):
        NameFile = chat.split("SendFile")[0]
        label = QLabel(f"{NameFile}")
        
        
        labelTime = QLabel(f"{time}")
        
        saveFile = QPushButton()
        
        
        
        
        Frame = QFrame()
        Frame.setContentsMargins(0,0,0,0)
        VBox = QVBoxLayout()
        VBox.setContentsMargins(0,0,0,0)
        VBox.setSpacing(0)
        
        HBox = QHBoxLayout()
        HBox.setContentsMargins(0,0,0,0)
        
        
        if val == 0 :
            HBox.addWidget(label)
            VBox.addStretch()
            VBox.addWidget(saveFile)
            VBox.addStretch()
            VBox.addWidget(labelTime)
            HBox.addLayout(VBox)
            label.setAlignment(Qt.AlignCenter)
            VBox.setAlignment(Qt.AlignRight)
            labelTime.setAlignment(Qt.AlignRight)
            
        else:
            VBox.addStretch()
            VBox.addWidget(saveFile)
            VBox.addStretch()
            VBox.addWidget(labelTime)
            HBox.addLayout(VBox)
            HBox.addWidget(label)
            label.setAlignment(Qt.AlignCenter)
            VBox.setAlignment(Qt.AlignLeft)
            labelTime.setAlignment(Qt.AlignLeft)
        
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        labelTime.setTextInteractionFlags(Qt.TextSelectableByMouse)
        Frame.setStyleSheet(u"QFrame{\n"
                "background-color: rgb(29, 44, 58);\n"
                "color:rgb(255, 255, 255);\n"
                "border: 1px solid rgb(29, 44, 58) ;\n" #
                "padding: 1px;\n"
                "border-radius: 9px;}")
        labelTime.setStyleSheet("QLabel{font-size:10px;color:#999999;}")
        saveFile.setStyleSheet("""
                            QPushButton{color:#fff;
                            background-image:url(img/download.png);
                            background-repeat: no-repeat;
                            background-color: rgb(29, 44, 58);
                            background-position: center;
                            border:0px;
                            }
                            QPushButton:hover{background-color: #006699;border-radius: 9px;}
                            """)
            
        
        Frame.setLayout(HBox)
        
        saveFile.setMinimumSize(48,48)
        Frame.setFixedSize(400,60)
        saveFile.clicked.connect(lambda:self.SaveFile(chat,saveFile))
        return Frame
    
    def StateShowSendFile(self,chat,time, val, pixmap4):
        if "SendFile" in chat :
            nameImage = chat.split("SendFile")[1]
            typeFile = nameImage.split(".")[-1]
            _isImag = ["png","jpg","jpeg","ico"]
            _isAudio =["mp3"]
            _isVideo = ["wmv"]
            statsavefile = self.curdblist.execute("SELECT * from filemessages where filename=? ",(chat,)).fetchone()
            if statsavefile == None:
                self.curdblist.execute("INSERT INTO filemessages VALUES(?,?)",(f"{chat}",""))
                self.dblite.commit()
                statsavefile= [chat,""]

            
            path = ""
            _fileMessagef = fileMessagef.replace("\\","/")
            if os.path.isfile(statsavefile[1]):
                path = statsavefile[1].replace("\\","/")

            elif os.path.isfile(_fileMessagef+"/"+chat):
               path = _fileMessagef+"/"+chat
            if typeFile in _isImag and path != "" and pixmap4!= "":  # Show Image
               return self.ShowImageMessage(time,chat,val, path,statsavefile,pixmap4)
            elif typeFile in _isAudio and path != "":  # Show Audio
               return self.ShowAudioMessage(path=path,chat=chat,time=time)
            elif typeFile in _isVideo and path != "":  # Show Audio
               return self.showVideo(path,time,chat)
            elif path != "":               # Show File
                return self.ShowFileMessage(time,chat,val, path)
            else:                          # Show File Download
                return self.ShowFileDownloadMessage(time,chat,val)
            
    def createLayout_group_shat(self, chat,time, val, pixmap4=None):
        _time = datetime.datetime.now().strftime("%d/%m/%Y")
        time1 = time.split(" ")
        if _time == time1[0]:
            time = time1[1]
        
        
        if "SendFile" in chat :
            return self.StateShowSendFile(chat,time, val, pixmap4)
            
        ##   Show Message Text    
        Frame = QFrame()
        Frame.setContentsMargins(0,0,0,0)
        HBox = QHBoxLayout()
        HBox.setContentsMargins(0,0,0,0)
        HBox.setSpacing(0)
        
        label = QLabel(f"{chat}")
        labelTime = QLabel(f"{time}")
        
        HBox.addWidget(label)
        HBox.addWidget(labelTime)
        print(f"val: {val}")
        if val == 0 :
            label.setAlignment(Qt.AlignLeft)
            labelTime.setAlignment(Qt.AlignRight)
            Frame.setStyleSheet(u"QFrame{\n"
                "background-color: rgb(26, 39, 51);\n"
                "color:rgb(255, 255, 255);\n"
                "border: 1px solid rgb(26, 39, 51) ;\n" #
                "padding: 1px;\n"
                "border-radius: 7px;}")
        else:
            label.setAlignment(Qt.AlignLeft)
            labelTime.setAlignment(Qt.AlignRight)
            
            Frame.setStyleSheet(u"QFrame{\n"
                "background-color: rgb(29, 44, 58);\n"
                "color:rgb(255, 255, 255);\n"
                "border: 1px solid rgb(29, 44, 58) ;\n" #
                "padding: 1px;\n"
                "border-radius: 7px;}")
        

        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        labelTime.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        labelTime.setStyleSheet("QLabel{font-size:10px;color:#999999;}")
            
        

        Frame.setLayout(HBox)
        Frame.raise_()
        Frame.setFixedWidth(450)
        return Frame
    

    
    def createLayout_Container_shatThrid(self, i,s =0):
        if len(i) == 1  and i[0]== "minimumSizeMinueFrind":
            self.mainFrindLeave()
            return
        print(f'i : {i}')
        
        if i[0] == "my":
            self.VBoxMy.insertWidget(0,self.createLayout_group_shat(i[1],i[2], 0, i[3]),alignment= Qt.AlignLeft)
            
        else:
            self.VBoxMy.insertWidget(0,self.createLayout_group_shat(i[1],i[2], 1, i[3]),alignment= Qt.AlignRight)


        
    def createLayout_Container_shat(self,val):
        global _listShat, selectchate
        print("createLayout_Container_shat")
        selectchate = True
        listShat= val[0]
        index = val [2]
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget()
        widget.setStyleSheet("background-color: rgb(14, 22, 33)")
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)
        
        self.Hchat = QHBoxLayout()
        
        self.Hchat.setAlignment(Qt.AlignBottom)
        self.VBoxMy = QVBoxLayout()
        self.VBoxYou = QVBoxLayout()
        
        
        self.Hchat.addLayout(self.VBoxMy)
        self.layout_SArea.addLayout(self.Hchat)
        self.Hchat.addLayout(self.VBoxYou)
        
        self.LableIndx = QLabel(f"{index}")
        

        _listShat = listShat
        
        print("\n\ncreateLayout_Container_shat 1\n\n")
        self.thread.run2()

        print("\n\ncreateLayout_Container_shat 2\n\n")
        

    def createLayout_group_Frind(self, data, index):
        global indexSendTo
        for i in data:
            key = i
            data = data[key]

        #############################
        rightVBox = QVBoxLayout()
        mainHBox = QHBoxLayout()
        #############################

        
        self.mainFrame = QFrame()
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.mainFrame.setCursor(QCursor(Qt.PointingHandCursor))
        self.mainFrame.setFixedHeight(60)
        

        self.mainFrame.setStyleSheet(u"""
                                     QFrame{background-color:  rgb(23, 33, 43);}
                                     QFrame:hover{background-color:  rgb(46, 66, 86)}
                                     QLabel:hover{background-color:  #000}
                                     """)
        
        self.pushButton = QPushButton()
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.setStyleSheet(u"background-color: rgba(255, 255, 255,70);")
        self.label = QLabel(data["name"])
        self.label.setFont(QFont('Arial', 12))
        self.label.setStyleSheet(u"color: #fff; padding-left: 5px;background-color: rgba(23, 33, 43,0) ;")
        self.label.setObjectName(u"label")
        
        self.label_2 = QLabel("")
        if data["chat"] != []:
            self.label_2.setText(data["chat"][-1][1])
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"color: #d9d9d9; padding-left: 6px;background-color: rgba(23, 33, 43,0) ;")
        self.label_3 = QLabel("")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        print(f"data[img']: {data['img']}")
        
        self.label_3.setStyleSheet(f"""border-image: url('{data["img"]}');border-radius: 20px; background-color: rgba(255, 255, 255,70);
                                    """)
        self.label_3.setMargin(20)
       

        self.label_3.setScaledContents(True)

        self.label_3.setFixedSize(45,45)
        
        self.statemassage = QLabel("")
        self.statemassage.setAlignment(Qt.AlignCenter)
        self.statemassage.setStyleSheet("QLabel{background-color:#4da6ff;color:#000;font-size:14px;border-radius: 7px;}")
        self.statemassage.setFixedSize(15,15)


        
        rightVBox.addWidget(self.label)
        rightVBox.addWidget(self.label_2)
        rightVBox.addStretch()
        
        mainHBox.addWidget(self.label_3)
        mainHBox.addLayout(rightVBox)
        
        if  data["statechat"]:
            if int(data["statechat"]) == 0:
                print(f'data["statechat"]:{data["id"]} {data["statechat"]}')
                self.statemassage.setStyleSheet("QLabel{background-color:rgba(23, 33, 43,0);}")
        mainHBox.addWidget(self.statemassage)

        self.mainFrame.setLayout(mainHBox)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.mainFrame)
        mainLayout.addStretch()
        
        
        self.mainFrame.leaveEvent = lambda e:self.mainFrameLeave(e)
        self.mainFrame.enterEvent = lambda e: self.mainFrameEnter(e)
        self.mainFrame.mouseReleaseEvent=lambda event:self.slectFrind(event,data["chat"], key, index)

        return self.mainFrame
    def mainFrameLeave(self,_):
        self.label_2.setStyleSheet("QLabel{background-color: rgba(23, 33, 43,0) ;color: #d9d9d9; padding-left: 6px;}")#rgb(23, 33, 43)
        self.label.setStyleSheet("QLabel{background-color: rgba(23, 33, 43,0);color: #fff; padding-left: 5px;}")#rgb(23, 33, 43)
    
    def mainFrameEnter(self,_):
        self.label_2.setStyleSheet("QLabel{background-color:  rgba(46, 66, 86,0);color: #d9d9d9; padding-left: 6px;}")
        self.label.setStyleSheet("QLabel{background-color: rgba(46, 66, 86,0);color: #fff; padding-left: 5px;}")
        self.scrollarea1.setFixedWidth(200)

        
    def slectFrind(self,_,shat, key,index):
        global sendTo, _key , _index, ListSund,listVidoeShow
        try:
            for i in listVidoeShow:
                del(i[1])
        except:
            print("\n\n Eroor slectFrind video")
        try:
            for i in ListSund:
                print(f"I:{i}")
                i[0](i[1][0],i[1][1],i[1][2])
        except:
            print("\n\n Eroor slectFrind Sund")
        ListSund = []
        listVidoeShow = []
        self.Label.hide()
        self.FrindInfomain.hide()
        self.chatmain.show()
        self.QFMainRightBlock.hide() 
        self.QFMainRightBotton.show() 
        self.curdb.execute(f"SELECT block FROM frind WHERE username='{_my_username}' and frinduser='{key}';")
        myBlock = self.curdb.fetchone()
        print(f"\n\nusername='{_my_username}' and frinduser='{key}'\nisBlock:{myBlock}\n\n")
        if myBlock[0] == "1":
            self.blockLable.setText("You blocked your friend")
            self.QFMainRightBlock.show() 
            self.QFMainRightBotton.hide()

        
        self.curdb.execute(f"SELECT block FROM frind WHERE username='{key}' and frinduser='{_my_username}';")
        youBlock = self.curdb.fetchone()
        print(f"\n\nusername='{_my_username}' and frinduser='{key}'\nisBlock:{youBlock}\n\n")
        if youBlock:
            if youBlock[0] == "1":
                self.blockLable.setText("You can't send messages, your friend has blocked you")
                self.QFMainRightBlock.show() 
                self.QFMainRightBotton.hide()

            
        
        
        print(f"slectFrind: {key} \t {Frind[ index][key]['statechat']}")
        if int(Frind[ index][key]["statechat"]) == 1:
            print("statechat \n")
            Frind[ index][key]["statechat"]= "0"
            self.curdblist.execute("UPDATE frind SET statechate=? WHERE username=?",(0,key))
            self.dblite.commit()
            print(self.curdblist.execute("SELECT statechate from frind WHERE username=?",(key,)).fetchone())
            self.UpDate()
        sendTo = key
        self.upchatInfoUsermainFrame.show()
        self.lableNameupchat.setText(Frind[ index][key]["name"])
        _bio = Frind[ index][key]["bio"]
        _bio = _bio.split(" ")
        bio= ""
        word = 0
        for i in _bio:
            if word == 13:
                break
            if len(i) < 10:
                bio += f"{i} "
            else:
                break
            word += 1
        
        self.thread1.start()
        self.lableBioupchat.setText(bio+ "...")
        self.lableimageupchat.setStyleSheet("QLabel{border-image:url('%s');border-radius: 22px;}"%(Frind[ index][key]["img"],))
        self.thread.slectFrind(shat, key, index)

    def stateConnectFrind(self, value):
        block = value["block"]
        myblock = value["myblock"]
        
        if int(block) == 1:
            self.curdblist.execute("UPDATE frind SET block='1' WHERE username=?",(sendTo,))
            self.dblite.commit()
            self.blockLable.setText("You can't send messages, your friend has blocked you")
            self.QFMainRightBlock.show() 
            self.QFMainRightBotton.hide()
        elif int(block) == 0 and myblock == 0:
            self.curdblist.execute("UPDATE frind SET block='0' WHERE username=?",(sendTo,))
            self.dblite.commit()
            self.QFMainRightBlock.hide() 
            self.QFMainRightBotton.show()
        val = value["stateC"]
        
        if int(val) == 0 or int(block) == 1:
            self.connectFrind.setStyleSheet("QLabel{background-color:#ff4d4d;border-radius: 5px;}")
        elif int(val) == 1:
            self.connectFrind.setStyleSheet("QLabel{background-color:#4dff4d;border-radius: 5px;}")
            
    
    def createLayout_Container_Frind(self):
        print("createLayout_Container_Frind")
        self.scrollarea1.setStyleSheet("QScrollArea{border:0px;}")
        self.scrollarea1.setWidgetResizable(True)

        widget = QWidget()
        widget.setStyleSheet("background-color: rgb(37, 49, 61); border:0px;")
        self.scrollarea1.setWidget(widget)
        self.layout_SArea1 = QVBoxLayout(widget)

        c = 0
        for i in Frind:
            self.layout_SArea1.addWidget(self.createLayout_group_Frind(i, c))
            c += 1
        
        self.layout_SArea1.setSpacing(0)
        self.layout_SArea1.setContentsMargins(0,0,0,0)
        self.layout_SArea1.addStretch()
        
        
    def styleSendLine(_) :
        return"""
            QTextEdit{
                font-size:14px;
                background-color: rgb(29, 44, 58);
                color:rgb(255, 255, 255);
                /*border: 1px solid rgb(29, 44, 58); */
                /*padding-left: 10px;*/
                /*border-radius: 9px;*/
                /*margin: 10;*/
            }
            QTextEdit:hover{border: 1px solid rgb(29, 44, 58);}
            QTextEdit:focus {border: 1px solid rgb(29, 44, 58);}
                """
    def QFMainRightBottonStyle(_):
        return"""
            QFrame{
                background-color: rgb(29, 44, 58);
                color:rgb(255, 255, 255);
                border: 1px solid rgb(29, 44, 58);
                /*padding-left: 10px;*/
                /*border-radius: 9px;*/
                /*margin: 10;*/
            }
            QFrame:hover{border: 1px solid #1464A0;}
            QFrame:focus{border: 1px solid #1464A0;}
        """
    def styleSendButton(_) :
        return"""
            QPushButton{
                border-image:url(img/send.png);
                background-color: rgb(29, 44, 58);
                /*color:rgb(255, 255, 255);*/
                /*border: 1px solid rgb(14, 22, 33);*/
                /*border-radius: 9px; */
                padding: 10px 7px 10px 7px;
                margin: 0px 5px 0px 0px;
            }
            QPushButton:hover{border-image:url(img/send.png);padding: 11px 11px 11px 11px;}
            QPushButton:pressed {
                /*background-color: rgb(47, 72, 106);*/
                padding: 7px 7px 7px 7px;
            }
        """
    def styleSendFile(_) :
        return"""
            QPushButton{
                border-image:url(img/attachment.png);
                background-color: rgb(29, 44, 58);
                /*color:rgb(255, 255, 255);*/
                /*border: 1px solid rgb(14, 22, 33);*/
                /*border-radius: 9px; */
                padding: 10px 7px 10px 7px;
                margin: 0px 5px 0px 0px;
            }
            QPushButton:hover{border-image:url(img/attachmentF.png);padding: 11px 11px 11px 11px;}
            QPushButton:pressed {
                /*background-color: rgb(47, 72, 106);*/
                padding: 7px 7px 7px 7px;
            }
        """
    def connectLabelStyal(_, val):
        if val:
            color = "green"
        else:
            color = "red"
        return "QLabel{"\
        "color : #fff;"\
        f"background-color: {color};"\
        "padding : 4px 60px 4px 60px;"\
        f"border: 1px solid {color};"\
        "border-radius: 4px;}"
    
    
    def UI(self):
        print("UI")
        mainLayout = QVBoxLayout()
        mainFrindeAndShatLayout = QHBoxLayout()
        self.QVMainRight = QVBoxLayout()

        connectLayout = QHBoxLayout()   
        self.mainFrind = QWidget()
        QVMainLeft = QVBoxLayout()
        
        self.mainFrind.setLayout(QVMainLeft)
        self.mainFrind.setMaximumWidth(60)
        self.mainFrind.leaveEvent = lambda _:self.mainFrindLeave()
        self.mainFrind.enterEvent = lambda e: self.mainFrindEnter(e)
        self.mainmenu = QWidget()
        self.mainmenu.setMaximumWidth(0)
        self.menuWidget()
        self.chatmain= QFrame()
        self.chatmain.setContentsMargins(0,0,0,0)
        
        self.chatmain.setLayout(self.QVMainRight)
        
        self.FrindInfomain = QFrame()
        self.FrindInfomain.hide()
        self.FrindInfomainLayout = QVBoxLayout()
        self.FrindInfomain.setLayout(self.FrindInfomainLayout)
        self.buttonHBox = QHBoxLayout()
        self.FrindInfomainUI("")
        
        
        
        self.addFrindMain = QFrame()
        self.addFrindMain.hide()
        self.addFrindMainUI()
        
        self.myacounntMain = QFrame()
        self.myacounntMain.hide()
        self.myacounntMainUI()
        
        self.mysttingesmain = QFrame()
        self.mysttingesmain.hide()
        self.mysttingesmainUI()
        
        self.upchatInfoUsermainFrame = QFrame()
        self.upchatInfoUsermainFrame.hide()
        
        HBoxSearsh = QHBoxLayout()
        HBoxSearsh.setContentsMargins(5,0,0,5)
        
        self.mainFrind.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(1)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainFrindeAndShatLayout.setSpacing(0)
        connectLayout.setSpacing(0)
        self.QVMainRight.setSpacing(0)
        self.QVMainRight.setContentsMargins(0,0,0,0)
        QVMainLeft.setSpacing(0)
        QVMainLeft.setContentsMargins(0,0,0,0)
        
        self.scrollarea = QScrollArea()
        self.scrollarea.setStyleSheet("QScrollArea{border: 0px;}")
        self.scrollarea.setAlignment(Qt.AlignBottom)
        self.scrollarea.verticalScrollBar().rangeChanged.connect(self.ResizeScroll)
        
        self.QVMainRight.addWidget(self.upchatInfoUsermainFrame)
        
        self.Label = QLabel("Select Frind Start chat")
        self.Label.setStyleSheet("QLabel{color:#fff; font-size:20px;}")
        self.Label.setAlignment(Qt.AlignCenter)
        self.QVMainRight.addStretch()
        self.QVMainRight.addWidget(self.Label, Qt.AlignCenter)
        
        self.QVMainRight.addWidget(self.scrollarea,90)
        self.scrollarea1 = QScrollArea()
        self.scrollarea1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollarea1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        bar = self.scrollarea1.verticalScrollBar()
        bar.rangeChanged.connect( lambda _,y: bar.setValue(y) )
           
        QVMainLeft.addLayout(HBoxSearsh,20)
        QVMainLeft.addWidget(self.scrollarea1)
        self.scrollarea1.setFixedWidth(60)

        
        QHMainRightBotton = QHBoxLayout()
        QHMainRightBotton.setSpacing(0)
        QHMainRightBotton.setContentsMargins(0,0,0,0)
        
        self.sendLine = QTextEdit()
        
        self.sendLine.setPlaceholderText(" Write a message...")
        self.sendLine.textChanged.connect(self.sendLineChanged)
        self.connectLabel = QLabel("No Connect")
        
        self.sendButton = QPushButton()
        self.sendButton.hide()
        self.sendButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.sendButton.clicked.connect(self.senMassag)
        shortcut = QShortcut(QKeySequence("Enter"), self)
        shortcut.activated.connect(self.senMassag)
        
        self.sendFile = QPushButton()
        self.sendFile.setCursor(QCursor(Qt.PointingHandCursor))
        self.sendFile.clicked.connect(self.SendFile)
        
        
        self.sendLine.setStyleSheet(self.styleSendLine())
        self.sendButton.setStyleSheet(self.styleSendButton())
        self.sendFile.setStyleSheet(self.styleSendFile())
        self.connectLabel.setStyleSheet(self.connectLabelStyal(False))
        
        QHMainRightBotton.addWidget(self.sendFile)
        QHMainRightBotton.addWidget(self.sendLine)
        QHMainRightBotton.addWidget(self.sendButton)
        

        
        self.QFMainRightBotton= QFrame()
        self.QFMainRightBotton.setFixedHeight(40)
        self.QFMainRightBotton.hide()
        self.QFMainRightBotton.setContentsMargins(0,0,0,0)
        self.QFMainRightBotton.setStyleSheet(self.QFMainRightBottonStyle())
        self.QFMainRightBotton.setLayout(QHMainRightBotton)
        
        
        QHMainBlock = QHBoxLayout()
        self.blockLable = QLabel("You blocked your friend")
        QHMainBlock.addWidget(self.blockLable,alignment=Qt.AlignCenter)
        self.QFMainRightBlock= QFrame()
        self.QFMainRightBlock.setFixedHeight(40)
        self.QFMainRightBlock.hide()
        self.QFMainRightBlock.setContentsMargins(0,0,0,0)
        self.QFMainRightBlock.setStyleSheet(self.QFMainRightBottonStyle())
        self.QFMainRightBlock.setLayout(QHMainBlock)
        
        self.QVMainRight.addWidget(self.QFMainRightBotton,12)
        self.QVMainRight.addWidget(self.QFMainRightBlock,12)
        
        mainFrindeAndShatLayout.addWidget(self.mainmenu,15)
        mainFrindeAndShatLayout.addWidget(self.mainFrind)
        mainFrindeAndShatLayout.addWidget(self.chatmain,70)
        mainFrindeAndShatLayout.addWidget(self.FrindInfomain,70)
        mainFrindeAndShatLayout.addWidget(self.addFrindMain,70)
        mainFrindeAndShatLayout.addWidget(self.myacounntMain,70)
        mainFrindeAndShatLayout.addWidget(self.mysttingesmain,70)
        
        connectLayout.addStretch()
        connectLayout.addWidget(self.connectLabel)
        connectLayout.addStretch()
        connectLayout.setContentsMargins(0,0,0,5)
        
        mainLayout.addLayout(connectLayout)
        
        
        mainLayoutupchat = QHBoxLayout()
        Layoutupchatinfo = QVBoxLayout()
        LayoutName = QHBoxLayout()
        mainLayoutupchat.setContentsMargins(5,0,0,0)
        Layoutupchatinfo.setContentsMargins(0,0,0,0)
        LayoutName.setContentsMargins(0,0,0,0)
        
        self.upchatInfoUsermainFrame.setFrameShape(QFrame.StyledPanel)
        self.upchatInfoUsermainFrame.setFrameShadow(QFrame.Raised)
        self.upchatInfoUsermainFrame.setCursor(QCursor(Qt.PointingHandCursor))
        self.upchatInfoUsermainFrame.setContentsMargins(5,0,0,5)
        self.upchatInfoUsermainFrame.mouseReleaseEvent=lambda event:self.UpchatInfoUsermainFrame(event)
        self.upchatInfoUsermainFrame.setStyleSheet(u"""
                                    QFrame{background-color:  rgb(23, 33, 43); border-radius: 0px;}
                                    QFrame:hover{background-color:  rgb(23, 33, 43)}
                                    QLabel:hover{background-color:  rgb(23, 33, 43)}
                                    """)
        self.lableNameupchat = QLabel("")
        self.lableNameupchat.setStyleSheet("color:#fff; font-size:16px ;")
        self.lableNameupchat.setContentsMargins(0,0,0,0)
        
        self.lableBioupchat = QLabel("")
        self.lableBioupchat.setStyleSheet("color:#a6a6a6; font-size:12px ;")
        self.lableBioupchat.setContentsMargins(0,0,0,0)
        self.lableBioupchat.setTextFormat(Qt.PlainText)
        
        self.lableimageupchat = QLabel()
        self.lableimageupchat.setFixedSize(40,40)
        self.lableimageupchat.setCursor(QCursor(Qt.PointingHandCursor))
        self.lableimageupchat.setStyleSheet("""QLabel{
                                            border-image:url(img/menu.png);
                                            /*margin: 0px 0px 5px 3px;*/
                                        }
                                        """)
        
        self.connectFrind= QLabel("")
        self.connectFrind.setAlignment(Qt.AlignCenter)
        self.connectFrind.setStyleSheet("QLabel{background-color:#ff4d4d;border-radius: 5px;}")
        self.connectFrind.setFixedSize(10,10)
        
        LayoutName.addWidget(self.lableNameupchat)
        LayoutName.addWidget(self.connectFrind)
        LayoutName.addStretch()
        Layoutupchatinfo.addLayout(LayoutName) 
        Layoutupchatinfo.addWidget(self.lableBioupchat)
        mainLayoutupchat.addWidget(self.lableimageupchat) 
        mainLayoutupchat.addLayout(Layoutupchatinfo)
        self.upchatInfoUsermainFrame.setLayout(mainLayoutupchat)
        
        self.createLayout_Container_Frind()
        
        self.searshFrind = QLineEdit()
        self.searshFrind.hide()
        self.searshFrind.setPlaceholderText("Search")
        self.searshFrind.setMinimumHeight(27)
        self.searshFrind.setTextMargins(10,0,0,0)
        self.searshFrind.setContentsMargins(5,0,5,5)
        self.searshFrind.textChanged.connect(self.searshChanged)
        self.searshFrind.setStyleSheet("""QLineEdit{
                                        border: 1px solid rgb(36, 47, 61);
                                        background-color: rgb(14, 22, 33);
                                        font-size:16px;
                                        color:#fff;
                                        border-radius: 4px;
                                        }""")
        self.clearSearsh = QPushButton("clear")
        self.menuButton = QPushButton()
        self.menuButton.setFixedSize(38,38)
        self.menuButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.menuButton.clicked.connect(self.MenuAction)
        self.menuButton.setStyleSheet("""QPushButton{
                                            border-image:url(img/menu.png);
                                            margin: 0px 0px 5px 3px;
                                        }
                                        QPushButton:hover{
                                            border-image:url(img/menuH.png);
                                            }
                                        """)
        
        
        HBoxSearsh.addWidget(self.menuButton)
        HBoxSearsh.addStretch()
        HBoxSearsh.addWidget(self.searshFrind)
        
        
        ##################################################

        mainLayout.addLayout(mainFrindeAndShatLayout)
        
        
        self.setLayout(mainLayout)
    
    def UpchatInfoUsermainFrame(self,_):
        self.FrindInfomain.show()
        self.chatmain.hide()
        print(f"{sendTo} :")
        self.FrindInfomainUI(sendTo)
        
        
    def sendLineChanged(self):
        if self.sendLine.toPlainText() == "":
            self.sendButton.hide()
            return
        self.sendButton.show()
    
    def ResizeScroll(self,_,Max):
        self.scrollarea.verticalScrollBar().setValue(Max)
    

    def mainFrindLeave(self):
        global _startAnimation1, _isStart
        print("\nmainFrindLeave\n")
        _startAnimation1 = False
        
        if self.searshFrind.hasFocus() or self.mainFrind.width() == 0 or selectchate == True:
            return
        if _isStart and  menuaction == 0:
            self.scrollarea1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            width = 200
            newWidth = 60
            self.animation = QPropertyAnimation(self.mainFrind, b"maximumWidth")
            self.animation.setDuration(1000)
            self.animation.setStartValue(width)
            self.animation.setEndValue(newWidth)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()
            self.searshFrind.hide()
            _isStart = False
            print("hode width")
            print("is .. :",self.mainmenu.isVisible())
        if menuaction == 1:
            self.mainFrind.setMaximumWidth(0)
                
        
        
    def mainFrindEnterProssor(self):
        global _isStart
        if _startAnimation1 == False and  menuaction == 0:
            return
        self.scrollarea1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        width = 60
        newWidth = 200
        self.animation11 = QPropertyAnimation(self.mainFrind, b"maximumWidth")
        self.animation11.setDuration(250)
        self.animation11.setStartValue(width)
        self.animation11.setEndValue(newWidth)
        self.animation11.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation11.start()

        self.scrollarea1.setFixedWidth(200)
        _isStart = True  
        
        if menuaction == 1:
            self.mainFrind.setMaximumWidth(0)
        self.searshFrind.show()

    def mainFrindEnter(self,_):
        global _startAnimation1, _isStart
        _startAnimation1 = True
        
        if self.searshFrind.hasFocus():
            return
        self.thread1.AnimationCheck()
        if menuaction == 1:
            self.mainFrind.setMaximumWidth(0)
        
    
    def updataConecctDB(self,username):
        try:
            self.db = mysql.connector.connect(user='root', password='123456', host='localhost',port=3307, db="chat")
            self.curdb = self.db.cursor(buffered=True)
        except:
            pass
        self.thread1.GetInfoDataUser()
    
    def FrindInfomainUI(self, username):
        if username == "":
            return
        for i in reversed(range(self.FrindInfomainLayout.count())):
            item = self.FrindInfomainLayout.itemAt(i)

            if item.widget():
                item.widget().close()


            # remove the item from layout
            self.FrindInfomainLayout.removeItem(item)
        for i in reversed(range(self.buttonHBox.count())):
            item = self.buttonHBox.itemAt(i)

            if item.widget():
                item.widget().close()
            # remove the item from layout
            self.buttonHBox.removeItem(item)
        
        loading = QLabel("Loading ...")
        loading.setStyleSheet("QLabel{font-size:20px; color:#cccccc;}")
        self.buttonHBox.addWidget(loading, alignment=Qt.AlignCenter)
        self.FrindInfomainLayout.addLayout(self.buttonHBox)
        
        threading.Thread(target=self.updataConecctDB, args=(username,)).start()
        
    def FrindInfomainUI1(self,username= ""):
        username = sendTo
        print("\nFrindInfomainUI1")
        for i in reversed(range(self.FrindInfomainLayout.count())):
            item = self.FrindInfomainLayout.itemAt(i)

            if item.widget():
                item.widget().close()


            # remove the item from layout
            self.FrindInfomainLayout.removeItem(item)
        for i in reversed(range(self.buttonHBox.count())):
            item = self.buttonHBox.itemAt(i)

            if item.widget():
                item.widget().close()
            # remove the item from layout
            self.buttonHBox.removeItem(item)
        try:
            self.curdb.execute(f"SELECT name ,bio,image FROM user WHERE username='{username}'")
            dataFrind  = self.curdb.fetchone()
            self.curdb.execute(f"SELECT block FROM frind WHERE username='{_my_username}' and frinduser='{username}';")
            myBlock = self.curdb.fetchone()
            self.curdb.execute(f"SELECT block FROM frind WHERE username='{username}' and frinduser='{_my_username}';")
            youBlock = self.curdb.fetchone()
        except:
            dataFrind = self.curdblist.execute("SELECT name ,bio,image from frind WHERE username=?",(username,)).fetchone()
            myBlock = ['0',]
            youBlock = ['1',]
        print("\ndataFrind:",dataFrind)
        _dirImage = dirImage.replace("\\","/")
        Image = QLabel("")
        Image.setAlignment(Qt.AlignCenter)
        Image.setContentsMargins(30,0,90,0)
        i = _dirImage+"/"+ dataFrind[2]
        Image.setStyleSheet("QLabel{border-image: url('"+i+"');border-radius: 20px; background-color: rgba(255, 255, 255,70);}")   
        Image.setScaledContents(True)
        Image.setMinimumSize(200,200)
        Image.setMaximumSize(300,300)        
        
        
        usernameFrind = QLabel("UserName: "+username)
        usernameFrind.setStyleSheet("QLabel{color:#fff;font-size:16px;}")
        usernameFrind.setTextInteractionFlags(Qt.TextSelectableByMouse)
        nameFrind = QLabel("Name: "+dataFrind[0])
        nameFrind.setStyleSheet("QLabel{color:#fff;font-size:16px;}")
        nameFrind.setTextInteractionFlags(Qt.TextSelectableByMouse)
        bioLabel = QLabel("Bio:")
        bioLabel.setStyleSheet("QLabel{color:#fff;font-size:16px;}")
        bio = QTextEdit(dataFrind[1])
        bio.setStyleSheet("QTextEdit{color:#fff;font-size:14px;}")
        bio.setFixedWidth(200)
        bio.setReadOnly(True)
        

        back = QPushButton("B A C K")
        back.setMinimumHeight(30)
        back.setStyleSheet("""QPushButton{
                        color:#fff;
                        font-size:14px;
                       
                        }
                            QPushButton:hover{
                                background-color: #999999;
                                color: #1D2C3A;
                                font-size:14px;
                                border: 3px solid #33ff33;
                                 margin-top: 150px;
                margin-bottom: 150px;
                                } 
                           """)
        back.clicked.connect(self.backFrindInfomain)
        
        
        deletShat = QPushButton("DELET Shate")
        deletShat.setMinimumHeight(30)
        deletShat.clicked.connect(lambda: self.DeletShat(username))
        deletShat.setStyleSheet("""QPushButton{
                color:#ff3333;
                font-size:14px;
                background-color:#1D2C3A;
                border:0px;
            }
            QPushButton:hover{
                background-color: #999999;
                                color: #1D2C3A;
                
                border:3px solid #ff3333;
                font-size:14px;
                margin-top: 150px;
                margin-bottom: 150px;
            }
            """)
        
        
        self.block = QPushButton("B L O C K")
        self.block.setMinimumHeight(30)
        self.block.clicked.connect(lambda: self.Block(username))
        self.block.setStyleSheet("""QPushButton{
                color:#ff3333;
                font-size:14px;
                background-color:#1D2C3A;
                border:0px;
                height: 20px;
                width: 100%;
            }
            QPushButton:hover{
                background-color: #999999;
                                color: #1D2C3A;
                
                border:3px solid #ff3333;
                font-size:14px;
                margin-top: 150px;
                margin-bottom: 150px;
            }
            QPushButton:disabled{
                background-color: #302F2F;
                border-width: 2px;
                border-color: #3A3939;
                border-style: solid;
                padding-top: 2px;
                padding-bottom: 2px;
                padding-left: 10px;
                padding-right: 10px;
                /*border-radius: 2px;*/
                color: #808080;
            }
            
            """)
        
        
        
        
        print(f"\n\nusername='{_my_username}' and frinduser='{username}'\nisBlock:{myBlock}\n\n")
        if myBlock[0] == "1":
            self.block.setText("U n  B L O C K")
            
        print(f"\n\nusername='{_my_username}' and frinduser='{username}'\nisBlock:{youBlock}\n\n")
        if youBlock != None:
            if youBlock[0] == "1":
                self.block.setEnabled(False)
            

        
        self.buttonHBox.addWidget(self.block)
        self.buttonHBox.addWidget(back)
        self.buttonHBox.addWidget(deletShat)
        
        self.FrindInfomainLayout.addWidget(Image, alignment=Qt.AlignHCenter)
        self.FrindInfomainLayout.addWidget(usernameFrind, alignment=Qt.AlignHCenter)
        self.FrindInfomainLayout.addWidget(nameFrind, alignment=Qt.AlignHCenter)
        self.FrindInfomainLayout.addWidget(bioLabel, alignment=Qt.AlignHCenter)
        self.FrindInfomainLayout.addWidget(bio, alignment=Qt.AlignHCenter)
        self.FrindInfomainLayout.addStretch()
        self.FrindInfomainLayout.addLayout(self.buttonHBox)    
        
        
        
    def backFrindInfomain(self):
        
        self.FrindInfomain.hide()
        self.chatmain.show()
    def DeletShat(self,username):
        global _listShat
        messageDelete = QMessageBox(self)
        messageDelete.setWindowIcon(QIcon("img\account.png"))
        messageDelete.setIcon(QMessageBox.Warning)
        messageDelete.setFixedSize(500,300)
        messageDelete.setWindowTitle('DELET SHATE')
        messageDelete.setStyleSheet("""QMessageBox{background:rgb(29, 44, 58);color:#fff;}
                                    QLabel{color:#fff;font-size:14px;padding: 10px 20px 10px 20px;}
                                    QPushButton{
                                        color:#ff3333;
                                        font-size:14px;
                                        background-color:#1D2C3A;
                                        border:0px;
                                        margin: 5px 10px 5px 10px;
                                        height: 20px;
                                        width: 100%;
                                    }
                                    QPushButton:hover{
                                        background-color: #999999;
                                                        color: #1D2C3A;
                                        
                                        border:2px solid #ff3333;
                                        font-size:14px;
                                        margin: 150px 10px 150px 10px;
                                        padding: 10px 20px 10px 20px;
                                    }
                                    """)
        messageDelete.setTextFormat(Qt.RichText)
        messageDelete.setText("DELET SHATE")
        messageDelete.setInformativeText("You are about to delete all messages between you and your friend,\n you have to know that you cannot retrieve them again and that they are erased from you and remain with your friend")
        
        messageDelete.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        stateMessage =  messageDelete.exec_()

        if stateMessage == QMessageBox.Ok:
            
            self.curdb.execute(f"DELETE FROM messages WHERE username = '{_my_username}' and sendto = '{username}';")
            self.dblite.execute("DELETE FROM messages WHERE username=?",(username,))
            self.dblite.commit()


            index = int(self.LableIndx.text())

            Frind[index][username]["chat"] = []
            _listShat = []
            print("yas",username)
            print("yas",Frind[index][username])
            self.createLayout_Container_shat([[],Frind[int(self.LableIndx.text())][sendTo],index])
            self.FrindInfomain.hide()
            self.chatmain.show()
            self.UpDate()

        if stateMessage == QMessageBox.Cancel:
            print("Cancel")

    def Block(self,username,menuBlock=0):
        print("Block")
        messageDelete = QMessageBox(self)
        messageDelete.setWindowIcon(QIcon("img\account.png"))
        messageDelete.setIcon(QMessageBox.Warning)
        messageDelete.setFixedSize(500,300)
        messageDelete.setWindowTitle('C-Cath')
        messageDelete.setStyleSheet("""QMessageBox{background:rgb(29, 44, 58);color:#fff;}
                                    QLabel{color:#fff;font-size:14px;padding: 10px 20px 10px 20px;}
                                    QPushButton{
                                        color:#ff3333;
                                        font-size:14px;
                                        background-color:#1D2C3A;
                                        border:0px;
                                        margin: 5px 10px 5px 10px;
                                        height: 20px;
                                        width: 100%;
                                    }
                                    QPushButton:hover{
                                        background-color: #999999;
                                                        color: #1D2C3A;
                                        
                                        border:2px solid #ff3333;
                                        font-size:14px;
                                        margin: 150px 10px 150px 10px;
                                        padding: 10px 20px 10px 20px;
                                    }
                                    """)
        messageDelete.setTextFormat(Qt.RichText)
        if menuBlock == 1:
            messageDelete.setText("<h1 style='color:#99ff99;'>UN BLOCK FRIND</h1>")
            messageDelete.setInformativeText("You are about to prevent a friend from sending you messages,\n you will not receive from him and you cannot send him messages")
            
            messageDelete.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            stateMessage =  messageDelete.exec_()

            if stateMessage == QMessageBox.Ok:
                print(_my_username, " ",username)
                self.curdb.execute(f"UPDATE  frind SET  block='0'  WHERE username = '{_my_username}' and frinduser = '{username}';")
                self.db.commit()
                self.curdblist.execute("UPDATE frind SET block='0' WHERE username=?",(username,))
                self.dblite.commit()
                _index = 0
                for i in Frind :
                    c = i.get(username)
                    if c != None :
                        break
                    _index += 1
                print(f"Frind[index][username]:{Frind[_index][username]}")
                Frind[_index][username]["block"] = '0'

                self.MenuBlockConnect()
                self.MenuBlockConnect()
                self.QFMainRightBlock.hide() 
                self.QFMainRightBotton.show()
                

            if stateMessage == QMessageBox.Cancel:
                print("Cancel")
            return  
        print(self.block.text())
        if self.block.text() == "B L O C K" :
            messageDelete.setText("<h1 style='color:#ff3333;'>BLOCK FRIND</h1>")
            messageDelete.setInformativeText("You are about to prevent a friend from sending you messages,\n you will not receive from him and you cannot send him messages")
            
            messageDelete.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            stateMessage =  messageDelete.exec_()

            if stateMessage == QMessageBox.Ok:
                print(_my_username)
                self.curdb.execute(f"UPDATE  frind SET  block='1'  WHERE username = '{_my_username}' and frinduser = '{username}';")
                self.db.commit()
                self.curdblist.execute("UPDATE frind SET block='1' WHERE username=?",(username,))
                self.dblite.commit()
                index = int(self.LableIndx.text())
                Frind[index][username]["block"] = '1'
                self.QFMainRightBlock.show() 
                self.QFMainRightBotton.hide()
                self.createLayout_Container_shat([Frind[index][username]["chat"],Frind[int(self.LableIndx.text())][sendTo],index])
                self.FrindInfomain.hide()
                self.chatmain.show()
                self.UpDate()

            if stateMessage == QMessageBox.Cancel:
                print("Cancel")
        elif self.block.text() == "U n  B L O C K":
            messageDelete.setText("<h1 style='color:#99ff99;'>UN BLOCK FRIND</h1>")
            messageDelete.setInformativeText("You are about to prevent a friend from sending you messages,\n you will not receive from him and you cannot send him messages")
   
            messageDelete.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            stateMessage =  messageDelete.exec_()

            if stateMessage == QMessageBox.Ok:
                print(_my_username)
                self.curdb.execute(f"UPDATE  frind SET  block='0'  WHERE username = '{_my_username}' and frinduser = '{username}';")
                self.db.commit()
                self.curdblist.execute("UPDATE frind SET block='0' WHERE username=?",(username,))
                self.dblite.commit()
                index = int(self.LableIndx.text())
                Frind[index][username]["block"] = '0'
                self.QFMainRightBlock.hide() 
                self.QFMainRightBotton.show()
                self.createLayout_Container_shat([Frind[index][username]["chat"],Frind[int(self.LableIndx.text())][sendTo],index])
                self.FrindInfomain.hide()
                self.chatmain.show()
                self.UpDate()

            if stateMessage == QMessageBox.Cancel:
                print("Cancel")

    
    def addFrindMainUI(self):
        v = QVBoxLayout()
        v.setAlignment(Qt.AlignCenter)
        addfrindLabel = QLabel("Search Friend in UserName")
        addfrindLabel.setStyleSheet("color:#fff;font-size:16px;margin-top:30px;margin-bottom:15px;")
        addfrindLabel.setAlignment(Qt.AlignCenter)
        
        self.searshFrindLineEdit = QLineEdit()
        self.searshFrindLineEdit.textChanged.connect(self.SearshFrindChanged)
        self.searshFrindLineEdit.setPlaceholderText("Search")
        self.searshFrindLineEdit.setMinimumHeight(50)
        self.searshFrindLineEdit.setStyleSheet("""QLineEdit{
                                        border: 1px solid rgb(36, 47, 61);
                                        background-color: rgb(14, 22, 33);
                                        font-size:16px;
                                        color:#fff;
                                        margin-right:30px;
                                        margin-left:30px;
                                        padding:10px;
                                        border-radius: 10px;
                                        }""")
        self.searshFrindscrollarea = QScrollArea()
        self.searshFrindscrollarea.setWidgetResizable(True)
        
        

        self.messageAddfrindLabel = QLabel()
        self.messageAddfrindLabel.setStyleSheet("color:#fff;font-size:16px;margin-top:5px;margin-bottom:5px;")
        self.messageAddfrindLabel.setAlignment(Qt.AlignCenter)
        self.messageAddfrindLabel.hide()
        
        
        v.addWidget(addfrindLabel)
        v.addWidget(self.searshFrindLineEdit)
        v.addWidget(self.searshFrindscrollarea,100)
        v.addWidget(self.messageAddfrindLabel)
        v.addStretch()
        self.addFrindMain.setLayout(v)
      
    def myacounntMainUI(self):
        Vmain = QVBoxLayout()
        
        hMage = QHBoxLayout()
        hMage.setContentsMargins(0,30,0,0)
        
        image = QLabel("My Image: ")
        image.setStyleSheet("QLabel{color:#fff;font-size:16px;}")
        myImage = QLabel("")
        myImage.setAlignment(Qt.AlignCenter)
        myImage.setContentsMargins(30,0,90,0)
        i = dirImage.replace("\\","/")+"/"+_myData['img']
        myImage.setStyleSheet("QLabel{border-image: url('"+i+"');border-radius: 20px; background-color: rgba(255, 255, 255,70);}")
  
        myImage.setScaledContents(True)
        myImage.setMinimumSize(200,200)
        myImage.setMaximumSize(300,300)
        hMage.addWidget(myImage)

        
        huserName = QHBoxLayout()
        huserName.setContentsMargins(0,30,0,0)
        
        username = QLabel("UserName: ")
        username.setStyleSheet("QLabel{color:#fff;font-size:16px;}")
        myUserName = QLabel(_myData['username'])
        myUserName.setContentsMargins(0,0,0,0)
        myUserName.setStyleSheet("QLabel{color:#fff;font-size:16px;}")
        myUserName.setTextInteractionFlags(Qt.TextSelectableByMouse)
        huserName.addWidget(username)
        huserName.addWidget(myUserName)
        
        hName = QHBoxLayout()
        hName.setContentsMargins(0,30,80,0)
        
        name = QLabel("Name: ")
        name.setStyleSheet("QLabel{color:#fff;font-size:16px;}")
        self.myname = QLineEdit()
        self.myname.setText(_myData['name'])
        self.myname.setMaximumHeight(100)
        self.myname.setContentsMargins(0,0,0,0)
        self.myname.setStyleSheet("QLineEdit{color:#fff;font-size:16px;}")
        
        
        hName.addWidget(name,50)
        hName.addWidget(self.myname,50)
        
        bioLayout = QHBoxLayout()
        bioLayout.setContentsMargins(0,30,80,0)
        
        bioLablel = QLabel("Bio: ")
        bioLablel.setStyleSheet("QLabel{color:#fff;font-size:16px;}")
        self.bioEdit = QTextEdit()
        self.bioEdit.setPlainText(_myData['bio'])
        self.bioEdit.setAcceptRichText(False)
        self.bioEdit.setMaximumHeight(100)
        bioLayout.addWidget(bioLablel,50)
        bioLayout.addWidget(self.bioEdit,50)
        
        saveLayout = QHBoxLayout()
        saveLayout.setContentsMargins(0,30,80,0)
        
        self.saveMyAcounnt = QPushButton("Save")
        self.saveMyAcounnt.setStyleSheet("QPushButton{color:#fff;font:14px;}QPushButton:hover{border: 1px solid #1464A0;}QPushButton:pressed {color:rgb(14, 22, 33);}")
        self.saveMyAcounnt.setMinimumWidth(100)
        self.saveMyAcounnt.clicked.connect(self.SaveMyAcounnt)
        
        saveLayout.addStretch()
        saveLayout.addWidget(self.saveMyAcounnt)
        saveLayout.addStretch()
        
        saveLableLayout = QHBoxLayout()
        saveLableLayout.setContentsMargins(0,30,80,0)
        
        self.saveLable = QLabel("")
        self.saveLable.setAlignment(Qt.AlignCenter)
        saveLableLayout.addWidget(self.saveLable)
        
        Vmain.addLayout(hMage)  
        Vmain.addLayout(huserName)
        Vmain.addLayout(hName)
        Vmain.addLayout(bioLayout)
        Vmain.addLayout(saveLayout)
        Vmain.addStretch()
        Vmain.addLayout(saveLableLayout)
        
        self.myacounntMain.setStyleSheet("QFrame{color:#fff;}")
        self.myacounntMain.setLayout(Vmain)
   
    def SaveMyAcounnt(self):
        
        def T(text):
            self.saveLable.setText(text)
            time.sleep(3)
            self.saveLable.setText("")
            
        
        self.saveLable.setText("Loading ...")
        print(self.bioEdit.toPlainText())
        print(self.myname.text())
        _myData["bio"] = self.bioEdit.toPlainText().replace('"1','”')
        _myData["name"] = self.myname.text()
        try:
            self.curdb.execute('UPDATE user SET name="%s", bio="%s" where username="%s";'%(_myData['name'],str(_myData['bio']),_myData['username']))
            self.curdblist.execute("UPDATE myData SET name=?, bio=? where username=?;",(_myData['name'],_myData['bio'],_myData['username']))
            self.db.commit()
            self.dblite.commit()
        except Exception as E:
            print(f"SaveMyAcounnt Error: {E}")
            threading.Thread(target=T, args=("Error",)).start()
            infoTxt = f"""
            <p style="font-size:16px; color:#fff; margin:0px;">{_myData["name"].capitalize()}</p>
            <p style="font-size:12px; color:#b3b3b3;margin:0px;">.   {_myData["username"]}</p>
            """
            return
        infoTxt = f"""
        <p style="font-size:16px; color:#fff; margin:0px;">{_myData["name"].capitalize()}</p>
        <p style="font-size:12px; color:#b3b3b3;margin:0px;">.   {_myData["username"]}</p>
        """
        self.menuUserName.setText(infoTxt)
        threading.Thread(target=T, args=("Dan Save",)).start()
    
    def mysttingesmainUI(self):
        HMain = QHBoxLayout()
        VMainLeft = QVBoxLayout()
        VMainRight = QVBoxLayout()
        
        VMainLeft.setSpacing(20)
        
        HMain.addLayout(VMainLeft)
        HMain.addLayout(VMainRight)
        
        HNotification = QHBoxLayout()
        VMainLeft.addLayout(HNotification)
        HNotification.setContentsMargins(10,50,0,0)
        HNotification.setSpacing(0)
        self.mysttingesmain.setLayout(HMain)
        
        self.LabelNotification = QLabel("Notifications")
        self.LabelNotification.setStyleSheet("QLabel{color:#fff;font-size:16px;}")
        HNotification.addWidget(self.LabelNotification)
        
        
        
        boxSize = QLabel()
        boxSize.setFixedWidth(50)
        HNotification.addWidget(boxSize)
        
        
        self.mainToggle = AnimatedToggle()

        
        HNotification.addWidget(self.mainToggle)
        
        notifications =  self.curdblist.execute("SELECT notifications FROM stting").fetchone()
        print(f"\n\nnotifications:{notifications}")
        if notifications[0] == "0":
            self.mainToggle.setChecked(False)
        else:
            self.mainToggle.setChecked(True)
        self.mainToggle.stateChanged.connect(self.NotificationState)
        
        HBlock = QHBoxLayout()
        self.MenuBlock = QPushButton("Menu Block",iconSize=QSize(38, 38))
        self.MenuBlock.setLayoutDirection(Qt.RightToLeft)
        self.MenuBlock.setMinimumSize(100,50)
        self.MenuBlock.setIcon(QIcon("img/arrow_backR.png"))
        self.MenuBlock.setIconSize(QSize(38, 38))
        self.MenuBlock.clicked.connect(self.MenuBlockConnect)
        HBlock.addWidget(self.MenuBlock)
        self.MenuBlockStyle = """
                                     QPushButton{
                                        color:#ff3333;
                                        font-size:16px;
                                        background-color:#1D2C3A;
                                        border:0px;
                                        margin: 5px 10px 5px 10px;
                                        height: 20px;
                                        width: 150%;
                                        font-size:16px;
                                        padding-left:0px;
                                    }
                                    QPushButton:hover{
                                        background-color: #999999;
                                        color: #1D2C3A;
                                        
                                        border-left:3px solid #ff3333;
                                        border-right:3px solid #ff3333;
                                        font-size:17px;
                                        /*margin:;*/
                                        /*padding: 10px 10px 10px 20px;*/
                                    }
                                    
                                     """
        self.MenuBlock.setStyleSheet(self.MenuBlockStyle)
        HBlock.addStretch()
        VMainLeft.addLayout(HBlock, 2)
        
        self.scrollareaBlock = QScrollArea()
        self.scrollareaBlock.hide()
        self.scrollareaBlock.setWidgetResizable(True)
        VMainRight.addWidget(self.scrollareaBlock)
        
        
            
        HNotification.addStretch()
        VMainLeft.addStretch()
        
    def UIUnBlock (self, username):
        PushButtonUnblock = QPushButton("U n b l o c k")
        PushButtonUnblock.setStyleSheet("""
                                        QPushButton{
                                            color:#fff;
                                            border:1px solid #ff6666;
                                            font-size:14;
                                            padding:5px 10px 5px 10px;
                                        }
                                        QPushButton:hover{
                                            color:#99ff99;
                                            border:1px solid #fff000;
                                            font-size:14;
                                        }
                                        """)
        PushButtonUnblock.clicked.connect(lambda: self.PushButtonUnBlockC(username))
        return PushButtonUnblock
    def MenuBlockConnect(self):
        global blockStat
        print(blockStat)
        if blockStat == 0:
            blockStat = 1 
            self.curdb.execute(f"SELECT frinduser FROM  frind WHERE username = '{_my_username}' and block='{1}' ;")
            usernames =  self.curdb.fetchall()
            self.WidgetBlock = QFrame()
            self.VBoxSB = QVBoxLayout()
            self.WidgetBlock.setLayout(self.VBoxSB)
            self.scrollareaBlock.setWidget(self.WidgetBlock)
            
            print(usernames)
            if usernames == []:
                HBoxuser = QHBoxLayout()
                labelImag = QLabel("No friend on block list")
                labelImag.setStyleSheet("QLabel{color:#fff;font-size:14px;}")
                HBoxuser.addWidget(labelImag,alignment=Qt.AlignHCenter)
                self.VBoxSB.addLayout(HBoxuser)
            else:
                for i in usernames:
                    HBoxuser = QHBoxLayout()
                    labelImag = QLabel()
                    pathImage= dirImage.replace("\\","/")
                    labelImag.setStyleSheet(f"""border-image: url('{pathImage}/{i[0]}.png');border-radius: 20px; background-color: rgba(255, 255, 255,70);""")
                    labelImag.setMargin(20)
                    labelImag.setScaledContents(True)

                    labelImag.setFixedSize(42,42)
                    HBoxuser.addWidget(labelImag)

                    labelName = QLabel(i[0])
                    labelName.setStyleSheet("QLabel{color:#fff;font-size:16px; padding-left:10px;}")
                    HBoxuser.addWidget(labelName)
                    
                    HBoxuser.addWidget(self.UIUnBlock(i[0]))
                    
                    self.VBoxSB.addLayout(HBoxuser)
                self.VBoxSB.addStretch()
            
            self.scrollareaBlock.show()
            self.MenuBlock.setIcon(QIcon("img/arrow_backL.png"))
            self.MenuBlock.setIconSize(QSize(38, 38))
            self.MenuBlock.setStyleSheet(self.MenuBlockStyle)
        else:
            blockStat = 0
            
            
            self.scrollareaBlock.hide()
            self.MenuBlock.setIcon(QIcon("img/arrow_backR.png"))
            self.MenuBlock.setIconSize(QSize(38, 38))
            self.MenuBlock.setStyleSheet(self.MenuBlockStyle)
    
    def PushButtonUnBlockC(self, username):
        print(username)
        self.Block(username=username, menuBlock=1)
    def NotificationState(self,val):
        print(val)
        n = self.curdblist.execute("SELECT notifications FROM stting").fetchone()
        if n == None:
            self.curdblist.execute("INSERT INTO  stting  (notifications)VALUES(?)",(val,))
        else:
            self.curdblist.execute("UPDATE stting SET notifications=?",(val,))
        self.dblite.commit()
        notifications =  self.curdblist.execute("SELECT notifications FROM stting").fetchone()

        print(notifications)
    def QSliderStyle(self):

        return """
        
            QSlider{
                background-color:argb(0,0,0,0);
            }
            QSlider::groove:horizontal {
                border: 0px solid argb(0,0,0,0);
                height: 9px;

                border-radius: 2px;
                }

            QSlider::handle:horizontal {
                width: 8px;
                height: 8px;
                background-image: url(img/slider.png)
                }

            QSlider::add-page:qlineargradient {
                background: lightgrey;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                }

            QSlider::sub-page:qlineargradient {
                background: blue;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                border-top-left-radius: 4px;
                border-bottom-left-radius: 4px;
                }
                                """
    def deleteLayout(self, layout, Image):
        try:
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        print(widget)
                        
                        widget.deleteLater()
                    else:
                        self.deleteLayout(item.layout())
                sip.delete(layout)
        except:
            pass
        return Image
    
    
    def SearshFrindChangedUITest(self, i):
        searshFrame = QFrame()
        searshFrame.setFrameShape(QFrame.StyledPanel)
        searshFrame.setFrameShadow(QFrame.Raised)
        searshFrame.setCursor(QCursor(Qt.PointingHandCursor))
        searshFrame.setFixedHeight(90)
        searshFrame.setContentsMargins(0,0,0,0)
        
        HBoxsearshFrame = QHBoxLayout()
        HBoxsearshFrame.setSpacing(0)
        HBoxsearshFrame.setContentsMargins(0,0,0,0)
        
        
        
        
        searshFrame.setStyleSheet("""QFrame{color:#fff; font-size:16px;border-radius: 5px;border:1px solid;
                            background-color: rgb(14, 22, 33);
                            }QFrame:hover{background-color:rgb(14, 22, 33);}
                            QLabel{color:#fff; font-size:16px;border: 0;
                            background-color: argb(0,0, 0, 0);
                            }QLabel:hover{background-color:argb(0,0, 0, 0);}
                            QTextEdit{color:#fff; font-size:16px;border: 1px;
                            background-color: background-color:rgb(14, 22, 33);
                            }QTextEdit:hover{background-color:argb(0,0, 0, 0);}
                            """)
        
        
        
        
        ################################################
        _dirImage = dirImage.replace("\\","/")
        Image = QLabel("")
        Image.setAlignment(Qt.AlignCenter)
        Image.setContentsMargins(30,0,90,0)
        img = _dirImage+"/"+ i[0]+".png"
        Image.setStyleSheet("QLabel{border-image: url('img/gg.png');border-radius: 20px; background-color: rgba(255, 255, 255,70);}")   
        Image.setScaledContents(True)
        Image.setMinimumSize(30,50)
        Image.setMaximumSize(300,300)
        
        
        
        VBox = QVBoxLayout()
        HBox = QHBoxLayout()
        
        userName = QLabel(f"Username:\t\t{i[0]}")
        name = QLabel(f"Name:    \t\t{i[1]}")
        bioLabel = QLabel("Bio:")
        bioLabel.hide()
        
        bio = QTextEdit(i[2])
        bio.setFixedSize(600,50)
        bio.setReadOnly(True)
        bio.hide()
        
        HBox.addWidget(bioLabel,10,alignment=Qt.AlignTop)
        HBox.addWidget(bio,90,alignment=Qt.AlignTop)
        
        
        VBox.addWidget(userName,alignment=Qt.AlignLeft)
        VBox.addWidget(name,alignment=Qt.AlignLeft)

        VBox.addLayout(HBox)
        VBox.setContentsMargins(30,0,0,0)
        VBox.setAlignment(Qt.AlignLeft)
        
       
        
        
        HBoxsearshFrame.addWidget(Image,alignment=Qt.AlignLeft)
        HBoxsearshFrame.addLayout(VBox,)
        

        
        self.thread.searshFrameImage(i[0], Image)
        
        
        searshFrame.setLayout(HBoxsearshFrame)
        ######################################################
        searshFrame.mouseReleaseEvent= lambda _:self.Click(i[0])
        searshFrame.leaveEvent = lambda e:self.SearshFrame(e, searshFrame,HBoxsearshFrame,  Image, bioLabel,bio)
        searshFrame.enterEvent = lambda e:self.SearshFrame(e, searshFrame,HBoxsearshFrame, Image,bioLabel,bio)
        
    
        
        return   searshFrame
    def SearshFrindChangedUI(self, i):
        searshFrame = QFrame()
        searshFrame.setFrameShape(QFrame.StyledPanel)
        searshFrame.setFrameShadow(QFrame.Raised)
        searshFrame.setCursor(QCursor(Qt.PointingHandCursor))
        searshFrame.setFixedHeight(90)
        searshFrame.setContentsMargins(0,0,0,0)
        
        HBoxsearshFrame = QHBoxLayout()
        HBoxsearshFrame.setSpacing(0)
        HBoxsearshFrame.setContentsMargins(0,0,0,0)
        
        searshFrame.setLayout(HBoxsearshFrame)
        self.but = QPushButton(f"Username:\t\t{i[0]}\n  Name:\t\t{i[1]}")
        self.but.setObjectName(u"but")
        self.but.setContentsMargins(10, 10, 10, 30)
        searshFrame.mouseReleaseEvent= lambda _:print(f"{i[0]}")
        searshFrame.leaveEvent = lambda e:self.SearshFrame(e, searshFrame,HBoxsearshFrame, i, Image)
        searshFrame.enterEvent = lambda e:self.SearshFrame(e, searshFrame,HBoxsearshFrame,i, Image)
        
        self.but.setStyleSheet("""QPushButton{color:#fff; font-size:16px;border: 0;
                            background-color: argb(0,0, 0, 0);
                            }QPushButton:hover{background-color:argb(0,0, 0, 0);}""")
        
        searshFrame.setStyleSheet("""QFrame{color:#fff; font-size:16px;border-radius: 5px;border:1px solid;
                            background-color: rgb(14, 22, 33);
                            }QFrame:hover{background-color:rgb(14, 22, 33);}
                            QLabel{color:#fff; font-size:16px;border: 0;
                            background-color: argb(0,0, 0, 0);
                            }QLabel:hover{background-color:argb(0,0, 0, 0);}
                            QTextEdit{color:#fff; font-size:16px;border: 1px;
                            background-color: background-color:rgb(14, 22, 33);
                            }QTextEdit:hover{background-color:argb(0,0, 0, 0);}
                            """)
        _dirImage = dirImage.replace("\\","/")
        Image = QLabel("")
        Image.setAlignment(Qt.AlignCenter)
        Image.setContentsMargins(30,0,90,0)
        img = _dirImage+"/"+ i[0]+".png"
        Image.setStyleSheet("QLabel{border-image: url('img/gg.png');border-radius: 20px; background-color: rgba(255, 255, 255,70);}")   
        Image.setScaledContents(True)
        Image.setMinimumSize(30,50)
        Image.setMaximumSize(100,300)
        
        searshFrame.mouseReleaseEvent= lambda _:print(f"{i[0]}")
        searshFrame.leaveEvent = lambda e:self.SearshFrame(e, searshFrame,HBoxsearshFrame, i, Image)
        searshFrame.enterEvent = lambda e:self.SearshFrame(e, searshFrame,HBoxsearshFrame,i, Image)
        
        
        HBoxsearshFrame.addWidget(Image)
        HBoxsearshFrame.addWidget(self.but)
        return   searshFrame
    def SearshFrindChanged(self,text):
        global AddFrind
        if text != "":
            self.curdb.execute(f"SELECT username, name,bio FROM user WHERE username LIKE '{text}%'")
            frind = self.curdb.fetchall()
            print(f"frind: {frind}")
        self.messageAddfrindLabel.hide()
        self.searshFrindscrollareaV = QVBoxLayout()
        searshFrindWidget = QWidget()
        searshFrindWidget.setLayout(self.searshFrindscrollareaV)
        self.searshFrindscrollarea.setWidget(searshFrindWidget)
        myFrind = self.curdblist.execute("SELECT username FROM frind").fetchall()
        
        if text != "":
            for i in frind:
                print(f"\nfrind: {frind}\ni: {i[0]}\tmyFrind :{myFrind}\n")
                if i[0] != _my_username and (i[0],) not in myFrind :
                    # AddFrind[i[0]]=""
                    self.searshFrindscrollareaV.addWidget(self.SearshFrindChangedUITest(i))
    
    def SearshFrame(self, e , searshFrame, HBoxsearshFrame, Image,bioLabel,bio):

        if  "QtCore.QEvent" in str(e):
            searshFrame.setFixedHeight(90)
            
            Image.setMinimumSize(30,50)
            Image.setMaximumSize(100,300)
            bioLabel.hide()
            bio.hide()

        else:

            searshFrame.setFixedHeight(180)
            
            Image.setMinimumSize(250,50)
            Image.setMaximumSize(300,300)
            bioLabel.show()
            bio.show()
            
            
    def Click(self,ButtonId):
        global _message

        
        print(ButtonId)
        self.searshFrindLineEdit.setText("")
        self.messageAddfrindLabel.show()
        self.messageAddfrindLabel.setText(f"Dan Add Frind {ButtonId}")
        _dirImage = dirImage.replace("\\","/")
        
        self.curdb.execute("SELECT * FROM user WHERE username='%s'"%(ButtonId))
        dataFrind =  self.curdb.fetchone()
        self.curdb.execute("INSERT INTO frind (username, frinduser)VALUES('%s','%s');"%(_my_username,ButtonId))
        self.db.commit()
        Frind.append({
                    ButtonId:{"id":ButtonId,"name":dataFrind[1], "img":f"{_dirImage}/{ButtonId}.png","bio":dataFrind[4], "chat":[],"statechat":0,"block":0}
                })
        print(f"Frind : {Frind}\n")
        self.curdblist.execute("INSERT INTO frind VALUES(?,?,?,?,?,?)",(ButtonId,dataFrind[1],dataFrind[4],f"{ButtonId}.png",dataFrind[5],0))
        self.dblite.commit()
        imageFrind= f"{_dirImage}/{ButtonId}.png"
        print(not os.path.isfile(imageFrind))
        if not os.path.isfile(imageFrind):
            print("get Image Server")
            _message = _my_username+"getImage"+ButtonId
            self.thread.start()
        else:
            self.UpDate()
        

            

    def MenuAction (self):
        global menuaction
        if menuaction == 0:
            newWidth = 200
            self.animation11.stop()
            self.mainFrind.setMaximumWidth(0)
            menuaction = 1
            width = self.mainmenu.width()
            self.animation = QPropertyAnimation(self.mainmenu, b"maximumWidth")
            self.animation.setDuration(250)
            self.animation.setStartValue(width)
            self.animation.setEndValue(newWidth)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()
            self.mainFrind.setMaximumWidth(0)
        else:
            newWidth = 60

            self.searshFrind.hide()
            self.mainmenu.setMaximumWidth(0)
            self.FrindInfomain.hide()
            self.chatmain.show()
            self.myacounntMain.hide()
            self.mysttingesmain.hide()
            self.addFrindMain.hide()
            menuaction = 0
            width = self.mainFrind.width()
            self.animation1 = QPropertyAnimation(self.mainFrind, b"maximumWidth")
            self.animation1.setDuration(250)
            self.animation1.setStartValue(width)
            self.animation1.setEndValue(newWidth)
            self.animation1.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation1.start()
        
        
    def menuWidget(self):
        self.mainmenu.setContentsMargins(0,0,0,0)
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)
        
        mainmenuUpLayout = QVBoxLayout()
        mainmenuUpLayout.addSpacing(0)
        mainmenuUpLayout.setContentsMargins(10,0,0,3)
        
        menuUpLayout = QHBoxLayout()
        menuUpLayout.addSpacing(0)
        menuUpLayout.setContentsMargins(7,5,7,0)
        menuUpLayout.setAlignment(Qt.AlignRight)
        
        menuDownLayout = QHBoxLayout()
        menuDownLayout.addSpacing(0)
        menuDownLayout.setContentsMargins(0,0,2,0)
        
          
        self.mainmenuUp = QFrame()
        self.mainmenuUp.setContentsMargins(0,0,0,0)
        self.mainmenuUp.setStyleSheet("QFrame{background-color: rgb(39, 104, 153);}")
        
        self.menuButton1 = QPushButton()
        self.menuButton1.setMinimumHeight(36)
        self.menuButton1.setMinimumWidth(36)
        self.menuButton1.setContentsMargins(0,0,0,0)
        self.menuButton1.setCursor(QCursor(Qt.PointingHandCursor))
        self.menuButton1.clicked.connect(self.MenuAction)
        self.menuButton1.setStyleSheet("""QPushButton{
                                            border-image:url(img/menu.png);
                                            margin: 0px 0px 5px 3px;
                                            background-color: rgb(39, 104, 153);
                                        }
                                        QPushButton:hover{
                                            border-image:url(img/menuH.png);
                                            background-color: rgb(39, 104, 153);
                                            }
                                        """)
        
        
        
        self.userImage = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.userImage.sizePolicy().hasHeightForWidth())
        self.userImage.setSizePolicy(sizePolicy)
        i = dirImage.replace("\\","/")+"/"+_myData['img']
        self.userImage.setStyleSheet("""
                                    QPushButton{border-image: url('%s');
                                                border-radius: 22px;
                                                background-color: rgb(255, 255, 255);
                                                padding: 100px;
                                                border:3px solid red;
                                                }
                                    QPushButton:hover{background-color: #80dfff}
                                    """%(i))


        self.userImage.setFixedSize(45,45)
        
        
        self.menuUserName = QLabel()
        infoTxt = f"""
        <p style="font-size:16px; color:#fff; margin:0px;">{_myData["name"].capitalize()}</p>
        <p style="font-size:12px; color:#b3b3b3;margin:0px;">.   {_myData["username"]}</p>
        """
        self.menuUserName.setText(infoTxt)
        self.menuUserName.setContentsMargins(0,0,0,0)
        
        self.menuLogout = QPushButton()
        self.menuLogout.setFixedSize(45,45)
        self.menuLogout.clicked.connect(self.MenuLogout)
        self.menuLogout.setStyleSheet("""QPushButton{
                                            border-image:url(img/Expand More.png);
                                            margin: 0px 0px 5px 3px;
                                            background-color: rgb(39, 104, 153);
                                        }
                                        QPushButton:hover{
                                            border-image:url(img/Expand MoreH.png);
                                            background-color: rgb(39, 104, 153);
                                            } """)
        
        
        menuUpLayout.addWidget(self.userImage)
        menuUpLayout.addStretch()
        menuUpLayout.addWidget(self.menuButton1)
        

        
        menuDownLayout.addWidget(self.menuUserName)
        menuDownLayout.addWidget(self.menuLogout)
        
        
        
        mainmenuUpLayout.addLayout(menuUpLayout)
        mainmenuUpLayout.addLayout(menuDownLayout)
        mainmenuUpLayout.addStretch()

        
        
        self.mainmenuUp.setLayout(mainmenuUpLayout)
        
        
        self.Framelogout = QFrame()
        self.Framelogout.hide()
        self.FrameLogout()
        
        
        self.mainmenuBottom = QFrame()
        self.mainmenuBottom.setContentsMargins(0,0,0,0)
        self.MainMenuBottom()
        
        
        
        
        mainLayout.addWidget(self.mainmenuUp,5)
        mainLayout.addWidget(self.Framelogout,10)
        mainLayout.addWidget(self.mainmenuBottom,95)
        mainLayout.addStretch()
        self.mainmenu.setLayout(mainLayout)
    
    def MainMenuBottom(self):
        mainLayout = QVBoxLayout()
        
        self.addFrindmenu = QFrame()
        self.addFrindmenu.mouseReleaseEvent=lambda event:self.AddFrind(event)
        self.addFrindmenu.setStyleSheet("QFrame:hover{background-color:#2b4055;}")
        self.addFrindmenu.leaveEvent = lambda e:self.AddFrindLeave(e)
        self.addFrindmenu.enterEvent = lambda e: self.AddFrindEnter(e)
        FrindLayout = QHBoxLayout()
        self.FrindLabel = QLabel("Add Frind")
        self.FrindLabel.setStyleSheet("color:#fff;font-size:14px;font-weight: bold;font-family: 'Courier New', Courier, monospace")
        self.IconFrind = QLabel()
        self.IconFrind.setFixedSize(25,25)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.userImage.sizePolicy().hasHeightForWidth())
        self.IconFrind.setSizePolicy(sizePolicy)
        self.IconFrind.setStyleSheet("""
                                    QLabel{border-image: url('img/addFrind.png');
                                                border-radius: 13px;
                                                background-color: rgb(29, 44, 58);
                                                padding: 100px;
                                                border:3px solid red;
                                                }
                                    
                                    """)
        FrindLayout.addWidget(self.IconFrind)
        FrindLayout.addWidget(self.FrindLabel)
        self.addFrindmenu.setLayout(FrindLayout)
        
        self.myAcounntmenu = QFrame()
        self.myAcounntmenu.mouseReleaseEvent=lambda event:self.MyAcounnt(event)
        self.myAcounntmenu.setStyleSheet("QFrame:hover{background-color:#2b4055;}")
        self.myAcounntmenu.leaveEvent = lambda e:self.MyAcounntLeave(e)
        self.myAcounntmenu.enterEvent = lambda e: self.MyAcounntEnter(e)
        myAcounntLayout = QHBoxLayout()
        self.myAcounntLabel = QLabel("My Acounnt")
        self.myAcounntLabel.setStyleSheet("color:#fff;font-size:14px;font-weight: bold;font-family: 'Courier New', Courier, monospace")
        self.IconmyAcounnt = QLabel()
        self.IconmyAcounnt.setFixedSize(25,25)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.IconmyAcounnt.sizePolicy().hasHeightForWidth())
        self.IconmyAcounnt.setSizePolicy(sizePolicy)
        self.IconmyAcounnt.setStyleSheet("""
                                    QLabel{border-image: url('img/account.png');
                                                border-radius: 13px;
                                                background-color: rgb(29, 44, 58);
                                                padding: 100px;
                                                border:3px solid red;
                                                }
                                    
                                    """)
        myAcounntLayout.addWidget(self.IconmyAcounnt)
        myAcounntLayout.addWidget(self.myAcounntLabel)
        self.myAcounntmenu.setLayout(myAcounntLayout)
        
        self.settingsmenu = QFrame()
        self.settingsmenu.mouseReleaseEvent=lambda event:self.Settings(event)
        self.settingsmenu.setStyleSheet("QFrame:hover{background-color:#2b4055;}")
        self.settingsmenu.leaveEvent = lambda e:self.SettingsLeave(e)
        self.settingsmenu.enterEvent = lambda e: self.SettingsEnter(e)
        settingsLayout = QHBoxLayout()
        self.settingsLabel = QLabel("Settings")
        self.settingsLabel.setStyleSheet("color:#fff;font-size:14px;font-weight: bold;font-family: 'Courier New', Courier, monospace")
        self.Iconsettings = QLabel()
        self.Iconsettings.setFixedSize(25,25)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.userImage.sizePolicy().hasHeightForWidth())
        self.Iconsettings.setSizePolicy(sizePolicy)
        self.Iconsettings.setStyleSheet("""
                                    QLabel{border-image: url('img/settings.png');
                                                border-radius: 13px;
                                                background-color: rgb(29, 44, 58);
                                                padding: 100px;
                                                border:3px solid red;
                                                }
                                    
                                    """)
        settingsLayout.addWidget(self.Iconsettings)
        settingsLayout.addWidget(self.settingsLabel)
        self.settingsmenu.setLayout(settingsLayout)
        
        info = QLabel("C-Chat, v1")
        info.setStyleSheet("color:#b3b3b3;")
        
        
        mainLayout.addWidget(self.addFrindmenu)
        mainLayout.addWidget(self.myAcounntmenu)
        mainLayout.addWidget(self.settingsmenu)
        mainLayout.addStretch()
        mainLayout.addWidget(info)
        self.mainmenuBottom.setLayout(mainLayout)
    
    
    def AddFrindLeave(self, _):
        self.FrindLabel.setStyleSheet("QLabel{background-color: rgb(29, 44, 58);color:#fff;font-size:14px;font-weight: bold;font-family: 'Courier New', Courier, monospace;}")       
        self.IconFrind.setStyleSheet("QLabel{background-color: rgb(29, 44, 58);border-image: url('img/addFrind.png');}")   
    def AddFrindEnter(self, _):
        self.FrindLabel.setStyleSheet("QLabel{background-color: #2b4055;color:#fff;font-size:16px;font-weight: bold;font-family: 'Courier New', Courier, monospace;}")
        self.IconFrind.setStyleSheet("QLabel{background-color: #2b4055;border-image: url('img/addFrind.png');}")     
    def AddFrind(self, _):
        print("AddFrind")
        print(self.addFrindMain.isVisible())
        if not self.addFrindMain.isVisible():
            self.chatmain.hide()
            self.myacounntMain.hide()
            self.mysttingesmain.hide()
            self.FrindInfomain.hide()
            self.addFrindMain.show()
        else:
            self.FrindInfomain.hide()
            self.addFrindMain.hide()
            self.myacounntMain.hide()
            self.mysttingesmain.hide()
            self.chatmain.show()

    def MyAcounntLeave(self, _):
        self.myAcounntLabel.setStyleSheet("QLabel{background-color: rgb(29, 44, 58);color:#fff;font-size:14px;font-weight: bold;font-family: 'Courier New', Courier, monospace;}")       
        self.IconmyAcounnt.setStyleSheet("QLabel{background-color: rgb(29, 44, 58);border-image: url('img/account.png');}")   
    def MyAcounntEnter(self, _):
        self.myAcounntLabel.setStyleSheet("QLabel{background-color: #2b4055;color:#fff;font-size:16px;font-weight: bold;font-family: 'Courier New', Courier, monospace;}")     
        self.IconmyAcounnt.setStyleSheet("QLabel{background-color: #2b4055;border-image: url('img/account.png');}")   
    def MyAcounnt(self, _):
        print("MyAcounnt")
        print(self.myacounntMain.isVisible())
        if self.myacounntMain.isVisible():
            self.FrindInfomain.hide()
            self.chatmain.show()
            self.myacounntMain.hide()
            self.mysttingesmain.hide()
            self.addFrindMain.hide()
        else:
            self.FrindInfomain.hide()
            self.addFrindMain.hide()
            self.mysttingesmain.hide()
            self.myacounntMain.show()
            self.chatmain.hide()
    
    def SettingsLeave(self, _):
        self.settingsLabel.setStyleSheet("QLabel{background-color: rgb(29, 44, 58);color:#fff;font-size:14px;font-weight: bold;font-family: 'Courier New', Courier, monospace;}")       
        self.Iconsettings.setStyleSheet("QLabel{background-color: rgb(29, 44, 58);border-image: url('img/settings.png');}")   
    def SettingsEnter(self, _):
        self.settingsLabel.setStyleSheet("QLabel{background-color: #2b4055;color:#fff;font-size:16px;font-weight: bold;font-family: 'Courier New', Courier, monospace;}")     
        self.Iconsettings.setStyleSheet("QLabel{background-color: #2b4055;border-image: url('img/settings.png');}")   
    def Settings(self, _):
        print("Settings")
        print(self.mysttingesmain.isVisible())
        if self.mysttingesmain.isVisible():
            self.FrindInfomain.hide()
            self.chatmain.show()
            self.myacounntMain.hide()
            self.mysttingesmain.hide()
            self.addFrindMain.hide()
        else:
            self.FrindInfomain.hide()
            self.addFrindMain.hide()
            self.mysttingesmain.show()
            self.myacounntMain.hide()
            self.chatmain.hide()
        
        
    def FrameLogout(self):
        self.Framelogout.setStyleSheet("background-color:red;")
        self.Framelogout.setCursor(QCursor(Qt.PointingHandCursor))
        self.Framelogout.mouseReleaseEvent=lambda event:self.LogOut(event)
        h = QHBoxLayout()
        
        self.logout =  QLabel("Log out")
        self.logout.setStyleSheet("color:#fff;font-size:14px;;margin-left:10;")
        h.addWidget(self.logout)
        self.Framelogout.setLayout(h)
        
    def LogOut(self, _):
        global _LogOut
        print("LogOut")
        Q = QMessageBox.question(self,"LogOut chat", "  Are you sure to log out?  ")
        if Q == QMessageBox.Yes:
            dblite = sqlite3.connect(f"{dirfile}\\chat.db")
            curdblist = dblite.cursor()
            curdblist.execute("DELETE FROM frind;")
            curdblist.execute(f"DELETE FROM messages;")
            curdblist.execute("DELETE FROM myData;")
            curdblist.execute("DELETE FROM filemessages;")
            dblite.commit()
            dblite.close()
            print("yse")
            _LogOut = 1         
            self.thread.CloseClient()
            self.window = LoginScren()
            self.close()
            _LogOut = 0
    
    def MenuLogout(self):
        if "Expand More.png" in self.menuLogout.styleSheet():
            self.Framelogout.show()
            self.menuLogout.setStyleSheet("""QPushButton{
                                                border-image:url(img/Expand Less.png);
                                                margin: 0px 0px 5px 3px;
                                                background-color: rgb(39, 104, 153);
                                            }
                                            QPushButton:hover{
                                                border-image:url(img/Expand LessH.png);
                                                background-color: rgb(39, 104, 153);
                                                } """)
        else:
            self.Framelogout.hide()
            self.menuLogout.setStyleSheet("""QPushButton{
                                            border-image:url(img/Expand More.png);
                                            margin: 0px 0px 5px 3px;
                                            background-color: rgb(39, 104, 153);
                                        }
                                        QPushButton:hover{
                                            border-image:url(img/Expand MoreH.png);
                                            background-color: rgb(39, 104, 153);
                                            } """)
    
    def searshChanged(self,text):
        global Frind
        print("searshChanged")
        newFrind = []
        
        for i in Frind:
            for key in i:
                print(key)
                try:
                    if key.startswith(text):
                        newFrind.append(i)
                        
                    elif i[key]["name"].startswith(text):
                        newFrind.append(i)
                except:
                    pass
        Frind = newFrind
        self.createLayout_Container_Frind()
        
        self.getDataFrind()
                    
        
    def getDataFrind(self):
        global _my_username,Frind
        
        myData = self.curdblist.execute("select  * from myData").fetchone()
        
                    
        if myData != None or myData == []:
            
            _my_username = myData[0]
            frindData = self.curdblist.execute("select  * from frind").fetchall()
            Frind = []
            c1 = []
            for index, i in enumerate(frindData):
                c1.append(i[0])
                _dirImage = dirImage.replace("\\","/")
                i4 = i[4]
                if i4==None:
                    i4 = 0
                i5 = i[5]
                if i5==None:
                    i5 = 0
                Frind.append({
                    i[0]:{"id":i[0],"name":i[1],"bio":i[2], "img":f"{_dirImage}/{i[3]}", "chat":[],'statechat':i4,"block":i5}
                })
                chat = self.curdblist.execute(f"select  state,message,time from messages where username='{i[0]}'").fetchall()
                try:
                    for c in chat:
                        Frind[index][i[0]]["chat"].append(list(c))
                except:
                    pass
            return 1      
            
            
    def SendFile(self):
        print("SendFile")
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;*.png")
        if fileName:
            print(fileName)
            time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            _time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            nemeFile = os.path.basename(fileName)
            _fileMessagef = fileMessagef.replace("\\","/")
            namefileNew = nemeFile +"SendFile"+time+"."+nemeFile.split('.')[-1]
            dirfileNew = _fileMessagef+"/"+namefileNew
            with open(fileName, "rb")as R:  
                with open(dirfileNew, "wb")as W:
                    W.write(R.read()) 

            self.curdblist.execute("INSERT INTO filemessages VALUES(?,?)",(f"{nemeFile}",fileName))
            self.dblite.commit()
            Frind[int(self.LableIndx.text())][sendTo]['chat'].append(["my",f"{namefileNew}",time])
            
            _isImag = ["png","jpg","jpeg","ico"]
            typeFile = f"{fileName}".split(".")[-1]
            
            
            if typeFile in _isImag :
                pixmap = QPixmap(fileName)
                pixmap4 = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.VBoxMy.addWidget(self.createLayout_group_shat(f"{namefileNew}",time, 0, pixmap4),alignment= Qt.AlignLeft)
            else:
                self.VBoxMy.addWidget(self.createLayout_group_shat(f"{namefileNew}",time, 0, ''),alignment= Qt.AlignLeft)
            self.curdblist.execute("insert into messages values(?,?,?,?)",(sendTo,"my",namefileNew,_time))        
            self.dblite.commit()
            self.thread.sendMessageFile(dirfileNew, namefileNew)
            print(dirfileNew)

    def senMassag(self):
        global _message
        print(sendTo)
        if StateConnect and sendTo != "":
            mess = self.sendLine.toPlainText()
            print(mess)
            _message = mess
            time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            Frind[int(self.LableIndx.text())][sendTo]['chat'].append(["my",f"{mess}",time])
            
            # self.createLayout_Container_shatThrid(["my",f"{mess}",str(time)], 1)
            self.VBoxMy.addWidget(self.createLayout_group_shat(f"{mess}",str(time), 0, ''),alignment= Qt.AlignLeft)
            
            self.curdblist.execute("insert into messages values(?,?,?,?)",(sendTo,"my",f"{mess}",time))        
            self.dblite.commit()
            
            
            print(int(self.LableIndx.text()))
            
            self.sendLine.clear()
            self.thread.start()
        self.sendLine.clear()
    def sendNewFrind (self, userName,time='', messag=''):
        self.db = mysql.connector.connect(user='root', password='123456', host='localhost',port=3307, db="chat")
        self.curdb = self.db.cursor(buffered=True)
        self.curdb.execute("SELECT * FROM user WHERE username='%s';"%(userName,))
        data = self.curdb.fetchone()
        index = len(Frind)
        print(f"userName: {userName}\ndata: {data}")
        bio = ""
        if data[4] == None:
            bio = " "
        Frind.append({
                userName:{"id":userName,"name":f"{data[1]}","bio":f"{bio}", "img":f"{userName}.png", "chat":[],"statechat":"1","block":0}
                })
        self.curdblist.execute("INSERT INTO frind (username,name,image,bio,statechate,block)VALUES(?,?,?,?,?,?)",(userName,f"{data[1]}",f"{userName}.png",f"{data[4]}",1,0))
        

        Frind[index][userName]["chat"].append(["you",messag,time])
        self.curdblist.execute("INSERT INTO messages VALUES(?,?,?,?)",(userName,"you",messag,time))
        self.dblite.commit()
        
        self.curdb.execute(f"INSERT INTO frind VALUES('%s','%s','','',0);"%(_my_username,userName))
        self.db.commit()
        
        self.UpDate()
    def setMessag(self,val):
        print(F"setMessag\n\tval : {val}")
        global Frind, _message
        if val[0] == "imagUser":
            print("\nget imagUser\n")
            print(f"val[1] {val[1]}")
            self.createLayout_Container_Frind()
            self.searshChanged(text="")
            return
        

        
        if val[0] == "getFile":
            _index = 0
            chick = -1
            for i in Frind :
                c = i.get(namefrindFileUpdate)
                if c != None :
                    chick = _index
                    break
                _index += 1
            if chick != -1:
                self.createLayout_Container_Frind()
                if namefrindFileUpdate == sendTo:
                    self.createLayout_Container_shat( [Frind[int(self.LableIndx.text())][sendTo]['chat'], Frind[int(self.LableIndx.text())][sendTo],int(self.LableIndx.text()),""])
                else:
                    Frind[_index][namefrindFileUpdate]["statechat"]= "1"
                    self.curdblist.execute("UPDATE frind SET statechate=? WHERE username=?",(1,namefrindFileUpdate))
                    self.dblite.commit()
                    self.UpDate()
                return
            else:
                self.sendNewFrind(namefrindFileUpdate)
                return
        if val[0] == "SendFile":
            
            username = val[1]
            time = val[2]
            messag = val[3]
            _index = 0
            chick = -1
            for i in Frind :
                c = i.get(username)
                if c != None :
                    chick = _index
                    break
                _index += 1
            print(_index)
            print(f" 3439 _index: {_index}\t chick:{chick}\nFrind[_index][username]:{Frind[_index][username]}")
            if chick != -1:
                
                
                self.curdblist.execute("insert into messages values(?,?,?,?)",(username,"you",f"{messag}",str(time)))
                self.curdblist.execute("insert into filemessages values(?,?)",(messag,""))
                self.dblite.commit()
                Frind[_index][username]['chat'].append(["you",f"{messag}",str(time)])
                print(Frind[_index][username])
                if username == sendTo:
                    _fileMessagef = fileMessagef.replace("\\","/")

                    if os.path.isfile(_fileMessagef+"/"+messag):
                        path = _fileMessagef+"/"+messag
                    _isImag = ["png","jpg","jpeg","ico"]
                    typeFile = f"{messag}".split(".")[-1]
                    
                    if typeFile in _isImag :
                        pixmap = QPixmap(path)
                        pixmap4 = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.VBoxMy.addWidget(self.createLayout_group_shat(f"{messag}",time, 0, pixmap4),alignment= Qt.AlignRight)
                    else:
                        self.VBoxMy.addWidget(self.createLayout_group_shat(f"{messag}",time, 0, ''),alignment= Qt.AlignRight)
                else:
                    Frind[_index][username]["statechat"]= "1"
                    self.curdblist.execute("UPDATE frind SET statechate=? WHERE username=?",(1,username))
                    self.dblite.commit()
                    self.UpDate()
                self.Notifications(username, "Send File")
                return
                
                # Frind.append({
                #     username:{"id":username,"name":"","bio":"", "img":f"{username}.png", "chat":[],"statechat":"0","block":"0"}
                # })
                # threading.Thread(target=self.connectDB).start()
                # self.UpDate()
                    
            else:
                self.sendNewFrind(username,time,messag)
                return
        
        print("\nset Message\n")   
        
        username = val[0]
        messag = val[1]
        _index = 0
        chick = -1
        for i in Frind :
            c = i.get(username)
            if c != None :
                chick = _index
                break
            _index += 1
        print(_index)
        # try:
        
        time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if chick != -1:
            print(Frind)
            Frind[_index][username]['chat'].append(["you",f"{messag}",str(time)])
            print(Frind[_index][username])
            self.curdblist.execute("insert into messages values(?,?,?,?)",(username,"you",f"{messag}",str(time)))
            self.dblite.commit()
            if username == sendTo:
                self.VBoxMy.addWidget(self.createLayout_group_shat(f"{messag}",str(time), 1, ""),alignment= Qt.AlignRight)
            else:
                Frind[_index][username]["statechat"]= "1"
                self.curdblist.execute("UPDATE frind SET statechate=? WHERE username=?",(1,username))
                self.dblite.commit()
                self.UpDate()
            
            self.Notifications(username, messag)
            
        else:
            chackimag = 0
            self.sendNewFrind(username,time,messag)
            self.Notifications(username, messag)
            _dirImage = dirImage.replace("\\","/")
            if not os.path.isfile(f"{_dirImage}/{username}.png"):
                chackimag = 1
                print(f"Image : {_dirImage}/{username}.png")
                _message = _my_username+"getImage"+username
                self.thread.start()
                
            else:
                print("Yas Image")
            if chackimag == 1:
                self.searshFrind.setText(" ")
                self.searshFrind.setText("")
            return
            # Frind.append({
            #         username:{"id":username,"name":"","bio":"", "img":f"{username}.png", "chat":[],"statechat":"0","block":"0"}
            #     })
            # threading.Thread(target=self.connectDB).start()
            # self.UpDate()
        # except Exception as e:
        #     print(f"Erorr setMessag: {e}")
       
       
    def Connect1(self):
        print("errorConnect")
        self.Connect()
    def Connect(self):
        try:
            self.thread = Thread()
            self.thread.getMessg.connect(self.setMessag)
            self.thread.stateConnct.connect(self.StateConnect)
            self.thread.errorConnect.connect(self.Connect)
            self.thread.slectFrindT.connect(self.createLayout_Container_shat)
            self.thread.MessageThread.connect(self.createLayout_Container_shatThrid)
            
            try:
                self.thread.connect1()
            except Exception as e:
                print(f"E : {e}")
                pass
            
        except:
            print(3)

        
    def s(self):
        time.sleep(2)
        self.connectLabel.hide()
    def StateConnect(self, val):
        
        if val:
            if  self.connectLabel.isVisible():
                self.connectLabel.setText("Connect")
                self.connectLabel.setStyleSheet( self.connectLabelStyal(True))
                threading.Thread(target=self.s).start()

        else:
            
            if not self.connectLabel.isVisible():
                self.connectLabel.show()
                self.connectLabel.setText("No Connect")
                self.connectLabel.setStyleSheet( self.connectLabelStyal(False))

    def UpDate(self):
        self.searshFrind.setText(" ")
        self.searshFrind.setText("")
    def chackMessages(self):
        global _message
        print("\nchackMessages")
        chack = 0
        dblite = sqlite3.connect(f"{dirfile}\\chat.db")
        curdblist = dblite.cursor()
        # check New Frind
        self.curdb.execute("SELECT frinduser FROM frind WHERE username='%s';"%(_my_username,))
        frindsUserName = self.curdb.fetchall()
        self.curdb.execute("SELECT username FROM frind WHERE frinduser='%s';"%(_my_username,)) 
        frindsUserName1 = self.curdb.fetchall()
        print(f"\nfrindsUserName 1: {frindsUserName}")
        for i in frindsUserName1:
            if i not in frindsUserName:
                frindUserName = curdblist.execute("SELECT username FROM frind WHERE username=?",(i[0],)).fetchone()
                print(_my_username)
                self.curdb.execute(f"INSERT INTO frind VALUES('%s','%s','','',0);"%(_my_username,i[0]))
                self.db.commit()
                if frindUserName == None:
                    curdblist.execute("INSERT INTO frind (username,image,statechate,block)VALUES(?,?,?,?)",(i[0],f"{i[0]}.png",0,0))
                    dblite.commit()
                    Frind.append({
                    i[0]:{"id":i[0],"name":"","bio":"", "img":f"{i[0]}.png", "chat":[],"statechat":"0","block":"0"}
                })

        
        print("\n")
        # check Frind 
        self.curdb.execute("SELECT frinduser FROM frind WHERE username='%s';"%(_my_username,))
        frindsUserName = self.curdb.fetchall()
        print(f"\nfrindsUserName: {frindsUserName}")
        for i in frindsUserName:
            frindUserName = curdblist.execute("SELECT username FROM frind WHERE username=?",(i[0],)).fetchone()
            if frindUserName == None:
                curdblist.execute("INSERT INTO frind (username,image,statechate,block)VALUES(?,?,?,?)",(i[0],f"{i[0]}.png",0,0))
                dblite.commit()
                Frind.append({
                i[0]:{"id":i[0],"name":"","bio":"", "img":f"{i[0]}.png", "chat":[],"statechat":"0","block":"0"}
            })
        
        
        # Check Name and Bio in Friend
        _Frind  = curdblist.execute(f"select * from frind ").fetchall()
        print(f"_Frind _Fr : {_Frind}")
        for index, i in enumerate(_Frind):
            self.curdb.execute(f"SELECT frind.username,frind.frinduser,user.name,user.image,user.bio FROM frind,user WHERE frind.username='{_my_username}' and frind.frinduser='{i[0]}'  and frind.frinduser=user.username;")
            ismassMysql = self.curdb.fetchall()
            if i[1]==ismassMysql[0][2] and i[2]==ismassMysql[0][4]:
                print("yas Frind")
                
            else:
                chack = 1
                Frind[index][i[0]]["name"] = ismassMysql[0][2]
                Frind[index][i[0]]["bio"] = ismassMysql[0][4]

                curdblist.execute(f"UPDATE frind SET name=?,bio=? where username=?;",(ismassMysql[0][2],ismassMysql[0][4],ismassMysql[0][1]))
                dblite.commit()
                
                print("\n")
            
        # Check Message Friend
        _Frind  = curdblist.execute(f"select  username from frind ").fetchall()
        for index,i in enumerate(_Frind):
            ismassLite  = curdblist.execute(f"select  state,message from messages where username='{i[0]}'").fetchall()
            self.curdb.execute(f"select  state,message from messages where username='{_my_username}' AND sendto = '{i[0]}'")
            ismassMysql = self.curdb.fetchall()
            if ismassLite == ismassMysql:
                print("yas Messages")
            else:
                chack = 1
                print("\nNo Messages\n")
                curdblist.execute(f"DELETE FROM messages where username='{i[0]}'")
                dblite.commit()
                

                self.curdb.execute(f"select  state,message,time from messages where username='{_my_username}' AND sendto = '{i[0]}'")
                ismassMysql = self.curdb.fetchall()
                
                Frind[index][i[0]]["chat"] = []
                Frind[index][i[0]]["statechat"] = "1"
                
                
                
                # print(Frind[index][i[0]]["chat"])
                # print(Frind[index][i[0]]["statechat"])
                try:
                    for c in ismassMysql:
                        print(f"Frind: {Frind}")
                        Frind[index][i[0]]["chat"].append(list(c))
                        curdblist.execute("INSERT INTO messages VALUES(?,?,?,?)",(i[0],c[0],c[1],c[2]))
                                
                
                    curdblist.execute("UPDATE frind SET statechate=? WHERE username=?",(1,i[0]))
                except Exception as e:
                    print(f"Erorr sqlite : {e}")
                dblite.commit()
                print(f"Frind: {Frind}")
        
        
        # check image Frined 
        _Frind  = curdblist.execute(f"select  username,image from frind ").fetchall()
        _dirImage = dirImage.replace("\\","/")
        for i in _Frind:
            if not os.path.isfile(f"{_dirImage}/{i[1]}"):
                chack = 1
                print(f"Image : {_dirImage}/{i[1]}")
                _message = _my_username+"getImage"+i[0]
                self.thread.start()
                
            else:
                print("Yas Image")
        if chack == 1:
            self.searshFrind.setText(" ")
            self.searshFrind.setText("")

        
        print("Dan chack data")
    
    def closeEvent(self, _):
        global _stateEnd
        if  _LogOut == 0:
            self.hide()
            self.close()
            print("Exit")
            _stateEnd = True
            sys.exit()

    def styleScrollBar(self):
        return"""
            QScrollBar:horizontal
            {
                height: 15px;
                margin: 3px 15px 3px 15px;
                border: 1px transparent #2A2929;
                border-radius: 4px;
                background-color: #2A2929;
            }

            QScrollBar::handle:horizontal
            {
                background-color: #605F5F;
                min-width: 5px;
                border-radius: 4px;
            }

            QScrollBar::add-line:horizontal
            {
                margin: 0px 3px 0px 3px;
                border-image: url(img/right_arrow_disabled.png);
                width: 10px;
                height: 10px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:horizontal
            {
                margin: 0px 3px 0px 3px;
                border-image: url(img/left_arrow_disabled.png);
                height: 10px;
                width: 10px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }

            QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on
            {
                border-image: url(img/right_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }


            QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on
            {
                border-image: url(img/left_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
            {
                background: none;
            }


            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
            {
                background: none;
            }

            QScrollBar:vertical
            {
                background-color: #2A2929;
                width: 15px;
                margin: 15px 3px 15px 3px;
                border: 1px transparent #2A2929;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical
            {
                background-color: #605F5F;
                min-height: 5px;
                border-radius: 4px;
            }

            QScrollBar::sub-line:vertical
            {
                margin: 3px 0px 3px 0px;
                border-image: url(img/up_arrow_disabled.png);
                height: 10px;
                width: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::add-line:vertical
            {
                margin: 3px 0px 3px 0px;
                border-image: url(img/down_arrow_disabled.png);
                height: 10px;
                width: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
            {

                border-image: url(img/up_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }


            QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
            {
                border-image: url(img/down_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
            {
                background: none;
            }


            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
            {
                background: none;
            }
    """


def connectDBLite():
        dblite = sqlite3.connect(f"{dirfile}\\chat.db")
        curdblist = dblite.cursor()
        curdblist.execute("""
            create table if not exists frind(
                `username` TEXT NOT NULL,
                `name` TEXT NULL,
                "bio" TEXT,
                `image` TEXT NULL,
                "statechate" TEXT NULL,
                "block" TEXT "0");
                """)
        curdblist.execute(""" create table if not exists `messages` (
            `username` TEXT NULL,
            `state` TEXT NULL,
            `message` TEXT NULL,
            "time" TEXT);
            
            """)
        curdblist.execute(""" create table if not exists "myData" (
                "username"	TEXT,
                "name"	TEXT,
                "bio" TEXT,
                "image"	TEXT
                );
            """)
        curdblist.execute(""" create table if not exists "filemessages" (
                "filename"	TEXT,
                "filedir"	TEXT);""")
        curdblist.execute(""" create table if not exists "stting" (
                "notifications"	TEXT);""")
        
        dblite.commit() #Notifications




def StateLogIn():
    
    global _my_username,Frind, _myData
    connectDBLite()
    dblite = sqlite3.connect(f"{dirfile}\\chat.db")
    curdblist = dblite.cursor()
    myData = curdblist.execute("select  * from myData").fetchone()
    
                
    if myData != None or myData == []:
        _myData = {"username":myData[0], "name":myData[1],"bio":myData[2] , "img":myData[3]}
        _my_username = myData[0]
        frindData = curdblist.execute("select  * from frind").fetchall()
        Frind = []
        c1 = []
        for index, i in enumerate(frindData):
            c1.append(i[0])
            _dirImage = dirImage.replace("\\","/")
            i4 = i[4]
            i5 = i[5]
            if i4 == None:
                i4 = 0
            if i5 == None:
                i5 = "0"
                
            Frind.append({
                i[0]:{"id":i[0],"name":i[1],"bio":i[2], "img":f"{_dirImage}/{i[3]}", "chat":[],"statechat":i4,"block":i5}
            })
            chat = curdblist.execute(f"select  state,message,time from messages where username='{i[0]}'").fetchall()
            for c in chat:
                Frind[index][i[0]]["chat"].append(list(c))           
        return 1
    else:
        return 0

def main():
    App = QApplication(sys.argv)
    stat = StateLogIn()
    if stat == 1:
        w = WindowMain()
        w.show()
    else:
        _ = LoginScren()
    sys.exit(App.exec_())

if __name__ == "__main__":
    main()