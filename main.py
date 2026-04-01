import gymnasium as gym
from gymnasium import spaces
import random
from stable_baselines3 import DQN
import numpy as np
import sys,os
from stable_baselines3.common.buffers import ReplayBuffer
import pickle
import torch

#GLOBAL DEĞİŞKENLER

MODEL = "O"
KULLANICI = "X"
BUFFER_SİZE = 100000#100bin
BUFFER_YOLU = "./buffer/replay_buffer.pkl"
MODEL_PATH = "./model/model.zip"

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

class Tictactoe(gym.Env):
    def __init__(self):
        super().__init__()
        self.engine_list = []
        self.rakip_list = []
        self.ÖDÜL = 1
        self.CEZA = -1
        self.İLLEGALHAMLE = -5
        self.BERABERE = -0.5
        self.player = False
        self.kazanma_koşulları = [[0,1,2],
                            [3,4,5], #0,1,2
                            [6,7,8], #3,4,5
                            [0,3,6], #6,7,8
                            [1,4,7],
                            [2,5,8],
                            [0,4,8],
                            [2,4,6]]
        # self.seçili_aksiyon = spaces.Discrete(3)
        self.action_space = spaces.Discrete(9)

        # self.durum = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=-1, high=1, shape=(9,), dtype=np.float32)

        self.karşı_hamle = 4
        self.durum = [0,0,0,0,0,0,0,0]


    def reset(self,seed=None,options=None,player = False,otomatikmi=True):
        global KULLANICI,MODEL
        self.karşı_hamle =4
        self.engine_list = []
        self.rakip_list = []

        self.player = player
        self.durum = veri_görselleştir(self.engine_list,self.rakip_list,ret= True)
        self.otomatik = otomatikmi

        if self.otomatik:
            sayi = random.randint(0,1)
            if sayi == 0:
                self.sıraModeldemi = True
                MODEL = "O"
                KULLANICI = "X"
            else:
                self.sıraModeldemi = False
                MODEL = "X"
                KULLANICI = "O"
        else:
            self.sıraModeldemi = True
        return np.array(self.durum,dtype = np.float32), {}
    def get_state(self):
        return np.array(self.durum,dtype = np.float32)
    def step(self,action,sıraModelde=True,kopy_model=False):
        if self.otomatik == False: # eğer otomatik değilse monuelse
            self.sıraModeldemi = sıraModelde #sıranın kimde olduğunu manuel ver
        

        if self.sıraModeldemi: #sıra kimde? modelde ise
            self.karşı_hamle = 4

        else:
            self.karşı_hamle = action # oynayan eğer player ise zaten bu geçerli olucak eğer değilse rastgele birşey seçilcek çünkü aksi halde gelen şey 0 oluyor



        liste = self.rakip_list + self.engine_list
        reward = 0

        
        if self.sıraModeldemi:
            self.engine_list.append(action)#modelin hamlesi işleniyor
            if action in liste:# illegal hamle kontrolu 
                reward = self.İLLEGALHAMLE
                done = True
            else:
                if len(self.engine_list+self.rakip_list) <9:
                    if self.kontrol(self.engine_list): #kazanma kaybetme beraberlik kontrolü
                        reward = self.ÖDÜL
                        done = True
                    else:  
                        done = False
                        reward = 0
                else:
                    done = True
                    reward = self.BERABERE



        else:
            if self.player == False: #hamleyi yapan oyuncu değilse
                if kopy_model == False: #hamleyi yapan kopya model değilse
                    self.karşı_hamle = self.RastgeleHamle() #rastgele hamle seçer
                    self.rakip_list.append(self.karşı_hamle)#hamleyi karşı tarafa ekle
                else:

    

                    if self.karşı_hamle in liste: #İLLEGAL HAMLE KONTROLÜ
                        self.karşı_hamle = self.RastgeleHamle() #rastgele hamle
                        self.rakip_list.append(self.karşı_hamle)# hamleyi karşı tarafa ekler
                    else:
                        self.rakip_list.append(self.karşı_hamle)# hamleyi karşı tarafa ekler
            else:
                self.rakip_list.append(self.karşı_hamle)# oyuncu ise zaten hamle seçilmiştir
            
            if len(self.engine_list+self.rakip_list) <9: #0,1,2...8 len > 1,2,3..9
                if self.kontrol(self.rakip_list):
                    reward = self.CEZA
                    done = True
                else:
                    done = False   
                    reward = 0
            else:
                done = True
                reward = self.BERABERE

        
        if self.sıraModeldemi:
            self.sıraModeldemi = False
        else:self.sıraModeldemi = True
        self.durum = veri_görselleştir(self.engine_list,self.rakip_list,ret= True)
        
        return np.array(self.durum,dtype=np.float32), reward, done,False ,{"SıraBende":self.sıraModeldemi}
    
    def RastgeleHamle(self):
        while True:
            hamle = random.randint(0,8) # rastgele bir sayı seç
            if len(self.engine_list+self.rakip_list) < 9:# eğer boş yer varsa
                if not hamle in (self.rakip_list + self.engine_list): # bu hamle daha önce oynanmamışsa
                    break #döngüden çık
            else:# döngüden çık çünkü seçilen hamlenin bir önemi yok
                break
        return hamle
        

    def kontrol(self,liste):
        for koşul in self.kazanma_koşulları:
            eleman_index = 0
            for eleman in koşul:
                if eleman in liste:
                    eleman_index +=1
            if eleman_index >= 3:
                return True
        return False
    

        
