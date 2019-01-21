####################################################################################################################
# Project: Yaks vs Yetis
# Last Revision date: Jan. 2018
# Group members: Daniel, Athena, Sean, Jerry
# Description: Play it and find out :). Essentially a unique recreation of the popular plants vs zombies mobile game.
####################################################################################################################
#dependencies
import ctypes
import pygame
import random
from threading import Timer
import pickle
import sys
import math
#setup pygame
pygame.init()
ctypes.windll.user32.SetProcessDPIAware()  # without this, fullscreen window is way too large as it ignored dpi
true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
gameDisplay = pygame.display.set_mode(true_res, pygame.FULLSCREEN)
pygame.display.set_caption('Yaks vs Yetis')#game title
pygame.display.set_icon(pygame.image.load("logo.png"))#game icon
clock = pygame.time.Clock()#to be used later for fps

# Globals (default values)
#the story array, contains the story per level
levelStory = ["The struggle begins: Since the great Himalayan war the region had enjoyed relative peace.\nThis all ended on September first with the invasion of the mountain goat territory which lay between the Yak and Yeti territory by the Yak empire.\nThrough defensive alliances and rising tensions, the Himalayan musk deer and the Himalayan Wolf were forced to declare war on the Yaks as they couldn’t allow such aggression.\nAfter the quick capitulation of the Mountain goats, the Yak prepared for their offensive against the musk deer.\nThe Yeti had declared neutrality in these events hoping to avoid the violence which was respected by the Yak as they believed they’d be stuck in a long drawn out conflict with the deer as they had in the great Himalayan war.\nWhen the Yak launched their attack they were able to outmaneuver and encircle the Deer armies forcing their capitulation.\nThe once great Deer republic had fallen to the Yak empire in a matter of weeks with little casualties.\nUnable to attack the wolf coalition as it was in a far-off land the Yak prepared for their largest operation yet.\nThis resulted in ending the Yeti’s neutrality on June 22nd, when the Yaks launched their full fletched invasion of the Yeti commune.\nThey were able to detect the weakness of the Yeti as the Yeti had struggled in the warmer years which had passed.\nTheir mutual food source, grasses, herbs, wildflowers, mosses, tubers (root or underground stems), and lichens (fungus), was dwindling and led the Yak to conclude that the Yeti must be crushed.\nThough it ultimately comes down to the Yak’s bloodlust.\nIt is their ultimate goal to eliminate the Yeti from the Himalayan region.\nIt is up to the Yeti to stop the Yak onslaught for the good of all who appreciate peace and the sake of the entire Himalayan region.\nYou are the Captain of the Infantry company 103 serving in the Northern portion of the border",
              "The retreat: Even though the Yeti are fighting valiantly you’ve been forced to make a tactical withdrawal into your territory.\nNo Yeti forces have been routed as order has been kept.\nThrough the courageous fighting of you and your men, the Yaks have not been making the progress they had hoped for.\nThey are going to have to dedicate more and more of their elite forces to crush you and your heroic unit.\nMeanwhile, across the territory, the Wolves are re-arming and readying themselves to fight the Yak.\nIt’s vital that the Yaks are stalled long enough and dedicate enough of the troops to the Yeti front that the Wolves will be able to attack.\n",
              "Frustration: It seems the waves of Yak will never end.\nThough moral is running high in the Yeti there are the beginnings of a sense of impending doom.\nWith each day we are able to invest more funds and mobilize more troops.\nThe wolves have informed us that they will be unable to stage an offensive for a long time as they had not been ready for the war that we find ourselves in.\nMeanwhile, it is clear that the Yak require a quicker victory over our people as they are being slowly drained of their resources.\n",
              "The Lost Battalion: Your forces have been encircled! Due to the quick maneuvers of the Yaks, they have been able to surround the entire battalion.\nIn order to offer a chance of escape, you and your men have to offer rear support as the rest of the formation makes a push for freedom.\nWithstand the imminent onslaught so your forces can punch a hole to liberate your whole battalion.\n",
              "Breakthrough: A hole in the lines! Now’s your chance.\nAs you and your men are escaping the Yak have begun a counterattack to re-surround you.\nIf you fail to beat off this assault you’ll surely be destroyed.\nThe fate of you and your men has come down to this escape.\nYou’ve never seen your men more determined and it all comes down to this.\n",
              "The Winter: With the realization that winter is coming the Yaks will be redoubling their efforts to capture force our capitulation before their advance must be halted in the aggressive Himalayan winter.\nThey’ve already penetrated more than 100 kilometers deep into of our territory.\nThough they have captured much of our land their advance has begun to stall.\nTheir oil reserves are running low and they’ve gone so deep that their logistics are beginning to fail.\nThey are slowly beginning to dwindle on the resources they need to continue their advance.\n",
              "Order 227: To regain order in the army the an order has been issued by high command. Order 227 outlines that we must not take one step back. We must now hold our ground and failure is unacceptable. If you fail it means nothing less than full annihilation of you and your men. This will be the toughest resistance yet and you’ll have to withstand the full might of the Yak army.",
              "The struggle intensifies: The Yaks assault is only getting more intense as they know this is our last stand. Their most elite units are being dedicated to their effort to crack us in our last stand. If we lose now we will not have the time to reinforce our defense. Your men fight with vigor as they are enthused by giving their last stand. They will fight to the end to save the people and homeland they love.",
              "A Second Front: From across the Himalayas the Wolves are ready to begin their offensive. They will bring the fight to Yak occupied Himalaya and greatly aid our war effort. With the offensive to the west, the Yak’s will have to move many of their divisions to defend leaving them to fight with less in the East. Their resources are also dwindling heavily so they have issues moving equipment to the front. We have gained the advantage as long as they cannot break us now so they’ll fight now as if it’s their last chance for victory in the East.",
              "Fanatical attack: The wolves have landed in Yak occupied territory. If they beat us here in the East the Yaks will be able to make our great nation capitulate and move their units to the west to similarity defeat the wolves. They will attack with a ferocity as this is it. We will be able to stop their advance completely and wait until an offensive can be formed. The war can be won here and now. Fight for all that matters, peace, honour, and freedom."
              ]
#used by game to scale to different screens
SCREEN_HEIGHT = true_res[1]
SCREEN_WIDTH = true_res[0]
LANE_WIDTH = int(round(SCREEN_WIDTH / 8))
LANE_HEIGHT = int(round(SCREEN_HEIGHT / 6))
#empty arrays that will contain the game elemements
yaks = [[], [], [], [], [], []]
yetis = 6*[[]*8]#[[None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None],[None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
startingScore = 0 #reset score


# updates the globals to be used later
# @param w -> screen width
# @param h -> screen height
def updateGlobals(w, h, display, loose, level):
    global SCREEN_HEIGHT, SCREEN_WIDTH, LANE_HEIGHT, LANE_WIDTH, yaks, startingScore
    SCREEN_WIDTH = w
    SCREEN_HEIGHT = h
    LANE_WIDTH =  int(w / 7)
    LANE_HEIGHT = int(h / 7)
    yaks = [[], [], [], [], [], [], []]
    if level == 0:
        yaks = createYaks(display, loose, 20, 1, 0, 0)  # starting points: 75  YAK: 20x white, 1x Brown
        startingScore = 75
    elif level == 1:
        yaks = createYaks(display, loose, 20, 5, 0, 0)  # starting points: 125 YAK: 20x white, 5x Brown
        startingScore = 125
    elif level == 2:
        yaks = createYaks(display, loose, 15, 10, 0, 0)  # starting points: 150 YAK: 15x white, 10x Brown
        startingScore = 150
    elif level == 3:
        yaks = createYaks(display, loose, 15, 15, 0, 0)  # starting points: 175 YAK: 15x white, 15x Brown
        startingScore = 175
    elif level == 4:
        yaks = createYaks(display, loose, 15, 8, 2, 0)  # starting points: 225 YAK: 15x white, 8x Brown, 2xBlack
        startingScore = 225
    elif level == 5:
        yaks = createYaks(display, loose, 10, 15, 4, 0)  # starting points: 250 YAK: 10x White, 15x Brown, 4x Black
        startingScore = 250
    elif level == 6:
        yaks = createYaks(display, loose, 0, 20, 6, 0)  # starting points: 275 YAK: 20x Brown, 6x Black
        startingScore = 275
    elif level == 7:
        yaks = createYaks(display, loose, 0, 15, 8, 2)  # starting points: 325 YAK: 15x Brown, 8x Black, 2x Red
        startingScore = 325
    elif level == 8:
        yaks = createYaks(display, loose, 0, 10, 10, 5)  # starting points: 375 YAK: 10x Brown, 10x Black, 5x Red
        startingScore = 375
    elif level == 9:
        yaks = createYaks(display, loose, 0, 10, 20, 10)  # starting points: 450 YAK: 10x Brown, 20x Black, 10x Red
        startingScore = 450

