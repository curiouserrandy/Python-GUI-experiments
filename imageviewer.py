#!/usr/bin/env python

## Note that I (Randy Smith) am hacking this file as part of my learning. 

#############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

from PyQt4 import QtCore, QtGui
import os


class QScrollZoomArea(QtGui.QScrollArea):
    """Specialization of QScrollArea to include integrated zooming.
    This specialization requires the contained widget to automatically
    size/zoom its contents according to the size of the widget, and
    to have a sizeHint() that indicates the "natural size" of the contents."""
    def __init__(self):
        self.scaleFactor = 1.0
        QtGui.QScrollArea.__init__(self)

    def scaleFactor(self):
        """How much has the contained widget been zoomed?"""
        return self.scaleFactor

    def normalSize(self):
        """Re-adjust contained widget to natural size."""
        self.widget().adjustSize()
        self.scaleFactor = 1.0

    def scale(self, factor, zoomPoint = None):
        """Zoom the contained widget around the given zoomPoint (default
        center of viewport)."""
        hscroll = self.horizontalScrollBar()
        vscroll = self.verticalScrollBar()

        if zoomPoint is None:
            zoomPoint = (hscroll.pageStep()/2, vscroll.pageStep()/2)

        self.scaleFactor *= factor
        self.widget().resize(self.scaleFactor * self.widget().sizeHint())

        self.adjustScrollBar(hscroll, factor, zoomPoint[0])
        self.adjustScrollBar(vscroll, factor, zoomPoint[1])

    def adjustScrollBar(self, scrollBar, factor, zoomPoint):
        """Modify the scroll bar location to take account of the zoom factor,
        keeping the zoomPoint (in viewport coords) in the same place
        in the viewport."""
        if zoomPoint is None: zoomPoint = scrollBar.pageStep()/2
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * zoomPoint)))

    # Default user interface bindings--google maps style
    def wheelEvent(self, ev):
        if ev.orientation() != 2:
            return              # Ignore horizontal scrolling

        # Choosing to ignore the amount by which the wheel was turned
        # as I think it's way too little for stroke scrolling.
        delta = 1 if ev.delta() > 0 else -1

        self.scale(1.2 ** delta, (ev.pos().x(), ev.pos().y()))

class ImageViewer(QtGui.QMainWindow):
    def __init__(self, image_file = None):
        super(ImageViewer, self).__init__()

        self.printer = QtGui.QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollZoomArea() # See above class derivation
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.resize(500, 400)

        if image_file: self.__open(image_file)

    def __open(self, filename):
        image = QtGui.QImage(filename)
        if image.isNull():
            QtGui.QMessageBox.information(self, "Image Viewer",
                    "Cannot load %s." % filename)
            return

        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
        self.scaleFactor = 1.0

        self.printAct.setEnabled(True)
        self.fitToWindowAct.setEnabled(True)
        self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()

    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                QtCore.QDir.currentPath())
        if fileName: self.__open(filename)

    def print_(self):
        dialog = QtGui.QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QtGui.QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scrollArea.scale(1.25)

    def zoomOut(self):
        self.scrollArea.scale(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QtGui.QMessageBox.about(self, "About Image Viewer",
                "<p>The <b>Image Viewer</b> example shows how to combine "
                "QLabel and QScrollArea to display an image. QLabel is "
                "typically used for displaying text, but it can also display "
                "an image. QScrollArea provides a scrolling view around "
                "another widget. If the child widget exceeds the size of the "
                "frame, QScrollArea automatically provides scroll bars.</p>"
                "<p>The example demonstrates how QLabel's ability to scale "
                "its contents (QLabel.scaledContents), and QScrollArea's "
                "ability to automatically resize its contents "
                "(QScrollArea.widgetResizable), can be used to implement "
                "zooming and scaling features.</p>"
                "<p>In addition the example shows how to use QPainter to "
                "print an image.</p>")

    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.printAct = QtGui.QAction("&Print...", self, shortcut="Ctrl+P",
                enabled=False, triggered=self.print_)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.zoomInAct = QtGui.QAction("Zoom &In (25%)", self,
                shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QtGui.QAction("Zoom &Out (25%)", self,
                shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)

        self.normalSizeAct = QtGui.QAction("&Normal Size", self,
                shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)

        self.fitToWindowAct = QtGui.QAction("&Fit to Window", self,
                enabled=False, checkable=True, shortcut="Ctrl+F",
                triggered=self.fitToWindow)

        self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QtGui.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QtGui.QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    (program_directory, program_name) = os.path.split(sys.argv[0])
    imageViewer = ImageViewer(program_directory + "/iw_test.tiff")
    imageViewer.show()
    sys.exit(app.exec_())