def temizle():
    if sys.platform == "darwin":
        os.system("clear")
    elif sys.platform == "win32":
        os.system("cls")
    elif sys.platform == "linux":
        os.system("clear") 
        
    

def test(model,kaçkere=20):
    env = Tictactoe()      # oyun ortamını başlat
    obs, _ = env.reset(otomatikmi=False)     # oyunu sıfırla
    i=0
    berabere = 0
    illegalhamle = 0
    kazanma = 0
    kaybetme = 0
    s = random.randint(0,1) #ilk kim başliyacak
    if s==0:#0 rastgele 1 model
        d = False
    else:d=True
    while i<kaçkere:   
        
        if s == 1:
            action, _ = model.predict(obs)   # modelin hareketini al
            obs, reward, done, _, _ = env.step(action,sıraModelde=True)   # hareket uygula
            s = 0
            print(f"durum: {obs}, Bot seçti: {action}, Ödül: {reward}")
        else:
            obs, reward, done, _, _ = env.step(0,sıraModelde=False)
            s=1
            print(f"durum: {obs}")
        if done: # oyun biterse baştan başlat
            obs, _ = env.reset(otomatikmi=False)
            i+=1   
            if reward == env.İLLEGALHAMLE:
                illegalhamle +=1
            elif reward == env.ÖDÜL:
                kazanma +=1
            elif reward == env.CEZA:
                kaybetme +=1
            else:#berabere
                berabere +=1
    print(f"berabere = {berabere}, kazanma = {kazanma}, kaybetme = {kaybetme}, illegal hamle = {illegalhamle}")

def hareketAl(liste = []):
    while True:
        m="""
[0,1,2]
[3,4,5]
[6,7,8]

sayı seçin:
"""
        print(m)
        rakip_hareket = int(input("\n0-8: "))
        if rakip_hareket >= 0 and rakip_hareket <=8:
            if not rakip_hareket in liste:
                return rakip_hareket
            else:
                print("\n >>>>>>>>><seçilmiş, başka bir tane seç<<<<<<<<<<<<<\n")
def eğitim():
    env = Tictactoe()
    try:
        model = DQN.load(MODEL_PATH,env=env,device=device)
    except:
        model = DQN("MlpPolicy",env,verbose=1,device=device)
    model.learn(total_timesteps=5000)
    model.save("tictactoe")

  

def player_vs_model():
    global MODEL,KULLANICI
    game = Tictactoe()
    model = DQN.load(MODEL_PATH,env=game,device=device)
    s = random.randint(0,1)#0 player 1 model
    if s == 0:
        MODEL = "O"
        KULLANICI = "X"
    else:
        MODEL = "X"
        KULLANICI = "O"
    game.reset(player=True,otomatikmi=False)
    durum = veri_görselleştir(game.engine_list,game.rakip_list,ret=True)
    durum_göster(game)
    for i in range(500):
        d = "devam ediyor"
        if s == 0:
            rh = hareketAl(game.engine_list+game.rakip_list)
            temizle()
            durum, r, done, f, info = game.step(rh,sıraModelde=False)
            s = 1 #hamle sırasını diyerine ver
            durum_göster(game)
        else:
            hareket, a = model.predict(np.array(durum,dtype = np.float32))
            durum, r, done, f, info = game.step(hareket,sıraModelde=True)
            s = 0# sırayı değiştir
            durum_göster(game)
            
        d = ""
        if r == game.İLLEGALHAMLE:
            d = "bot illegal hamle yaptı:"
        elif r == game.ÖDÜL:
            d = f"kaybettin {game.engine_list}"
        elif r  == game.CEZA:
            d = f"Kazandın {game.rakip_list}"
        elif r == game.BERABERE:
            d = "berabere"
        if done:
            s = random.randint(0,1)#0 player 1 model
            if s == 0:
                MODEL = "X"
                KULLANICI = "O"
            else:
                MODEL = "O"
                KULLANICI = "X"
            game.reset(player=True,otomatikmi=False)
            print("\n\n OYUN BİTTİ \n\n")
            print(f"{d}")


        
def durum_göster(game):
        m = f"""

========================
        DURUM
========================
"""
        m2="""

========================
"""
        print(m)
        print(veri_görselleştir(game.engine_list,game.rakip_list))
        print(m2)
        input("\n\nlütfen 'enter'a basın")
        temizle()

            
            
