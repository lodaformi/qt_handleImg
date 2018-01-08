# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import sys
import os
import time
import traceback

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from  myWidget import ImageRecogWidget

class detectionInterface(QWidget):
    def __init__(self, parent=None):
        super(detectionInterface, self).__init__(parent)
        self.setWindowTitle("detection")
        self.setMinimumSize(1000,900)

        self.imageRecogWidget = ImageRecogWidget()

        self.layout = QHBoxLayout()
        # self.layout.setSpacing(30)
        # self.layout.setMargin(50)

        self.layout.addWidget(self.imageRecogWidget)
        self.setLayout(self.layout)

    # def excepthook(excType, excValue, tracebackobj):
    #     """
    #     Global function to catch unhandled exceptions.
    #     @param excType exception type
    #     @param excValue exception value
    #     @param tracebackobj traceback object
    #     """
    #     separator = '-' * 80
    #     logFile = os.path.join("simple.log")
    #     notice = \
    #         """An unhandled exception occurred. Please report the problem\n"""\
    #         """using the error reporting dialog or via email to <%s>.\n"""\
    #         """A log has been written to "%s".\n\nError information:\n""" % \
    #         ("yourmail at server.com", logFile)
    #     versionInfo = "0.0.1"
    #     timeString = time.strftime("%Y-%m-%d, %H:%M:%S")
    #
    #     tbinfofile = StringIO()
    #     traceback.print_tb(tracebackobj, None, tbinfofile)
    #     tbinfofile.seek(0)
    #     tbinfo = tbinfofile.read()
    #     errmsg = '%s: \n%s' % (str(excType), str(excValue))
    #     sections = [separator, timeString, separator, errmsg, separator, tbinfo]
    #     msg = '\n'.join(sections)
    #     try:
    #         with open(logFile, "w") as f:
    #             f.write(msg)
    #             f.write(versionInfo)
    #     except IOError:
    #         pass
    #     errorbox = QMessageBox()
    #     errorbox.setText(str(notice)+str(msg)+str(versionInfo))
    #     errorbox.setWindowTitle(' An Unhandled Exception Occurred')
    #     errorbox.exec_()
    #
    # sys.excepthook = excepthook

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    di = detectionInterface()
    di.show()
    sys.exit(app.exec_())