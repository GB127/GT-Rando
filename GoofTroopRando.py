import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from main import generateFile
import random



import ctypes

# Query DPI Awareness (Windows 10 and 8)
awareness = ctypes.c_int()
errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
print(awareness.value)

# Set DPI Awareness  (Windows 10 and 8)
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
# the argument is the awareness level, which can be 0, 1 or 2:
# for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)

# Set DPI Awareness  (Windows 7 and Vista)
success = ctypes.windll.user32.SetProcessDPIAware()

class GT_GUI(QWidget):
    def __init__(self, parent = None):
        super(GT_GUI, self).__init__(parent)
        self.setGeometry(100, 100, 405, 322) 
        self.setWindowTitle("Goof Troop Randomizer V2.0")
        self.setFont(QtGui.QFont("Calibri", 10))
        
        
        #Source file
        self.btn1 = QPushButton("Select source file", self)
        self.btn1.clicked.connect(self.getfile)
        self.btn1.move(13,10)
        self.filenameBox = QLineEdit(self)
        self.filenameBox.move(118,11)
        self.filenameBox.setFixedWidth(274)

        #Exits
        self.labelExits = QLabel("EXITS", self)
        self.labelExits.move(15, 40)
        self.checkExits1 = QCheckBox("Randomize exits", self)
        self.checkExits1.move(18, 57)
        self.checkExits2 = QCheckBox("Unmatch exit direction", self)
        self.checkExits2.move(25, 74)
        self.checkExits3 = QCheckBox("Unpair exits", self)
        self.checkExits3.move(25, 91)

        self.checkExits1.toggled.connect(lambda checked: not checked and self.checkExits2.setChecked(False))
        self.checkExits1.toggled.connect(lambda checked: not checked and self.checkExits2.setEnabled(False))
        self.checkExits1.toggled.connect(lambda checked: checked and self.checkExits2.setEnabled(True))

        self.checkExits1.toggled.connect(lambda checked: not checked and self.checkExits3.setChecked(False))
        self.checkExits1.toggled.connect(lambda checked: not checked and self.checkExits3.setEnabled(False))
        self.checkExits1.toggled.connect(lambda checked: checked and self.checkExits3.setEnabled(True))

        self.checkExits2.setEnabled(False)
        self.checkExits3.setEnabled(False)

        #Items
        self.labelItems = QLabel("ITEMS",self)
        self.labelItems.move(15, 111)
        self.checkItems1 = QCheckBox("Shuffle items",self)
        self.checkItems1.move(18, 128)
        self.checkItems2 = QCheckBox("Totally random items",self)
        self.checkItems2.move(18, 145)

        self.checkItems1.toggled.connect(lambda checked: not checked and self.checkItems2.setChecked(False))
        self.checkItems1.toggled.connect(lambda checked: not checked and self.checkItems2.setEnabled(True))
        self.checkItems1.toggled.connect(lambda checked: checked and self.checkItems2.setEnabled(False))

        self.checkItems2.toggled.connect(lambda checked: not checked and self.checkItems1.setChecked(False))
        self.checkItems2.toggled.connect(lambda checked: not checked and self.checkItems1.setEnabled(True))
        self.checkItems2.toggled.connect(lambda checked: checked and self.checkItems1.setEnabled(False))

        #Dark
        self.labelDark = QLabel("DARK ROOMS",self)
        self.labelDark.move(15, 165)
        self.checkDark1 = QCheckBox("Remove dark rooms",self)
        self.checkDark1.move(18, 182)
        self.checkDark2 = QCheckBox("Randomize dark rooms",self)
        self.checkDark2.move(18, 199)
        self.checkDark3 = QCheckBox("Randomize and add more",self)
        self.checkDark3.move(18, 216)
        self.checkDark4 = QCheckBox("All rooms are dark",self)
        self.checkDark4.move(18, 233)

        self.checkDark1.toggled.connect(lambda checked: not checked and self.checkDark2.setChecked(False))
        self.checkDark1.toggled.connect(lambda checked: not checked and self.checkDark2.setEnabled(True))
        self.checkDark1.toggled.connect(lambda checked: checked and self.checkDark2.setEnabled(False))
        self.checkDark1.toggled.connect(lambda checked: not checked and self.checkDark3.setChecked(False))
        self.checkDark1.toggled.connect(lambda checked: not checked and self.checkDark3.setEnabled(True))
        self.checkDark1.toggled.connect(lambda checked: checked and self.checkDark3.setEnabled(False))
        self.checkDark1.toggled.connect(lambda checked: not checked and self.checkDark4.setChecked(False))
        self.checkDark1.toggled.connect(lambda checked: not checked and self.checkDark4.setEnabled(True))
        self.checkDark1.toggled.connect(lambda checked: checked and self.checkDark4.setEnabled(False))
        
        self.checkDark2.toggled.connect(lambda checked: not checked and self.checkDark1.setChecked(False))
        self.checkDark2.toggled.connect(lambda checked: not checked and self.checkDark1.setEnabled(True))
        self.checkDark2.toggled.connect(lambda checked: checked and self.checkDark1.setEnabled(False))
        self.checkDark2.toggled.connect(lambda checked: not checked and self.checkDark3.setChecked(False))
        self.checkDark2.toggled.connect(lambda checked: not checked and self.checkDark3.setEnabled(True))
        self.checkDark2.toggled.connect(lambda checked: checked and self.checkDark3.setEnabled(False))
        self.checkDark2.toggled.connect(lambda checked: not checked and self.checkDark4.setChecked(False))
        self.checkDark2.toggled.connect(lambda checked: not checked and self.checkDark4.setEnabled(True))
        self.checkDark2.toggled.connect(lambda checked: checked and self.checkDark4.setEnabled(False))

        self.checkDark3.toggled.connect(lambda checked: not checked and self.checkDark1.setChecked(False))
        self.checkDark3.toggled.connect(lambda checked: not checked and self.checkDark1.setEnabled(True))
        self.checkDark3.toggled.connect(lambda checked: checked and self.checkDark1.setEnabled(False))
        self.checkDark3.toggled.connect(lambda checked: not checked and self.checkDark2.setChecked(False))
        self.checkDark3.toggled.connect(lambda checked: not checked and self.checkDark2.setEnabled(True))
        self.checkDark3.toggled.connect(lambda checked: checked and self.checkDark2.setEnabled(False))
        self.checkDark3.toggled.connect(lambda checked: not checked and self.checkDark4.setChecked(False))
        self.checkDark3.toggled.connect(lambda checked: not checked and self.checkDark4.setEnabled(True))
        self.checkDark3.toggled.connect(lambda checked: checked and self.checkDark4.setEnabled(False))

        self.checkDark4.toggled.connect(lambda checked: not checked and self.checkDark1.setChecked(False))
        self.checkDark4.toggled.connect(lambda checked: not checked and self.checkDark1.setEnabled(True))
        self.checkDark4.toggled.connect(lambda checked: checked and self.checkDark1.setEnabled(False))
        self.checkDark4.toggled.connect(lambda checked: not checked and self.checkDark2.setChecked(False))
        self.checkDark4.toggled.connect(lambda checked: not checked and self.checkDark2.setEnabled(True))
        self.checkDark4.toggled.connect(lambda checked: checked and self.checkDark2.setEnabled(False))
        self.checkDark4.toggled.connect(lambda checked: not checked and self.checkDark3.setChecked(False))
        self.checkDark4.toggled.connect(lambda checked: not checked and self.checkDark3.setEnabled(True))
        self.checkDark4.toggled.connect(lambda checked: checked and self.checkDark3.setEnabled(False))


        #First frame
        self.labelFirst = QLabel("STARTING ROOM",self)
        self.labelFirst.move(200, 40)
        self.checkFirst1 = QCheckBox("Randomize starting room",self)
        self.checkFirst1.move(203, 57)

        #Icy
        self.labelIcy = QLabel("SLIPPERY/ICY ROOMS",self)
        self.labelIcy.move(200, 77)
        self.checkIcy1 = QCheckBox("Remove slippery rooms",self)
        self.checkIcy1.move(203, 94)
        self.checkIcy2 = QCheckBox("Randomize slippery rooms",self)
        self.checkIcy2.move(203, 111)
        self.checkIcy3 = QCheckBox("Randomize and add more",self)
        self.checkIcy3.move(203, 128)
        self.checkIcy4 = QCheckBox("All rooms are slippery",self)
        self.checkIcy4.move(203, 145)

        self.checkIcy1.toggled.connect(lambda checked: not checked and self.checkIcy2.setChecked(False))
        self.checkIcy1.toggled.connect(lambda checked: not checked and self.checkIcy2.setEnabled(True))
        self.checkIcy1.toggled.connect(lambda checked: checked and self.checkIcy2.setEnabled(False))
        self.checkIcy1.toggled.connect(lambda checked: not checked and self.checkIcy3.setChecked(False))
        self.checkIcy1.toggled.connect(lambda checked: not checked and self.checkIcy3.setEnabled(True))
        self.checkIcy1.toggled.connect(lambda checked: checked and self.checkIcy3.setEnabled(False))
        self.checkIcy1.toggled.connect(lambda checked: not checked and self.checkIcy4.setChecked(False))
        self.checkIcy1.toggled.connect(lambda checked: not checked and self.checkIcy4.setEnabled(True))
        self.checkIcy1.toggled.connect(lambda checked: checked and self.checkIcy4.setEnabled(False))

        self.checkIcy2.toggled.connect(lambda checked: not checked and self.checkIcy1.setChecked(False))
        self.checkIcy2.toggled.connect(lambda checked: not checked and self.checkIcy1.setEnabled(True))
        self.checkIcy2.toggled.connect(lambda checked: checked and self.checkIcy1.setEnabled(False))
        self.checkIcy2.toggled.connect(lambda checked: not checked and self.checkIcy3.setChecked(False))
        self.checkIcy2.toggled.connect(lambda checked: not checked and self.checkIcy3.setEnabled(True))
        self.checkIcy2.toggled.connect(lambda checked: checked and self.checkIcy3.setEnabled(False))
        self.checkIcy2.toggled.connect(lambda checked: not checked and self.checkIcy4.setChecked(False))
        self.checkIcy2.toggled.connect(lambda checked: not checked and self.checkIcy4.setEnabled(True))
        self.checkIcy2.toggled.connect(lambda checked: checked and self.checkIcy4.setEnabled(False))

        self.checkIcy3.toggled.connect(lambda checked: not checked and self.checkIcy1.setChecked(False))
        self.checkIcy3.toggled.connect(lambda checked: not checked and self.checkIcy1.setEnabled(True))
        self.checkIcy3.toggled.connect(lambda checked: checked and self.checkIcy1.setEnabled(False))
        self.checkIcy3.toggled.connect(lambda checked: not checked and self.checkIcy2.setChecked(False))
        self.checkIcy3.toggled.connect(lambda checked: not checked and self.checkIcy2.setEnabled(True))
        self.checkIcy3.toggled.connect(lambda checked: checked and self.checkIcy2.setEnabled(False))
        self.checkIcy3.toggled.connect(lambda checked: not checked and self.checkIcy4.setChecked(False))
        self.checkIcy3.toggled.connect(lambda checked: not checked and self.checkIcy4.setEnabled(True))
        self.checkIcy3.toggled.connect(lambda checked: checked and self.checkIcy4.setEnabled(False))

        self.checkIcy4.toggled.connect(lambda checked: not checked and self.checkIcy1.setChecked(False))
        self.checkIcy4.toggled.connect(lambda checked: not checked and self.checkIcy1.setEnabled(True))
        self.checkIcy4.toggled.connect(lambda checked: checked and self.checkIcy1.setEnabled(False))
        self.checkIcy4.toggled.connect(lambda checked: not checked and self.checkIcy2.setChecked(False))
        self.checkIcy4.toggled.connect(lambda checked: not checked and self.checkIcy2.setEnabled(True))
        self.checkIcy4.toggled.connect(lambda checked: checked and self.checkIcy2.setEnabled(False))
        self.checkIcy4.toggled.connect(lambda checked: not checked and self.checkIcy3.setChecked(False))
        self.checkIcy4.toggled.connect(lambda checked: not checked and self.checkIcy3.setEnabled(True))
        self.checkIcy4.toggled.connect(lambda checked: checked and self.checkIcy3.setEnabled(False))

        #Other
        self.labelOther = QLabel("OTHER STUFF",self)
        self.labelOther.move(200, 165)
        self.checkCheat = QCheckBox("Password cheat",self)
        self.checkCheat.move(203, 182)
        self.checkOHKO = QCheckBox("One hit KO",self)
        self.checkOHKO.move(203, 199)
        
        #Seed
        self.labelSeed = QLabel("SEED :",self)
        self.labelSeed.move(15, 260)
        self.seedBox = QLineEdit(self)
        self.seedBox.move(50,259)
        self.seedBox.setFixedWidth(325)

        #Generate
        self.btn2 = QPushButton("Generate randomized file", self)
        self.btn2.clicked.connect(self.generateFileButton)
        self.btn2.move(248,290)
        self.labelGenerate1 = QLabel("Generating file... could take a few minutes", self)
        self.labelGenerate1.move(13, 295)
        self.labelGenerate1.hide()
        self.labelGenerate2 = QLabel("Done!", self)
        self.labelGenerate2.move(13, 295)
        self.labelGenerate2.hide()
            
    def generateFileButton(self):
        filename = self.filenameBox.text()
        class struct(object): #simple structure to reproduce argparse's output
            pass
        options = struct()
        options.seed = self.seedBox.text()
        if options.seed == "":
            options.seed = str(random.random())[2:]
        options.Rexits = self.checkExits1.isChecked()
        options.Rexits_matchdir = not(self.checkExits2.isChecked())
        options.Rexits_pair = not(self.checkExits3.isChecked())
        options.Ritems_pos = self.checkItems1.isChecked()
        options.Ritems = self.checkItems2.isChecked()
        options.nodark = self.checkDark1.isChecked()
        options.Rdark = self.checkDark2.isChecked()
        options.Rverydark = self.checkDark3.isChecked()
        options.Adark = self.checkDark4.isChecked()
        options.Rfirst = self.checkFirst1.isChecked()
        options.noicy = self.checkIcy1.isChecked()
        options.Ricy = self.checkIcy2.isChecked()
        options.Rveryicy = self.checkIcy3.isChecked()
        options.Aicy = self.checkIcy4.isChecked()
        options.Wselect = self.checkCheat.isChecked()
        options.ohko = self.checkOHKO.isChecked()
        self.labelGenerate2.hide()
        self.labelGenerate1.show()
        self.repaint()
        generateFile(options, filename)
        self.labelGenerate1.hide()
        self.labelGenerate2.show()

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\')
        self.filenameBox.setText(fname[0])
            
    def getfiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter("Text files (*.txt)")
        filenames = QStringList()
            
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')
                
            with f:
                data = f.read()
                self.contents.setText(data)
				
def main():
    app = QApplication(sys.argv)
    ex = GT_GUI()
    ex.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    main()