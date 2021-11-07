#!/usr/bin/python
# -*- coding: latin-1 -*-

# Challenge Editor - Edits NSMBU's challenge data file.
# Copyright (C) 2016 Grop

# main.py
# This is the main executable for Challenge Editor

################################################################
################################################################
version = '1.0'

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import struct

class Entry():
    """Class that represents an entry"""
    def __init__(self, data=None):
        """Initialises the entry"""
        if data is not None:
            self.load(data)
        else:
            self.babyyoshi = 0
            self.level = 0 
            self.powerup = 0 
            self.unk3 = 0
            self.unk4 = 0
            self.unk5 = 0 
            self.catid = 0
            self.unk6 = 0
            self.world = 0
            self.unk7 = 0
            self.unk8 = 0
            self.prequel = 0 # Unknown effect
            self.unk9 = 0
            self.unk10 = 0
            self.time = 0 
            self.stars = 0 
            self.area = 0
            self.entrance = 0 
            self.id = 0
            self.unk15 = 0
            self.unk16 = 0
            self.bronzeminimum = 0
            self.silverminimum = 0
            self.goldenminimum = 0

    def load(self, data):
        """Parses entry data"""
        self.babyyoshi = data[0]
        self.level = data[1]
        self.powerup = data[2]
        self.unk3 = data[3]
        self.unk4 = data[4]
        self.unk5 = data[5]
        self.catid = data[6]
        self.unk6 = data[7]
        self.world = data[8]
        self.unk7 = data[9]
        self.unk8 = data[10]
        self.prequel = data[11]
        self.unk9 = data[12]
        self.unk10 = data[13]
        self.time = data[14]
        self.stars = data[15]
        self.area = data[16]
        self.entrance = data[17]
        self.id = data[18]
        self.unk15 = data[19]
        self.unk16 = data[20]
        self.bronzeminimum = data[21]
        self.silverminimum = data[22]
        self.goldenminimum = data[23]

    def save(self):
        """Returns the entry"""
        data = struct.pack(">10I2iIi5I2i3I", self.babyyoshi, self.level, self.powerup, self.unk3, self.unk4, self.unk5, self.catid, self.unk6, self.world, self.unk7,
            self.unk8, self.prequel, self.unk9, self.unk10, self.time, self.stars, self.area, self.entrance, self.id, self.unk15, self.unk16, self.bronzeminimum,
            self.silverminimum, self.goldenminimum)
        return bytearray(data)


class File():
    """Class that represents a challenge file"""
    def __init__(self, rawdata=None):
        """Initialises the exbin file"""
        if rawdata == None:
            self.initAsEmpty()
        else:
            self.initFromData(rawdata)

    def initAsEmpty(self):
        """Empties the challenges"""
        self.challenges = []

    def initFromData(self, rawdata):
        """Initialises the file from data"""
        self.challenges = []
        for i in range(0, 80):
            data = struct.unpack_from(">10I2iIi5I2i3I", rawdata, 0x10 + (i * 0x60))
            challenge = Entry(data)
            self.challenges.append(challenge)

    def save(self):
        """Saves the Challenge data edits"""
        data = bytearray(b'\x00\x00\x0B\xB8\x00\x00\x03\xE8\x00\x00\x00\x00\x00\x00\x00\x00')
        for challenge in self.challenges:
            data += challenge.save()
        return data