#creates the yaks and randomly places, prepares and organizes them into their arrays
#@param display -> pygame display
#@param loose -> function to call once a yak reaches the end of the board and the player looses
#@param amountWhite -> amount of white yaks to create
#@param amountBrown -> amount of brown yaks to create
#@param amountBlack -> amount of black yaks to create
#@param amountRed -> amount of red yaks to create
def createYaks(display, loose, amountWhite, amountBrown, amountBlack,amountRed):
    arr = [[], [], [], [], [], []]
    delay = 0
    #loop through and create them
    #row = the row to place the yak in
    #delay, the delay after which the yak will start attacking (space between yaks)
    for yak in range(amountWhite):
        row = random.randint(0, 5)
        delay += random.randint(1000, 4000)
        arr[row].append(whiteYak(display, (SCREEN_WIDTH + 1, (row + 1) * LANE_HEIGHT), delay, loose))

    for yak in range(amountBrown):
        row = random.randint(0, 5)
        delay += random.randint(1000, 4000)
        arr[row].append(brownYak(display, (SCREEN_WIDTH + 1, (row + 1) * LANE_HEIGHT), delay, loose))

    for yak in range(amountBlack):
        row = random.randint(0, 5)
        delay += random.randint(1000, 4000)
        arr[row].append(blackYak(display, (SCREEN_WIDTH + 1, (row + 1) * LANE_HEIGHT), delay, loose))

    for yak in range(amountRed):
        row = random.randint(0, 5)
        delay += random.randint(1000, 4000)
        arr[row].append(redYak(display, (SCREEN_WIDTH + 1, (row + 1) * LANE_HEIGHT), delay, loose))
    return arr

