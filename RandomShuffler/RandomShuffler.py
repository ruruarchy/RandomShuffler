'''
Description: a plugin to shuffle layers positions randomly

By ruruarchy

Special thanks to all Krita developers :D !

Developed from all publicly available information across the internet

'''


import sys , random 

from PyQt5 import QtTest
from PyQt5.QtCore import pyqtSlot, Qt, QPointF
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QPainter, QPalette, QPixmap, QImage, QBrush, QPen, QIcon
from PyQt5.QtWidgets import QWidget, QTabWidget, QListView, QVBoxLayout, QFrame #apakah semua ini diperlukan, hmmm entahlah biarin ja as long as workable
from krita import *

class RandomShufflerExtensionClass(Extension):                                  #baru tau bisa 2 class dalam 1 file, sangat bermanfaat, extension dipake untuk shorcut
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):                                                            #default harus ada, tanpa ini jadinya NotImplementedError: Extension.setup() is abstract and must be overridden
        pass 

    def createActions(self, window):                                            #dipakai untuk mengkonek kan ke file yang .action yg isinya ada shortcut 7 dan 8
        action = window.createAction("shuffle_action", "Random_Shuffler.shuffle!")
        action.triggered.connect(RandomShufflerDockerClass.shuffle)
        action = window.createAction("area_shuffle_action", "Random_Shuffler.area_shuffle!")
        action.triggered.connect(RandomShufflerDockerClass.area_shuffle)

