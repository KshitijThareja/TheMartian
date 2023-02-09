from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from datetime import date
from threading import *
import requests
import json
import urllib.request
from PIL import Image
import os, shutil
import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel
from dotenv import load_dotenv
load_dotenv()
class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #000000;")
        self.setWindowIcon(QIcon('icon.png')) 

        self.setFixedSize(700,700)
        self.setWindowTitle("Gmail Wizard")
        self.textbox = QLineEdit(self)
        # self.textbox.resize(200,100)
        self.textbox.setPlaceholderText("Recipients")
        self.textbox.setGeometry(200, 200, 300, 50)
        self.textbox1 = QLineEdit(self)
        self.textbox.setStyleSheet("QLineEdit"
                             "{"
                             "border : 1px solid;"
                             "border-color : #6B728E;"
                             "}"
                             "QLineEdit::hover"
                                "{"
                                "border : 1px solid white;"
                                "}")
        self.textbox1.setStyleSheet("QLineEdit"
                             "{"
                             "border : 1px solid;"
                             "border-color : #6B728E;"
                             "}"
                             "QLineEdit::hover"
                                "{"
                                "border : 1px solid white;"
                                "}")
        
        self.textbox1.setPlaceholderText("Subject")
        self.textbox1.setGeometry(200,300,300,50)                                     
        self.textbox2 = QLineEdit(self)
        self.textbox2.setStyleSheet("QLineEdit"
                             "{"
                             "border : 1px solid;"
                             "border-color : #6B728E;"
                             "}"
                             "QLineEdit::hover"
                                "{"
                                "border : 1px solid white;"
                                "}")
        self.textbox2.setPlaceholderText("Body")
        self.textbox2.setGeometry(200, 400, 300, 200)
        self.buttontxt = QPushButton('Submit', self)
        self.buttontxt.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #000000;"
                             "border : 1.5px solid;"
                             "border-color : #B42B51;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #B42B51;"
                                "border : 1.5px solid;"
                                "border-color : white;"
                             "}"
                             )
        self.buttontxt.setGeometry(200,650, 140,30)
        self.btn = QPushButton('Exit', self)
        self.btn.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #000000;"
                             "border : 1.5px solid;"
                             "border-color : #B42B51;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #B42B51;"
                                "border : 1.5px solid;"
                                "border-color : white;"
                             "}"
                             )
        self.btn.setGeometry(360, 650, 140,30)
        self.btn.clicked.connect(self.close)
        self.buttontxt.clicked.connect(self.thread)
    def thread(self):
        t1=Thread(target=self.email)
        t1.start()
    
    def email(self):

        import ezgmail
        from email.message import EmailMessage
        recipient = self.textbox.text()
        subject = self.textbox1.text()
        body = self.textbox2.text()
        self.textbox.setText("")
        self.textbox1.setText("")
        self.textbox2.setText("")
        rec_list= recipient.split(', ')
        files=[]
        for filename in os.listdir('images'):
            if filename.endswith(".png"):
                files.append(os.path.join('images', filename))

        for receivers in rec_list:
            try:
                ezgmail.send(receivers, subject, body, attachments=files)
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Result")
                dlg.setText("Email sent successfully")
                dlg.exec()
                
            except:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Result")
                dlg.setText("Email not sent")
                dlg.exec()

class appWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarsMan")
        self.setWindowIcon(QIcon('icon.png')) 
        self.setStyleSheet("background-color: #000000;")
        self.setGeometry(100, 100, 500, 500)
        self.setFixedSize(1000,800)
        # self.setWindowIcon(QIcon("logor.png"))
        
        self.i=0
        self.w = None
        self.uicomponents()
    def uicomponents(self):
        self.labellogo = QLabel(self)
        self.labellogo.setGeometry(QRect(-110, -120, 500, 500))
        self.pixmap=QPixmap(f'logofin.png')
        self.labellogo.setPixmap(self.pixmap)
        
        self.labellogo.show()

        self.date_edit = QDateEdit(self)
             
        self.result_label = QLabel('', self)
        # self.result_label.setStyleSheet("background-color: #3F0071")

        labeldate= QLabel('Set Date', self)
        # labeldate.setStyleSheet("background-color: #3F0071")
        labeldate.setGeometry(30, 230, 80, 20)

        self.date_edit.setGeometry(110,220,150,40)
        label = QLabel("Camera", self)
        # label.setStyleSheet("background-color: #3F0071")

        self.combo_box = QComboBox(self)                            
 
        self.combo_box.setGeometry(110, 280, 150, 40)
 
        cam_list = ['navcam', 'fhaz', 'rhaz', 'mast', 'chemcam', 'mahli', 'mardi']
 
        self.combo_box.addItems(cam_list)
 
        self.combo_box.setEditable(True)
        label.setGeometry(30, 290, 80, 20)
        label.setWordWrap(True)
        button = QPushButton("Fetch Images", self)
        button.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #000000;"
                             "border : 1.5px solid;"
                             "border-color : #B42B51;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #B42B51;"
                                "border : 1.5px solid;"
                                "border-color : white;"
                             "}"
                             )
        button.setGeometry(30, 350, 230, 40)
        self.labelfirst = QLabel(self)
        self.labelfirst.setGeometry(QRect(350, 20, 600, 700))
        self.label = QLabel(self)
        self.label.setGeometry(QRect(350, 20, 600, 700))
        buttonnxt = QPushButton(">", self)
        buttonnxt.setGeometry(670, 735, 50, 40)
        buttonnxt.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #000000;"
                             "border : 1.5px solid;"
                             "border-color : #B42B51;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #B42B51;"
                                "border : 1.5px solid;"
                                "border-color : white;"
                             "}"
                             )

        buttonnxt.clicked.connect(self.next)

        buttonxt = QPushButton("<", self)
        buttonxt.setGeometry(570, 735, 50, 40)
        buttonxt.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #000000;"
                             "border : 1.5px solid;"
                             "border-color : #B42B51;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #B42B51;"
                                "border : 1.5px solid;"
                                "border-color : white;"
                             "}"
                             )

        buttonxt.clicked.connect(self.prev)
        rad_label= QLabel("Send data as Email attachments?", self)
        # rad_label.setStyleSheet("background-color: #3F0071")
        rad_label.setGeometry(40,500,250, 60)
        self.rb = QRadioButton('Yes', self)
        self.rb.setStyleSheet(
                             "QRadioButton::indicator:unchecked" 
                             "{"
                            "background-color:black;"
                            "border:1px solid white;"
                            "}"
                             )
        self.rb2 = QRadioButton('No', self)
        self.rb2.setStyleSheet(
                             "QRadioButton::indicator:unchecked" 
                             "{"
                            "background-color:black;"
                            "border:1px solid white;"
                            "}"
                             )
        self.rb.move(40, 540)
        self.rb2.move(40, 570)
        self.rad_button= QPushButton("Confirm", self)
        self.rad_button.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #000000;"
                             "border : 1.5px solid;"
                             "border-color : #B42B51;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #B42B51;"
                                "border : 1.5px solid;"
                                "border-color : white;"
                             "}"
                             )
        self.rad_button.setGeometry(30, 610, 230, 40)
        self.rad_button.clicked.connect(self.rad)
        btn_reset= QPushButton("Reset selection", self)
        btn_reset.setStyleSheet("QPushButton"
                             "{"
                             "background-color : #000000;"
                             "border : 1.5px solid;"
                             "border-color : #B42B51;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #B42B51;"
                                "border : 1.5px solid;"
                                "border-color : white;"
                             "}"
                             )
        btn_reset.setGeometry(30, 400, 230, 40)
        btn_reset.clicked.connect(self.delf)
        button.clicked.connect(self.thread)
    
    def thread(self):
        t1=Thread(target=self.find)
        t1.start()
        
    def find(self):

        content = self.combo_box.currentText()
        value = self.date_edit.date()
        pydate=str(value.toPyDate())
        print(pydate, content)
        secret=str(os.getenv('SECRET'))

        params = {"earth_date":pydate, "api_key":secret, "camera":content, "page":1}
        f = fr"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?"
        data = requests.get(f, params = params)
        a = json.loads(data.text)
        datalist=[]
        url_list=[]
        for i in a["photos"]:
            datalist.append(i)
        for j in range(len(datalist)):
            b = datalist[j]["img_src"]
            url_list.append(b)
        if len(url_list)==0:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Fetch error")
            dlg.setText("No files for given date")
            dlg.exec()
        p=os.getcwd()
        np= os.path.join(p, f'images')
        os.makedirs(np)
        

        try:
            for url_num in range(len(url_list)):
                urls = url_list[url_num]
                urllib.request.urlretrieve(urls, f"images/image{url_num}.png")
            self.pixmapfirst=QPixmap(f'images/image0.png')
            self.labelfirst.setPixmap(self.pixmapfirst)
            self.labelfirst.show()
            self.next()
        except:
            print("No files for given date")
    def next(self):
        self.i+=1
        self.pixmap=QPixmap(f'images/image{self.i}.png')
        self.label.setPixmap(self.pixmap)
        
        self.label.show()
            
    def prev(self):
        self.pixmap=QPixmap(f'images/image{self.i}.png')
        self.label.setPixmap(self.pixmap)
        self.i-=1
        self.label.show()
    def delf(self):
        shutil.rmtree("images", ignore_errors=False, onerror=None) 

    def rad(self):
        if self.rb.isChecked():
            val="Yes"
        elif self.rb2.isChecked():
            val="No"
        else:
            val=None
        if val=="Yes":
            if self.w is None:
                self.w = AnotherWindow()
            self.w.show()

        else:
            
            pass
        