#main screen for game
class UI(pygame.sprite.Sprite):
    # sets up the ui and game
    # @param display -> where to blit to
    # @param restorePreviousGame -> should load previous game
    # @param level -> what level to load
    def __init__(self, display, restorePreviousGame, level,transition):
        global yaks, yetis
        yetis = [[None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]] #reset yetis
        updateGlobals(display.get_width(), display.get_height(), display, self.loose,int(level))  # update the globals to be used later

        pygame.sprite.Sprite.__init__(self)
        # load and show background
        self.image = pygame.image.load("background2.png")
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.display = display

        pygame.mixer.Channel(0).play(pygame.mixer.Sound('gameMusic.ogg'), -1)

        # create variables and start logic
        self.clickedOnYeti = False  # is a yeti currently being dragged
        self.yetiClicked = None  # current yeti being dragged
        self.scoreMonitor = self.ScoreMonitor(
            display)  # this will be used to manage the score-related aspects of the game (score, falling snowflakes, etc.)
        self.clock = pygame.time.Clock()  # used to time the game
        self.controls = self.Controls(self.display, self.toTitle,transition)  # will be used to create new yetis, toggle pause and other control-based aspects of the game

        self.transition = transition

        # load previous game
        self.saver = self.Saver()
        if restorePreviousGame:
            loadedData = self.saver.load(display, self.loose)
            self.scoreMonitor.updateScore(loadedData[1])
            yetis = loadedData[0]
            self.level = loadedData[2]
            yaks = loadedData[3]
        else:
            self.scoreMonitor.updateScore(startingScore)  # get the starting score
            self.level = level  # stores the current level

        # start the game
        self.crashed = False

        self.mainLoop()

    # save progress and bring player back to title from the game
    #@param transition -> transition to use between screens
    def toTitle(self,transition):
        transition.fadeOutAuto()
        pygame.mixer.music.stop()
        self.saver.save(self.scoreMonitor.score, self.level)
        self.crashed = True
        Title(self.transition)

    # main update/render loop
    def mainLoop(self):
        while not self.crashed:
            self.clock.tick(30)  # makes game run at 30 frames per second

            for event in pygame.event.get():  # check for user input
                if event.type == pygame.QUIT:
                    self.crashed = True
                    self.saveAndExit()  # if exiting, save current game
                else:
                    self.processEvent(event)  # process user input

            self.render()  # render the game
            self.transition.fadeIn()
            pygame.display.flip()  # update the entire display

    # save and exit game
    def saveAndExit(self):
        pygame.mixer.music.stop()
        self.saver.save(self.scoreMonitor.score, self.level)
        pygame.quit()
        sys.exit()

    # yak reaches the left side of the screen, player looses
    def loose(self):
        if self.controls.pause.hasWon is None:
            self.controls.pause.hasWon = False

    # all yaks are dead this level was won
    def win(self):
        if self.controls.pause.hasWon is None:
            self.controls.pause.hasWon = True
            #save and unlock next level
            try:
                pkl_file = open('levels.pkl', 'rb')
                arr = pickle.load(pkl_file)
                level = arr["level"]  # get the highest unlocked level
                pkl_file.close()
            except:
                level = 1

            if int(self.level)+1 == int(level):  # make sure we aren't loosing access to levels if we go back to a previous one
                output = open('levels.pkl', 'wb')  # save that
                pickle.dump({"level": int(level) + 1}, output)  # save it
                output.close()  # close file

    # proceses events and calls their respective actons
    # @param event -> the user input to process
    def processEvent(self, event):
        # process mouse events
        #clamp mouse coords to screen
        x = max(min(pygame.mouse.get_pos()[0],SCREEN_WIDTH-LANE_WIDTH),0)
        y = max(min(pygame.mouse.get_pos()[1], SCREEN_HEIGHT-LANE_HEIGHT), 0)
        if event.type == pygame.MOUSEBUTTONDOWN:  # if clicked down on mouse
            self.yetiClicked = self.controls.isClickOnItem((x,y))
            if self.yetiClicked[0]:  # check if above a listItem (if yes, buy it)
                if not self.scoreMonitor.updateScore(-self.yetiClicked[1].price):  # if not enough funds don't buy
                    self.controls.messageView.showMessage("Not enough funds!")
                    self.yetiClicked = None
                    return
                self.yetiClicked[1].createYeti([x,y], self.yetiClicked[1].price)  # if can buy, then buy and start the dragging/placing
                self.yetiClicked[1].yeti.moveable = True

            elif self.scoreMonitor.snowflake is not None and self.scoreMonitor.snowflake.isClicked():  # if not above a listItem, check if clicking on a snowflake
                self.scoreMonitor.updateScore(25)  # if yes, update the score
                self.scoreMonitor.snowflake.collected = True

        elif event.type == pygame.MOUSEMOTION and self.yetiClicked is not None and self.yetiClicked[0] and self.yetiClicked[1].yeti.moveable:  # check if dragging a yeti
            self.yetiClicked[1].yeti.moveTo(self.snapMousePos(x,y))  # if yes, move the yeti to the closest possible location, to the mouse, on the board

        elif event.type == pygame.MOUSEBUTTONUP and self.yetiClicked is not None and self.yetiClicked[1] is not None:  # check if placing a yeti
            if not self.yetiAlreadyThere(x,y) and self.snapMousePos(x,y)[1] != 0:  # if not placing over the control panel or above another yeti, then place it
                self.yetiClicked[1].yeti.moveTo(self.snapMousePos(x, y))
                self.yetiClicked[1].yeti.placeYeti()  # place yeti

                yetis[round(y / LANE_HEIGHT)-1][round(x / LANE_WIDTH)] = self.yetiClicked[1].yeti

            else:  # otherwise, show an error message and refund the player
                self.controls.messageView.showMessage("Can't place yeti here!")
                self.scoreMonitor.updateScore(self.yetiClicked[1].price)  # if yeti already there, reimburse the player

            # regardless of previous events, clear the following variables to allow for interacting with new ones
            self.yetiClicked[1].yeti = None
            self.yetiClicked = None

        # check if pause clicked (p button)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.controls.pause.togglePause()  # if yes, toggle pause

    # helper method to determine if a yeti is below mouse
    @staticmethod
    def yetiAlreadyThere(x2,y2):
        y = round(y2 / LANE_HEIGHT)-1
        x = round(x2 / LANE_WIDTH)
        if -1 < y < 6 and -1 < x < 7:
            canPlace = yetis[y][x] is not None
            return canPlace
        return False

    # helper method to "Snap" the mouseposition to the nearest tile (defined by LANE_WIDTH x LANE_HEIGHT)
    @staticmethod
    def snapMousePos(x,y):
        mouseLocX = int(round(x / LANE_WIDTH) * LANE_WIDTH)  # round to nearest possible position (screen width/7)
        mouseLocY = int(round(y / LANE_HEIGHT) * LANE_HEIGHT)  # round to nearest possible position (screen height/7)
        return mouseLocX, mouseLocY

    # main render method. This one calls all the individual ones from the other classes
    def render(self):
        self.display.blit(self.image, self.rect)  # clear screen

        if not self.controls.pause.isPaused:  # check if paused, if yes then we don't need to move the yetis and yaks around the screen
            self.scoreMonitor.update()

            # loop though the rows and update everything in them
            for row in range(6):
                for yak in yaks[row]:
                    yak.update()
                for yeti in yetis[row]:
                    if yeti is not None:#is a yetis is actually there
                        yeti.update()

            #check if all yaks are dead, if so player wins
            if yaks == [[], [], [], [], [], []]:
                self.win()

            # update the yeti that you are currently dragging if you are dragging it
            if self.yetiClicked is not None and self.yetiClicked[0]:
                self.yetiClicked[1].yeti.update()

        self.controls.update(self.display)  # update controls

    # this class is responsible for monitoring the ingame controls (pause, the listItems, error messages, etc.)
    class Controls(pygame.sprite.Sprite):
        # init the class and create necessary variables
        def __init__(self, display, toTitle,transition):
            pygame.sprite.Sprite.__init__(self)
            # load the background image of the control panel
            self.rect = pygame.Rect(25, LANE_HEIGHT / 2, 550, 125)
            self.rect[1] = 0
            self.rect[0] = 15  # adjust it's location
            # create variables to use later
            self.messageView = self.UIMessage(display)
            self.pause = self.Dialog(display, toTitle,transition)
            # create array of listeitems that will allow player to buy yetis
            self.items = [self.listItem((self.rect[0] + 100, self.rect[1] + 35), "yetis/blue_yeti1_4.png", display, 25),
                          self.listItem((self.rect[0] + 200, self.rect[1] + 35), "yetis/orange_yeti1_4.png", display,
                                        70),
                          self.listItem((self.rect[0] + 300, self.rect[1] + 35), "yetis/pink_yeti1_4.png", display,
                                        100)]

        # controls update function
        # @param *args -> ignored
        def update(self, *args):
            for index in range(len(self.items)):  # lop through the listItems and update them
                args[0].blit(self.items[index].image, self.items[index].rect)
                args[0].blit(self.items[index].text, self.items[index].textRect)

            self.pause.update()  # update the pause menu (does nothing if not paused. the logic is handled in the class)

            self.messageView.update()  # update the messages (does nothing if not shown. the logic is handled in the class)

        # helper function to detect if mouse is clicking on a listItem
        def isClickOnItem(self,coords):
            for index in range(len(self.items)):  # loop through the listItems and compare their rects which contain x,y and width,height
                if self.items[index].rect.collidepoint(coords):
                    return [True, self.items[index]]
            return [False, None]

        # Used to display entries in the control panel
        class listItem(pygame.sprite.Sprite):
            # init the listItem and setup variables
            # @param location -> where to create this item
            # @param img -> the yeti
            # @param display -> where to blit to
            # @param price -> cost of buying such yeti
            def __init__(self, location, img, display, price):
                pygame.sprite.Sprite.__init__(self)
                # setup the image (load, resize and position it)
                self.img = img
                self.image = pygame.image.load(img)
                self.image = pygame.transform.scale(self.image, (int(LANE_HEIGHT / 2 + 25), int(LANE_HEIGHT / 2 + 25)))  # resize to make smaller
                self.rect = self.image.get_rect()
                self.rect[0] = location[0]
                self.rect[1] = location[1]
                self.font = pygame.font.Font("font.ttf", 15)
                self.text = self.font.render("$"+str(price), True, (255, 255, 255))
                self.textRect = self.text.get_rect()
                self.textRect[0] = location[0]
                self.textRect[1] = location[1]

                # create varaiables to use later
                self.display = display  # were to blit to
                self.yeti = None  # the target yeti to create on buy
                self.price = price  # cost of the yeti

            # when yeti is placed this is called, it creates a yeti at the proper location
            # @param pos -> position to create yeti at
            # @param price -> used to determine which yeti to create
            # @param yetis -> parent array of all yetis, used to remove yetui once it dies
            def createYeti(self, pos, price):
                if price == 25:
                    self.yeti = Phil(self.display, [pos[0], pos[1]])
                elif price == 70:
                    self.yeti = Dave(self.display, [pos[0], pos[1]])
                else:
                    self.yeti = Bob(self.display, [pos[0], pos[1]])

        # used to display a message to the user
        class UIMessage(pygame.sprite.Sprite):
            # create the view
            # @param display -> where to blit to
            def __init__(self, display):
                pygame.sprite.Sprite.__init__(self)
                # create the variables needed
                self.display = display
                self.font = pygame.font.Font("font.ttf", 52)
                self.text = self.font.render("", True, (0, 0, 0))
                self.duration = 2000
                self.startTime = 0

            # show the user a message
            # @param message -> message to show the user
            def showMessage(self, message):
                self.text = self.font.render(str(message), True, (0, 0, 0), (255, 255, 255))
                self.startTime = pygame.time.get_ticks()

            # if should show, show (defined as if shown for less then max time)
            def update(self, *args):
                if pygame.time.get_ticks() - self.startTime <= self.duration:
                    self.display.blit(self.text, (15, 125))

        # used for pause and eventually win/lose dialogs
        class Dialog(pygame.sprite.Sprite):
            # init and create the variables/pre-setup the background and texts
            def __init__(self, display, goToTitle,transition):
                pygame.sprite.Sprite.__init__(self)
                self.display = display
                # setup text
                self.font = pygame.font.Font("font.ttf", 52)
                self.text = self.font.render("", True, (0, 0, 0))
                # setup background
                self.background = pygame.image.load("DialogBackground.png")
                self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                # setup variables
                self.isPaused = False
                self.textRect = [0, 0, 0, 0]
                self.transition = transition
                # winningloosing variables
                self.hasWon = None

                self.exitButton = Button("Exit", (SCREEN_WIDTH / 2 - 10, SCREEN_HEIGHT / 2 + 256), (255, 255, 255), True, goToTitle)

                # winning & loosing
                self.endImg = pygame.image.load("Victory.png")
                self.endImgRect = self.endImg.get_rect()
                mult = (SCREEN_HEIGHT - 20) / self.endImgRect[3]
                self.endImg = pygame.transform.scale(self.endImg, (int(self.endImgRect[2] * mult), int(self.endImgRect[3] * mult)))
                self.endImgRect = self.endImg.get_rect()

            # toggles pause
            def togglePause(self):
                self.isPaused = not self.isPaused  # toggle varaibles
                if self.isPaused:  # if paused render the paused stuff
                    self.display.blit(self.background, (0, 0))
                    self.text = self.font.render("Press p again to resume onslaught!", True, (0, 0, 0), (255, 255, 255))
                    self.textRect = self.text.get_rect()

            # if paused, update screen to maintain the pause screen visible
            def update(self, *args):
                if self.isPaused:
                    self.display.blit(self.background, (0, 0))
                    self.display.blit(self.text, (SCREEN_WIDTH / 2 - (self.textRect[2] / 2), (SCREEN_HEIGHT / 2 - self.textRect[3] / 2)))
                    self.exitButton.update()

                    for event in pygame.event.get():  # check for user input
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.exitButton.isClicked(gameDisplay,self.transition)
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                            self.isPaused = False

                elif self.hasWon is not None:
                    if not self.hasWon:  # player looses, show loosing message
                        self.endImg = pygame.image.load("Defeat.png")
                        self.endImgRect = self.endImg.get_rect()
                        mult = (SCREEN_HEIGHT - 20) / self.endImgRect[3]
                        self.endImg = pygame.transform.scale(self.endImg, (int(self.endImgRect[2] * mult), int(self.endImgRect[3] * mult)))
                        self.endImgRect = self.endImg.get_rect()
                    # show the message
                    self.display.blit(self.endImg, (SCREEN_WIDTH / 2 - self.endImgRect[2]/2, 10))
                    self.exitButton.update()
                    for event in pygame.event.get():  # check for user input
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.exitButton.isClicked(gameDisplay,self.transition)

    # this class monitors all things related to the score (score variables, text, and the snowflakes)
    class ScoreMonitor(pygame.sprite.Sprite):
        # init function that sets up the variable and pre-setsup the
        def __init__(self, display):
            pygame.sprite.Sprite.__init__(self)
            self.rect = pygame.Rect(SCREEN_WIDTH / 2, 50, 100, 100)
            self.display = display
            self.score = 0
            self.snowflake = self.Snowflake(display, random.randint(25,
                                                                    SCREEN_WIDTH - 25))  # create the snowflake that will fall form sky and give points to player
            self.font = pygame.font.Font("font.ttf", 52)
            self.text = self.font.render("$0", True, (255, 255, 255))

        # updates the score variable and updates the text
        # @param score -> by how much should the score be incremented
        def updateScore(self, score):
            newScore = self.score + score
            if newScore < 0:  # if result of adding the score is less than 0, fail the purchase (can't happen when collecting snowflakes)
                return False
            # if purchase not failed, or snowflake collected, actually update the score and the text
            self.score = newScore
            self.text = self.font.render("$" + str(self.score), True, (255, 255, 255))
            self.display.blit(self.text, (self.rect[0], self.rect[1]))
            return True

        # show text and update the snowflak (make it fall)
        def update(self, *args):
            self.snowflake.update()
            self.display.blit(self.text, (self.rect[0], self.rect[1]))

        # this class handles the snowflakes
        class Snowflake(pygame.sprite.Sprite):
            # create the snowflake and it's proper variables
            def __init__(self, display, xLoc):
                pygame.sprite.Sprite.__init__(self)
                # setup the image and position it
                self.img = "snowflake.png"
                self.image = pygame.image.load(self.img)  # resize to make smaller
                self.image = pygame.transform.scale(self.image, (40, 40))
                self.rect = self.image.get_rect()
                self.rect[0] = xLoc
                self.rect[1] = 0
                # setup variables for later
                self.display = display
                self.collected = False  # has the snowflake been clicked on by the user
                self.ready = True  # is the snowflake ready to fall again

            # this is a helper function that resets the snowflake after being collected or falling to the ground
            def setup(self):
                self.rect[0] = random.randint(125, SCREEN_WIDTH - 125)
                self.collected = False
                self.ready = True

            # control the snowflake and show it on screen
            def update(self, *args):
                if (self.rect[
                        1] >= SCREEN_HEIGHT or self.collected) and self.ready:  # if collected, or hit ground, and is ready to fall again
                    # reset core variables to prevent it from being shown on screen
                    self.ready = False
                    self.collected = True
                    self.rect[1] = 0  # so can't click on snowflake again until it falls
                    Timer(3.0, self.setup).start()  # start a timer after which the snowflake will fall again

                elif not self.collected:  # otherwise if not collected, move it down 5 px every frame
                    self.rect[1] += 5
                    self.display.blit(self.image, self.rect)

            # helper function that compares if mouse if clicking on a snowflake
            def isClicked(self):
                mousePos = pygame.mouse.get_pos()
                # checks if mouse x position is within the bounds of the rect. Same with the y
                return (self.rect[0] <= mousePos[0] <= (self.rect[0] + self.rect[2])) and (
                            self.rect[1] <= mousePos[1] <= (self.rect[1] + self.rect[3]))

    # helper class used to save and load the game
    class Saver:
        # save the game
        def save(self, score, level):
            output = open('gameSave.pkl', 'wb')  # save in gameSave.pkl
            pickle.dump({"score": score, "yetis": self.getYetiArray(), "level": level, "yaks": self.getYakArray()},
                        output)  # save it
            output.close()  # close file

        # helper function to filter out array with only valuable parts of the yeti (contained in yeti.save)
        @staticmethod
        def getYetiArray():
            arr = [[None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
            index = 0
            column = 0
            for yetiRow in yetis:  # loop through al yetis and append the save function values to a new array
                for yeti in yetiRow:
                    if yeti is not None:
                        arr[index][column] = yeti.save()
                    column +=1
                index += 1
                column = 0
            return arr  # reutrn the new array

        # helper function to filter out array with only valuable parts of the yeti (contained in yak.save)
        @staticmethod
        def getYakArray():
            arr = [[], [], [], [], [], [], []]
            index = 0
            for yakRow in yaks:  # loop through al yetis and append the save function values to a new array
                for yak in yakRow:
                    arr[index].append(yak.save())
                index += 1
            return arr  # reutrn the new array

        # loads the previous game
        @staticmethod
        def load(display, loose):
            # loop the whole thing in a try-except block to catch all errors in the process (i.e. game hasn't been saved before, file is corrupt, file is missing things, etc)
            try:
                pkl_file = open('gameSave.pkl', 'rb')
                arr = pickle.load(pkl_file)  # load from gameSave.pkl into a dictionary
                score = arr["score"]  # get the score
                yetisRaw = arr["yetis"]  # get the yetis important values (this does not return actual yeti objects)
                yaksRaw = arr["yaks"]  # get the yak important values (this does not return actual yak objects)
                level = arr["level"]  # get the previously saved level
                pkl_file.close()  # close file
                yetis = [[None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None]]
                yaksArr = [[], [], [], [], [], [], []]  # create an array to contain actaul yak objects
                index = 0
                column = 0
                for yetiRow in yetisRaw:  # loop through all yeti data and create actual yetis from it
                    for yeti in yetiRow:
                        if yeti is None:
                            continue
                        if yeti[2] == 0:
                            yetis[index][column] = (Phil(display, yeti[0], yeti[1]))
                        elif yeti[2] == 1:
                            yetis[index][column] = (Dave(display, yeti[0], yeti[1]))
                        elif yeti[2] == 2:
                            yetis[index][column] = (Bob(display, yeti[0], yeti[1]))
                        column += 1
                    index += 1
                    column = 0
                index = 0
                for yakRow in yaksRaw:  # loop through all yeti data and create actual yetis from it
                    for yak in yakRow:
                        if yak[3] == 0:
                            yaksArr[index].append(whiteYak(display, yak[0], yak[2], loose, yak[1]))
                        elif yak[3] == 1:
                            yaksArr[index].append(brownYak(display, yak[0], yak[2], loose, yak[1]))
                        elif yak[3] == 2:
                            yaksArr[index].append(blackYak(display, yak[0], yak[2], loose, yak[1]))
                        elif yak[3] == 3:
                            yaksArr[index].append(redYak(display, yak[0], yak[2], loose, yak[1]))
                    index += 1
            except FileNotFoundError:  # if an error occurs, load as if no previously saved data
                score = 0
                yetis = [[None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None]]
                level = 0
                yaksArr = [[], [], [], [], [], []]

            # just in case something slips through (i.e. a value is missing in the file), set it to default values
            if score is None:
                score = 0
            if yetis is None:
                yetis = [[None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None]]
            if yaksArr is None:
                yaksArr = [[], [], [], [], [], [], []]
            if level is None:
                level = 0

            return yetis, score, level, yaksArr  # return the loaded information


# YETIS-----------------------------------------------------------------------------------------------------------------------------------

class Yeti(pygame.sprite.Sprite):

    # this is used to create the yeti
    # @param: self -> instance of a class
    # @param display -> display
    # @param: pos -> position of sprite
    # @param: hp -> health points
    # @param: dmg -> damage points
    # @param: img -> image of yeti
    # @param: moveable -> condition of yeti (moveable or not)
    def __init__(self, display, pos, hp, dmg, imgs, moveable, type):
        pygame.sprite.Sprite.__init__(self)
        self.yetiimgs = imgs
        self.framenumber = 0
        self.display = display
        self.rect = self.yetiimgs[0][0].get_rect()
        self.rect[0] = pos[0]
        self.rect[1] = pos[1]
        self.hp = hp
        self.originalHP = hp
        self.dmg = dmg
        self.moveable = moveable
        self.weaponPos = pos
        self.weapon = None
        self.startTime = pygame.time.get_ticks()
        self.type = type
        self.throwing = True

    # update the position of Yeti
    # @param: update the instance (self) of the class
    def update(self):
        if self.throwing:
            self.framenumber += 0.3
            if self.framenumber >= 3:
                self.framenumber = 0
                self.throwing = False

        if self.weapon is not None:
            self.weapon.defend()

        elif pygame.time.get_ticks() - self.startTime >= 2000 and self.weapon is None and len(yaks[int(self.rect[1] / LANE_HEIGHT)-1]) > 0:
            self.placeYeti()
            self.startTime = pygame.time.get_ticks()
            self.throwing = True
            self.framenumber = 1

        if self.hp >= self.originalHP:
            self.display.blit(self.yetiimgs[0][int(self.framenumber)], self.rect)

        elif self.hp >= self.originalHP / 4 * 3:
            self.display.blit(self.yetiimgs[1][int(self.framenumber)], self.rect)

        elif self.hp >= self.originalHP / 2:
            self.display.blit(self.yetiimgs[2][int(self.framenumber)], self.rect)

        elif self.hp >= self.originalHP / 4:
            self.display.blit(self.yetiimgs[3][int(self.framenumber)], self.rect)

    # decrease health by the damage
    def takeDamage(self, dmg,coords):
        self.hp -= dmg
        if self.hp <= 0:
            self.die(coords)

    # once health is 0, kill yeti
    def die(self,coords):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('yetis/yetiDie.ogg'),0)

        row = coords[0]
        column = coords[1]

        yetis[row][column] = None
        try:
            del self
        except:
            print("error killing yeti")

    # move the yeti to a certain position 'pos'
    # @param pos -> where to move yeti too
    def moveTo(self, pos):
        self.rect[0] = pos[0]
        self.rect[1] = pos[1]
        self.weaponPos = pos
        self.display.blit(self.yetiimgs[0][0], pos)

    # once yeti is placed, the moveable variable is set to False (cannot move yeti after placed)
    def placeYeti(self):
        self.moveable = False

    # save the condition of the yeti
    def save(self):
        # return array of everything that is important to save
        return self.rect, self.hp, self.type

    class Weapon(pygame.sprite.Sprite):
        # this is used to create the weapon
        # @param: self -> instance of a class
        # @param display -> display
        # @param: pos -> position of sprite
        # @param: img -> image of weapon
        # @param: dmg -> the damage that the weapon does
        # @param: parent -> the yeti attached to this weapon
        def __init__(self, display, pos, img, dmg, parent):
            pygame.sprite.Sprite.__init__(self)
            self.weaponImg = img
            self.frame = 0
            self.display = display
            self.display.blit(self.weaponImg[0], pos)
            self.rect = self.weaponImg[0].get_rect()
            self.rect[0] = pos[0]
            self.rect[1] = pos[1] + 35
            self.moveable = True
            self.weaponPos = pos
            self.dmg = dmg
            self.parent = parent

            self.yakIndex = 0
            self.targetYak = None
            for yak in yaks[int(self.rect[1]/LANE_HEIGHT)-1]:
                if yak.rect[0] >= self.rect[0]:
                    self.targetYak = yak
                    break
                self.yakIndex += 1


        # moves weapon to the right of the screen 7 pixels per frame and updates with the blit function
        def defend(self):
            if self.targetYak is not None and self.targetYak.rect[0] < SCREEN_WIDTH:
                self.rect[0] += 14
                self.frame += 0.3
                self.display.blit(self.weaponImg[int(self.frame)], self.rect)
                if self.frame >= 2.9:
                    self.frame = 0

                if self.targetYak is not None and self.targetYak.rect[0] <= self.rect[0] <= self.targetYak.rect[0] + 30:
                    self.damage(self.targetYak, self.yakIndex)
                    self.parent.weapon = None


        # damages the yak and deletes its self as it's humble duty is complete
        def damage(self, yak,yakIndex):
            yak.takeDamage(self.dmg,yakIndex)
            del self


# 3 types of yetis
class Phil(Yeti):
    # initiates a phil object, parameters have same purpose as superclass Yeti
    # passes in new parameters fit for the phil class
    def __init__(self, display, pos, health=50):
        self.display = display
        imgs = [
            # full health
            [pygame.transform.scale(pygame.image.load("yetis/blue_yeti1_4.png"),(LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/blue_yeti2_4.png"),(LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/blue_yeti3_4.png"),(LANE_HEIGHT, LANE_HEIGHT))],
            # 3/4 health
            [pygame.transform.scale(pygame.image.load("yetis/blue_yeti1_3.png"),(LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/blue_yeti2_3.png"),(LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/blue_yeti3_3.png"),(LANE_HEIGHT, LANE_HEIGHT))],
            # 1/2 health
            [pygame.transform.scale(pygame.image.load("yetis/blue_yeti1_2.png"),(LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/blue_yeti2_2.png"),(LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/blue_yeti3_2.png"),(LANE_HEIGHT, LANE_HEIGHT))],
            # 1/4health
            [pygame.transform.scale(pygame.image.load("yetis/blue_yeti1_1.png"),(LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/blue_yeti2_1.png"),(LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/blue_yeti3_1.png"),(LANE_HEIGHT, LANE_HEIGHT))]]
        Yeti.__init__(self, display, pos, health, 10, imgs, True, 0)

    # places phil object and creates weapon object
    def placeYeti(self):
        Yeti.placeYeti(self)
        self.weapon = Phil.Snowball(self.display, self.rect, self)

    class Snowball(Yeti.Weapon):
        # initializes snowball object extending off of weapon
        def __init__(self, display, pos, parent):
            imgs = [pygame.transform.scale(pygame.image.load("weapons/snowball.png"),(50,50)),pygame.transform.scale(pygame.image.load("weapons/snowball2.png"),(50,50)),pygame.transform.scale(pygame.image.load("weapons/snowball3.png"),(50,50))]
            Yeti.Weapon.__init__(self, display, pos, imgs, 10, parent)


class Dave(Yeti):
    # initiates a dave object, parameters have same purpose as superclass Yeti
    # passes in new parameters fit for the dave class
    def __init__(self, display, pos, health=70):
        self.display = display
        imgs = [
            # full health
            [pygame.transform.scale(pygame.image.load("yetis/orange_yeti1_4.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/orange_yeti2_4.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/orange_yeti3_4.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            # 3/4 health
            [pygame.transform.scale(pygame.image.load("yetis/orange_yeti1_3.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/orange_yeti2_3.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/orange_yeti3_3.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            # 1/2 health
            [pygame.transform.scale(pygame.image.load("yetis/orange_yeti1_2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/orange_yeti2_2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/orange_yeti3_2.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            # 1/4health
            [pygame.transform.scale(pygame.image.load("yetis/orange_yeti1_1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/orange_yeti2_1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/orange_yeti3_1.png"), (LANE_HEIGHT, LANE_HEIGHT))]]

        Yeti.__init__(self, display, pos, health, 20, imgs, True, 1)

    # places dave object and creates weapon object
    def placeYeti(self):
        Yeti.placeYeti(self)
        self.weapon = Dave.Axe(self.display, self.rect, self)

    class Axe(Yeti.Weapon):
        #  initializes axe object extending off of weapon
        def __init__(self, display, pos, parent):
            imgs = [pygame.transform.scale(pygame.image.load("weapons/axe.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("weapons/axe2.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("weapons/axe3.png"), (50, 50))]

            Yeti.Weapon.__init__(self, display, pos, imgs, 20, parent)


class Bob(Yeti):
    # initiates a bob object, parameters have same purpose as superclass Yeti
    # passes in new parameters fit for the bob class
    def __init__(self, display, pos, health=100):
        self.display = display
        imgs = [
            # full health
            [pygame.transform.scale(pygame.image.load("yetis/pink_yeti1_4.png"), (LANE_HEIGHT ,LANE_HEIGHT )),
             pygame.transform.scale(pygame.image.load("yetis/pink_yeti2_4.png"), (LANE_HEIGHT ,LANE_HEIGHT )),
             pygame.transform.scale(pygame.image.load("yetis/pink_yeti3_4.png"), (LANE_HEIGHT ,LANE_HEIGHT ))],
            # 3/4 health
            [pygame.transform.scale(pygame.image.load("yetis/pink_yeti1_3.png"), (LANE_HEIGHT ,LANE_HEIGHT )),
             pygame.transform.scale(pygame.image.load("yetis/pink_yeti2_3.png"), (LANE_HEIGHT ,LANE_HEIGHT )),
             pygame.transform.scale(pygame.image.load("yetis/pink_yeti3_3.png"), (LANE_HEIGHT ,LANE_HEIGHT ))],
            # 1/2 health
            [pygame.transform.scale(pygame.image.load("yetis/pink_yeti1_2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/pink_yeti2_2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/pink_yeti3_2.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            # 1/4health
            [pygame.transform.scale(pygame.image.load("yetis/pink_yeti1_1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/pink_yeti2_1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yetis/pink_yeti3_1.png"), (LANE_HEIGHT, LANE_HEIGHT))]]

        Yeti.__init__(self, display, pos, health, 30, imgs, True, 2)

    # places bob object and creates weapon object
    def placeYeti(self):
        Yeti.placeYeti(self)
        self.weapon = Bob.Sword(self.display, self.rect, self)

    class Sword(Yeti.Weapon):
        #  initializes sword object extending off of weapon
        def __init__(self, display, pos, parent):
            imgs = [pygame.transform.scale(pygame.image.load("weapons/sword.png"), (60, 60)),
                    pygame.transform.scale(pygame.image.load("weapons/sword2.png"), (60, 60)),
                    pygame.transform.scale(pygame.image.load("weapons/sword3.png"), (60, 60))]

            Yeti.Weapon.__init__(self, display, pos, imgs, 30, parent)


# YAKS-------------------------------------------------------------------------------------------------------------------------------------
class Yak(pygame.sprite.Sprite):

    # this is used to create the yak
    #@param display -> the gameDisplay to use for rendering
    #@param pos -> position at which to make the yak
    #@param hp-> the health of the yak
    #@param imgs -> an array of images for the walking animation as well as the health indictors
    #@param delay -> how long before yak should attack
    #@param yakdmg -> dmg that the yak will do to yetis
    #@param looseFunc -> the function to call once yak gets to end of board, and player looses
    #@param type -> used for saving and identifying the yak
    def __init__(self, display, pos, hp, imgs, delay, yakdmg, looseFunc, type):
        pygame.sprite.Sprite.__init__(self)
        #setup variables
        self.display = display
        self.pos = pos
        self.hp = hp
        self.originalHP = hp
        self.moveable = True
        self.startTime = pygame.time.get_ticks()
        self.delay = delay
        self.enabled = False
        self.yakimgs = imgs
        self.framenumber = 0
        self.yakdmg = yakdmg
        self.rect = self.yakimgs[0][0].get_rect()
        self.rect[0] = pos[0]
        self.rect[1] = pos[1]
        self.looseFunc = looseFunc
        self.type = type
        self.targetYeti = None
        self.targetYetiCoords = None

    #called every frame to display yak and attack yetis
    def update(self, *args):
        #check if at end of board and if so player looses
        if self.rect[0] <= 0:
            self.looseFunc()
        #if not, check if enough time has passed to start attacking, if yes attack
        elif pygame.time.get_ticks() - self.startTime >= self.delay:
            self.enabled = True

            #if there is a yeti nearby attack it
            if self.targetYeti is not None and self.targetYeti.hp>0:
                if self.targetYeti.rect[0] - LANE_WIDTH/4 < self.rect[0] < self.targetYeti.rect[0] + LANE_WIDTH/2: #yak is at proper distance, attack, otherwise ignore this yeti and move on
                    self.targetYeti.takeDamage(self.yakdmg,self.targetYetiCoords)
                else:
                    self.targetYeti = None
                    self.rect[0] -= 7
            #otherwise continue moving in on base and searching for yetis
            else:
                self.rect[0] -= 7
                self.framenumber += 0.28
                if self.framenumber > 2:
                    self.framenumber = 0

                self.targetYetiCoords = [round(self.rect[1] / LANE_HEIGHT) - 1, round(self.rect[0] / LANE_WIDTH)]
                self.targetYeti = yetis[self.targetYetiCoords[0]][self.targetYetiCoords[1]]

        #display current health in the form of number of legs
        if self.hp >= self.originalHP:
            self.display.blit(self.yakimgs[0][int(self.framenumber)], self.rect)
        elif self.hp >= self.originalHP / 3 * 2:
            self.display.blit(self.yakimgs[1][int(self.framenumber)], self.rect)
        else:
            self.display.blit(self.yakimgs[2][int(self.framenumber)], self.rect)

    # decrease health of yak
    #@param dmg -> the damage delt to the yak
    #@param index -> the yak id in its row
    def takeDamage(self, dmg, index):
        self.hp -= dmg
        if self.hp <= 0:
            self.die(index)

    # once health is 0, kill yak
    # @param index -> the yak id in its row
    def die(self,index):
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('yaks/yakDie.ogg'), 0)

        row = int(self.rect[1] / LANE_HEIGHT)-1

        if len(yaks[row]) > 0:
            del yaks[row][index]
        del self

    #helper function to extract only what is needed for saving
    def save(self):
        return self.rect, self.hp, self.delay - (pygame.time.get_ticks() - self.startTime), self.type

#types of yaks
class blackYak(Yak):
    def __init__(self, display, pos, delay, looseFunc, health=80):
        imgs = [
            # full health
            [pygame.transform.scale(pygame.image.load("yaks/Case black 1.1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case black 2.1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case black 3.1.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            # 2/3 health
            [pygame.transform.scale(pygame.image.load("yaks/Case black 1.2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case black 2.2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case black 3.2.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            # 1/3 health
            [pygame.transform.scale(pygame.image.load("yaks/Case black 1.3.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case black 2.3.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case black 3.3.png"), (LANE_HEIGHT, LANE_HEIGHT))],
        ]
        super().__init__(display, pos, health, imgs, delay, 7, looseFunc, 1)


class whiteYak(Yak):
    def __init__(self, display, pos, delay, looseFunc, health=40):
        imgs = [
            # full health
            [pygame.transform.scale(pygame.image.load("yaks/Case white 1.1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case white 2.1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case white 3.1.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            # 2/3 health
            [pygame.transform.scale(pygame.image.load("yaks/Case white 1.2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case white 2.2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case white 3.2.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            # 1/3 health
            [pygame.transform.scale(pygame.image.load("yaks/Case white 1.3.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case white 2.3.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case white 3.3.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            ]
        super().__init__(display, pos, health, imgs, delay, 2, looseFunc, 0)


class brownYak(Yak):
    def __init__(self, display, pos, delay, looseFunc, health=60):
        imgs = [
            # full health
            [pygame.transform.scale(pygame.image.load("yaks/Case brown 1.1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case brown 2.1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case brown 3.1.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            # 2/3 health
            [pygame.transform.scale(pygame.image.load("yaks/Case brown 1.2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case brown 2.2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case brown 3.2.png"),(LANE_HEIGHT, LANE_HEIGHT))],
            # 1/3 health
            [pygame.transform.scale(pygame.image.load("yaks/Case brown 1.3.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case brown 2.3.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case brown 3.3.png"), (LANE_HEIGHT, LANE_HEIGHT))],
           ]
        super().__init__(display, pos, health, imgs, delay, 5, looseFunc, 2)


class redYak(Yak):
    def __init__(self, display, pos, delay, looseFunc, health=120):
        imgs = [
            # full health
            [pygame.transform.scale(pygame.image.load("yaks/Case red 1.1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case red 2.1.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case red 3.1.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            # 2/3 health
            [pygame.transform.scale(pygame.image.load("yaks/Case red 1.2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case red 2.2.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case red 3.2.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            # 1/3 health
            [pygame.transform.scale(pygame.image.load("yaks/Case red 1.3.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case red 2.3.png"), (LANE_HEIGHT, LANE_HEIGHT)),
             pygame.transform.scale(pygame.image.load("yaks/Case red 3.3.png"), (LANE_HEIGHT, LANE_HEIGHT))],
            ]
        super().__init__(display, pos, health, imgs, delay, 10, looseFunc, 3)


# BUTTONS------------------------------------------------------------------------------------------------------------------------------------
class Button(pygame.sprite.Sprite):
    #create button
    #@param text -> text to show on button
    #@param pos -> position of th ebutton on screen
    #@param colour -> optional way to custmize colour of button
    #@param enabled -> optional way to disable the button
    #@param action -> optional action for th button
    def __init__(self, text, pos, colour=(255, 255, 255), enabled=True, *action):
        pygame.sprite.Sprite.__init__(self)
        #setup variables
        self.surface = pygame.Surface((0, 0))
        self.font = pygame.font.Font("font.ttf", 60)
        if enabled:
            self.text = self.font.render(text, True, colour)
        else:
            self.text = self.font.render(text, True, (105, 105, 105))
        self.action = text.lower()
        self.actionFunc = action
        self.rect = pygame.Rect(pos[0] - self.text.get_rect()[2] / 2, pos[1] - self.text.get_rect()[3] / 2,
                                self.text.get_rect()[2], self.text.get_rect()[3])
        self.enabled = enabled

    #used to render button on screen
    def update(self):
        gameDisplay.blit(self.surface, self.rect)
        gameDisplay.blit(self.text, self.rect)

    #used to determine if a button is being clicked upon (only works is button is enabled)
    #@param curScreen -> gameDisplay
    #@param transition -> transition instance that is passed between screens to animate fading in and out
    def isClicked(self, curScreen, transition):
        mousePos = pygame.mouse.get_pos()
        # checks if mouse x position is within the bounds of the rect. Same with the y
        clicked = (self.rect[0] <= mousePos[0] <= (self.rect[0] + self.rect[2])) and (
                    self.rect[1] <= mousePos[1] <= (self.rect[1] + self.rect[3]))
        if clicked and self.enabled:
            self.doAction(curScreen,transition)
        return clicked and self.enabled

    #if button is clicked this unction is called to do the associated action. For simplicity, some actions are predefined
    #@param curScreen -> gameDisplay
    #@param transition -> transition instance that is passed between screens to animate fading in and out
    def doAction(self, curScreen, transition):
        #other - passed in via actionFunc variable
        if self.actionFunc is not None and len(self.actionFunc) > 0:
            transition.fadeOutAuto()
            self.actionFunc[0](transition)

        #start game
        elif self.action == "start":
            transition.fadeOutAuto()
            LevelSelection(transition)
            del curScreen

        #load previous game
        elif self.action == "load":
            transition.fadeOutAuto()
            UI(gameDisplay, True, -1,transition)

        #quiting game
        elif self.action == "quit":
            pygame.quit()
            quit()

        #choosing level, go to desired evel
        elif self.action.startswith("level"):
            transition.fadeOutAuto()
            StoryScreen(self.action[6:],transition)
            del curScreen


# Story dialogs---------------------------------------------------------------------------------------------------------------------------------------
class StoryScreen(pygame.sprite.Sprite):
    #setup story screen
    #@param levelToSow -> the level to show the story for
    #@param transition -> the animation to display
    def __init__(self,levelToShow,transition):
        pygame.sprite.Sprite.__init__(self)
        #setup varaiables
        self.level = int(levelToShow) - 1
        self.font = pygame.font.Font("Nunito.ttf", 30)
        self.x = 150
        self.y = 200
        self.nextBtn = Button("Affirmative", (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2), (0,0,0),True, self.goToGame, True)
        self.button_y = self.blit_text(gameDisplay, levelStory[self.level], (20, 20), self.font)
        self.background = pygame.image.load("textScreen.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        crashed = False
        #setup render loop
        while not crashed:
            clock.tick(30)  # makes game run at 30 frames per second
            for event in pygame.event.get():  # check for user input
                if event.type == pygame.QUIT:
                    crashed = True
                elif event.type == pygame.MOUSEBUTTONDOWN and self.nextBtn.isClicked(self,transition):#if clicking on the affirmative button, go to game
                        crashed = True
                        self.goToGame(transition)

                elif event.type == pygame.KEYDOWN:#controls for navigating story up and down arrows
                    if event.key == pygame.K_UP:
                        self.y+=50
                    elif event.key == pygame.K_DOWN:
                        self.y-=50

            #display screen
            gameDisplay.blit(self.background,(0,0,SCREEN_WIDTH, SCREEN_HEIGHT))
            self.blit_text(gameDisplay, levelStory[self.level], (self.x,self.y), self.font)
            self.nextBtn.update()

            #make sure button is always very visible and stays on screen
            if self.nextBtn.rect[1] > 600:
                self.y -= 1
                self.nextBtn.rect[1] = self.y + self.button_y + 70

            transition.fadeIn()

            pygame.display.flip()  # update the entire display

    #Function to take player to the game
    def goToGame(self,transition):
        UI(gameDisplay, False, self.level,transition)

    #helper function to make sure that the story fits in the frame and the screen. Looks at word length and calculates where to position it
    def blit_text(self,surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        size = surface.get_size()
        max_width = size[0] - pos[0]
        max_height = size[1]
        x, y = pos
        lines = 0
        #loop through lines and potioitn words where needed
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                    lines += 1
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        self.nextBtn.update()
        return y +  word_height

# Screen Transitions----------------------------------------------------------------------------------------------------------------------------
class Transition(pygame.sprite.Sprite):
    #setup transition variable
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #setup variables
        self.alphaSurface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))  # The custom-surface of the size of the screen.
        self.rect = self.alphaSurface.get_rect()
        self.alphaSurface.fill((0,0,0))  # Fill it with whole white before the main-loop.
        self.alphaSurface.set_alpha(0)  # Set alpha to 0 before the main-loop.
        self.alpha = 0  # The increment-variable.

    #animates the fading and and out inside its own loop
    def animate(self, action = None):
        done = False
        state = True
        #start loop
        while not done:
            clock.tick(30)
            #depending on state either fade in or out
            if state:
                self.alpha += 1
            else:
                self.alpha -= 1
            #display it
            self.alphaSurface.set_alpha(self.alpha)
            gameDisplay.blit(self.alphaSurface, self.rect)
            pygame.display.flip()

            #changing if states once done
            if self.alpha >= 255:
                state = False
                if action is not None:
                    action()
            elif self.alpha <= 0:
                done = True

    #only fade out in a loop
    def fadeOutAuto(self):
        while self.alpha < 100:
            clock.tick(30)
            self.alpha += 2
            self.alphaSurface.set_alpha(self.alpha)
            gameDisplay.blit(self.alphaSurface, self.rect)
            pygame.display.flip()
        self.alpha = 255

    # only fade in in a loop
    def fadeInAuto(self):
        while self.alpha > 0:
            clock.tick(30)
            self.alpha -= 2
            self.alphaSurface.set_alpha(self.alpha)
            gameDisplay.blit(self.alphaSurface, self.rect)
            pygame.display.flip()
        self.alpha = 0

    #fade out but needs to be placed into a loop
    def fadeOut(self):
        if self.alpha < 255:
            self.alpha += 8
            self.alphaSurface.set_alpha(self.alpha)
            gameDisplay.blit(self.alphaSurface, self.rect)
            pygame.display.flip()

    # fade in but needs to be placed into a loop
    def fadeIn(self):
        if self.alpha > 0:
            self.alpha -= 8
            self.alphaSurface.set_alpha(self.alpha)
            gameDisplay.blit(self.alphaSurface, self.rect)


# Level selection-------------------------------------------------------------------------------------------------------------------------------
class LevelSelection(pygame.sprite.Sprite):
    #setup for the level selection screen
    def __init__(self,transition):
        #setup variables
        pygame.sprite.Sprite.__init__(self,)
        self.font = pygame.font.Font("font.ttf", 115)
        self.text = self.font.render("Yaks vs Yetis", True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect = [SCREEN_WIDTH / 2 - self.textRect[2] / 2, 15, self.textRect[2], self.textRect[3]]
        self.image = pygame.image.load("title.png")
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        crashed = False

        #load the sav efile to know which was the last level to be beat
        try:
            pkl_file = open('levels.pkl', 'rb')
            arr = pickle.load(pkl_file)
            level = int(arr["level"])  # get the highest unlocked level
        except:
            level = 1

        #setup for buttons
        self.buttons = []
        rows = [SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2, SCREEN_HEIGHT / 2 + 200, SCREEN_HEIGHT / 2 + 400]
        columns = [SCREEN_WIDTH * 1 / 4, SCREEN_WIDTH / 2, SCREEN_WIDTH * 3 / 4]
        rowsIndex = 0
        columnsIndex = 0

        #add the buttons and disable or enable them based on if they have been beat or not
        for i in range(1, 11):
            enabled = i <= level
            if i == 10:
                self.buttons.append(
                    Button("Level " + str(i), (columns[columnsIndex + 1], rows[rowsIndex]), (255, 255, 255), enabled))
            else:
                self.buttons.append(
                    Button("Level " + str(i), (columns[columnsIndex], rows[rowsIndex]), (255, 255, 255), enabled))
            columnsIndex += 1
            if columnsIndex >= 3:
                rowsIndex += 1
                columnsIndex = 0

        #render and input loop
        while not crashed:
            clock.tick(30)  # makes game run at 45 frames per second

            self.render()  # render the game
            transition.fadeIn()
            for event in pygame.event.get():  # check for user input
                if event.type == pygame.QUIT:
                    crashed = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.isClicked(self,transition):
                            crashed = True

            pygame.display.flip()  # update the entire display

    #render function to display everything to screen
    def render(self):
        gameDisplay.blit(self.image, self.image.get_rect())
        gameDisplay.blit(self.text, self.textRect)

        for button in self.buttons:
            button.update()


# TITLE--------------------------------------------------------------------------------------------------------------------------------------
class Title(pygame.sprite.Sprite):
    #setup title screen
    def __init__(self, transition):
        #setup variables
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("font.ttf", 115)
        self.text = self.font.render("Yaks vs Yetis", True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect = [SCREEN_WIDTH / 2 - self.textRect[2] / 2, 15, self.textRect[2], self.textRect[3]]
        self.image = pygame.image.load("title.png")
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.imgRect = self.image.get_rect()

        self.snow = pygame.image.load("titleSnow2.png")
        self.snow = pygame.transform.scale(self.snow, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.snowRect = self.snow.get_rect()
        self.snowRect[1] = -SCREEN_HEIGHT

        self.snow2 = pygame.image.load("titleSnow2.png")
        self.snow2 = pygame.transform.scale(self.snow2, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.snow2Rect = self.snow.get_rect()
        self.snow2Rect[1] = -SCREEN_HEIGHT*2

        crashed = False

        #start wind sounds
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('titleMusic.ogg'),-1)

        #create buttons
        self.buttons = [
            Button("Start", (SCREEN_WIDTH / 2, 350)),
            Button("Load", (SCREEN_WIDTH / 2, 550)),
            Button("Quit", (SCREEN_WIDTH / 2, 750))
        ]

        #render and input loop
        while not crashed:
            clock.tick(30)  # makes game run at 30 frames per second

            self.render()  # render the game
            transition.fadeIn()
            for event in pygame.event.get():  # check for user input
                if event.type == pygame.QUIT:
                    crashed = True
                    pygame.mixer.music.stop()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.isClicked(self,transition):
                            crashed = True

            pygame.display.flip()  # update the entire display

    #render function to draw everything to screen
    def render(self):
        gameDisplay.blit(self.image, self.imgRect)
        gameDisplay.blit(self.text, self.textRect)

        #snow falling effect. 2 identical images take turns moving down the screen to create a continuous snowfall effect
        self.snowRect[1] += 5
        self.snow2Rect[1] += 5
        if self.snowRect[1] >= SCREEN_HEIGHT:
            self.snowRect[1] = -SCREEN_HEIGHT
        elif self.snow2Rect[1] >= SCREEN_HEIGHT:
            self.snow2Rect[1] = -SCREEN_HEIGHT

        gameDisplay.blit(self.snow, self.snowRect)
        gameDisplay.blit(self.snow2, self.snow2Rect)

        #show buttons
        for button in self.buttons:
            button.update()

#start program
Title(Transition())