Krita.instance().addExtension(RandomShufflerExtensionClass(Krita.instance()))   #darisononya darisananya

 
class RandomShufflerDockerClass(DockWidget):                                    #dockwidget dipake untuk tampilan di docker
    def __init__(self):                                                         #Init the docker
        super(RandomShufflerDockerClass, self).__init__()
       
        self.main_scroll = QScrollArea()
        self.main_scroll .setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.main_scroll .setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.main_scroll .setWidgetResizable(True)

        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        widget1 = QWidget()
        widget2 = QWidget()
        widget3 = QWidget()
        widget1 .setMinimumWidth(1)                                              #can be shrinked really smol
        widget1 .setMinimumHeight(1)

        self.how_to_use_btn       = QPushButton()
        self.shuffle_btn          = QPushButton()
        self.area_shuffle_btn     = QPushButton()
        self.how_to_use_textEdit  = QTextEdit()
        self.checkbox1            = QCheckBox()
        self.checkbox2            = QCheckBox()
        self.checkbox3            = QCheckBox()
        self.how_to_use_dialog    = QDialog()
        self.warning              = QMessageBox()

        self.how_to_use_dialog .resize(670,480)
        self.how_to_use_btn    .setText("how_to_use")
        self.shuffle_btn       .setText("shuffle!")
        self.area_shuffle_btn  .setText("area_shuffle!")
        self.checkbox3         .setText("use_non_rectangular_selection, slower") #slower, precise, but not within area yet, (slower at first only, each change selection shape e.g re-select, after that, fast)
        self.checkbox2         .setText("keep_within_area ( rectangular_only )")
        self.checkbox1         .setText("debug_stuff")

        self.how_to_use_btn    .clicked.connect(self.how_to_use)
        self.shuffle_btn       .clicked.connect(self.shuffle)
        self.area_shuffle_btn  .clicked.connect(self.area_shuffle)
        self.checkbox1         .clicked.connect(self.debug_stuff)
        self.checkbox2         .stateChanged.connect(self.ch2_state_changed)
        self.checkbox3         .stateChanged.connect(self.ch3_state_changed)
        self.checkbox2         .setChecked(True)                                 #default true karna lebih bagus
        self.checkbox3         .setChecked(False)                                #buat defaultnya false aja, kalo perlu ja tinggal dicentang

        global lab1                                                              #lab -> label
        global lab2
        lab1  = QLabel('selected_layers = ')
        lab2  = QLabel('layer_pos\'s = ')

        layout1.addWidget(self.main_scroll)
        layout2.addWidget(self.how_to_use_btn)
        layout2.addWidget(self.shuffle_btn)
        layout2.addWidget(self.area_shuffle_btn)
        layout2.addWidget(self.checkbox3)
        layout2.addWidget(self.checkbox2)
        layout2.addWidget(self.checkbox1)
        layout2.addWidget(lab1)
        layout2.addWidget(lab2)
        layout3.addWidget(self.how_to_use_textEdit)
        widget1.setLayout(layout1)
        widget2.setLayout(layout2)

        lab1.setVisible(False)
        lab2.setVisible(False)

        self.main_scroll        .setWidget(widget2)
        self.how_to_use_dialog  .setLayout(layout3)
        self.how_to_use_dialog  .setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.how_to_use_dialog  .setWindowTitle(i18n("Random_Shuffler"))
        self.warning            .setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
        global storedpxd
        storedpxd = QByteArray()
        global list_pxd
        list_pxd  = []
        
        global ch2_checked                                                   #ch -> checkbox
        ch2_checked = True
        global ch3_checked
        ch3_checked = False

        self.setWidget(widget1)                                              #Add the widget to the docker.
               
        self.how_to_use_textEdit.setPlainText('''How to Use :

--shuffle!--
1. select the layers ( at least 2 layers )
2. click shuffle!

--area_shuffle!--
1. select area using RectangularSelection tool
2. select the layers
3. click area_shuffle!

you can change the shortcut in Settings > Configure Krita > Keyboard Shorcuts > look on Scripts > RandomShuffler
current shotcut is 7 for shuffle! and 8 for area_shuffle!

Limitation :
1. only usable for Paint Layers type, haven't tried the others
2. area_shuffle! 2/more selection area interpreted as 1 selection area 
3. position anchor using topleft of the layers (default)
4. area_shuffle! selection : rectangular shape only (min x,y max x,y)
5. area_shuffle! use_non_rectangular_selection can't keep positions within area
6. beware! be aware : there's no undo yet so we'd better to duplicate the layers first for initial positions, (except if it doesn't matter) <----‼️‼️‼️

Updates :
V4 -- area_shuffle! use_non_rectangular_selection added
number 2 & 4 fix by V4 but the limitation is doesn't have keep_within_area yet, seem's complicated
number 1 if using vector layer, its broken goes to somewhere after some clicks, mean to be used for PaintLayer
number 3 mean as shuffle! based anchor, now using center, looks more approriate
add previews on github
''')
        
        
        QtCore.QTimer.singleShot(100, self.shrink_title)                     #hacky way to make shrinkable title, only works once, before maximized/docked window, dont know yet how and why which cause that hmmm... behaviour


    def canvasChanged(self, canvas):                                         #diperlukan gatau kenapa tanpa ini error
        pass
        
    def how_to_use(self):                                                    #membuka how to use dialog
        self.how_to_use_dialog.open()

    def debug_stuff(self):                                                   #menampilkan label untuk mengecek di beberapa line of codes nya, ndebug
        if self.checkbox1.isChecked():
            lab1.setVisible(True)
            lab2.setVisible(True)   
        else :
            lab1.setVisible(False)
            lab2.setVisible(False)

    def shrink_title(self): 
        self.setWindowTitle(i18n("Random_Shuffler"))                         #dont know how, this was used for name on the docker list, dipake sama singleshot

    def shuffle(self):    
        suflist = []
        w = Krita.instance().activeWindow()
        v = w.activeView()
        selected_nodes = v.selectedNodes()                                   #ambil layer yang diseleksi
        
        for i in range(0,len(selected_nodes)):                               #mengisi suflist dengan posisi awal nya selected layers
            suflist.append(selected_nodes[i].bounds().center())              #pakai center, topLeft ada
        
        abc ='layer_pos\'s = '
        for i in suflist :                                                   #melihat isi suflist
            abc += "["+str(i.x())+','+str(i.y())+"]  "
        lab2.setText(str(abc) )

        random.shuffle(suflist)                                              #mengacak isi suflist

        for i in range(0,len(selected_nodes)):                               #mindah posisinya sesuai hasil sufle di suflist
            bb = selected_nodes[i].bounds() 
            selected_nodes[i].move( (selected_nodes[i].position().x()-(bb.x()-suflist[i].x())) - (bb.center().x()-bb.x()) , (selected_nodes[i].position().y()-(bb.y()-suflist[i].y())- (bb.center().y()-bb.y()) ) )

        doc = Krita.instance().activeDocument()
        if self == False :                                                   #ternyata = ngeklik di Tools > Scripts    #ternyata no.2 - ternyata ngeklik shorcut dari sini juga
            if doc == None :
                warning              = QMessageBox()
                warning.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                warning.setText('open a document / file first.           ')
                warning.exec()
                return

        if doc == None :
            self.warning.setText('open a document / file first           ')
            self.warning.open()
            return

        doc.refreshProjection()
        lab1.setText('selected_layers = '+ str(len(selected_nodes)) +' layer' )
        
    def ch2_state_changed(self):                                             #dipake untuk globvar karena 441&493
        global ch2_checked
        if self.checkbox2.isChecked():
            ch2_checked = True
        else :    
            ch2_checked = False

    def ch3_state_changed(self):    
        global ch3_checked
        if self.checkbox3.isChecked():
            ch3_checked = True
        else :    
            ch3_checked = False

    def area_shuffle(self):                                                  #mengacak posisi layer yang diseleksi secara random sesuai area yang diseleksi      
        list_baru = []
        w = Krita.instance().activeWindow()
        v = w.activeView()
        layer_yang_terseleksi = v.selectedNodes()                            #ambil layer yang diseleksi, return list
        doc = Krita.instance().activeDocument()
        zxcc = []

        if self == False :                                                   #checker ngeklik dari Tools > Scripts > Random_Shuffler.area_shuffle!/shuffle!
            if doc == None :
                warning = QMessageBox()
                warning.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                warning.setText('open a document / file first.           ')
                warning.exec()
                return                                                       #wajib ada, ga ada ini kelanjut code berikutnya

            elif doc.selection() == None :
                warning = QMessageBox()
                warning.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                warning.setText('select area first.           ')
                warning.exec()
                return 

        if doc == None :                                                     #belum membuka file
             self.warning.setText('open a document / file first           ') #untuk makan makan bersama #becanda xD
             self.warning.open()
             return
             
        if doc.selection() == None : 
             self.warning.setText('select area first           ')            #sudah membuka file, belum seleksi area
             self.warning.open()
             return
             
        global ch3_checked                                                   #pake globvar biar bisa diakses sama extensionclass               
        if ch3_checked == True :                                             #pakai non rectangular selection kayak lasso dsj 
            dc = doc.selection()
            pxd = dc.pixelData(dc.x(),dc.y(),dc.width(),dc.height())
            global list_pxd
            global storedpxd
            list_ambil = []
            
            if pxd == storedpxd :                                            #lewati proses kalo seleksinya sama(tdk dirubah), langsung ke move saja
                pass
            
            else:                                                            #simpan pixeldatanya biar kalo sama gausa di calc lagi
                storedpxd = pxd                                              #lanjut proses
                list_pxd.clear()                                             #tanpa ini keappend ketumpuk karena global jadi perlu di clear biar kosong isinya

                for i in range(pxd.size()):                                  #loop code yg keren bet, berfungsi untuk membuat real koordinat di pixel data pada titik tertentu (urut dari kiri ke kanan, row 1 ke row 2 up to widht height pada selesksi dgn posisi x,y)
                    if 'xff' in str(pxd.at(i)) :
                        x = dc.x()
                        y = dc.y()
                        w = dc.width()
                        x_coord = 0
                        y_coord = 0

                        if (i+1) % w == 0:                                   #njilimet tapi alhamdulillah bisa, workable yayy
                            x_coord = x + ( w - 1 )
                            y_coord = y + ( ( (i+1) / w )- 1 )
                        else :
                            x_coord = x + ( ( (i+1) % w )- 1 )
                            y_coord = y + int( (i+1) / w )
 
                        list_pxd.append(QPoint(x_coord,y_coord))
                        
                    else :                                                   #selain xff lewati (tidak terseleksi dsj, qbytearray base16 hexadecimal tampaknya)
                        pass
            
            list_ambil = random.sample(list_pxd, k= len(layer_yang_terseleksi))

            for i in range(0,len(layer_yang_terseleksi)):                    #mindah posisinya sesuai hasil sufle di list_ambil
                bb = layer_yang_terseleksi[i].bounds()
                layer_yang_terseleksi[i].move(layer_yang_terseleksi[i].position().x()-(bb.x()-list_ambil[i].x()) , layer_yang_terseleksi[i].position().y()+(list_ambil[i].y()-bb.y()))

            lab1.setText('selected_layers = '+ str(len(layer_yang_terseleksi)) +' layer' )
            abc ='layer_pos\'s = '
            for i in list_ambil :                                              
                abc += "["+str(i.x())+','+str(i.y())+"]  "
            lab2.setText(str(abc) )
            doc.refreshProjection()
            return
        else :
            pass

        x_max = doc.selection().x() + doc.selection().width()
        y_max = doc.selection().y() + doc.selection().height()

        global ch2_checked                                                   #pake globvar biar bisa diakses sama extensionclass               
        if ch2_checked == True :                                             #pakai keep within area (rectangular selection only)
            for i in range(0,len(layer_yang_terseleksi)):                    #mengisi list_baru dengan posisi awal
                list_baru.append(QPoint( random.randrange(doc.selection().x(),x_max),random.randrange(doc.selection().y(),y_max) )) #yrand bisa largerthan ymax
               
            for i in range(0,len(layer_yang_terseleksi)):
                bound = layer_yang_terseleksi[i].bounds()
                
                if (list_baru[i].y()+ bound.height()) >= y_max :
                    list_baru[i].setY( y_max - bound.height() )
                if (list_baru[i].x()+ bound.width()) >= x_max :
                    list_baru[i].setX( x_max - bound.width() )

        else :
            for i in range(0,len(layer_yang_terseleksi)):                    #mengisi suflist dengan posisi awal
                list_baru.append(QPoint( random.randrange(doc.selection().x(),x_max),random.randrange(doc.selection().y(),y_max) )) #yrand bisa largerthan ymax

        for i in range(0,len(layer_yang_terseleksi)):                        #mindah posisinya sesuai hasil sufle di suflist
            bb = layer_yang_terseleksi[i].bounds()
            layer_yang_terseleksi[i].move(layer_yang_terseleksi[i].position().x()-(bb.x()-list_baru[i].x()) , layer_yang_terseleksi[i].position().y()+(list_baru[i].y()-bb.y()))

        lab1.setText('selected_layers = '+ str(len(layer_yang_terseleksi)) +' layer' )
        abc ='layer_pos\'s = '
        for i in list_baru :                                                 #melihat isi list_baru
            abc += "["+str(i.x())+','+str(i.y())+"]  "
        lab2.setText(str(abc) )
        doc.refreshProjection()                                              #wiiiiiiii sugoiiiiiiii xD , sangat bermanfaat, sebelumnya tampak ga ngefek kecuali di hide show layernya


