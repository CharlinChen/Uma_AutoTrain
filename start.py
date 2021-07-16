import subprocess
from io import BytesIO
import time
import matplotlib.pyplot as plt
import numpy as np
import random

SAVE_DATA = True # Whether to save logs

screenshot = None
# Preload the number icon
SX0 = plt.imread('icon/0.png')
SX1 = plt.imread('icon/1.png')
SX2 = plt.imread('icon/2.png')
SX3 = plt.imread('icon/3.png')
SX4 = plt.imread('icon/4.png')
SX5 = plt.imread('icon/5.png')
SX6 = plt.imread('icon/6.png')
SX7 = plt.imread('icon/7.png')
SX8 = plt.imread('icon/8.png')
SX9 = plt.imread('icon/9.png')
def get_RB_color(T):
    index_0_R = (-T[:, :, 0] + 1) < 0.1
    index_0_G = (-T[:, :, 1] + 1) < 0.1
    index_0_B = (-T[:, :, 2] + 1) < 0.1
    index_0 = index_0_R & index_0_G & index_0_B
    index_1_R = abs(-T[:, :, 0] + 0.66) < 0.16
    index_1_G = abs(-T[:, :, 1] + 0.36) < 0.18
    index_1_B = abs(-T[:, :, 2] + 0.22) < 0.24
    index_1 = index_1_R & index_1_G & index_1_B
    p = np.zeros(shape=T.shape)
    p[index_0, 0] = 1
    p[index_1, 1] = 1
    return p
B0 = get_RB_color(plt.imread('icon/b0.png'))
B1 = get_RB_color(plt.imread('icon/b1.png'))
B2 = get_RB_color(plt.imread('icon/b2.png'))
B3 = get_RB_color(plt.imread('icon/b3.png'))
B4 = get_RB_color(plt.imread('icon/b4.png'))
B5 = get_RB_color(plt.imread('icon/b5.png'))
B6 = get_RB_color(plt.imread('icon/b6.png'))
B7 = get_RB_color(plt.imread('icon/b7.png'))
B8 = get_RB_color(plt.imread('icon/b8.png'))
B9 = get_RB_color(plt.imread('icon/b9.png'))

