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
    print(Data[1:10])
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
screen = pygame.display.set_mode([1280,720],pygame.FULLSCREEN)
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
def mselect(songtitle):
    modes = ["Normal","HackedData","ExtremRAM","HistoDot"]
    fonts = []
    hfonts = []
    logo = pygame.image.load("MazicsLogoWhite.png")
    font = pygame.font.SysFont("Arial", 40)
    print(songtitle)
    song = font.render("track: "+songtitle.split("Music/")[1], True,[255,255,255])
    colors = [[255,255,255],
              [0,255,0],
              [255,0,0],
              [255,255,255]]
    for tid,typ in enumerate(modes):
        image = font.render(typ, True,colors[tid])
        fonts.append(image)
        image = font.render(typ, True,[255,255,0])
        hfonts.append(image)
    lactive = True
    Mode = None
    while lactive:
        pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lactive = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
            elif event.type == pygame.KEYDOWN:
                lactive = False
        # render logo
        screen.blit(logo,[20,20])
        screen.blit(song,[20,600])
        for fid,f in enumerate(fonts):
            mp = pygame.mouse.get_pos()
            rendered = False
            if mp[0] > 700 and mp[0] < 850:
                if mp[1] > 40+fid*50 and mp[1] < 80+fid*50:
                    screen.blit(hfonts[fid],[700,40+fid*50])
                    rendered = True
                    if pressed :
                        Mode = modes[fid]
            if not rendered:
                screen.blit(f,[700,40+fid*50])
        pygame.display.flip()
        if Mode is not None:
            print("STOP")
            lactive = False
    return Mode

pygame.display.set_caption("Mazics Visualiser Tool (external Version)")
pygame.mixer.music.load(Data[0])
Mode = mselect(Data[0])
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
            elif event.type == pygame.KEYDOWN:
                Aktiv = False
elif Mode == "HackedData":
    DisplayFont = []
    while Aktiv :
        screen.fill([0,0,0])
        cl.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Aktiv = False
            elif event.type == pygame.KEYDOWN:
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
        cl.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Aktiv = False
            elif event.type == pygame.KEYDOWN:
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
elif Mode == "HistoDot":
    history = []
    lowhistory = []
    avh = []
    hlen = 100
    cstp = 255/hlen
    Thikn = screen.get_width()/DataPoints
    while Aktiv:
        AktData = NextPack(Data)
        Sdata = ColorUp(AktData)
        screen.fill([0,0,0])
        cl.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Aktiv = False
            elif event.type == pygame.KEYDOWN:
                Aktiv = False
        Y = 0
        LY = 100000
        LX = 0
        for dpid, dp in enumerate(AktData):
            if dp > Y :
                Y = dp
                X = dpid* Thikn
            if dp <= LY :
                LY = dp
                LX = dpid
        pos = [X,Y]
        lpos = [LX,LY*10]
        history.append(pos)
        lowhistory.append((lpos))
        lp = []
        llp = []
        for hid,item in enumerate(history):
            if item[1] > 700 :
                item[1] = 700
            pygame.draw.rect(screen,[cstp*hid, 0, 0],[item[0]-4,item[1]-4,8,8])
            try:
                pygame.draw.line(screen,[cstp*hid, cstp*hid, cstp*hid],[item[0]-1,item[1]],lp,2)
            except:
                pass
            lp = [item[0],item[1]]
        for hid,item in enumerate(lowhistory):
            if item[1] > 700 :
                item[1] = 700
            pygame.draw.rect(screen,[0, 0, cstp*hid],[item[0]-2,item[1]-2,4,4])
            try:
                pygame.draw.line(screen,[cstp*hid, cstp*hid, cstp*hid],[item[0]-1,item[1]],llp)
            except:
                pass
            llp = [item[0],item[1]]
        avx = (llp[0] +lp[0]*2)/3
        avh.append([avx,Sdata[2]])
        avlp = []
        for hid,item in enumerate(avh):
            if item[1] > 700 :
                item[1] = 700
            pygame.draw.rect(screen,[0, cstp*hid, 0],[item[0]-2,item[1]-2,4,4])
            try:
                pygame.draw.line(screen,[cstp*hid, cstp*hid, cstp*hid],[item[0]-1,item[1]],avlp)
            except:
                pass
            avlp = [item[0],item[1]]
        if len(history) > hlen :
            history = history[1:]
        if len(avh) > hlen :
            avh = avh[1:]
        if len(lowhistory) > hlen:
            lowhistory = lowhistory[1:]
        pygame.display.flip()


pygame.quit()