Application.addDockWidgetFactory(DockWidgetFactory("RandomShuffler", DockWidgetFactoryBase.DockRight, RandomShufflerDockerClass)) # Add docker to the application :) !



#log perubahan
# V1   : shuffle biasa
# V2   : area suffle added
# V2.5 : add how to use, debug stuff, dsj
# V3   : area_shuffle! keep within area added
# V4   : area_shuffle! bisa pakai non rectangular selection 


#next thing to do, available thing to do
#keep within area yang versi non rectangular selection (lebih sulit)
#nambah scale, rotate dsj
#nambah undoable/ previous next
#nambah semacam save load kalau perlu nyimpan urutannya
#nambah move along path kalau bisa di compress samller size slamer size smaller size
#warna random ?? < terlihat sangat advanced, mungkin bisanya klo vector
#anchor shuffle nya diberi opsi 9 
#hanya ide saja : shrink if area smaller than layers

#bisa dibayangkan = 50/50 bisa diwujudkan, tergantung realita nya

#found bug:
#441 bool object has no attribute checkbox3 > kalo pake shortcut selfnya tidak kedetect karna beda kelas kayaknya
#441 self = False soalnya diakses dari shrtcut tampaknya berupa yang extensionclass sedangkan disana ga ada definisinya
#441 ketemu RecursionError maximum recursion depth exceeded while calling a python object 
#441 fix checkbox3 via shortcut by add some codes
#493 RuntimeError: wrapped C/C++ object of type QLabel has been deleted
#493 tampaknya karena tidak diberi self.label = Qlabel() tapi hanya label = Qlabel() jadinya kena flush
#done 441&493 by nambai globvar untuk extensionclass biar bisa ke akses