class uma():
    YaRuKi = 0
    TiLi = 0
    Friend = False
    Health = False
    Speed = 0
    Stamina = 0
    Power = 0
    Root = 0
    Intellect = 0
    Skill_num = 0

    def __init__(self):
        self.Turns = 0
        self.autoLearnSkill = True
        self.distance = 0
        self.target = [0,0,0,0,0]
        self.progress = np.zeros(5)

    def get_target(self):
        if self.distance == 0:
            # Short range target
            self.target = [999, 400, 900, 100, 500]
        elif self.distance == 1:
            # Miles target
            self.target = [950, 500, 800, 200, 400]
        elif self.distance == 2:
            # Middle range target
            self.target = [900, 650, 750, 300, 300]
        elif self.distance == 3:
            # Long range target
            self.target = [800, 800, 750, 350, 300]
        elif self.distance == 4:
            # Custom target
            self.target = [700, 999, 800, 350, 300]
        elif self.distance == 5:
            # Custom target
            self.target = [900, 400, 900, 100, 900]

    def cal_target_progress(self):
        '''
        Calculate the target progress
        :return:
        '''
        sx = [self.Speed, self.Stamina, self.Power, self.Root, self.Intellect]
        for i in range(5):
            if sx[i] < 10:
                sx[i] = 1000 #OCR can't recognize four digits
            self.progress[i] = (sx[i])/self.target[i]
        print("progress:\n",self.progress*100,"%")

    def add_Turns(self):
        self.Turns += 1
        print("\n===============\nターン：",self.Turns,"\n===============\n")
        if SAVE_DATA:
            with open('data.txt','a') as f:
                data_str = str(self.Turns)+","\
                           +str(self.TiLi)+","\
                           +str(self.Speed)+","\
                           +str(self.Stamina)+","\
                           +str(self.Power)+","\
                           +str(self.Root)+","\
                           +str(self.Intellect)+","\
                           +str(self.YaRuKi)+"\n"
                f.write(data_str)

    def get_SX(self):
        '''
        Get the attributes
        :return:
        '''
        # Speed
        SD = cilp_screenshot(105, 1705, 100, 35) # Please change it to the corresponding area on your mobile phone
        self.Speed = SX_number_OCR(SD)
        # Stamina
        SM = cilp_screenshot(275, 1705, 100, 35)
        self.Stamina = SX_number_OCR(SM)
        # Power
        LL = cilp_screenshot(445, 1705, 100, 35)
        self.Power = SX_number_OCR(LL)
        # Root
        GX = cilp_screenshot(615, 1705, 100, 35)
        self.Root = SX_number_OCR(GX)
        # Intellect
        ZH = cilp_screenshot(785 - 3, 1705, 100, 35)
        self.Intellect = SX_number_OCR(ZH)

    def get_TL(self):
        '''
        get current stamina
        :return:
        '''
        p = cilp_screenshot(360, 300, 382, 40) # Change to the target area on your phone
        c1 = p[:, :, 0] == p[:, :, 1]
        c2 = p[:, :, 0] == p[:, :, 2]
        c3 = p[:, :, 2] == p[:, :, 1]
        c = c1 * c2 * c3
        self.TiLi = int((1 - np.sum(c) / (382 * 42)) * 100)

    def get_friend(self):
        '''
        Whether the friend incident happened
        :return:
        '''
        # C1, C2, C3, and C4 are four feature points to identify whether the event is reversed. 
        # For different mobile phones, their positions are different and cannot be shared
        # Please choose the 4 feature points and change the color and position
        c1 = get_color(620, 2056)
        t1 = compcolor([255, 63, 121], c1) < 32
        c2 = get_color(668, 2046)
        t2 = compcolor([255, 69, 131], c2) < 32
        c3 = get_color(643, 2028)
        t3 = compcolor([255, 255, 255], c3) < 32
        c4 = get_color(634, 2071)
        t4 = compcolor([255, 255, 255], c4) < 32
        if t1 & t2 & t3 & t4:
            self.Friend = True
        else:
            self.Friend = False

    def get_health(self):
        '''
        Whether sick?
        :return:
        '''
        # C1, C2, C3, and C4 are four feature points to identify whether the event is reversed. 
        # For different mobile phones, their positions are different and cannot be shared
        # Please choose the 4 feature points and change the color and position
        c1 = get_color(152, 2102)
        t1 = compcolor([154, 152, 159], c1) > 16
        c2 = get_color(365, 2111)
        t2 = compcolor([152, 148, 154], c2) > 16
        c3 = get_color(181, 2049)
        t3 = compcolor([253, 253, 253], c3) < 16
        c4 = get_color(303, 2167)
        t4 = compcolor([255, 255, 255], c4) < 16
        if t1 & t2 & t3 & t4:
            self.Health = False
        else:
            self.Health = True

    def get_YRK(self):
        '''
        get YaRuKi (やる気)
        :return:
        '''
        YLK = np.zeros(5)
        Y1 = [169, 81, 256]
        Y2 = [19, 137, 243]
        Y3 = [256, 165, 4]
        Y4 = [256, 125, 57]
        Y5 = [249, 71, 129]
        C = get_color(900, 340) # Please change the coordinates
        YLK[0] = compcolor(C, Y1)
        YLK[1] = compcolor(C, Y2)
        YLK[2] = compcolor(C, Y3)
        YLK[3] = compcolor(C, Y4)
        YLK[4] = compcolor(C, Y5)
        self.YaRuKi = np.argmin(YLK)
        YRK_text = ["Very Bad", "Bad", "Normal", "Good", "Very Good"]
        self.YaRuKi_Text = YRK_text[int(self.YaRuKi)]

    def show_info(self):
        print("==================")
        print(" ▲Stamina：",self.TiLi)
        print(" ▲YaRuKi：", self.YaRuKi_Text)
        print("------------------")
        print("  ★Speed：",self.Speed)
        print("  ★Stamina：", self.Stamina)
        print("  ★Power：", self.Power)
        print("  ★Root：", self.Root)
        print("  ★Intellect：", self.Intellect)
        print("==================")
        if self.Friend :
            print("The friend events has occurred!")
        if not self.Health:
            print("fall ill!")

    def toRest(self):
        print("Stamina：",self.TiLi,"\n==>Take a rest!")
        TAP(167,1900)
        PAUSE(0.3)
        TAP(777, 1500)
        PAUSE(1.5)

    def toGoOut(self):
        print("やる気：",self.YaRuKi_Text,"\n==>go out!")
        TAP(539,2116)
        PAUSE(0.3)
        TAP(516,902)
        PAUSE(0.5)
        TAP(777, 1500)

    def toTore(self):
        print("All going well==>train")
        deta = random.randint(-20, 20)
        TAP(534 + deta, 1904 + deta)
        PAUSE(0.5)
        CAP()
        T = tore()
        T.get_all_score()
        # get target progress
        self.cal_target_progress()
        # T.beta = (np.ones(5) - self.progress)*(1-self.Turns/80)*5 + np.ones(5)
        T.beta = 50*np.exp(-5*self.progress) + np.ones(5)
        if self.Turns <= 11: 
            T.toreninngu(0)
        elif self.Turns <= 25: 
            T.toreninngu(1)
        elif self.Turns > 25 and self.Turns < 65: 
            # T.beta = [0.8,1.4,0.6,0.6,1.0]
            # T.beta = [1,0.6,1.6,0.3,1.5]
            T.toreninngu(1)
        else:
            # T.beta = [1,1,1,1,1]
            T.toreninngu(1)

    def toHospital(self):
        print("Fall ill=>Go to the health room")
        TAP(259,2018)
        PAUSE(1)
        TAP(774,1496)
        PAUSE(1)

    def toLearnSkill(self):
        if not self.autoLearnSkill:
            return
        print("Start learning the first three skills!")
        TAP(900,1900)
        PAUSE(1)
        TAP(974,1122)
        PAUSE(0.2)
        TAP(974,1344)
        PAUSE(0.2)
        TAP(974,1567)
        PAUSE(0.2)
        TAP(541,2047)
        PAUSE(1)
        TAP(769, 2019)
        self.Skill_num += 3
        PAUSE(7)
        TAP(538,1498)
        PAUSE(1)
        TAP(130,2263)
        PAUSE(0.3)