def veri_görselleştir(liste1,liste2,ret=False):
    grid = [[0,0,0],
            [0,0,0],
            [0,0,0]]

    # for eleman1,eleman2 in zip(liste1,liste2):
    #     satir1 = (eleman1-1)//3#1 için
    #     sutun1 = (eleman1-1)%3
    #     grid[satir1][sutun1] = "O"

    #     satir2 = (eleman2-1)//3#-1 için
    #     sutun2 = (eleman2-1)%3
    #     grid[satir2][sutun2] = "X"
    #O for
    for eleman1 in liste1: #1-9 = (elemanX-1) 0-8 = (elemanX)
        satir1 = (eleman1)//3
        sütun1 = (eleman1)%3
        grid[satir1][sütun1] = MODEL
    #X for
    for eleman2 in liste2:
        satir2 = (eleman2)//3
        sütun2 = (eleman2)%3
        grid[satir2][sütun2] = KULLANICI

    if ret:
        liste = grid[0]+grid[1]+grid[2]
        newliste = []
        for i in liste:
            if type(i) == int:
                newliste.append(i)
            elif type(i) == str:
                if i == MODEL:
                    newliste.append(1)
                else:
                    newliste.append(-1)
        return newliste
    else:
        for satir in grid:
            print(satir)
def modelleri_yükle():
    game = Tictactoe()
    try:
        model = DQN.load(MODEL_PATH,env=game,device=device)
        kopy_model = DQN.load(MODEL_PATH,env=game,device=device)
    except:
        print("model bulunamadı, sıfırdan model oluşturuluyor...")
        model = DQN("MlpPolicy",env=game,device=device,verbose=1)
        kopy_model = DQN("MlpPolicy",env=game,device=device,verbose=1)
    return model,kopy_model
 
def self_play(kaçkere=20,kaydetme_sıklığı=2): #rastgele ile öğrenmiyor
    game = Tictactoe()
    model,kopy_model = modelleri_yükle()
    print("model yükleniyor")
    i=1
    s = random.randint(0,1)
    # durum = veri_görselleştir([],[],ret=True)
    durum, _ = game.reset(otomatikmi=False)

    hareketler = []
    öncekidurumlar = []
    rewardlar = []
    doneler = []
    sonrakidurumlar = []
    infolar = []
    print("buffer yükleniyor...")
    try:
        with open(BUFFER_YOLU,"rb")as file:
            buffer = pickle.load(file)
    except:
        print("buffer bulunamadı... sıfırdan buffer oluşturuluyor")
        buffer = ReplayBuffer(BUFFER_SİZE,game.observation_space,game.action_space,device=device) #replay_buffer

    print(f"\n...self-play {i}/{kaçkere}")
    while i<kaçkere+1:
        hareketler.clear()
        öncekidurumlar.clear()
        sonrakidurumlar.clear()
        rewardlar.clear()
        doneler.clear()
        infolar.clear()

        if s == 0:#0 model
            oncekidurum = game.get_state()
            action, _ = model.predict(durum)
            durum, reward,done,done2,info = game.step(action,sıraModelde=True)

            hareketler.append(action)
            sonrakidurumlar.append(durum)
            öncekidurumlar.append(oncekidurum)

            rewardlar.append(reward)
            doneler.append(done)
            infolar.append(info)
            s = 1

        else: # 1 kopy_model
            action, _ = kopy_model.predict(durum)
            durum,reward,done,done2,info = game.step(action,sıraModelde=False,kopy_model=True)
            s=0

        if done:
            durum, _ = game.reset(otomatikmi=False)
            i+=1
            print(f"\n...self-play {i}/{kaçkere}")
            if i >= kaydetme_sıklığı:
                for action,durum,nextdurum,ödül,tamamlandı,info in zip(hareketler,öncekidurumlar,sonrakidurumlar,rewardlar,doneler,infolar):
                    buffer.add(durum,nextdurum,action,ödül,tamamlandı,[info]) 
                
                model.learn(total_timesteps=1)
                model.replay_buffer = buffer                   
                
                print("\nmodel eğitiliyor")
                model.train(batch_size=64,gradient_steps=100) #rastgele 64 veri çek , 100 kere tekrar et
                print("\nmodel kaydediliyor...")
                model.save(MODEL_PATH)
                print(f"\nreplay buffer diske kaydediliyor {BUFFER_YOLU}")
                with open(BUFFER_YOLU,"wb") as file:
                    pickle.dump(buffer,file)
                print("\nreplay_buffer kaydediliyor")
                print("\nmodeller tekrar yükleniyor...")
                model, kopy_model = modelleri_yükle()
              

    model.save(MODEL_PATH)
    print("\nmodel kaydedildi")
        
    




if __name__ == "__main__":
    self_play(5000) #5K self-play 