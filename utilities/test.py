from PyQt4 import QtCore, QtGui
import sys

class myWindow(QtGui.QWidget):
	def __init__(self, parent=None):
		super(myWindow, self).__init__(parent)
		myLayout = QtGui.QVBoxLayout(self)
		Button = QtGui.QPushButton('Resize')
		myLayout.addWidget(Button)
		Button.setMinimumWidth(200)
		Button.clicked.connect(self.resizeDialog)

	def resizeDialog(self):
		self.animation = QtCore.QPropertyAnimation(self, "size")
		self.animation.setDuration(1000) #Default 250ms
		if self.size().width()==200:
			self.animation.setEndValue(QtCore.QSize(600,300))
		else:
			self.animation.setEndValue(QtCore.QSize(200,100))
		self.animation.start()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('myApp')
    dialog = myWindow()
    dialog.resize(200,100)
    dialog.show()
    sys.exit(app.exec_())
