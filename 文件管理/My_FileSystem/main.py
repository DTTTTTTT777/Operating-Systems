import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.Qt import *
from MainForm import *

if __name__=='__main__':
    app=QApplication(sys.argv)

    mainform=mainForm()

    mainform.show()

    sys.exit(app.exec_())

