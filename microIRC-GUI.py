'''
Created on Jun 26, 2015

@author: micromu
'''
#! /usr/bin/python

import sys
import microIRC
from PyQt5 import QtCore, QtGui, QtWidgets
from pygments import highlight 
from pygments.lexers import guess_lexer, get_lexer_by_name 
from pygments.formatters import HtmlFormatter 

class Notepad(QtWidgets.QMainWindow):
    def __init__(self):
        super(Notepad, self).__init__()
        self.initUI()
        self.highlighter = MicroHighlighter(self.messages)
        self.ircListener = ircListener()
        #scrivere il bound del segnale
        self.ircListener.start()
        
    def initUI(self):
        
        menubar = self.menuBar()
        
        #menu
        '''newAction = QtWidgets.QAction('New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Create new file')
        newAction.triggered.connect(self.newFile)
        
        saveAction = QtWidgets.QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current file')
        saveAction.triggered.connect(self.saveFile)
        
        openAction = QtWidgets.QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.openFile)'''
        
        closeAction = QtWidgets.QAction('Close', self) #QAction is a widget that acts as an option in a menu
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Micro') #pop-ups when a user hovers the mouse over the closeAction widget
        closeAction.triggered.connect(self.close) #uses the signals-slots pattern (closeAction send a signal to the slot of the self object that will run the close action
        
        fileMenu = menubar.addMenu('&File') #the & tell the widget to add a shortcut that will be triggered with Ctrl+"first letter of the following word"
        #fileMenu.addAction(newAction)
        #fileMenu.addAction(saveAction)
        #fileMenu.addAction(openAction)
        fileMenu.addAction(closeAction)
        
        '''pythonAction = QtWidgets.QAction('Python', self)
        pythonAction.setShortcut('Ctrl+P')
        pythonAction.setStatusTip('Syntax highlighting for Python')
        pythonAction.setCheckable(True)
        pythonAction.setChecked(True)
        pythonAction.toggled.connect(lambda x: self.updateLanguage('python'))
        
        htmlAction = QtWidgets.QAction('html', self)
        htmlAction.setShortcut('Ctrl+H')
        htmlAction.setStatusTip('Syntax highlighting for html')
        htmlAction.setCheckable(True)
        htmlAction.toggled.connect(lambda x: self.updateLanguage('html'))
        
        languageGroup = QtWidgets.QActionGroup(self)
        languageGroup.addAction(pythonAction)
        languageGroup.addAction(htmlAction)
        
        languageMenu = menubar.addMenu('&Language')
        languageMenu.addAction(pythonAction)
        languageMenu.addAction(htmlAction)'''
        
        #message window
        self.messages = QtWidgets.QTextEdit(self)
        self.messages.setFixedSize(300,300)
        self.messages.setReadOnly(True)
        
        #input field
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.setFixedSize(200,30)
        #self.input_field.setShortcut('Ctrl+s')
        #self.input_field.triggered.connect(self.send)
        self.input_field.returnPressed.connect(self.send)
        
        #this widget is needed for the QVBoxLayout to work properly
        self.mainWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.mainWidget)
        
        layout = QtWidgets.QVBoxLayout(self.mainWidget)
        layout.addWidget(self.messages)
        layout.addWidget(self.input_field)

        self.setLayout(layout)
        
        #self.setGeometry(500,500,500,500)
        self.setWindowTitle('MicroIRC')
        self.show()
    
    def newFile(self):
        self.messages.clear()
    
    def saveFile(self):
        #PyQt differs from Qt. getSaveFileName returns a tuple of strings, where the first element is the file path
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', QtCore.QDir.homePath())
        f = open(filename[0], 'w')
        filedata = self.messages.toPlainText()
        f.write(filedata)
        f.close()
    
    def openFile(self):
        #PyQt differs from Qt. getOpenFileName returns a tuple of strings, where the first element is the file path
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', QtCore.QDir.homePath())
        f = open(filename[0], 'r')
        filedata = f.read()
        self.messages.setText(filedata)
        f.close()
        
    def updateLanguage(self, language):
        self.highlighter.language = language
        self.highlighter.rehighlight()
        #class pygments.lexers.textfmts.IrcLogsLexer
        
    def write():
        self.messages.setText(self.messages.toPlainText() + message)
        
    def send(self):
        message = self.input_field.text()
        self.ircListener.client.send_msg(microIRC.CHANNEL, message)
        self.messages.setText(self.messages.toPlainText() + "\n" + message)
        print('QUI')
        
    def ircSignalHandler():
        #we got a signal from the irc thread
        print ('got signal')
        sys.exit(0)

class MicroHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, textEdit):
        super(MicroHighlighter, self).__init__(textEdit.document())
        self.formatter = MicroFormatter(linenos=True)
        self.messages = textEdit
        self.language = 'irc'
    
    def highlightBlock(self, messages):
        
        currentPosition = self.currentBlock().position()
        textToHighlight = str(self.messages.toPlainText()) + '\n'
        
        highlight(textToHighlight, get_lexer_by_name(self.language, stripall=True), self.formatter)
        
        for i in range(len(str(messages))):
            try:
                self.setFormat(i,1,self.formatter.data[currentPosition+i])
            except IndexError:
                pass

class MicroFormatter(HtmlFormatter):
    
    def __init__(self, linenos):
        super(HtmlFormatter, self).__init__()
        self.linenos = linenos
        
        self.data = []
        self.styles = {}
        
        for token, style in self.style:
            textFormatter = QtGui.QTextCharFormat()

            if style['color']:
                textFormatter.setForeground(QtGui.QColor('#' + style['color'])) 
            if style['bgcolor']:
                textFormatter.setBackground(QtGui.QColor('#' + style['bgcolor'])) 
            if style['bold']:
                textFormatter.setFontWeight(QtGui.QFont.Bold)
            if style['italic']:
                textFormatter.setFontItalic(True)
            if style['underline']:
                textFormatter.setFontUnderline(True)
            
            self.styles[str(token)] = textFormatter
    
    def format(self, tokensource, outfile):
        global styles
        self.data = []
        
        for ttype, value in tokensource:
            l = len(value)
            t = str(ttype)                
            self.data.extend([self.styles[t],]*l)

            
class ircListener(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.client = microIRC.IRC_Client()
        
    def run(self):
        self.client.irc_conn()
        self.client.login(microIRC.NICKNAME)
        self.client.join(microIRC.CHANNEL)
        
        while (1):
            raw_msg = self.client.irc_recv()
            if self.client.connected is not True:
                self.client.connected = True
            
            print(raw_msg)
            msg = raw_msg.split(':')
            
            if "PING" in msg[0]: #check if server have sent ping command
                print(msg)
                self.client.irc_send("PONG %s" % msg[1]) #answer with pong as per RFC 1459
            if len(msg) > 2 and "PRIVMSG" in msg[1] and NICKNAME in msg[2]:
                #filetxt = open('/tmp/msg.txt', 'a+') #open an arbitrary file to store the messages
                nick_name = msg[0][:str.find(msg[0],"!")] #if a private message is sent to you catch it
                message = ' '.join(msg[3:])
                #filetxt.write(string.lstrip(nick_name, ':') + ' -> ' + string.lstrip(message, ':') + '\n') #write to the file
                #filetxt.flush() #don't wait for next message, write it now!
            if len(msg) > 2 and 'PRVMSG' in msg[1]:
                self.client.lastmex = " ".join(msg[3:])
            

def main():
    app = QtWidgets.QApplication(sys.argv)
    notepad = Notepad()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