class ChallengeViewer(QtWidgets.QWidget):
    """Widget that views challenge info"""
    def __init__(self):
        """Initialises the widget"""
        QtWidgets.QWidget.__init__(self)
        self.file = File()

        # Create the list of challenges
        Challenges = QtWidgets.QGroupBox('Challenges')
        self.ChallengeList = QtWidgets.QListWidget()
        self.ChallengeList.currentItemChanged.connect(self.HandleDifferentChallenge)

        # Create the edit for the selected challenge
        Challenge = QtWidgets.QGroupBox('Selected Challenge')
        
        # ID / Stars / Time
        self.id = QtWidgets.QLineEdit()
        self.id.setFixedWidth(40)
        self.id.setMaxLength(5)

        self.starsplus = QtWidgets.QPushButton("+")
        self.starsplus.clicked.connect(self.addStar)
        self.starsplus.setEnabled(False)
        self.starsplus.setFixedWidth(25)

        self.stars = QtWidgets.QHBoxLayout()
        
        self.starsmin = QtWidgets.QPushButton("-")
        self.starsmin.clicked.connect(self.removeStar)
        self.starsmin.setEnabled(False)
        self.starsmin.setFixedWidth(25)

        self.time = QtWidgets.QSpinBox()
        self.time.setMaximum(999)

        timeicon = QtWidgets.QLabel()
        timeicon.setPixmap(QtGui.QPixmap("images/clock.png"))
        
        starL = QtWidgets.QHBoxLayout()
        starL.addWidget(QtWidgets.QLabel("Challenge #"))
        starL.addWidget(self.id)
        starL.addWidget(self.starsmin)
        starL.addStretch(1)
        starL.addLayout(self.stars)
        starL.addStretch(1)
        starL.addWidget(self.starsplus)
        starL.addWidget(timeicon)
        starL.addWidget(self.time)

        # Category
        category = QtWidgets.QGroupBox("Category")
        l = QtWidgets.QHBoxLayout()
        self.Category = QtWidgets.QComboBox()
        self.Category.setEnabled(False)
        l.addWidget(self.Category)
        category.setLayout(l)

        # Level ID it's using
        self.WorldNum = QtWidgets.QLineEdit()
        self.WorldNum.setFixedWidth(20)
        self.WorldNum.setMaxLength(2)
        self.LevelNum = QtWidgets.QLineEdit()
        self.LevelNum.setFixedWidth(20)
        self.LevelNum.setMaxLength(2)
        minus = QtWidgets.QLabel("-")
        minus.setFixedWidth(5)

        # Level, Area and entrance
        location = QtWidgets.QGroupBox("Location of challenge")
        areanentrance = QtWidgets.QVBoxLayout()

        levelL = QtWidgets.QHBoxLayout()
        levelL.addWidget(QtWidgets.QLabel("Level"))
        levelL.addStretch(1)
        levelL.addWidget(self.WorldNum)
        levelL.addWidget(minus)
        levelL.addWidget(self.LevelNum)
        levelL.addWidget(QtWidgets.QLabel(".szs"))

        areanentrance.addLayout(levelL)

        self.area = QtWidgets.QLineEdit()
        self.area.setFixedWidth(20)
        areaL = QtWidgets.QHBoxLayout()
        areaL.addWidget(QtWidgets.QLabel("Area:"))
        areaL.addWidget(self.area)

        areanentrance.addLayout(areaL)
        
        self.entrance = QtWidgets.QLineEdit()
        self.entrance.setFixedWidth(20)
        entranceL = QtWidgets.QHBoxLayout()
        entranceL.addWidget(QtWidgets.QLabel("Entrance:"))
        entranceL.addWidget(self.entrance)

        areanentrance.addLayout(entranceL)

        location.setLayout(areanentrance)

        # Unknowns
        # Left column
        UNKS = QtWidgets.QGroupBox("Unknown Values")

        LL = QtWidgets.QVBoxLayout()
        self.unk3 = QtWidgets.QLineEdit()
        self.unk3.setFixedWidth(30)

        unk3L = QtWidgets.QHBoxLayout()
        unk3L.addWidget(QtWidgets.QLabel("Unknown 3 (0x0C):"))
        unk3L.addWidget(self.unk3)
        LL.addLayout(unk3L)

        self.unk4 = QtWidgets.QLineEdit()
        self.unk4.setFixedWidth(30)

        unk4L = QtWidgets.QHBoxLayout()
        unk4L.addWidget(QtWidgets.QLabel("Unknown 4 (0x10):"))
        unk4L.addWidget(self.unk4)
        LL.addLayout(unk4L)

        self.unk5 = QtWidgets.QLineEdit()
        self.unk5.setFixedWidth(30)

        unk5L = QtWidgets.QHBoxLayout()
        unk5L.addWidget(QtWidgets.QLabel("Unknown 5 (0x14):"))
        unk5L.addWidget(self.unk5)
        LL.addLayout(unk5L)

        self.unk6 = QtWidgets.QLineEdit()
        self.unk6.setFixedWidth(30)

        unk6L = QtWidgets.QHBoxLayout()
        unk6L.addWidget(QtWidgets.QLabel("Unknown 6 (0x1C):"))
        unk6L.addWidget(self.unk6)
        LL.addLayout(unk6L)

        self.unk7 = QtWidgets.QLineEdit()
        self.unk7.setFixedWidth(30)

        unk7L = QtWidgets.QHBoxLayout()
        unk7L.addWidget(QtWidgets.QLabel("Unknown 7 (0x24):"))
        unk7L.addWidget(self.unk7)
        LL.addLayout(unk7L)

        # Right column
        RL = QtWidgets.QVBoxLayout()

        self.unk8 = QtWidgets.QLineEdit()
        self.unk8.setFixedWidth(30)

        unk8L = QtWidgets.QHBoxLayout()
        unk8L.addWidget(QtWidgets.QLabel("Unknown 8 (0x28):"))
        unk8L.addWidget(self.unk8)
        RL.addLayout(unk8L)

        self.unk9 = QtWidgets.QLineEdit()
        self.unk9.setFixedWidth(30)

        unk9L = QtWidgets.QHBoxLayout()
        unk9L.addWidget(QtWidgets.QLabel("Unknown 9 (0x30):"))
        unk9L.addWidget(self.unk9)
        RL.addLayout(unk9L)

        self.unk10 = QtWidgets.QLineEdit()
        self.unk10.setFixedWidth(30)

        unk10L = QtWidgets.QHBoxLayout()
        unk10L.addWidget(QtWidgets.QLabel("Unknown 10 (0x34):"))
        unk10L.addWidget(self.unk10)
        RL.addLayout(unk10L)

        self.unk15 = QtWidgets.QLineEdit()
        self.unk15.setFixedWidth(30)

        unk15L = QtWidgets.QHBoxLayout()
        unk15L.addWidget(QtWidgets.QLabel("Unknown 15 (0x4C):"))
        unk15L.addWidget(self.unk15)
        RL.addLayout(unk15L)

        self.unk16 = QtWidgets.QLineEdit()
        self.unk16.setFixedWidth(30)

        unk16L = QtWidgets.QHBoxLayout()
        unk16L.addWidget(QtWidgets.QLabel("Unknown 16 (0x50):"))
        unk16L.addWidget(self.unk16)
        RL.addLayout(unk16L)

        UNKL = QtWidgets.QHBoxLayout()
        UNKL.addLayout(LL)
        UNKL.addLayout(RL)

        UNKS.setLayout(UNKL)

        # Medal times
        TGB = QtWidgets.QGroupBox("Medals") # Don't even know what TGB stands for myself...

        L = QtWidgets.QVBoxLayout()
        GL = QtWidgets.QHBoxLayout()
        self.goldenminimum = QtWidgets.QLineEdit()
        self.goldenminimum.setFixedWidth(100)
        goldmedal = QtWidgets.QLabel()
        goldmedal.setPixmap(QtGui.QPixmap("images/time_gold.png"))
        GL.addWidget(goldmedal)
        GL.addStretch(1)
        GL.addWidget(self.goldenminimum)
        L.addLayout(GL)

        SL = QtWidgets.QHBoxLayout()
        self.silverminimum = QtWidgets.QLineEdit()
        self.silverminimum.setFixedWidth(100)
        silvermedal = QtWidgets.QLabel()
        silvermedal.setPixmap(QtGui.QPixmap("images/time_silver.png"))
        SL.addWidget(silvermedal)
        SL.addStretch(1)
        SL.addWidget(self.silverminimum)
        L.addLayout(SL)

        BL = QtWidgets.QHBoxLayout()
        self.bronzeminimum = QtWidgets.QLineEdit()
        self.bronzeminimum.setFixedWidth(100)
        bronzemedal = QtWidgets.QLabel()
        bronzemedal.setPixmap(QtGui.QPixmap("images/time_bronze.png"))
        BL.addWidget(bronzemedal)
        BL.addStretch(1)
        BL.addWidget(self.bronzeminimum)
        L.addLayout(BL)

        TGB.setLayout(L)

        # Challenge values
        CGB = QtWidgets.QGroupBox("Challenge settings")
        q = QtWidgets.QVBoxLayout()

        # Powerup
        self.powerup = QtWidgets.QComboBox()
        self.powerup.setEnabled(False)

        powerupL = QtWidgets.QHBoxLayout()
        powerupL.addWidget(QtWidgets.QLabel("Start powerup:"))
        powerupL.addStretch(1)
        powerupL.addWidget(self.powerup)
        q.addLayout(powerupL)

        # Baby Yoshi
        self.babyyoshi = QtWidgets.QComboBox()
        self.babyyoshi.setEnabled(False)

        babyyoshiL = QtWidgets.QHBoxLayout()
        babyyoshiL.addWidget(QtWidgets.QLabel("Baby Yoshi:"))
        babyyoshiL.addStretch(1)
        babyyoshiL.addWidget(self.babyyoshi)
        q.addLayout(babyyoshiL)

        # Prequel ID
        self.prequel = QtWidgets.QLineEdit()
        self.prequel.setFixedWidth(40)
        self.prequel.setMaxLength(5)

        IDL = QtWidgets.QHBoxLayout()
        IDL.addWidget(QtWidgets.QLabel("Prequel ID:"))
        IDL.addWidget(self.prequel)
        q.addLayout(IDL)

        CGB.setLayout(q)

        BTMH = QtWidgets.QHBoxLayout()
        BTMH.addWidget(CGB)
        BTMH.addWidget(TGB)

        # Save button
        self.save = QtWidgets.QPushButton("Save this challenge")
        self.save.clicked.connect(self.saveFields)
        self.save.setEnabled(False)

        # Make a layout
        L = QtWidgets.QGridLayout()
        L.addWidget(self.ChallengeList)
        Challenges.setLayout(L)

        L = QtWidgets.QVBoxLayout()
        L.addLayout(starL)
        L.addWidget(category)
        L.addWidget(location)
        L.addWidget(UNKS)
        L.addLayout(BTMH)
        L.addWidget(self.save)
        Challenge.setLayout(L)

        # Make a main layout
        HL = QtWidgets.QHBoxLayout()
        HL.addWidget(Challenges)
        HL.addWidget(Challenge)
        L = QtWidgets.QVBoxLayout()
        L.addLayout(HL)

        self.setLayout(L)

    def setFile(self, file):
        """Changes the file to view"""
        self.file = file
        i = 1
        for item in self.file.challenges:
            li = QtWidgets.QListWidgetItem(str(i))
            self.ChallengeList.addItem(li)
            i += 1

        self.Category.addItems(("Time Attack", "Coin Collection", "1-UP Rally", "Special", "Boost Mode"))
        self.powerup.addItems(("Small", "Super Mushroom", "Fire Flower", "Mini Mushroom", "Propeller Mushroom", "Penguin Suit", "Ice Flower", "Acorn Mushroom", "P-Acorn Mushroom"))
        self.babyyoshi.addItems(("None", "Blue Baby Yoshi", "Pink Baby Yoshi", "Yellow Baby Yoshi*"))
        self.challenge = 0
        self.updateFields(self.challenge)

        # Enable buttons
        self.save.setEnabled(True)
        self.Category.setEnabled(True)
        self.powerup.setEnabled(True)
        self.babyyoshi.setEnabled(True)

    def saveFile(self):
        """Returns the file in saved form"""
        return self.file.save()

    def HandleDifferentChallenge(self, newitem, olditem):
        """Handles a different challenge being chosen"""
        self.challenge = self.ChallengeList.row(newitem)
        while self.stars.count() > 0:
            star = self.stars.itemAt(self.stars.count()-1).widget()
            star.hide()
            self.stars.removeWidget(star)
        self.updateFields(self.challenge)

    def updateFields(self, challenge):
        """Updates fields"""
        challenge = self.file.challenges[self.challenge]

        # Stars are special
        self.initstars(challenge)

        self.Category.setCurrentIndex( challenge.catid             )
        self.powerup.setCurrentIndex(  challenge.powerup           )
        self.babyyoshi.setCurrentIndex(challenge.babyyoshi         )
        self.WorldNum.setText(         str(challenge.world + 1)    )
        self.LevelNum.setText(         str(challenge.level + 1)    )
        self.id.setText(               str(challenge.id)           )
        self.prequel.setText(          str(challenge.prequel)      )
        self.time.setValue(            challenge.time              )
        self.unk3.setText(             str(challenge.unk3)         )
        self.unk4.setText(             str(challenge.unk4)         )
        self.unk5.setText(             str(challenge.unk5)         )
        self.unk6.setText(             str(challenge.unk6)         )
        self.unk7.setText(             str(challenge.unk7)         )
        self.unk8.setText(             str(challenge.unk8)         )
        self.unk9.setText(             str(challenge.unk9)         )
        self.unk10.setText(            str(challenge.unk10)        )
        self.area.setText(             str(challenge.area + 1)     )
        self.entrance.setText(         str(challenge.entrance)     )
        self.unk15.setText(            str(challenge.unk15)        )
        self.unk16.setText(            str(challenge.unk16)        )
        self.goldenminimum.setText(    str(challenge.goldenminimum))
        self.silverminimum.setText(    str(challenge.silverminimum))
        self.bronzeminimum.setText(    str(challenge.bronzeminimum))

    def initstars(self, challenge):
        """Inits the stars"""
        if challenge.stars < 5:
            self.starsplus.setEnabled(True)
        else:
            challenge.stars = 5
            self.starsplus.setEnabled(False)
        
        if challenge.stars > 1:
            self.starsmin.setEnabled(True)
        else:
            challenge.stars = 1
            self.starsmin.setEnabled(False)

        for i in range(challenge.stars):
            star = QtWidgets.QLabel()
            star.setPixmap(QtGui.QPixmap("images/star.png"))
            self.stars.addWidget(star)

    def saveFields(self, eventsthatarenotneededbutneedtobeherebecauseotherwisethesignatureswontmatch):
        """Save all fields"""
        challenge = self.file.challenges[self.challenge]

        challenge.catid =         self.Category.currentIndex()
        challenge.powerup =       self.powerup.currentIndex()
        challenge.babyyoshi =     self.babyyoshi.currentIndex()
        challenge.world =         int(self.WorldNum.text()) - 1
        challenge.level =         int(self.LevelNum.text()) - 1
        challenge.id =            int(self.id.text())
        challenge.prequel =       int(self.prequel.text())
        challenge.time =          self.time.value()
        challenge.stars =         self.stars.count()
        challenge.entrance =      int(self.entrance.text())
        challenge.unk3 =          int(self.unk3.text())
        challenge.unk4 =          int(self.unk4.text())
        challenge.unk5 =          int(self.unk5.text())
        challenge.unk6 =          int(self.unk6.text())
        challenge.unk7 =          int(self.unk7.text())
        challenge.unk8 =          int(self.unk8.text())
        challenge.unk9 =          int(self.unk9.text())
        challenge.unk10 =         int(self.unk10.text())
        challenge.area  =         int(self.area.text()) - 1
        challenge.unk15 =         int(self.unk15.text())
        challenge.unk16 =         int(self.unk16.text())
        challenge.goldenminimum = int(self.goldenminimum.text())
        challenge.silverminimum = int(self.silverminimum.text())
        challenge.bronzeminimum = int(self.bronzeminimum.text())

    def addStar(self, stuff):
        """Adds a star"""
        self.file.challenges[self.challenge].stars += 1
        stars = self.file.challenges[self.challenge].stars
        
        star = QtWidgets.QLabel()
        star.setPixmap(QtGui.QPixmap("images/star.png"))
        self.stars.addWidget(star)

        if stars < 5:
            self.starsplus.setEnabled(True)
        else:
            self.starsplus.setEnabled(False)
        if stars > 1:
            self.starsmin.setEnabled(True)
        else:
            self.starsmin.setEnabled(False)

    def removeStar(self, stuff):
        """Removes a star"""
        self.file.challenges[self.challenge].stars -= 1
        stars = self.file.challenges[self.challenge].stars
        
        star = self.stars.itemAt(self.stars.count()-1).widget() 
        star.hide()
        self.stars.removeWidget(star)

        if stars > 1:
            self.starsmin.setEnabled(True)
        else:
            self.starsmin.setEnabled(False)
        if stars < 5:
            self.starsplus.setEnabled(True)
        else:
            self.starsplus.setEnabled(False)