class tore():
    toSpeed = [0,0,0,0,0]
    toStamina = [0,0,0,0,0]
    toPower = [0,0,0,0,0]
    toRoot = [0,0,0,0,0]
    toIntellect = [0,0,0,0,0]
    beta = [1,1,1,1,1]
    fSpeed = 0
    fStamina = 0
    fPower = 0
    fRoot = 0
    fIntellect = 0

    def get_up_score(self):
        score_array = np.zeros(5)
        for i in range(5):
            T = get_RB_color(cilp_screenshot(40+i*170, 1590, 170, 60))
            score_array[i] = B_number_OCR(T)
        # print(score_array)
        return score_array
    def get_all_score(self):
        # speed
        CAP()
        c = get_color(106,2169)
        T1 = compcolor(c, [255, 255, 132]) < 16*3
        c = get_color(180,2109)
        T2 = compcolor(c, [255, 255, 255]) < 16
        c = get_color(186, 2144)
        T3 = compcolor(c, [177, 74, 0]) <16*3
        if(T1&T2&T3):
            print("Do Not Touch")
        else:
            self.tap_points("SD")
            CAP()
        self.toSpeed=self.get_up_score()
        self.fSpeed = self.get_friends_num()
        print("Speed\nUP:",sum(self.toSpeed),self.toSpeed,"\nNumber of partners：",self.fSpeed,"!")
        # Stamina
        self.tap_points("SM")
        CAP()
        self.toStamina=self.get_up_score()
        self.fStamina = self.get_friends_num()
        print("Stamina:\nUP:",sum(self.toStamina),self.toStamina,"\nNumber of partners：",self.fStamina,"!")
        # Power
        self.tap_points("LL")
        CAP()
        self.toPower=self.get_up_score()
        self.fPower = self.get_friends_num()
        print("Power:\nUP:",sum(self.toPower),self.toPower,"\nNumber of partners：",self.fPower,"!")
        # Root
        self.tap_points("GX")
        CAP()
        self.toRoot=self.get_up_score()
        self.fRoot = self.get_friends_num()
        print("Root:\nUP:",sum(self.toRoot),self.toRoot,"\nNumber of partners：",self.fRoot,"!")
        # Intellect
        self.tap_points("ZH")
        CAP()
        self.toIntellect=self.get_up_score()
        self.fIntellect = self.get_friends_num()
        print("Intellect:\nUP:",sum(self.toIntellect),self.toIntellect,"\nNumber of partners：",self.fIntellect,"!")
    def get_friends_num(self):
        c0 = [109,108,117]
        c1 = [42,192,255]
        c2 = [162,230,29]
        c3 = [255,172,30]
        c4 = [255,235,120]
        c_base=[81,81,81]
        for i in range(6,-1,-1):
            c = get_color(902,501+180*i)
            T_base = compcolor(c_base,c) < 32
            c = get_color(915,501+180*i)
            T0 = compcolor(c0, c) < 16
            T1 = compcolor(c1, c) < 16
            T2 = compcolor(c2, c) < 16
            T3 = compcolor(c3, c) < 16
            T4 = compcolor(c4, c) < 16
            if T_base & (T0 | T1 | T2 | T3 | T4 ):
                return i+1
        return 0
    def tap_points(self,style):
        deta = random.randint(-20, 20)
        if style == "SD":
            TAP(156 + deta, 2044 + deta)
        elif style == "SM":
            TAP(347 + deta, 2025 + deta)
        elif style == "LL":
            TAP(535 + deta, 2033 + deta)
        elif style == "GX":
            TAP(730 + deta, 2025 + deta)
        elif style == "ZH":
            TAP(921 + deta, 2025 + deta)
        else:
            print("parameter error!!")
        PAUSE(0.1)
    def toreninngu(self,w):
        if w==0:
            # Number of partners takes precedence
            P_array = [self.fSpeed+np.sum(self.toSpeed)/100,
                       self.fStamina+np.sum(self.toStamina)/100,
                       self.fPower+np.sum(self.toPower)/100,
                       self.fRoot+np.sum(self.toRoot)/100,
                       self.fIntellect+np.sum(self.toIntellect)/100]
            print("Number of partners takes precedence:\n",P_array)
            fmax = max(P_array)
            if P_array[0] == fmax:
                self.tap_points("SD")
                self.tap_points("SD")
            elif P_array[1] == fmax:
                self.tap_points("SM")
                self.tap_points("SM")
            elif P_array[2] == fmax:
                self.tap_points("LL")
                self.tap_points("LL")
            elif P_array[3] == fmax:
                self.tap_points("GX")
                self.tap_points("GX")
            elif P_array[4] == fmax:
                self.tap_points("ZH")
                self.tap_points("ZH")
        elif w==1:
            # Points takes precedence (weighting)
            P_array = [np.sum(self.toSpeed*self.beta),
                          np.sum(self.toStamina*self.beta),
                          np.sum(self.toPower*self.beta),
                          np.sum(self.toRoot*self.beta),
                          np.sum(self.toIntellect*self.beta)]
            print("Points takes precedence (weighting)")
            print("Current weighting coefficient:\n",self.beta)
            print("The weighted results:\n",P_array)
            fmax = max(P_array)
            if P_array[0] == fmax:
                self.tap_points("SD")
                self.tap_points("SD")
            elif P_array[1] == fmax:
                self.tap_points("SM")
                self.tap_points("SM")
            elif P_array[2] == fmax:
                self.tap_points("LL")
                self.tap_points("LL")
            elif P_array[3] == fmax:
                self.tap_points("GX")
                self.tap_points("GX")
            elif P_array[4] == fmax:
                self.tap_points("ZH")
                self.tap_points("ZH")

