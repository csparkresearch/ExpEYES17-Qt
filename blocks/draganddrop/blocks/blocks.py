#!/usr/bin/env python

############################################################################
#
#  Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
#
#  This file is part of the example classes of the Qt Toolkit.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  self file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
#
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact the
#  sales department at sales@trolltech.com.
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
############################################################################

# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QVariant', 2)

from __future__ import print_function

import os
from PyQt4 import QtCore, QtGui

import blocks_rc


class BlockWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(BlockWidget, self).__init__(parent)

        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QtCore.QRect()
        self.inPlace = 0

        self.setAcceptDrops(True)
        self.setMinimumSize(400, 400)
        self.setMaximumSize(400, 400)

    def clear(self):
        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QtCore.QRect()
        self.inPlace = 0
        self.update()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('image/x-Block-piece'):
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        updateRect = self.highlightedRect
        self.highlightedRect = QtCore.QRect()
        self.update(updateRect)
        event.accept()

    def dragMoveEvent(self, event):
        updateRect = self.highlightedRect.unite(self.targetSquare(event.pos()))

        if event.mimeData().hasFormat('image/x-Block-piece') and self.findPiece(self.targetSquare(event.pos())) == -1:
            self.highlightedRect = self.targetSquare(event.pos())
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            self.highlightedRect = QtCore.QRect()
            event.ignore()

        self.update(updateRect)

    def dropEvent(self, event):
        if event.mimeData().hasFormat('image/x-Block-piece') and self.findPiece(self.targetSquare(event.pos())) == -1:
            pieceData = event.mimeData().data('image/x-Block-piece')
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            square = self.targetSquare(event.pos())
            pixmap = QtGui.QPixmap()
            dataStream >> pixmap

            self.piecePixmaps.append(pixmap)
            self.pieceRects.append(square)

            self.hightlightedRect = QtCore.QRect()
            self.update(square)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

        else:
            self.highlightedRect = QtCore.QRect()
            event.ignore()

    def findPiece(self, pieceRect):
        try:
            return self.pieceRects.index(pieceRect)
        except ValueError:
            return -1

    def mousePressEvent(self, event):
        square = self.targetSquare(event.pos())
        found = self.findPiece(square)

        if found == -1:
            return

        pixmap = self.piecePixmaps[found]
        del self.piecePixmaps[found]
        del self.pieceRects[found]

        self.update(square)

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)

        dataStream << pixmap

        mimeData = QtCore.QMimeData()
        mimeData.setData('image/x-Block-piece', itemData)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - square.topLeft())
        drag.setPixmap(pixmap)

        if drag.exec_(QtCore.Qt.MoveAction) != QtCore.Qt.MoveAction:
            self.piecePixmaps.insert(found, pixmap)
            self.pieceRects.insert(found, square)
            self.update(self.targetSquare(event.pos()))

            if location == QtCore.QPoint(square.x() / 80, square.y() / 80):
                self.inPlace += 1

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QtCore.Qt.white)

        if self.highlightedRect.isValid():
            painter.setBrush(QtGui.QColor("#ffcccc"))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRect(self.highlightedRect.adjusted(0, 0, -1, -1))

        for rect, pixmap in zip(self.pieceRects, self.piecePixmaps):
            painter.drawPixmap(rect, pixmap)

        painter.end()

    def targetSquare(self, position):
        return QtCore.QRect(position.x() // 80 * 80, position.y() // 80 * 80, 80, 80)


class componentsList(QtGui.QListWidget):
    def __init__(self, parent=None):
        super(componentsList, self).__init__(parent)

        self.setDragEnabled(True)
        self.setViewMode(QtGui.QListView.IconMode)
        self.setIconSize(QtCore.QSize(60, 60))
        self.setSpacing(10)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('image/x-Block-piece'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('image/x-Block-piece'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('image/x-Block-piece'):
            pieceData = event.mimeData().data('image/x-Block-piece')
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            pixmap = QtGui.QPixmap()
            dataStream >> pixmap

            self.addPiece(pixmap)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def addPiece(self, pixmap):
        """
        adds a pixmap, and returns the QListWidgetItem created
        """
        pieceItem = QtGui.QListWidgetItem(self)
        pieceItem.setIcon(QtGui.QIcon(pixmap))
        pieceItem.setData(QtCore.Qt.UserRole, pixmap)
        pieceItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
        return pieceItem

    def startDrag(self, supportedActions):
        item = self.currentItem()

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        pixmap = QtGui.QPixmap(item.data(QtCore.Qt.UserRole))

        dataStream << pixmap

        mimeData = QtCore.QMimeData()
        mimeData.setData('image/x-Block-piece', itemData)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            self.takeItem(self.row(item))


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.BlockImage = QtGui.QPixmap()

        self.setupMenus()
        self.setupWidgets()

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                QtGui.QSizePolicy.Fixed))
        self.setWindowTitle("Block")
        
    def load(self):
        """
        Loads a component composition
        """
        return
        
    def save(self):
        """
        Saves the current component composition
        """
        return
        
    def saveAs(self, filename=None):
        """
        Saves the current component composition in a new file
        @param filename name of the file, defaults to None
        """
        return
        
    def loadComponents(self, path=None):
        if not path:
            path = QtGui.QFileDialog.getExistingDirectory(self)

        if path:
            self.BlockImages=[]
            newImage=None
            for entry in sorted(os.listdir(path)):
                if entry.endswith('.svg'):
                    newImage = QtGui.QPixmap()
                    if not newImage.load(entry):
                        QtGui.QMessageBox.warning(self, "Open Image",
                                "The image file %s could not be loaded." %entry,
                                QtGui.QMessageBox.Cancel)
                        continue
                    else:
                        self.BlockImages.append(newImage)
            self.setupBlock()
        return

    def setCompleted(self):
        QtGui.QMessageBox.information(self, "Block Completed",
                "Congratulations! You have completed the Block!\nClick OK "
                "to start again.",
                QtGui.QMessageBox.Ok)

        self.setupBlock()

    def setupBlock(self):
        self.componentsList.clear()
        for img in self.BlockImages:
            item=self.componentsList.addPiece(img)
            self.componentsList.insertItem(0, item)
        self.BlockWidget.clear()
        return

    def setupMenus(self):
        fileMenu = self.menuBar().addMenu("&File")

        openAction = fileMenu.addAction("&Open...")
        openAction.setShortcut("Ctrl+O")

        saveAction = fileMenu.addAction("&Save...")
        openAction.setShortcut("Ctrl+S")

        exitAction = fileMenu.addAction("E&xit")
        exitAction.setShortcut("Ctrl+Q")


        openAction.triggered.connect(self.load)
        saveAction.triggered.connect(self.save)
        exitAction.triggered.connect(QtGui.qApp.quit)
        

    def setupWidgets(self):
        frame = QtGui.QFrame()
        frameLayout = QtGui.QHBoxLayout(frame)

        self.componentsList = componentsList()

        self.BlockWidget = BlockWidget()

        frameLayout.addWidget(self.componentsList)
        frameLayout.addWidget(self.BlockWidget)
        self.setCentralWidget(frame)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.loadComponents('.')
    window.show()
    sys.exit(app.exec_())
