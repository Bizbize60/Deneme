import mysql.connector
import sys
from PyQt5.QtWidgets import  QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDesktopWidget,QLabel,QPushButton,QLineEdit,QCheckBox,QComboBox

from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class button_widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin123",
            database="kullanici")
        self.mycursor=self.mydb.cursor()
        self.properties()
        self.textures()
        self.input_button.clicked.connect(self.addData)
    def properties(self):
        self.resize(500,500)
        self.move(500,500)
        self.setWindowTitle("Input Screen")
    def textures(self):
        self.cmb=QComboBox(self)
        self.cmb.addItem("ALINACAK")
        self.cmb.addItem("VERİLECEK")
        
        self.input_company=QLineEdit("Şirket",self)
        self.input_company.move(100,0)
        
        self.input_price=QLineEdit("Fiyat",self)
        self.input_price.move(200,0)
        
        self.input_date=QLineEdit("Tarih",self)
        self.input_date.move(300,0)
        
        self.input_button=QPushButton("Ekle",self)
        self.input_button.move(400,0)
    def addData(self):
        data="Insert Into kasa (tip,sirket,fiyat,tarih) VALUES (%s,%s,%s,%s)"
        val=[self.cmb.currentText(),self.input_company.text(),self.input_price.text(),self.input_date.text()]
        self.mycursor.execute(data,val)
        self.mydb.commit()
    
class Canvas(FigureCanvas):
    def __init__(self,parent):
        self.mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin123",
            database="kullanici")
        self.mycursor=self.mydb.cursor()
        self.mycursor.execute("Select tarih,fiyat from kasa where tip='alinacak' ")
        results=self.mycursor.fetchall()
        dates=[x[0] for x in results]
        prices=[x[1] for x in results]
        fig,self.ax=plt.subplots(figsize=(8,4),dpi=100)
        super().__init__(fig)
        self.setParent(parent)
        self.ax.plot(dates,prices)
        self.ax.set(xlabel="tarih",ylabel="ALINACAK",title="GENEL")
        self.ax.grid()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin123",
            database="kullanici")
        self.mycursor=self.mydb.cursor()
        self.properties_MainWindow()
        self.textures_MainWindow()
        self.CaseLabel_MainWindow()
        
        self.chart=Canvas(self)
        self.chart.move(0,350)
        
        
        self.table_MainWindow()
   
        self.button_MainWindow.clicked.connect(self.input_button)
        
        
        
        
        
    def properties_MainWindow(self):
        self.resize(750,750)
        self.move(600,100)
        self.setWindowTitle("ana ekran")
    def textures_MainWindow(self):
        self.button_MainWindow=QPushButton("girdi ekle",self)
        self.button_MainWindow.move(400,0)
    
        self.label_MainWindow=QLabel(self)
        self.label_MainWindow.setText(self.CaseLabel_MainWindow())
        self.label_MainWindow.move(300,300)
        self.label_MainWindow.setFont(QFont("Arial",16))        
    def CaseLabel_MainWindow(self):
        self.mycursor.execute("Select fiyat from kasa where tip='alinacak' ")
        self.results=self.mycursor.fetchall()
        self.income_case=0
        for income in self.results:
            self.income_case+=income[0]
        self.mycursor.execute("Select fiyat from kasa where tip='verilecek' ")
        self.results=self.mycursor.fetchall()
        for outcome in self.results:
            self.income_case-=outcome[0]
        return f"kasa:{self.income_case}"    
    def table_MainWindow(self):
        self.mycursor.execute("Select * from kasa")
        self.results=self.mycursor.fetchall()
      
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        
        self.table.setRowCount(1000)
        self.table.setMinimumHeight(300)
        self.table.setMinimumWidth(400)
        self.mycursor.execute("SELECT * from kasa")
        self.results=self.mycursor.fetchall()
        self.length=len(self.results)  
        for i in range(self.length):
             for j in range(4):
                 self.table.setItem(i,j,QTableWidgetItem(str(self.results[i][j])))
    
    def input_button(self):
        self.button_widget=button_widget()
        self.button_widget.show()
                         
        
    
        
class FirstPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin123"
            )
        self.mycursor=self.mydb.cursor()
        self.properties_FirsPage()
        self.textures_FirstPage()
        self.FirstPageButton.clicked.connect(self.login)
        
    def properties_FirsPage(self):
        self.resize(450,250)
        self.move(600,300)
        self.setWindowTitle("Giriş Ekranı")
        self.show()        

    def textures_FirstPage(self):
        self.username=QLineEdit("Username",self)
        self.username.move(50,25)
        self.username.show()
        
        self.password=QLineEdit("Password",self)
        self.password.move(50,60)
        self.password.show()
             
        self.FirstPageButton=QPushButton("Giriş",self)
        self.FirstPageButton.resize(50,65)
        self.FirstPageButton.move(160,25)
        self.FirstPageButton.setIcon(QIcon('C:/Users/BBS/Desktop/huziyüz.jpg'))
        self.FirstPageButton.show()

        self.FirstPageLabel=QLabel(self)
        self.FirstPageLabel.move(50,90)
        self.FirstPageLabel.show()        
    def login(self):
        self.mycursor.execute("USE kullanici")
        if  self.username.text()=="" or self.password.text()=="":
            self.FirstPageLabel.setText("Kullanici Adi Ve Şifre Girin")
            self.FirstPageLabel.adjustSize()
            
        else:
            self.mycursor.execute("SELECT * FROM users")
            self.results=self.mycursor.fetchall()
            for x in self.results:
                if self.username.text()==x[0] and self.password.text()==x[1]:
                    self.FirstPageLabel.setText("Giriş Yapıldı")
                    self.hide()
                    self.MainWindow=MainWindow()
                    self.MainWindow.show()
                else:
                   self.FirstPageLabel.setText("Yanlış Giriş")
        
app=QApplication(sys.argv)
window=FirstPage() 
sys.exit(app.exec_())