class state():
    state = 0

    def get_state(self):
        pass
    def isChoose2(self):
        c1 = get_color(72,1307)
        t1 = compcolor([153,219,46],c1) < 32
        c2 = get_color(72,1475)
        t2 = compcolor([255,205,24],c2) < 32
        c3 = get_color(917,1327)
        t3 = compcolor([255,255,255],c3) < 32
        c4 = get_color(934,1279)
        t4 = compcolor([255, 255, 255], c4) < 32
        if t1&t2&t3&t4:
            return True
        else:
            return False
    def toChoose2(self):
        print("Options branch appears!")
        TAP(522,1324)
    def isChoose3(self):
        c1 = get_color(72, 1139)
        t1 = compcolor([153, 219, 46], c1) < 32
        c2 = get_color(72, 1309)
        t2 = compcolor([255, 205, 24], c2) < 32
        c3 = get_color(72, 1476)
        t3 = compcolor([255, 131, 182], c3) < 32
        c4 = get_color(697, 1332)
        t4 = compcolor([255, 255, 255], c4) < 32
        if t1 & t2 & t3 & t4:
            return True
        else:
            return False
    def toChoose3(self):
        print("Options branch appears!")
        TAP(519, 1153)
    def isMain(self):
        c1 = get_color(387, 1951)
        t1 = compcolor([47, 133, 218], c1) < 32
        c2 = get_color(513, 1943)
        t2 = compcolor([255, 255, 255], c2) < 32
        c3 = get_color(580, 1943)
        t3 = compcolor([47, 137, 223], c3) < 32
        c4 = get_color(658, 1933)
        t4 = compcolor([255, 255, 255], c4) < 32
        if t1 & t2 & t3 & t4:
            return True
        else:
            return False
    def isGoRace(self):
        c1 = get_color(923,738)
        t1 = compcolor([128,205,12],c1) < 32
        c2 = get_color(102,872)
        t2 = compcolor([249,249,249],c2) < 32
        c3 = get_color(337,1617)
        t3 = compcolor([121,64,22],c3) < 32
        c4 = get_color(801,1626)
        t4 = compcolor([255, 255, 255], c4) < 32
        if t1&t2&t3&t4:
            return True
        else:
            return False
    def toGoRace(self):
        print("Target fans not enough, enter the contest!")
        TAP(767, 1624)
        PAUSE(4)
        TAP(756, 2039)
        PAUSE(2)
        # TAP(763, 2045)
        # PAUSE(2)
        TAP(775, 1626)
        PAUSE(2)
    def isRace(self):
        # C1, C2, C3, and C4 are four feature points to identify whether the event is reversed. 
        # For different mobile phones, their positions are different and cannot be shared
        # Please choose the 4 feature points and change the color and position
        c1 = get_color(234, 2080)
        t1 = compcolor([47, 197, 218], c1) < 32
        c2 = get_color(753, 2102)
        t2 = compcolor([247, 74, 138], c2) < 32
        c3 = get_color(314, 2082)
        t3 = compcolor([255, 255, 255], c3) < 32
        c4 = get_color(763, 2080)
        t4 = compcolor([255, 255, 255], c4) < 32
        if t1 & t2 & t3 & t4:
            return True
        else:
            return False
    def toRace(self):
        print("enter contest!")
        TAP(756, 2039)
        PAUSE(4)
        TAP(763, 2045)
        PAUSE(1)
        TAP(775, 1626)
        PAUSE(1)
    def isStartRace(self):
        # C1, C2, C3, and C4 are four feature points to identify whether the event is reversed. 
        # For different mobile phones, their positions are different and cannot be shared
        # Please choose the 4 feature points and change the color and position
        c1 = get_color(369, 2177)
        t1 = compcolor([121, 64, 22], c1) < 32
        c2 = get_color(961, 2208)
        t2 = compcolor([122, 65, 24], c2) < 32
        c3 = get_color(300, 1687)
        t3 = compcolor([255, 255, 255], c3) < 32
        c4 = get_color(679, 2180)
        t4 = compcolor([255, 255, 255], c4) < 32
        if t1 & t2 & t3 & t4:
            return True
        else:
            return False
    def toStartRace(self):
        print("view the results!")
        TAP(373, 2180)
        PAUSE(10)
        TAP(527, 2178)
        PAUSE(5)
        TAP(537, 2188)
        PAUSE(5)
        TAP(750, 2200)
    def isInherit(self):
        c1 = get_color(410, 1971)
        t1 = compcolor([255, 255, 246], c1) < 32
        c2 = get_color(466, 2093)
        t2 = compcolor([254, 146, 29], c2) < 48
        if t1 & t2:
            return True
        else:
            return False
    def toInherit(self):
        print("Inheritance factor!!")
        TAP(535,2001)
    def isRaceSuccess(self):
        # C1, C2, C3, and C4 are four feature points to identify whether the event is reversed. 
        # For different mobile phones, their positions are different and cannot be shared
        # Please choose the 4 feature points and change the color and position
        c1 = get_color(340, 518)
        t1 = compcolor([209, 251, 66], c1) < 32
        c2 = get_color(359, 2049)
        t2 = compcolor([164, 223, 8], c2) < 32
        c3 = get_color(515, 2088)
        t3 = compcolor([255, 255, 255], c3) < 32
        c4 = get_color(33, 1453)
        t4 = compcolor([254, 254, 254], c4) < 32
        if t1 & t2 & t3 & t4:
            return True
        else:
            return False
    def toRaceSuccess(self):
        print("goal clear!")
        TAP(537, 2090)
        PAUSE(3)
        TAP(537, 2090)

    def isRaceFail(self):
        # C1, C2, C3, and C4 are four feature points to identify whether the event is reversed. 
        # For different mobile phones, their positions are different and cannot be shared
        # Please choose the 4 feature points and change the color and position
        c1 = get_color(1039, 711)
        t1 = compcolor([142, 212, 8], c1) < 32
        c2 = get_color(283, 1436)
        t2 = compcolor([255, 189, 195], c2) < 32
        c3 = get_color(266, 1623)
        t3 = compcolor([121, 64, 22], c3) < 32
        c4 = get_color(776, 1623)
        t4 = compcolor([255, 255, 255], c4) < 32
        if t1 & t2 & t3 & t4:
            return True
        else:
            return False

    def toRaceFail(self):
        print("he goal is not achieved, ending...")
        # TAP(291,1628)

    def isEnd(self):
        # C1, C2, C3, and C4 are four feature points to identify whether the event is reversed. 
        # For different mobile phones, their positions are different and cannot be shared
        # Please choose the 4 feature points and change the color and position
        c1 = get_color(165, 2059)
        t1 = compcolor([32, 187, 211], c1) < 32
        c2 = get_color(632, 2056)
        t2 = compcolor([250, 78, 142], c2) < 32
        c3 = get_color(267, 2012)
        t3 = compcolor([255, 255, 255], c3) < 32
        c4 = get_color(818, 2037)
        t4 = compcolor([255, 255, 255], c4) < 32
        if t1 & t2 & t3 & t4:
            return True
        else:
            return False


