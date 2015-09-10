'''
Created on Jun 25, 2015

@author: micromu
'''
#! /usr/bin/python

import socket, ssl, string

#some user data, change as per your taste
SERVER = 'nexlab.azzurra.org'
PORT = 443
NICKNAME = 'test_py'
CHANNEL = '#test_py'

class IRC_Client():
    def __init__(self):
        super(IRC_Client, self).__init__()
        
        self.lastmex = ''
        self.connected = False
        
        #open an ssl socket to handle the connection
        self.sslsocket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        
    
    ###### BASIC FUNCTIONS #######
    
    #connect to the server
    def irc_conn(self):
        self.sslsocket.connect((SERVER, PORT))
    
    #send data through the socket
    def irc_send(self, command):
        #if(self.connected):
        self.sslsocket.send((command + '\n').encode('utf-8'))
        #else:
        #    print("Still Connecting!")
        
    def irc_recv(self):
        return self.sslsocket.recv(2048).decode('utf-8').strip('\n\r')
    
    ###### IRC COMMANDS ######
    
    def ping(self):
        self.irc_send("PONG :pingis\n")
    
    def join(self, channel):
        self.irc_send("JOIN "+ channel +"\n")
    
    def send_msg(self, channel, msg):
        self.irc_send("PRIVMSG "+ channel +" :"+ msg +"\n")
    
    def hello(self): # This function responds to a user that inputs "Hello Mybot"
        self.irc_send("PRIVMSG "+ channel +" :Hello!\n")

    def login(self, nickname, username='user', password = None, realname='Pythonist', hostname='Helena', servername='Server'):
        self.irc_send("USER %s %s %s %s" % (username, hostname, servername, realname))
        self.irc_send("NICK " + nickname)

def main():
    client = IRC_Client()
    client.irc_conn()
    client.login(NICKNAME)
    client.join(CHANNEL)
    
    while (1):
        raw_msg = client.irc_recv()
        if client.connected is not True:
            client.connected = True
        
        print(raw_msg)
        msg = raw_msg.split(':')
		
        if "PING" in msg[0]: #check if server have sent ping command
            print(msg)
            client.irc_send("PONG %s" % msg[1]) #answer with pong as per RFC 1459
        if len(msg) > 2 and "PRIVMSG" in msg[1] and NICKNAME in msg[2]:
            #filetxt = open('/tmp/msg.txt', 'a+') #open an arbitrary file to store the messages
            nick_name = msg[0][:str.find(msg[0],"!")] #if a private message is sent to you catch it
            message = ' '.join(msg[3:])
            #filetxt.write(string.lstrip(nick_name, ':') + ' -> ' + string.lstrip(message, ':') + '\n') #write to the file
            #filetxt.flush() #don't wait for next message, write it now!
        if len(msg) > 2 and 'PRVMSG' in msg[1]:
            client.lastmex = " ".join(msg[3:])


if __name__ == '__main__':
    main()
