import socket
import threading
import time
import MySQLdb
import hashlib


db = MySQLdb.connect("localhost","root","protozerg", "datachat")
cursor = db.cursor()
db.autocommit(True)



f = False
join = False

def read_sok(name, sockk):
    while not f:
        try:
         while True:
             data, adr = sock.recvfrom(1024)
             print(data.decode('utf-8'))
             time.sleep(0.3)
        except:
            pass


host = socket.gethostbyname(socket.gethostname())
port = 0
server = (host, 6046)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#sock.connect(('localhost', 6046))
sock.bind((host, port))
sock.setblocking(0)


name = input("username: ")
password = input("password: ")

h = hashlib.md5(b"password")
p = h.hexdigest()

values = (name, p)
cursor.execute("INSERT Users(name, password) VALUES (%s, %s);", values)

cursor.execute("Select * from Users where `name` = 'nameee' and `password` = 'sdsd';")
data = cursor.fetchone() # одна строка из бд
rows = cursor.fetchall() # много строк из бд
print(data)

for rall in rows:
    print("{0} {1} {2}".format(rall[0], rall[1], rall[2]))


#sock.send('Hello'.encode())
#data = sock.recv(1024)
#print(data.encode("utf-8"))


x = threading.Thread(target=read_sok, args=("RecvThread", sock))
x.start()

while f == False:
    if join == False:
        sock.sendto(("["+name+"] is connected to the chat").encode("utf-8"), server)
        join = True
    else:
        try:
            message = input()
            if message!= "":
                sock.sendto(("[" +name+ "] :: "+message+ " ").encode("utf-8"), server)
            time.sleep(0.3)
        except:
            sock.sendto(("[" + name + "] = leaved chat").encode("utf-8"), server)
            f = True

x.join()
sock.close()