class MainWindow(QtWidgets.QMainWindow):
    """Main window"""
    def __init__(self):
        """Initialises the window"""
        QtWidgets.QMainWindow.__init__(self)
        self.fp = None # file path

        # Create the viewer
        self.view = ChallengeViewer()
        self.setCentralWidget(self.view)

        # Create the menubar and a few actions
        self.CreateMenubar()

        # Set window title and show the window
        self.setWindowTitle('Challenge Editor')
        self.show()

    def CreateMenubar(self):
        """Sets up the menubar"""
        m = self.menuBar()

        # File Menu
        f = m.addMenu('&File')

        openAct = f.addAction('Open File...')
        openAct.setIcon(QtGui.QIcon("images/open.png"))
        openAct.setShortcut('Ctrl+O') 
        openAct.triggered.connect(self.HandleOpen)

        self.saveAct = f.addAction('Save File')
        self.saveAct.setIcon(QtGui.QIcon("images/save.png"))
        self.saveAct.setShortcut('Ctrl+S')
        self.saveAct.triggered.connect(self.HandleSave)
        self.saveAct.setEnabled(False)

        self.saveAsAct = f.addAction('Save File As...')
        self.saveAsAct.setIcon(QtGui.QIcon("images/saveas.png"))
        self.saveAsAct.setShortcut('Ctrl+Shift+S')
        self.saveAsAct.triggered.connect(self.HandleSaveAs)
        self.saveAsAct.setEnabled(False)

        f.addSeparator()

        exitAct = f.addAction('Exit')
        exitAct.setIcon(QtGui.QIcon("images/exit.png"))
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.HandleExit)

        # Help Menu
        h = m.addMenu('&Help')

        aboutAct = h.addAction('About...')
        aboutAct.setIcon(QtGui.QIcon("images/about.png"))
        aboutAct.setShortcut('Ctrl+H')
        aboutAct.triggered.connect(self.HandleAbout)

    def HandleOpen(self):
        """Handles file opening"""
        fp = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'Challenge data files (*.exbin);;All Files (*.*)')[0]
        if fp == '': return
        self.fp = fp

        # Open the file
        file = open(fp, 'rb')
        data = file.read()
        file.close()
        FileData = File(data)

        # Update the viewer with this data
        self.view.setFile(FileData)

        # Enable saving
        #a = False
        a = True
        self.saveAct.setEnabled(a)
        self.saveAsAct.setEnabled(a)

    def HandleSave(self):
        """Handles file saving"""
        data = self.view.saveFile()

        # Open, write and close
        file = open(self.fp, 'wb')
        file.write(data)
        file.close()

    def HandleSaveAs(self):
        """Handles saving to a new file"""
        fp = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'Challenge data files (*.exbin);;All Files (*.*)')[0]
        if fp == '': return
        self.fp = fp

        # Save it
        self.HandleSave()

        # Enable saving
        #self.saveAct.setEnabled(True)

    def HandleExit(self):
        """Exits"""
        raise SystemExit

    def HandleAbout(self):
        """Shows the About dialog"""
        try: readme = open('about.txt', 'r').read()
        except: readme = 'Challenge Data Editor %s by Grop\n(No about.txt found!)\nLicensed under GPL 3' % version

        txtedit = QtWidgets.QPlainTextEdit(readme)
        txtedit.setReadOnly(True)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(txtedit)
        layout.addWidget(buttonBox)

        dlg = QtWidgets.QDialog()
        dlg.setLayout(layout)
        dlg.setModal(True)
        dlg.setWindowTitle('Challenge Editor - About')

        buttonBox.accepted.connect(dlg.accept)
        dlg.exec_()

# Main function
def main():
    """Main startup function"""
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())

main()