def PAUSE(s):
    time.sleep(s)
def ADB(cmd):
    result = subprocess.Popen('adb\\adb.exe '+cmd,shell=True,stdout=subprocess.PIPE)
    out, err = result.communicate()
    return out.replace(b'\r\n', b'\n')
def TAP(x,y):
    ADB('shell input tap '+ str(x) +' '+str(y))
def CAP():
    global screenshot
    img = ADB('shell screencap -p')
    picture_stream = BytesIO(img)
    # Save the picture to memory to reduce disk load
    # screenshot = plt.imread(picture_stream)
    try:
       screenshot = plt.imread(picture_stream)
    except:
       print("cannot get screen information!")
    plt.ion()
    plt.clf()
    plt.imshow(screenshot)
    plt.axis('off')  
    plt.tight_layout(pad=0, h_pad=0, w_pad=0)
    plt.pause(0.01)

def cilp_screenshot(x,y,w,h):
    global screenshot
    return screenshot[y:y+h,x:x+w,0:3]

def SX_number_OCR(p):
    SX = [SX0,SX1,SX2,SX3,SX4,SX5,SX6,SX7,SX8,SX9]
    num = np.zeros((10,5))
    for n in range(0,10):
        ans = np.zeros(100 - 25)
        for i in range(0,100-25):
            A_gry = ( SX[n][:,:,0]+SX[n][:,:,1]+SX[n][:,:,2] )/3 > 0.95
            B_gry = ( p[:,i:i+25,0]+p[:,i:i+25,1]+p[:,i:i+25,2] )/3 >0.95
            ans[i] = np.sum(A_gry==B_gry)
        #print(n,ans)
        ii = 0
        while np.max(ans) > 830 and ii <4 :
            ii += 1
            num[n,0]=n
            num[n,ii]=np.argmax(ans)
            ans[np.argmax(ans)]=0
    num_arry = num[:,1:4].T.reshape(-1)
    SX_number=0
    last_max=0
    x=0
    while np.max(num_arry) > 0:
        SX_number += (np.argmax(num_arry)%10)*10**x
        x+=1
        last_max = np.max(num_arry)
        num_arry[np.argmax(num_arry)]=0
        while last_max-np.max(num_arry)<20 and last_max>0:
            last_max = np.max(num_arry)
            num_arry[np.argmax(num_arry)] = 0
    # print(SX_number)
    return int(SX_number)

