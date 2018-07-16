import pickle,pygame,random,easygui
pygame.init()
#Def Def
def NextPack(Data):
    global FrameID
    FrameID += 1
    if FrameID > MaxFrameID :
        FrameID = 0
    return Data[FrameID]
def Unpack():
    File = open( "Saves/SaveFile.maz", "rb" )
    Data = pickle.load(File)
    File.close()
    return Data,len(Data)-2,len(Data[1])
def ColorUp(Data):
    B = 0
    Bpos = 0
    L = 10000
    Lpos = 0
    Av = 0
    Avmeng = 0
    for PosX,Item in enumerate(Data):
        if Item > B:
            B = Item
            Bpos = PosX
        if Item < L:
            L = Item
            Lpos = PosX
        Av += Item
        Avmeng += 1
    return [Bpos,Lpos,Av/Avmeng]
def GetColor(ID,InputData):
    if ID in InputData :
        if ID == InputData[0]:
            Color = LowColor
        elif ID == InputData[1]:
            Color = PeakColor
    else:
        Color = BaseColor
    return Color
def AddFeatures(Sdata):
    pygame.draw.line(screen,AvColor,[0,Sdata[2]],[screen.get_width(),Sdata[2]],1)
def Render(Data):
    B = 0
    Thikn = screen.get_width()/DataPoints
    Ycap = screen.get_height()-20
    Sdata = ColorUp(Data)
    for PosX,Item in enumerate(Data):
        Color = GetColor(PosX,Sdata)
        if Item >= Ycap :
            Item = Ycap
        if Item > B :
            B = Item
        pygame.draw.rect(screen,Color,[PosX*Thikn,0,Thikn-1,int(Item)])
    AddFeatures(Sdata)
# Var Def
# Colors
BackgroundColor = [0,0,0]
BaseColor = [255,255,255]
LowColor = [255,0,0]
PeakColor = [0,0,255]
AvColor = [0,255,0]
# AnimPlayer
FrameID = 0
MaxFrameID = 0
screen = pygame.display.set_mode([1280,720])
# Render Mode
RenderBars = True
RenderAv = True
RenderGraph = 0
# MainLoop Vars
Aktiv = True
# MainLoop Stup
Data,MaxFrameID,DataPoints = Unpack()
# MainLoop
cl = pygame.time.Clock()
#Music
pygame.display.set_caption("Mazics Visualiser Tool (external Version)")
Mode = easygui.choicebox("Display Mode:","Choose View Mode",["Normal","HackedData","ExtremRAM"])
pygame.mixer.music.load(Data[0])
Data = Data[1:]
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)
if Mode == "Normal":
    while Aktiv:
        cl.tick(10)
        # Reset
        screen.fill(BackgroundColor)
        # Render
        Render(NextPack(Data))
        # Reload screen
        pygame.display.flip()
        # eventhandler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Aktiv = False
elif Mode == "HackedData":
    DisplayFont = []
    while Aktiv :
        screen.fill([0,0,0])
        cl.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Aktiv = False
        font = pygame.font.SysFont("Arial",20)
        DataText = DataPoints
        AktData = NextPack(Data)
        AktData2 = []
        for Item in AktData :
            AktData2.append(int(Item))
        DisplayFont.append(font.render(str(AktData2), True,[0,255,0]))
        if len(DisplayFont) > 35:
            DisplayFont = DisplayFont[1:]
        for Enu,Obj in enumerate(DisplayFont) :
            screen.blit(Obj,[0,Enu*20])
        pygame.display.flip()
elif Mode == "ExtremRAM" :
    for ID in range(0,len(Data[0])):
        exec("DataBit"+str(ID)+" = []")
    while Aktiv :
        screen.fill([0,0,0])
        #cl.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Aktiv = False
        AktData = NextPack(Data)
        for ID,Item in enumerate(AktData) :
            Db = eval("DataBit"+str(ID))
            Db.append([-10,Item])
            if len(Db) > 128:
                exec("DataBit"+str(ID)+" = Db[1:]")
            for Item in Db :
                Item[0] += 10
            try :
                pygame.draw.lines(screen,[ID,ID,ID],False,Db,2)
            except :
                pass
        pygame.display.flip()

pygame.quit()