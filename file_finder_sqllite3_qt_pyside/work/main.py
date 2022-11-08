import sys
from PySide import QtGui

import UI

'''
A script created using sqlite3 and QT for a job test 
'''

if __name__ == '__main__':
    qt_app = QtGui.QApplication(sys.argv)
    window = UI.FileFinder()
    window.show()
    qt_app.exec_()