def B_number_OCR(p):
    B = [B0,B1,B2,B3,B4,B5,B6,B7,B8,B9]
    num = np.zeros((10,5))
    for n in range(0,10):
        ans = np.zeros(170 - 45)
        A_0 = B[n][:, :, 0]
        A_1 = B[n][:, :, 1]
        for i in range(0,170-45):
            B_0 = p[:, i:i + 45, 0]
            B_1 = p[:, i:i + 45, 1]
            ans[i] = 50*(np.sum(A_0 + B_0 == 2)/np.sum(A_0) + np.sum(A_1 + B_1 == 2)/np.sum(A_1))
        # print(n,np.max(ans))
        ii = 0
        while np.max(ans) > 75 and ii < 4 :
            ii += 1
            num[n,0]=n
            num[n,ii]=np.argmax(ans)
            ans[np.argmax(ans)]=0
    num_arry = num[:,1:4].T.reshape(-1)
    SX_number=0
    last_max=0
    x=0
    while np.max(num_arry) > 0:
        SX_number += (np.argmax(num_arry)%10)*10**x
        x+=1
        last_max = np.max(num_arry)
        num_arry[np.argmax(num_arry)]=0
        while last_max-np.max(num_arry)<30 and last_max>0:
            last_max = np.max(num_arry)
            num_arry[np.argmax(num_arry)] = 0
    # print(SX_number)
    return int(SX_number)

