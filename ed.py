
#! /usr/bin/python
# event3.py
# draws mouse points & prints x,y
# see http://www.riverbankcomputing.com/pipermail/pyqt/2008-September/020562.html
# see http://harmattan-dev.nokia.com/docs/library/html/qt4/qpoint.html#details
# bigger example http://ftp.ics.uci.edu/pub/centos0/ics-custom-build/BUILD/PyQt-x11-gpl-4.7.2/examples/widgets/scribble.py
# event3.py
#
from qt import *
import sys

# check out this QT serial library http://qt-project.org/wiki/QtSerialPort
# in leiu of serial port, redirect stdout  to file, then send file with comms program:
#  ~$ python ./event3.py >gcd.gcd


# LogFileName = None             # "print" Does not work inside of Python's IDLE
LogFileName = "stdout"         # a clue.. ..sys.stdout.write() does not work either

LogFileName = "Log.txt"      # Works inside with IDLE


# print "LogFileName: %s" % ( LogFileName )
# print "LogFileName: %s" % ( LogFileName )

# set origin offset
print 'g92 x0 y0'

# feedrate speed
print 'f10000'

# drive motors to 0, 0
print 'g0 x0 y0'

#-------

def Log_String( String, InitFile=False ) :
    if(   LogFileName == None )     :  print String

    elif( LogFileName == "stdout" ) :  sys.stdout.write( String )

    else :
        LogFile = open( "Log.txt", 'w' if(InitFile) else 'a' )
        LogFile.write( String + '\n' )
        LogFile.close()


#---

class Painting(QWidget):

    def __init__(self, *args):
        apply(QWidget.__init__,(self, ) + args)
        self.buffer = QPixmap()

    def paintEvent(self, ev):
        # blit the pixmap
        bitBlt(self, 0, 0, self.buffer)

    def mouseMoveEvent(self, ev):
        self.p = QPainter()
        self.p.begin(self.buffer)
        self.p.drawLine(self.currentPos, ev.pos())
        self.currentPos=QPoint(ev.pos())
        vx=self.currentPos.x()
        vy=self.currentPos.y()
        print 'G1','X'+str(vx),'Y'+str(vy)
        self.p.flush()
        self.p.end()
        bitBlt(self, 0, 0, self.buffer)

    def mousePressEvent(self, ev):
        self.p = QPainter()
        self.p.begin(self.buffer)
        self.p.drawPoint(ev.pos())
        self.currentPos=QPoint(ev.pos())
        self.p.flush()
        self.p.end()
        bitBlt(self, 0, 0, self.buffer)

    def resizeEvent(self, ev):
        tmp = QPixmap(self.buffer.size())
        bitBlt(tmp, 0, 0, self.buffer)
        self.buffer.resize(ev.size())
        self.buffer.fill()
        bitBlt(self.buffer, 0, 0, tmp)

class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,) + args)
        self.painting=Painting(self)
        self.setCentralWidget(self.painting)

def main(args):
  app=QApplication(args)
  win=MainWindow()
  win.show()
  app.connect(app, SIGNAL("lastWindowClosed()")
                 , app
                 , SLOT("quit()")
                 )
  app.exec_loop()

if __name__=="__main__":
  main(sys.argv)
