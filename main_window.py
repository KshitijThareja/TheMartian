from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from datetime import date
from threading import *
import test
import requests
import json
import webbrowser
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
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.textbox = QLineEdit(self)
        self.textbox.move(40, 600)
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(40, 650)
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(40, 700)
        self.buttontxt = QPushButton('Submit', self)
        self.buttontxt.move(40,850)
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
        # print(,textboxValue1,textboxValue2)
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
        self.setWindowIcon(QIcon("icon.png")) 
        self.setGeometry(100, 100, 500, 500)
        self.setMinimumSize(600,600)
        self.i=0
        self.w = None
        self.uicomponents()
    def uicomponents(self):
        # layout=QFormLayout()
        # self.setLayout(layout)
        
        self.date_edit = QDateEdit(self)
             
        self.result_label = QLabel('', self)

        labeldate= QLabel('Set Date', self)
        labeldate.setGeometry(30, 20, 200, 60)

        self.date_edit.setGeometry(30,70,150,40)
        label = QLabel("Camera", self)

        self.combo_box = QComboBox(self)
 
        self.combo_box.setGeometry(30, 200, 150, 40)
 
        cam_list = ['navcam', 'fhaz', 'rhaz', 'mast', 'chemcam', 'mahli', 'mardi']
 
        self.combo_box.addItems(cam_list)
 
        self.combo_box.setEditable(True)
        label.setGeometry(30, 150, 200, 60)
        label.setWordWrap(True)
        button = QPushButton("Fetch Images", self)
        button.setGeometry(30, 250, 150, 40)
        self.label = QLabel(self)
        self.label.setGeometry(QRect(400, 20, 550, 700))
        buttonnxt = QPushButton("Next", self)
        buttonnxt.setGeometry(30, 300, 150, 40)
        buttonnxt.clicked.connect(self.next)

        buttonxt = QPushButton("prev", self)
        buttonxt.setGeometry(30, 400, 150, 40)
        buttonxt.clicked.connect(self.prev)
        rad_label= QLabel("Email the images?", self) 
        rad_label.setGeometry(40,450,200, 60)
        self.rb = QRadioButton('Yes', self)
        self.rb2 = QRadioButton('No', self)
        self.rb.move(40, 490)
        self.rb2.move(40, 520)
        self.rad_button= QPushButton("Confirm", self)
        self.rad_button.setGeometry(30, 550, 150, 40)
        self.rad_button.clicked.connect(self.rad)
        # self.textbox = QLineEdit(self)
        # self.textbox.move(40, 600)
        # self.textbox1 = QLineEdit(self)
        # self.textbox1.move(40, 650)
        # self.textbox2 = QLineEdit(self)
        # self.textbox2.move(40, 700)
        # self.buttontxt = QPushButton('Submit', self)
        # self.buttontxt.move(40,850)
        # self.buttontxt.clicked.connect(self.email)
        # self.textbox.resize(280,40)
        button.clicked.connect(self.thread)
    


    def thread(self):
        t1=Thread(target=self.find)
        t1.start()
        
    def find(self):

        content = self.combo_box.currentText()
        value = self.date_edit.date()
        pydate=str(value.toPyDate())
        print(pydate, content )
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
        for url_num in range(len(url_list)):
            urls = url_list[url_num]
            urllib.request.urlretrieve(urls, f"image{url_num}.png")
            
        p=os.getcwd()
        np= os.path.join(p, f'images')
        try:
            for filename in os.listdir():
                if filename.endswith(".png"):
                    isexist= os.path.exists(np)
                    if isexist==True:
                        shutil.move(os.path.join(p,filename), np)
                    else:
                        os.makedirs(np)
                        shutil.move( os.path.join(p,filename), np)  
            
        except:
            print("No files for given date")
    def next(self):
        self.pixmap=QPixmap(f'images/image{self.i}.png')
        self.label.setPixmap(self.pixmap)
        self.i+=1
        self.label.show()
            
    def prev(self):
        self.pixmap=QPixmap(f'images/image{self.i}.png')
        self.label.setPixmap(self.pixmap)
        self.i-=1
        self.label.show()
    def rad(self):
        if self.rb.isChecked():
            val="Yes"
        elif self.rb2.isChecked():
            val="No"
        else:
            val=None
        # print(val)
        if val=="Yes":
            if self.w is None:
                self.w = AnotherWindow()
            self.w.show()

        else:
            shutil.rmtree("images", ignore_errors=False, onerror=None) 
            pass
