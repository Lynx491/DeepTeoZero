from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys,os
from stable_baselines3 import DQN
import random
from main import Tictactoe    
import torch
import glob

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu") 


#GLOBAL VERİABLE
APP_STYLE = """
QWidget{
background-color:#111111;
}

QLabel{
color:#FFFFFF;
}

QPushButton{
background-color:#222222;
color:#000000;
}
QPushButton::hover{
background-color:#555555;
}
"""

class Window(QWidget):
    hbr_player_hamle = Signal(int)
    def __init__(self,width,height,window_title,window_icon_path):
        super().__init__()
        self.USER = "X"
        self.NETWORK = "O"
        self.playerın_hamlesi:int
        self.genişlik = width
        self.yükseklik = height
        # self.setGeometry(0,0,self.genişlik,self.yükseklik)
        self.setWindowTitle(window_title)
        if window_icon_path != "": #eğer icon verilmemişse
            icon_path = self.iconyoluver = (window_icon_path)
            self.setWindowIcon(QIcon(icon_path))
        self.setStyleSheet(APP_STYLE)
        
        self.root_frame = QFrame(self)
        self.root_frame_w = 490
        self.root_frame_h = 600
        self.root_frame.setGeometry((self.genişlik/2)-(self.root_frame_w/2),(self.yükseklik/2)-(self.root_frame_h/2),self.root_frame_w,self.root_frame_h)


        self.label = QLabel(self.root_frame)
        self.label_font = QFont("Roboto",20)
        self.label.setFont(self.label_font)
        self.label.setGeometry(10,0,600,50)
        # self.label.setStyleSheet("color:#FFFFFF")
        self.label.setText("Tic-Tac-Toe")

        self.baslat = QPushButton(self.root_frame)
        self.baslat_font = QFont("Roboto",20)
        self.baslat.setFont(self.baslat_font)
        self.baslat.setGeometry(10,540,150,50)
        self.baslat.setText("START")
        self.baslat.clicked.connect(self.start)
        
        self.box_network = QComboBox(self.root_frame)
        self.box_network_font = QFont("Roboto",12)
        self.box_network.setFont(self.box_network_font)
        self.box_network.setGeometry(170,540,305,50)


        self.qframe = QFrame(self.root_frame)
        # self.qframe.setStyleSheet("background-color:#333333;")
        self.qframe_w = 490
        self.qframe_h = 490
        self.qframe.setGeometry(0,45,self.qframe_w,self.qframe_h)

        self.btn_x = 150
        self.btn_y = 150
        self.btn_font = QFont("Roboto",64)

        self.btn_sıfır = QPushButton(self.qframe)
        self.btn_sıfır.setGeometry(10,10,self.btn_x,self.btn_y)
        self.btn_sıfır.setFont(self.btn_font)
        self.btn_sıfır.clicked.connect(lambda: self.tetikleyici(0))

        self.btn_bir = QPushButton(self.qframe)
        self.btn_bir.setGeometry(170,10,self.btn_x,self.btn_y)
        self.btn_bir.setFont(self.btn_font)
        self.btn_bir.clicked.connect(lambda: self.tetikleyici(1))

        self.btn_iki = QPushButton(self.qframe)
        self.btn_iki.setGeometry(330,10,self.btn_x,self.btn_y)
        self.btn_iki.setFont(self.btn_font)
        self.btn_iki.clicked.connect(lambda: self.tetikleyici(2))

        self.btn_uc = QPushButton(self.qframe)
        self.btn_uc.setGeometry(10,170,self.btn_x,self.btn_y)
        self.btn_uc.setFont(self.btn_font)
        self.btn_uc.clicked.connect(lambda: self.tetikleyici(3))

        self.btn_dort = QPushButton(self.qframe)
        self.btn_dort.setGeometry(170,170,self.btn_x,self.btn_y)
        self.btn_dort.setFont(self.btn_font)
        self.btn_dort.clicked.connect(lambda: self.tetikleyici(4))

        self.btn_bes = QPushButton(self.qframe)
        self.btn_bes.setGeometry(330,170,self.btn_x,self.btn_y)
        self.btn_bes.setFont(self.btn_font)
        self.btn_bes.clicked.connect(lambda: self.tetikleyici(5))

        self.btn_altı = QPushButton(self.qframe)
        self.btn_altı.setGeometry(10,330,self.btn_x,self.btn_y)
        self.btn_altı.setFont(self.btn_font)
        self.btn_altı.clicked.connect(lambda: self.tetikleyici(6))

        self.btn_yedi = QPushButton(self.qframe)
        self.btn_yedi.setGeometry(170,330,self.btn_x,self.btn_y)
        self.btn_yedi.setFont(self.btn_font)
        self.btn_yedi.clicked.connect(lambda: self.tetikleyici(7))

        self.btn_sekiz = QPushButton(self.qframe)
        self.btn_sekiz.setGeometry(330,330,self.btn_x,self.btn_y)
        self.btn_sekiz.setFont(self.btn_font)
        self.btn_sekiz.clicked.connect(lambda: self.tetikleyici(8))

        self.buttons = [self.btn_sıfır,self.btn_bir,self.btn_iki,self.btn_uc,self.btn_dort,self.btn_bes,self.btn_altı,self.btn_yedi,self.btn_sekiz]
        self.network_bul()

    def network_bul(self):
        ayraç = os.sep
        çalıştırıldığı_dizin = os.path.dirname(sys.executable)
        yol = os.path.join(çalıştırıldığı_dizin,"models")
        if os.path.exists(yol):
            modeller_yolu = yol
        else:
            yol = rf".{ayraç}models"
            if os.path.exists(yol):
                modeller_yolu = yol
                
        modellerData = []
        modellerText = []
        i = 0
        game = Tictactoe()
        liste = glob.glob(modeller_yolu+ayraç+"*.zip")
        if liste:
            for file in liste: #/models kısmındaki bütün .zip ile bitenleri listele
                parçalar = file.split(ayraç) # isim kısmını alıyoruz çünkü basitlik sağlar
                sonindex = len(parçalar)-1
                text = parçalar[sonindex]
                modellerData.append(file)  
                modellerText.append(text)
            for yol,text in zip(modellerData,modellerText):  # combobox a ekle
                self.box_network.addItem(text,yol)   
        else:
            QMessageBox.critical(self,"Kaybolan SinirAğları...",f".{ayraç}models/ klasörü altında .zip ile biten sinir ağları bulunamadı.") 
            

    def iconyoluver(icon_name):
        if sys.platform == "linux" or sys.platform == "darwin": 
            icon_name += ".png"
        elif sys.platform == "win32":
            icon_name += ".ico"
        try:
            yol = sys._MEIPASS #temp yolu
        except:
            yol = os.path.abspath(".")
        path = f"{yol}/{icon_name}"
        if os.path.exists(path):
            return path

    def yüzde_hesapla(self,genişlik,yükseklik):
        g = (self.genişlik/100)*genişlik
        y = (self.yükseklik/100)*yükseklik
        return g,y
    
    def tetikleyici(self,hamle:int):
        self.hbr_player_hamle.emit(hamle) 

    def OyuncudanHamleAl(self,game):
        while True:
            self.dongu = QEventLoop() #hamle bekleniyor
            self.hbr_player_hamle.connect(self.player_hamle)
            self.dongu.exec()
            liste1, liste2 = game.get_lists()
            liste = liste1+liste2
            if len(liste)<9: #boş yer varmı? 
                if not self.playerın_hamlesi in liste:#illegalhamle değilse
                    break
            else:
                break # boş yer yok ya oyun sonlanır otomatik

        return self.playerın_hamlesi

    def player_hamle(self,hamle:int):
        self.dongu.quit()
        self.playerın_hamlesi = hamle

    def start(self):
        game = network()
        #combobox taki en üstteki seçeneği ele al
        data = self.box_network.currentData()
        game.load(data) #valueyi direkt al
        self.label.setText("Tic-Tac-Toe")
        for i in self.buttons:
            i.setText("")
        s = random.randint(0,1)
        durum = game.başlat()
        if s ==0: # 0 model, 1 player
            self.label.setText("İlk Motor başlıyor")
            self.NETWORK = "X"
            self.USER = "O"
        else:
            self.label.setText("İlk Oyuncu Başlıyor")
            self.NETWORK = "O"
            self.USER = "X"
        self.DurumuGöster(game)
        while True:
            if s == 0:
                action = game.hamle_al() #motor hamlesi alınıyor
                durum, reward, done = game.hamleyi_uygula(action,sıramodeldemi=True)
                s=1
                self.DurumuGöster(game)
            else:
                action = self.OyuncudanHamleAl(game) # oyuncudan hamle al
                durum, reward,done = game.hamleyi_uygula(action,sıramodeldemi=False)
                s=0
                self.DurumuGöster(game)

            
            if done:
                if reward == game.İLLEGALHAMLE:
                    self.label.setText("Motor İllegal hamle yaptı, oyun sonlandı")
                elif reward == game.ÖDÜL:
                    self.label.setText("Motor kazandı")
                elif reward == game.CEZA:
                    self.label.setText("Player kazandı")
                elif reward == game.BERABERE:
                    self.label.setText("Berabere")
                break

    def DurumuGöster(self,game):
        durum = game.get_state()
        index = 0
        for i in durum: #[-1,0,1]
            if i == 1: #model oynamış
                self.buttons[index].setText(self.NETWORK)
                if self.NETWORK == "X":
                    self.buttons[index].setStyleSheet("color:#FF0000;")#kırmızı
                else:
                    self.buttons[index].setStyleSheet("color:#0000FF;")#mavi
            elif i == -1: #oyuncu oynamış
                self.buttons[index].setText(self.USER)
                if self.USER == "X":
                    self.buttons[index].setStyleSheet("color:#FF0000;")#kırmızı
                else:
                    self.buttons[index].setStyleSheet("color:#0000FF;")#mavi
            else:
                self.buttons[index].setStyleSheet("color:#FFFFFF;") #beyaz
            index +=1





class network():
    def __init__(self):
        self.game = Tictactoe()
        self.model:DQN
        self.İLLEGALHAMLE = -5
        self.BERABERE = -0.5
        self.CEZA = -1
        self.ÖDÜL = 1
    def load(self,model_yolu):
        if os.path.exists(model_yolu):
            self.model = DQN.load(model_yolu,env=self.game,device=device)
            


    
    def başlat(self):
        durum, _ = self.game.reset(player=True,otomatikmi=False)
        return durum
    
    def hamle_al(self):
        hamle, _ = self.model.predict(self.game.get_state())
        return hamle
    
    def hamleyi_uygula(self,hamle,sıramodeldemi:bool):
        durum, reward, done, done2, info = self.game.step(hamle,sıraModelde=sıramodeldemi)
        return durum,reward,done
    def get_state(self):
        return self.game.durum
    def get_lists(self):
        return self.game.engine_list, self.game.rakip_list

    





    



if __name__ == "__main__":
    app = QApplication()
    
    qtscreen = app.primaryScreen()
    value = qtscreen.availableGeometry()
    window = Window(value.width(),value.height(),"Tic-Tac-Toe","DTZ_icon")
    window.showMaximized()
    sys.exit(app.exec())



