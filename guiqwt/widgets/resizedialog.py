# -*- coding: utf-8 -*-
#
# Copyright © 2009-2012 CEA
# Pierre Raybaut
# Licensed under the terms of the CECILL License
# (see guiqwt/__init__.py for details)

"""
resizedialog
------------

The `resizedialog` module provides a dialog box providing essential GUI 
for entering parameters needed to resize an image:
:py:class:`guiqwt.widgets.resizedialog.ResizeDialog`.

Reference
~~~~~~~~~

.. autoclass:: ResizeDialog
   :members:
   :inherited-members:
"""

from __future__ import division, print_function

from guidata.qt.QtGui import (QDialog, QDialogButtonBox, QVBoxLayout, QLabel,
                              QFormLayout, QLineEdit, QIntValidator, QCheckBox)
from guidata.qt.QtCore import SIGNAL, SLOT, Qt


from guiqwt.config import _


def is_edit_valid(edit):
    text = edit.text()
    state = edit.validator().validate(text, 0)
    if isinstance(state, (tuple, list)):
        state = state[0]
    return state == QIntValidator.Acceptable


class ResizeDialog(QDialog):
    def __init__(self, parent, new_size, old_size, text=""):
        QDialog.__init__(self, parent)
        
        self.keep_original_size = False
        self.width, self.height = new_size
        self.old_width, self.old_height = old_size
        self.ratio = self.width/self.height

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        formlayout = QFormLayout()
        layout.addLayout(formlayout)
        
        if text:
            label = QLabel(text)
            label.setAlignment(Qt.AlignHCenter)
            formlayout.addRow(label)
        
        self.w_edit = w_edit = QLineEdit(self)
        w_valid = QIntValidator(w_edit)
        w_valid.setBottom(1)
        w_edit.setValidator(w_valid)
                     
        self.h_edit = h_edit = QLineEdit(self)
        h_valid = QIntValidator(h_edit)
        h_valid.setBottom(1)
        h_edit.setValidator(h_valid)
        
        zbox = QCheckBox(_("Original size"), self)

        formlayout.addRow(_("Width (pixels)"), w_edit)
        formlayout.addRow(_("Height (pixels)"), h_edit)
        formlayout.addRow('', zbox)
        
        formlayout.addRow(_("Original size:"), QLabel("%d x %d" % old_size))
        self.z_label = QLabel()
        formlayout.addRow(_("Zoom factor:"), self.z_label)
        
        # Button box
        self.bbox = bbox = QDialogButtonBox(QDialogButtonBox.Ok|
                                            QDialogButtonBox.Cancel)
        self.connect(bbox, SIGNAL("accepted()"), SLOT("accept()"))
        self.connect(bbox, SIGNAL("rejected()"), SLOT("reject()"))
        layout.addWidget(bbox)

        self.w_edit.setText(str(self.width))
        self.h_edit.setText(str(self.height))
        self.update_widgets()
        
        self.setWindowTitle(_("Resize"))
        
        self.connect(w_edit, SIGNAL("textChanged(QString)"),
                     self.width_changed)
        self.connect(h_edit, SIGNAL("textChanged(QString)"),
                     self.height_changed)
        self.connect(zbox, SIGNAL("toggled(bool)"), self.toggled_no_zoom)

    def update_widgets(self):
        valid = True
        for edit in (self.w_edit, self.h_edit):
            if not is_edit_valid(edit):
                valid = False
        self.bbox.button(QDialogButtonBox.Ok).setEnabled(valid)
        self.z_label.setText("%d %s" % (100*self.width/self.old_width, '%'))
        
    def width_changed(self, text):
        if is_edit_valid(self.sender()):
            self.width = int(text)
            self.height = int(self.width/self.ratio)
            self.h_edit.blockSignals(True)
            self.h_edit.setText(str(self.height))
            self.h_edit.blockSignals(False)
        self.update_widgets()

    def height_changed(self, text):
        if is_edit_valid(self.sender()):
            self.height = int(text)
            self.width = int(self.ratio*self.height)
            self.w_edit.blockSignals(True)
            self.w_edit.setText(str(self.width))
            self.w_edit.blockSignals(False)
        self.update_widgets()

    def toggled_no_zoom(self, state):
        self.keep_original_size = state
        if state:
            self.z_label.setText("100 %")
            self.bbox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.update_widgets()
        for widget in (self.w_edit, self.h_edit):
            widget.setDisabled(state)
        
    def get_zoom(self):
        if self.keep_original_size:
            return 1
        elif self.width > self.height:
            return self.width/self.old_width
        else:
            return self.height/self.old_height

    
if __name__ == '__main__':
    import guidata
    qapp = guidata.qapplication()
    test = ResizeDialog(None, (150, 100), (300, 200), "Enter the new size:")
    if test.exec_():
        print(test.width)
        print(test.get_zoom())