def get_color(x,y):
    global screenshot
    R = int(screenshot[y, x, 0]*256)
    G = int(screenshot[y, x, 1]*256)
    B = int(screenshot[y, x, 2]*256)
    return [R,G,B]

def compcolor(c1,c2):
    R = abs(c1[0] - c2[0])
    G = abs(c1[1] - c2[1])
    B = abs(c1[2] - c2[2])
    return R+G+B

if __name__ == "__main__":
    print("This script works on phones with a 2340x1080 resolution and 76 pixels high bang, such as the Redmi Note 8 Pro.\nFor other mobile phones, please change the feature identification coordinates and color in the code by yourself.")
    print("If you don't know Python syntax and your phone doesn't meet the requirements, you can probably give up.\nBy：charlin55\n")
    input("Please enter any character and press Enter to continue...")
    print(str(ADB('version'), encoding="utf-8"))
    plt.rcParams['toolbar'] = 'None'
    fig = plt.figure(figsize=(2.6,5.63))
    fig.canvas.set_window_title('ウマ娘AutoScript')
    U = uma()
    S = state()
    U.Turns = int(input("Enter the Turns:"))
    print("\n===============\nShort:0\nMile:1\nMiddle:2\nLong:3\n===============")
    U.distance = int(input("Please enter distance type:"))
    U.get_target()
    while True:
        PAUSE(0.7)
        CAP()
        if S.isChoose2():
            S.toChoose2()
            continue
        elif S.isChoose3():
            S.toChoose3()
            continue
        elif S.isGoRace():
            U.add_Turns()
            S.toGoRace()
            continue

        elif S.isRace():
            U.add_Turns()
            S.toRace()
            continue

        elif S.isStartRace():
            S.toStartRace()
            continue

        elif S.isRaceSuccess():
            S.toRaceSuccess()
            continue

        elif S.isRaceFail():
            S.toRaceFail()
            break

        elif S.isMain():
            if U.Turns > 60 and U.Skill_num < 1:
                U.toLearnSkill()
                continue
            U.add_Turns()
            U.get_TL()
            U.get_YRK()
            U.get_SX()
            U.get_friend()
            U.get_health()
            U.show_info()
            if U.TiLi > 85:
                U.toTore()
                continue
            if not U.Health:
                U.toHospital()
                continue
            if U.Friend and U.YaRuKi < 4 and U.TiLi < 60:
                U.toGoOut()
                continue
            if U.Friend and U.Turns > 60 and U.TiLi < 50:
                U.toGoOut()
                continue
            if U.TiLi < 50:
                U.toRest()
                continue
            if U.YaRuKi < 4:
                U.toGoOut()
                continue
            # If everything is normal, go to training
            U.toTore()

        elif S.isInherit():
            S.toInherit()
            continue

        elif S.isEnd():
            print("Success!")
            break

        else:
            PAUSE(0.3)
            # TAP(750, 2200)
            # PAUSE(0.2)
            # TAP(537, 2188)
            # PAUSE(0.2)
            # TAP(537, 2090)
            # PAUSE(0.2)
            # TAP(756, 2039)
            # PAUSE(0.2)
