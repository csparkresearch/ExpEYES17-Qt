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

import os, re, copy
from PyQt4 import QtCore, QtGui

import blocks_rc

class Component(object):
    def __init__(self, pixmap, ident, mimetype, rect=None, hotspot=None):
        super(Component, self).__init__()
        if rect:
            self.rect=rect
        else:
            self.rect=pixmap.rect()
        if hotspot:
            self.hotspot=hospot
        else:
            self.hotspot=QtCore.QPoint(pixmap.width()/2, pixmap.height()/2)
        self.pixmap=pixmap
        self.ident=ident
        self.mimetype=mimetype
        return
        
    def __str__(self):
        return "Component(%s, %s, %s, %s)" %(self.ident, self.mimetype, self.rect, self.hotspot)        

    def serialize(self):
        """
        serializes a component into a QDataStream
        returns dta as a QByteArray instance
        """
        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        dataStream << self.pixmap << self.mimetype << self.hotspot << self.ident
        return itemData

class BlockWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(BlockWidget, self).__init__(parent)

        self.components = []

        self.setAcceptDrops(True)
        self.setMinimumSize(400, 400)
        self.setMaximumSize(400, 400)

    def clear(self):
        self.components = []
        self.update()

    def acceptedFormats(self, event):
        return [f for f in event.mimeData().formats() \
                    if f.contains("image/x-Block-")]
                    
    def dragEnterEvent(self, event):
        if self.acceptedFormats(event):
           event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self.acceptedFormats(event):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
        return

    def dropEvent(self, event):
        f = self.acceptedFormats(event)
        if f:
            pieceData = event.mimeData().data(f[0])
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            pixmap = QtGui.QPixmap()
            mimetype = QtCore.QString()
            ident = QtCore.QString()
            hotspot = QtCore.QPoint()
            dataStream >> pixmap >> mimetype >> hotspot >> ident

            rect = QtCore.QRect((event.pos()-hotspot), pixmap.size())

            comp=Component(pixmap,ident,mimetype,rect)
            self.components.append(comp)

            self.hightlightedRect = QtCore.QRect()
            self.update(rect)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

        else:
            event.ignore()


    def mousePressEvent(self, event):
        comps=self.targetComps(event.pos())
        if not comps:
            return
        comp = comps[-1]
        index=self.components.index(comp)
        comp=copy.copy(comp)

        del self.components[index]

        self.update(comp.rect)

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        hot=QtCore.QPoint(event.pos() - comp.rect.topLeft())

        dataStream << comp.pixmap << comp.mimetype << hot << comp.ident

        mimeData = QtCore.QMimeData()
        mimeData.setData(comp.mimetype, itemData)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(hot)
        drag.setPixmap(comp.pixmap)

        if drag.exec_(QtCore.Qt.MoveAction) != QtCore.Qt.MoveAction:
            self.components.insert(index, comp)
            self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QtCore.Qt.white)
        
        l=[(c.rect, c.pixmap) for c in self.components]
        for rect, pixmap in l:
            painter.drawPixmap(rect, pixmap)

        painter.end()

    def targetComps(self, position):
        """
        returns the list of components
        under a mouse click; the topmost component comes last.
        """
        comps = [c for c in self.components if c.rect.contains(position)]
        return comps

class componentsList(QtGui.QListWidget):
    def __init__(self, parent=None):
        super(componentsList, self).__init__(parent)

        self.setDragEnabled(True)
        self.setViewMode(QtGui.QListView.IconMode)
        self.setIconSize(QtCore.QSize(60, 60))
        self.setSpacing(10)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def acceptedFormats(self, event):
        return [f for f in event.mimeData().formats() \
                    if f.contains("image/x-Block-")]
                    
    def dragEnterEvent(self, event):
        if self.acceptedFormats(event):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self.acceptedFormats(event):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def readData(self, event, form):
        """
        reads data given by an event with a given mime format
        """
        pieceData = event.mimeData().data(form)
        dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
        pixmap = QtGui.QPixmap()
        mimetype = QtCore.QString()
        hotspot = QtCore.QPoint()
        ident = QtCore.QString()
        dataStream >> pixmap >> mimetype >> hotspot >> ident
        return pixmap, mimetype, hotspot, ident
        
    def dropEvent(self, event):
        f=self.acceptedFormats(event)
        if f:
            pixmap, mimetype, hotspot, ident = self.readData(event, f[0])

            # components of type 1 can be duplicated
            # so they should not be appended to the list
            if mimetype.contains("image/x-Block-1"):
                pass
            elif mimetype.contains("image/x-Block-2"):
                self.addPiece(pixmap, mimetype, ident)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def addPiece(self, pixmap, mimetype, ident):
        """
        adds a pixmap with a mime-type, an identifier,
        and returns the QListWidgetItem created
        """
        ident=QtCore.QString(ident)
        for i in range(self.count()):
            if self.item(i).data(QtCore.Qt.UserRole+2).toString()== ident:
                self.item(i).setHidden(False)
                return
        pieceItem = QtGui.QListWidgetItem(self)
        pieceItem.mimetype = mimetype
        pieceItem.setIcon(QtGui.QIcon(pixmap))
        pieceItem.setData(QtCore.Qt.UserRole, pixmap)
        pieceItem.setData(QtCore.Qt.UserRole+1, QtCore.QString(mimetype))
        pieceItem.setData(QtCore.Qt.UserRole+2, ident)
        pieceItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
        return pieceItem

    def currentComponent(self):
        item = self.currentItem()
        pixmap = QtGui.QPixmap(item.data(QtCore.Qt.UserRole))
        mimetype = item.data(QtCore.Qt.UserRole+1).toString()
        ident = item.data(QtCore.Qt.UserRole+2).toString()
        return Component(pixmap, ident, mimetype)
        
        
    def startDrag(self, supportedActions):
        component=self.currentComponent()
        itemData=component.serialize()

        mimeData = QtCore.QMimeData()
        mimeData.setData(component.mimetype, itemData)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(component.hotspot)
        drag.setPixmap(component.pixmap)

        # components of type 1 can be duplicated
        # so they should not be hidden from the list
        if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            if component.mimetype.contains("image/x-Block-1"):
                pass
            elif component.mimetype.contains("image/x-Block-2"):
                self.currentItem().setHidden(True)


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
        self.componentsList.clear()
        self.BlockWidget.clear()
        componentDirPattern = re.compile(r"components(.)")
        # browse top-level directories of the resource file
        for rcDir in sorted(QtCore.QDir(":/").entryList()):
            # directory's name matches r"components(.)" ???
            m=componentDirPattern.match(rcDir)
            if not m:
                continue
            else:
                mimetype = "image/x-Block-"+m.group(1)
            d=QtCore.QDir(":/"+rcDir)
            # browse SVG files contained in those directories
            for entry in sorted(d.entryList()):
                imgPath=":/"+rcDir+"/"+entry
                img=QtGui.QPixmap(imgPath)
                item=self.componentsList.addPiece(img, mimetype, entry)
                self.componentsList.insertItem(0, item)
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
    window.loadComponents()
    window.show()
    sys.exit(app.exec_())
