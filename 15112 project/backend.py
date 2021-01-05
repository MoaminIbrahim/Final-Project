
    
import socket





########## FILL IN THE FUNCTIONS TO IMPLEMENT THE CHATCOMM CLASS ##########
class chatComm:
## innitializing the properties of the client and the server
    def __init__(self,ipaddress,portnum):
        self.ipaddress = ipaddress
        self.portnum = portnum
        self.conn = self.startConnection()
    
    def startConnection(self):
## this function connects to a server and return that connection 
        conn = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        conn.connect((self.ipaddress,self.portnum))
        return conn
#### HELPER FUNCTIONS
##-----------------------------------------------------------------------------------------------
## Messege digst functions
    def leftrotate (x, c):
        return (x << c)&0xFFFFFFFF | (x >> (32-c)&0x7FFFFFFF>>(32-c))

    def messageDigest(M):
        
        lst = [7,12,17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22]
        lst2 = [5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20]
        lst3 = [4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23]
        lst4 = [6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
        
        s = lst+lst2+lst3+lst4
        K = [ 0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee ,0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665 ,0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]

        a0 = 0x67452301
        b0 = 0xefcdab89 
        c0 = 0x98badcfe
        d0 = 0x10325476 
        A = int(a0)
        B = int(b0)
        C = int(c0)
        D = int(d0)
        for i in range(64) : 
            if 0 <= i <= 15:
                F = (B & C) | ((~B) & D)
                F = F & 0xFFFFFFFF
                g = i
            elif 16 <= i<= 31:
                
                F = (D & B) |((~D) & C)
                F = F & 0xFFFFFFFF
                g = (5*i + 1)%16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                F = F & 0xFFFFFFFF
                g = (3*i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | (~D))
                F = F & 0xFFFFFFFF
                g = (7*i)% 16
            dTemp = D
            D = C
            C = B
            B = B + chatComm.leftrotate((A + F + K[i] + M[g]), s[i])
            B = B & 0xFFFFFFFF

            A = dTemp    
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF
        messagedigest = str(a0)+str(b0)+str(c0)+str(d0)
        return messagedigest
    
## this function takes a block of 512 characters and divides into 16 chunks of 32
    def getChunks(block):
        lstt = []
        while block != "":
            lstt.append(block[:32])
            block = block[32:]
        return lstt
## this function finds the su of the asci values of the chunks
    def getChunkSum(M):
        for i in range(16):
            count = 0 
            for j in M[i] :
                count += ord(j)
            M[i] = count
        return M
## this function creates the 512 character block
    def getBlock(pdch,nm):
    ##creating the block 
        block = pdch+"1"
    ## as long as there is room for a PDCH and the last 3 digits then add the PDCH and 
        while len(block)<(509-len(pdch)+1):
            block+=pdch    
    ##fill the rest of the block with zeros until there is nm digits left to fill
        while len(block)<512-(len(str(nm))):
            block+="0"
    ## add the nm digits to complete the block
        return block+str(nm)     

##-----------------------------------------------------------------------------------------------
            
## this function attempts to log into the server and return whether the login was succesful or not
## to login , the user must provide his username and password   
    def login(self,username, password):
        username = bytes(username.encode())
        conn = self.conn
## sending the login command
        conn.send(b"Login "+username+b"\n")
## recieving the user name + challenge string 
        reply = conn.recv(512)
## decoding the challenge
        reply = reply.decode("utf-8").replace(" ","")
## isolating the challenge
        challenge = reply[5+len(username):]
## finding the length of n+m
        nm = len(password+challenge)
##finding the string PD+CH
        pdch = password+challenge
        block = chatComm.getBlock(pdch,nm)
        M = chatComm.getChunks(block)
        M = chatComm.getChunkSum(M)
        messagedigest = bytes(chatComm.messageDigest(M).encode())
##sending the messagedigest to the server        
        conn.send(bytes(b"Login "+username+b" "+messagedigest+bytes("\n".encode("utf-8"))))
##recieving the status of the login proccess
        status = conn.recv(512).decode("utf-8")
        if "Successful" in status :
            return True
        else:
            return False

## this function retrieves the users and returns them in a list
    def getUsers(self):
## request the users from the server
        self.conn.send(b" @users \n")
        size = self.conn.recv(6)[1:].decode("utf-8")
        users = self.conn.recv(int(size)-6).decode("utf-8") 
## return the users in a list 
        return users.split("@")[3:]

## this function retrieves the users and returns them in a list
    def getFriends(self):
        self.conn.send(b" @friends \n")
## request the friends from the server
        size = self.conn.recv(6)[1:].decode("utf-8")
        friends = self.conn.recv(int(size)-6).decode("utf-8")
## return the friends in a list
        return friends.split("@")[3:]

## this function sends a friend request and returns whether the request was succesful or not 
    def sendFriendRequest(self, friend):
## to find the size of the message:
        size = str(22 + len(friend))
## to complete the size string to 5 digits , add 0 to its left until its length is 5
        while len(size) != 5:
            size = "0"+size
        size = bytes(size.encode())
        friend = bytes(friend.encode())
        self.conn.send(b"@"+size+b"@request@friend@"+friend+b"\n")
## retrieve the status of the request
        status = self.conn.recv(512).decode("utf-8")
        if "ok" in status:
            return True
        else:
            return False

## this function accepts a friend request and return whether the acceptance was succesful or not        
    def acceptFriendRequest(self,friend):
## to find the size of the request:
## add 21 to the size of the friend username
        size = str(21 + len(friend))
## to complete the size string to 5 digits , add 0 to its left until its length is 5
        while len(size) != 5:
            size = "0"+size
        size = bytes(size.encode())
        friend = bytes(friend.encode())
        self.conn.send(b"@"+size+b"@accept@friend@"+friend+b"\n")
## retrieve the status of the request
        status = self.conn.recv(512).decode("utf-8")
        if "ok" in status:
            return True
        else:
            return False

##this function sends a message to a friend and returns whether the proccess was succesful or not
    def sendMessage(self,friend, message):
## to find the size of the request:
        size = str(16 + len(friend)+len(message))
## to complete the size string to 5 digits , add 0 to its left until its length is 5
        while len(size) != 5:
            size = "0"+size
        size = bytes(size.encode())
        friend = bytes(friend.encode())
        message = bytes(message.encode())
        self.conn.send(b"@"+size+b"@sendmsg@"+friend+b"@"+message+b"\n")
## retrieve the status of the request
        status = self.conn.recv(512).decode("utf-8")
        if "ok" in status:
            return True
        else:
            return False

## this function send a file to a friend and returns whether the file was sent successfully or not 
    def sendFile(self,friend, filename):
##open the file for reading
        file = open(filename,"r")
## read the contents of the file       
        fileContent = file.read()
## close the file
        file.close()
## to find the size of the request:
        size = str(18 + len(friend)+len(filename)+len(fileContent))
## to complete the size string to 5 digits , add 0 to its left until its length is 5
        while len(size) != 5:
            size = "0"+size
        size = bytes(size.encode())
        friend = bytes(friend.encode())
        filename = bytes(filename.encode())
        fileContent = bytes(fileContent.encode())
        self.conn.send(b"@"+size+b"@sendfile@"+friend+b"@"+filename+b"@"+fileContent+b"\n")
## retrieve the status of the request
        status = self.conn.recv(512).decode("utf-8")
        if "ok" in status:
            return True
        else:
            return False
## this function retrieves friend requests and return them in a list        
    def getRequests(self):
        self.conn.send(b" @rxrqst \n")
## request the requests from the server
        size = self.conn.recv(6)[1:].decode("utf-8")
        requests = self.conn.recv(int(size)-6).decode("utf-8")
## return the requests in a list
        return requests.split("@")[2:]

##this function retrieves all the messages and files and returns them
## this function also saves the recieved files in a local directory   
    def getMail(self):
## request the messages and files from the server
        self.conn.send(b"@rxmsg\n")
        size = self.conn.recv(6)[1:].decode("utf-8")
        mail = self.conn.recv(int(size)-6).decode("utf-8")
        msgsfiles = mail.split("@")[2:]
##initiailize the list of messages
        msglist = []
##initialize the list of files
        filelist = []
## loop through the mail
        for i in range(0,len(msgsfiles),3): 
            if msgsfiles[i] == "msg":
                msglist.append((msgsfiles[i+1],msgsfiles[i+2]))
            if msgsfiles[i] == "file":
                filelist.append((msgsfiles[i+1],msgsfiles[i+2]))
## open a file with the filename as filename for writing 
                file = open(msgsfiles[i+2],"w")
## write the content of the file
                file.write(msgsfiles[i+3])
                file.close()
        return (msglist,filelist)

