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
    """
    This class describes a programmation component, which can be
    organized with other instances. It features a widget, summarized
    by an icon, and each icon has some points which can be linked
    to other components.
    
    When a collection of components are organized on top of some
    canvas, they can be compiled into some usable program.
    """
    def __init__(self, pixmap, ident, mimetype, rect=None, hotspot=None):
        """
        The constructor
        @param pixmap a drawing to make an icon, and able to suggest
        the function of the component
        @param ident an identifier
        @param mimetype a type which decides some behaviors in the user
        interface
        @param rect the surrounding rectangle; defaults to None, which
        will define rect as surrounding the given pixmap
        @param hotspot the position of the mouse during the drag of
        the pixmap
        """
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
        returns data as a QByteArray instance
        """
        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        dataStream << self.pixmap << self.mimetype << self.hotspot << self.ident
        return itemData
        
    @staticmethod
    def unserialize(event):
        """
        userialize given QEvent's data into a Component instance
        @param event a QEvent, presumably due to a drop.
        @return an instance of Component 
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
        gets a list of components from the application's QRC file
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
        creates and returns a QDrag object with the given parent
        @param parent a window, where a drag is starting
        @return the DQrag instance
        """
        itemData = self.serialize()

        mimeData = QtCore.QMimeData()
        mimeData.setData(self.mimetype, itemData)

        drag = QtGui.QDrag(parent)
        drag.setMimeData(mimeData)
        drag.setHotSpot(self.hotspot)
        drag.setPixmap(self.pixmap)
        return drag
