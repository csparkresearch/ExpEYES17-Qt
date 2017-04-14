# -*- coding: UTF-8 -*-
############################################################################
#
#  Copyright (C) 2017 Georges Khaznadar <georgesk@debian.org>
#
#
#  This file may be used under the terms of the GNU General Public
#  License version 3.0 as published by the Free Software Foundation,
#  or, at your preference, any later verion of the same.
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import print_function

import os, re
from PyQt4 import QtCore, QtGui

import blocks_rc

def acceptedFormats(event):
    """
    acceptable formats start with "image/x-Block-"
    returns a list of accepted formats.
    """
    return [f for f in event.mimeData().formats() \
                if f.contains("image/x-Block-")]

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
        
    @staticmethod
    def unserialize(event):
        """
        userialize the given event's data into a Component instance
        """
        f = acceptedFormats(event)
        if f:
            data = event.mimeData().data(f[0])
            dataStream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            pixmap = QtGui.QPixmap()
            mimetype = QtCore.QString()
            ident = QtCore.QString()
            hotspot = QtCore.QPoint()
            dataStream >> pixmap >> mimetype >> hotspot >> ident

            rect = QtCore.QRect((event.pos()-hotspot), pixmap.size())

            return Component(pixmap,ident,mimetype,rect)
        else:
            return None

    @staticmethod
    def listFromRC():
        """
        gets a list of components from the QRC file
        """
        componentDirPattern = re.compile(r"components(.)")
        result=[]
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
                result.append(Component(img, entry, mimetype))
        return result
        
    def makeDrag(self, parent):
        """
        craetes and returns a drag object with the given parent
        """
        itemData = self.serialize()

        mimeData = QtCore.QMimeData()
        mimeData.setData(self.mimetype, itemData)

        drag = QtGui.QDrag(parent)
        drag.setMimeData(mimeData)
        drag.setHotSpot(self.hotspot)
        drag.setPixmap(self.pixmap)
        return drag
