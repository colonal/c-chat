import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
import socket
import select
import time, datetime, os
import mysql.connector

_allUser = {}
_User = {}
_socketList =[]
uneqname = []
_onlain = []
_stateEnd = False
dirfile = os.environ['APPDATA']
if os.path.exists(f"{dirfile}\\Chat") == False :
        os.mkdir(f"{dirfile}\\Chat")
if os.path.exists(f"{dirfile}\\Chat\\imgServer") == False :
        os.mkdir(f"{dirfile}\\Chat\\imgServer")
if os.path.exists(f"{dirfile}\\Chat\\FileServer") == False :
        os.mkdir(f"{dirfile}\\Chat\\FileServer")
        
dirfile = f"{dirfile}\\chat"
dirImage = f"{dirfile}\\imgServer"
FileServer = f"{dirfile}\\FileServer"

class Thread(QThread):
    global _allUser, _socketList, _onlain,_User
    getMessg = pyqtSignal(str)
    getName = pyqtSignal(str)
    def __init__(self):
        global _allUser, _socketList, _onlain, uneqname
        super().__init__()
        self.connectDB()
        self.HEADER_LENGTH = 10

        IP = "127.0.0.1" #0.0.0.0
        PORT = 1234

        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SO_ - socket option
        # SOL_ - socket option level
        # Sets REUSEADDR (as a socket option) to 1 on socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind, so server informs operating system that it's going to use given IP and port
        # For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
        self.server_socket.bind((IP, PORT))

        # This makes server listen to new connections
        self.server_socket.listen()

        # List of sockets for select.select()
        self.sockets_list = [self.server_socket]
        _onlain = [self.server_socket]

        # List of connected clients - socket as a key, user header and name as data
        self.clients = {}

        print(f'Listening for connections on {IP}:{PORT}...')
        self.getMessg.emit(f'Listening for connections on {IP}:{PORT}...')
        
    

    def connectDB(self): 
        self.db = mysql.connector.connect(user='root', password='123456', host='localhost',port=3307, db="chat")
        self.curdb = self.db.cursor(buffered=True)
        print("connectDB")
        
        
        
    def receive_message(self,client_socket, val=1):
    
        try:

            # Receive our "header" containing message length, it's size is defined and constant
            message_header = client_socket.recv(self.HEADER_LENGTH)

            # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(message_header):
                return False
        
            # Convert header to int value
            message_length = int(message_header.decode('utf-8').strip())
            
            data =  client_socket.recv(message_length)
            print(f"\ndata:{data}")
            
            if "getFile" in data.decode() :
                print(f"getFile : {data.decode()}")
                
                senduser = data.decode().split("getFile")[0]
                imagUser = data.decode().split("getFile")[1]
                
                SendTo_header = client_socket.recv(self.HEADER_LENGTH)
                SendTo_header = int(SendTo_header.decode('utf-8').strip())
                
                print(f"SendTo_header:{SendTo_header}")
                SendTo =  client_socket.recv(SendTo_header).decode('utf-8')
                print(f"SendTo:{SendTo}")
                
                return {'header': message_header, 'senduser': senduser,"getFile":imagUser,"SendTo":SendTo}

            
            if "SendFile" in data.decode() :
                print("\n\n\nSendTo_header")
                SendTo_header = client_socket.recv(self.HEADER_LENGTH)
                _SendTo_header = int(SendTo_header.decode('utf-8').strip())
                SendTo = client_socket.recv(_SendTo_header).decode('utf-8')
                
                
                print("SendFile")
                nameImag_header = client_socket.recv(self.HEADER_LENGTH)
                _nameImag_header = int(nameImag_header.decode('utf-8').strip())
                nameImag = client_socket.recv(_nameImag_header).decode('utf-8')
                
                
                print("image_header")
                image_header = client_socket.recv(self.HEADER_LENGTH)
                _image_header = int(image_header.decode('utf-8').strip())
                image = client_socket.recv(_image_header)
                
                
                print(f"SendTo 1234: {SendTo}\n")
            
                return {"SendTo":SendTo,"nameImag":nameImag, "Image":image}
            
            if "getImage" in data.decode() :
                print("getImage")
                senduser = data.decode().split("getImage")[0]
                imagUser = data.decode().split("getImage")[1]
                
                SendTo_header = client_socket.recv(self.HEADER_LENGTH)
                SendTo_header = int(SendTo_header.decode('utf-8').strip())
                print(f"SendTo_header:{SendTo_header}")
                SendTo =  client_socket.recv(SendTo_header).decode('utf-8')
                
                
                return {'header': message_header, 'senduser': senduser,"imagUser":imagUser}
            
            if "getsearshImage" in data.decode() :
                print("getsearshImage")
                senduser = data.decode().split("getsearshImage")[0]
                imagUser = data.decode().split("getsearshImage")[1]
                
                SendTo_header = client_socket.recv(self.HEADER_LENGTH)
                SendTo_header = int(SendTo_header.decode('utf-8').strip())
                print(f"SendTo_header:{SendTo_header}")
                SendTo =  client_socket.recv(SendTo_header).decode('utf-8')
                
                
                return {'header': message_header, 'senduser': senduser,"getsearshImage":imagUser}
            
            if data.decode('utf-8') == "getCreateAcount":
                userName = ""
                Image = ""
                name = ""
                password = ""
                
                
                userName_header = client_socket.recv(self.HEADER_LENGTH)
                userName_header = int(userName_header.decode('utf-8').strip())
                print(f"userName_header:{userName_header}")
                userName =  client_socket.recv(userName_header).decode('utf-8')
                
                
                name_header = client_socket.recv(self.HEADER_LENGTH)
                name_header = int(name_header.decode('utf-8').strip())
                print(f"name_header:{name_header}")
                name =  client_socket.recv(name_header).decode('utf-8')
                
                
                pass_header = client_socket.recv(self.HEADER_LENGTH)
                pass_header = int(pass_header.decode('utf-8').strip())
                print(f"pass_header:{pass_header}")
                password =  client_socket.recv(pass_header).decode('utf-8')
                
                
                imag_header = client_socket.recv(self.HEADER_LENGTH)
                imag_header = int(imag_header.decode('utf-8').strip())
                print(f"imag_header:{imag_header}")
                Image =  client_socket.recv(imag_header)#.decode('utf-8')
                
                
                imgbnry = open(f"{dirImage}/{userName}.png", "wb")
                imgbnry.write(Image)
                imgbnry.close()
                
                
                Data  = {'data': data,"userName":userName,"name":name,"password":password,  "image":f"{dirImage}\\{userName}.png"}
                print(f"{Data}")
                self.curdb.execute(f"INSERT INTO user VALUES ('{Data['userName']}','{Data['name']}','{userName}.png','{Data['password']}','',0)")
                self.db.commit()
                return False
            
            
            
            SendTo = ""
            if val == 2:
                SendTo_header = client_socket.recv(self.HEADER_LENGTH)
                SendTo_header = int(SendTo_header.decode('utf-8').strip())
                print(f"SendTo_header:{SendTo_header}")
                
                SendTo =  client_socket.recv(SendTo_header).decode('utf-8')
                print(f"SendTo:{SendTo}")
            

            return {'header': message_header, 'data': data,"SendTo":SendTo}

        except Exception as e:
            print(f"ew : {e}")
 
            # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
            # or just lost his connection
            # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
            # and that's also a cause when we receive an empty message
            return False
    def run(self):
        global uneqname,_User
        while True:
        
        # Calls Unix select() system call or Windows select() WinSock call with three parameters:
        #   - rlist - sockets to be monitored for incoming data
        #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
        #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
        # Returns lists:
        #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
        #   - writing - sockets ready for data to be send thru them
        #   - errors  - sockets with some exceptions
        # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            #print(f"read_sockets: {read_sockets}\nexception_sockets:{exception_sockets}")


            # Iterate over notified sockets
            for notified_socket in read_sockets:
                # If notified socket is a server socket - new connection, accept it
                if notified_socket == self.server_socket:
                    print("if")

                    # Accept new connection
                    # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                    # The other returned object is ip/port set
                    client_socket, client_address = self.server_socket.accept()

                    # Client should send his name right away, receive it
                    user = self.receive_message(client_socket)

                    # If False - client disconnected before he sent his name
                    if user is False:
                        continue

                    # Add accepted socket to select.select() list
                    self.sockets_list.append(client_socket)
                    _socketList.append(client_socket)
                    _onlain.append(client_socket)

                    # Also save username and username header
                    self.clients[client_socket] = user
                    _allUser[client_socket] = user

                    print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                    self.getMessg.emit('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                    _User[user['data'].decode('utf-8')] = client_socket
                    self.getName.emit(user['data'].decode('utf-8'))
                    uneqname.append(user['data'].decode('utf-8'))
                    self.curdb.execute("UPDATE user SET  stateConnect=1  WHERE username='%s';"%(user['data'].decode('utf-8'),))
                    self.db.commit()
                    
                # Else existing socket is sending a message
                else:
                    print("else")
                    # Receive message
                    message = self.receive_message(notified_socket, 2)
                    if message is False:
                        print('Closed connection from: {}'.format(self.clients[notified_socket]['data'].decode('utf-8')))
                        self.getMessg.emit('Closed connection from: {}'.format(self.clients[notified_socket]['data'].decode('utf-8')))
                        self.curdb.execute("UPDATE user SET  stateConnect=0  WHERE username='%s';"%(self.clients[notified_socket]['data'].decode('utf-8'),))
                        self.db.commit()
                        # Remove from list for socket.socket()
                        self.sockets_list.remove(notified_socket)
                        _onlain.remove(notified_socket)

                        # Remove from our list of users
                        
                        try:
                            userClosed = self.clients[notified_socket]['data'].decode('utf-8')
                            del _User[userClosed]
                            del self.clients[notified_socket]
                        except Exception as E:
                            print(f"\n _User {userClosed} Error : {E}\n{_User}")                            
                        continue
                    
                    # send File
                    messageFile = message.get("nameImag")
                    if messageFile:
                        user = self.clients[notified_socket]
                        userName = user["data"].decode("utf-8")
                        SendTo = message["SendTo"]
                        nameImag = message["nameImag"]
                        image = message["Image"]
                        print(f"\n\n\nuserName: {userName}")
                        _FileServer = FileServer.replace("\\","/")
                        Filenaem = _FileServer+"/"+nameImag
                        with open(Filenaem, "wb") as F:
                            F.write(image)
                        
                        print(f"\n_FileServer: {Filenaem}\nnameImag:{nameImag}\n")
                        h = nameImag.split("SendFile")[1].split(".")[0].split("-")
                        time = f"{h[0]}/{h[1]}/{h[2]} {h[3]}:{h[4]}:{h[5]}"
                        print(f"time: {time}")
                        
                        im = "SendFile".encode()
                        im_header = f"{len('SendFile'):<{10}}".encode('utf-8')
                        
                        _userName = userName.encode()
                        userName_header = f"{len(_userName):<{10}}".encode('utf-8')
                        
                        _nameImag = nameImag.encode()
                        nameImag_header = f"{len(_nameImag):<{10}}".encode('utf-8')
                        
                        typeFile = nameImag.split(".")[-1]
                        _isImag = ["png","jpg","jpeg","ico"]
                        
                        
                        print(f"\ntypeFile :{typeFile}\n")
                        if typeFile in _isImag:
                            _image = image
                            image_header = f"{len(_image):<{10}}".encode('utf-8')
                        else:
                            _image = "image".encode()
                            image_header = f"{len(_image):<{10}}".encode('utf-8')
                        
                        _time = time.encode()
                        time_header = f"{len(_time):<{10}}".encode('utf-8')
                        
                        print(f"SendToSendTo SendTo :{SendTo}")
                        sendTo = _User.get(SendTo)
                        print(f"Socket: {sendTo}")
                        
                        if sendTo:
                            print(self.clients[sendTo])
                            sendTo.send(im_header + im+ userName_header+_userName + nameImag_header+_nameImag+image_header+ _image+ time_header+_time)
                        
                        
                        try:    
                            self.curdb.execute(f"insert into messages values('{userName}','{SendTo}','my','{nameImag}','{time}');")
                            self.curdb.execute(f"insert into messages values('{SendTo}','{userName}','you','{nameImag}','{time}');")
                            self.db.commit()
                        except Exception as E:
                            print(f"Erorr DB : {E}")
                            continue
                        print(f"('{userName}','{SendTo}','my','{nameImag}','{time}')")
                        continue
                    
                    # send image user                        
                    isImage = message.get("imagUser") 
                    try:
                        if isImage:
                            print(message["imagUser"])
                            imagUser = message["imagUser"]
                            senduser = message["senduser"]
                            print(f"imagUser : {imagUser}")
                            print(f"senduser : {senduser}")
                            _dirImage = dirImage.replace("\\","/")
                            print(f"{_dirImage}/{imagUser}.png")
                            if os.path.isfile(f"{_dirImage}/{imagUser}.png"):
                                print("yas image")
                                Img = open(f"{_dirImage}/{imagUser}.png","rb")
                                _Img= Img.read()
                                Img.close()
                                Img_header = f"{len(_Img):<{10}}".encode('utf-8')
                                
                                im = "imagUser".encode()
                                im_header = f"{len('imagUser'):<{10}}".encode('utf-8')
                                
                                imagUser_header = f"{len(imagUser):<{10}}".encode('utf-8')
                                
                                
                                sendTo = _User.get(senduser)
                                if sendTo:
                                    sendTo.send(im_header + im + imagUser_header+imagUser.encode()+Img_header+ _Img)
                                    continue
                                
                            continue
                    except Exception as e:
                        print(f"E: {e}")
                        continue
                    
                    
                    # send image Sersh Frind                        
                    isImage = message.get("getsearshImage") 
                    try:
                        if isImage:
                            print(message["getsearshImage"])
                            imagUser = message["getsearshImage"]
                            senduser = message["senduser"]
                            print(f"imagUser : {imagUser}")
                            print(f"senduser : {senduser}")
                            _dirImage = dirImage.replace("\\","/")
                            print(f"{_dirImage}/{imagUser}.png")
                            if os.path.isfile(f"{_dirImage}/{imagUser}.png"):
                                print("yas image")
                                Img = open(f"{_dirImage}/{imagUser}.png","rb")
                                _Img= Img.read()
                                Img.close()
                                Img_header = f"{len(_Img):<{10}}".encode('utf-8')
                                
                                im = "getsearshImage".encode()
                                im_header = f"{len('getsearshImage'):<{10}}".encode('utf-8')
                                
                                imagUser_header = f"{len(imagUser):<{10}}".encode('utf-8')
                                
                                print(f"Img_header: {Img_header}")
                                sendTo = _User.get(senduser)
                                if sendTo:
                                    sendTo.send(im_header + im + imagUser_header+imagUser.encode()+Img_header+ _Img)
                                    continue
                                

                            continue
                    except Exception as e:
                        print(f"E: {e}")
                        continue
                    
                    # get File 
                    isFile = message.get("getFile") #getFile
                    try:
                        if isFile:
                            print(message["getFile"])
                            getFile = message["getFile"]
                            senduser = message["senduser"]
                            SendTo = message["SendTo"]

                            
                            _dirImage = FileServer.replace("\\","/")
                            
                            
                            if os.path.isfile(f"{_dirImage}/{getFile}"):
                                print("yas image")
                                
                                Img = open(f"{_dirImage}/{getFile}","rb")
                                _Img= Img.read()
                                Img.close()
                                
                                Img_header = f"{len(_Img):<{10}}".encode('utf-8')
                                
                                im = "getFile".encode()
                                im_header = f"{len(im):<{10}}".encode('utf-8')
                                
                                print(f"getFile: {getFile}\n type: {type(getFile)}\nlen :{len(getFile)}")
                                _getFile = getFile.encode()
                                getFile_header = f"{len(_getFile):<{10}}".encode('utf-8')
                                
                                
                                sendTo = _User.get(SendTo)
                                print(f"im_header :{im_header}\n im :{im}\n getFile_header: {getFile_header}\ngetFile.encode(): {getFile.encode()}\nImg_header: {Img_header}\n _Img :")
                                if sendTo:
                                    sendTo.send(im_header + im + getFile_header+_getFile+Img_header+ _Img)
                                    continue
                            continue
                    except Exception as e:
                        print(f"E: {e}")
                        continue
                        #pass
                    
                    # If False, client disconnected, cleanup
                    

                    # Get user by notified socket, so we will know who sent the message
                    user = self.clients[notified_socket]
                    SendTo = message['SendTo']

                    print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                    self.getMessg.emit(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                    # Iterate over connected clients and broadcast message
                    
                    
                    sendTo = _User.get(SendTo)
                    
                    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    messageData = message["data"].decode("utf-8")
                    userName = user["data"].decode("utf-8")
                    print(f"\n\nSend To Massage: {SendTo}\nmessage: {message['data']}\nuser: {user['data']}\n\n")
                            
                    print(f"\n\n{_allUser[client_socket]}\n\n")
                    
                    self.curdb.execute(f"insert into messages values('{userName}','{SendTo}','my','{messageData}','{time}')")
                    self.curdb.execute(f"insert into messages values('{SendTo}','{userName}','you','{messageData}','{time}')")
                    self.db.commit()
                    if sendTo:
                        sendTo.send(user['header'] + user['data'] + message['header'] + message['data'])
                            

            # It's not really necessary to have this, but will handle some socket exceptions just in case
            for notified_socket in exception_sockets:

                # Remove from list for socket.socket()
                self.sockets_list.remove(notified_socket)
                _onlain.remove(notified_socket)

                # Remove from our list of users
                self.getMessg.emit('Closed connection from: {}'.format(self.clients[notified_socket]['data'].decode('utf-8')))
                self.curdb.execute("UPDATE user SET  stateConnect=0  WHERE username='%s';"%(self.clients[notified_socket]['data'].decode('utf-8'),))
                self.db.commit()
                
                del _User[self.clients[notified_socket]['data'].decode('utf-8')]
                del self.clients[notified_socket]
                
    

class Thread1 (QThread):
    onlainuser= pyqtSignal(int)
    def run(self):
        while True:
            
            if _stateEnd == True:
                sys.exit()
                
            self.onlainuser.emit(len(_onlain))
            time.sleep(1)
    
class Windoe (QWidget):
    def __init__ (self):
        super().__init__()
        self.setWindowTitle("Server")
        self.Ui()
        self.thread= Thread()
        self.thread.start()
        self.thread.getMessg.connect(self.GetMessg)
        self.thread.getName.connect(self.GetName)
        self.thread1 = Thread1()
        self.thread1.onlainuser.connect(self.getOnlinUser)
        self.thread1.start()
        
    def Ui(self):
        
        self.Hbox = QHBoxLayout()
        self.VBox = QVBoxLayout()
        
        self.onlineLabel = QLabel("On Line User : ")
        self.onlineLabel.setStyleSheet(''' font-size: 24px; ''')
        self.editor = QTextEdit()
        
        self.editor.setAcceptRichText(True)
        self.editor.setReadOnly(True)
        self.editor.setPlainText("Starte...\n")
        
        self.NameEditor = QTextEdit()
        self.NameEditor.setReadOnly(True)
        
        
        self.Hbox.addWidget(self.editor,50)
        self.Hbox.addWidget(self.NameEditor,20)
        
        
        

        self.botton = QPushButton("Get All User")
        self.botton.clicked.connect(self.getAllUser)
        self.Hbox.addWidget(self.botton,10)
        
        
        self.VBox.addWidget(self.onlineLabel)
        self.VBox.addLayout(self.Hbox)
        self.setLayout(self.VBox)

    
    def GetMessg(self, val):
        mas = self.editor.toPlainText() + f"{val}\n"
        self.editor.setPlainText(mas)
        
    def getAllUser(self):
        
        self.editor.setPlainText(self.editor.toPlainText() + "#"*10 + f"  _allUser  "+ "#10"+ "\n")
        self.editor.setPlainText(self.editor.toPlainText() + f"{_allUser} \n")
        self.editor.setPlainText(self.editor.toPlainText() + "#"*10 + f"  _socketList  "+ "#10"+ "\n")
        self.editor.setPlainText(self.editor.toPlainText() + f"{_socketList} \n")
        
    def getOnlinUser(self, val):
        self.onlineLabel.setText(f"On Line User : {val}")
        #print(val)
        
    def GetName(self,val):
        print(f"NameEditor: {val}")
        self.NameEditor.setPlainText(self.NameEditor.toPlainText()+val + "\n")
        
        
    def closeEvent(self, event):
        global _stateEnd
        print("Exit")
        _stateEnd = True
        sys.exit()
        

def main ():
    App = QApplication(sys.argv)
    window =Windoe()
    window.show()
    sys.exit(App.exec_()) 
    
if __name__ == "__main__":
    main()