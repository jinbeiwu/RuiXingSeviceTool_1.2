# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 CEA
# Pierre Raybaut
# Licensed under the terms of the CECILL License
# (see guidata/__init__.py for details)

"""
DataSetEditGroupBox and DataSetShowGroupBox demo

These group box widgets are intended to be integrated in a GUI application
layout, showing read-only parameter sets or allowing to edit parameter values.
"""

SHOW = True # Show test in GUI-based test launcher

from guidata.qt.QtGui import QMainWindow, QSplitter
from guidata.qt.QtCore import SIGNAL

from guidata.dataset.datatypes import (DataSet, BeginGroup, EndGroup,
                                       BeginTabGroup, EndTabGroup)
from guidata.dataset.dataitems import (ChoiceItem, FloatItem, StringItem,
                                       DirectoryItem, FileOpenItem)
from guidata.dataset.qtwidgets import DataSetShowGroupBox, DataSetEditGroupBox
from guidata.configtools import get_icon
from guidata.qthelpers import create_action, add_actions, get_std_icon

# Local test import:
from guidata.tests.activable_dataset import ExampleDataSet

class AnotherDataSet(DataSet):
    """
    Example 2
    <b>Simple dataset example</b>
    """
    param0 = ChoiceItem("Choice", ['deazdazk', 'aeazee', '87575757'])
    param1 = FloatItem("Foobar 1", default=0, min=0)
    a_group = BeginGroup("A group")
    param2 = FloatItem("Foobar 2", default=.93)
    param3 = FloatItem("Foobar 3", default=123)
    _a_group = EndGroup("A group")

class ExampleMultiGroupDataSet(DataSet):
    param0 = ChoiceItem("Choice", ['deazdazk', 'aeazee', '87575757'])
    param1 = FloatItem("Foobar 1", default=0, min=0)
    t_group = BeginTabGroup("T group")
    a_group = BeginGroup("A group")
    param2 = FloatItem("Foobar 2", default=.93)
    dir1 = DirectoryItem("Directory 1")
    file1 = FileOpenItem("File 1")
    _a_group = EndGroup("A group")
    b_group = BeginGroup("B group")
    param3 = FloatItem("Foobar 3", default=123)
    _b_group = EndGroup("B group")
    c_group = BeginGroup("C group")
    param4 = FloatItem("Foobar 4", default=250)
    _c_group = EndGroup("C group")
    _t_group = EndTabGroup("T group")
    
class OtherDataSet(DataSet):
    title = StringItem("Title", default="Title")
    icon = ChoiceItem("Icon", (("python.png", "Python"),
                               ("guidata.svg", "guidata"),
                               ("settings.png", "Settings")))
    opacity = FloatItem("Opacity", default=1., min=.1, max=1)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(get_icon('python.png'))
        self.setWindowTitle("Application example")
        
        # Instantiate dataset-related widgets:
        self.groupbox1 = DataSetShowGroupBox("Activable dataset",
                                             ExampleDataSet, comment='')
        self.groupbox2 = DataSetShowGroupBox("Standard dataset",
                                             AnotherDataSet, comment='')
        self.groupbox3 = DataSetEditGroupBox("Standard dataset",
                                             OtherDataSet, comment='')
        self.groupbox4 = DataSetEditGroupBox("Standard dataset",
                                             ExampleMultiGroupDataSet, comment='')
        self.connect(self.groupbox3, SIGNAL("apply_button_clicked()"),
                     self.update_window)
        self.update_groupboxes()
        
        splitter = QSplitter(self)
        splitter.addWidget(self.groupbox1)
        splitter.addWidget(self.groupbox2)
        splitter.addWidget(self.groupbox3)
        splitter.addWidget(self.groupbox4)
        self.setCentralWidget(splitter)
        self.setContentsMargins(10, 5, 10, 5)
        
        # File menu
        file_menu = self.menuBar().addMenu("File")
        quit_action = create_action(self, "Quit",
                                    shortcut="Ctrl+Q",
                                    icon=get_std_icon("DialogCloseButton"),
                                    tip="Quit application",
                                    triggered=self.close)
        add_actions(file_menu, (quit_action, ))
        
        # Edit menu
        edit_menu = self.menuBar().addMenu("Edit")
        editparam1_action = create_action(self, "Edit dataset 1",
                                          triggered=self.edit_dataset1)
        editparam2_action = create_action(self, "Edit dataset 2",
                                          triggered=self.edit_dataset2)
        editparam4_action = create_action(self, "Edit dataset 4",
                                          triggered=self.edit_dataset4)
        add_actions(edit_menu, (editparam1_action,
                                editparam2_action,
                                editparam4_action))
        
    def update_window(self):
        dataset = self.groupbox3.dataset
        self.setWindowTitle(dataset.title)
        self.setWindowIcon(get_icon(dataset.icon))
        self.setWindowOpacity(dataset.opacity)
        
    def update_groupboxes(self):
        self.groupbox1.dataset.set_readonly() # This is an activable dataset
        self.groupbox1.get()
        self.groupbox2.get()
        self.groupbox4.get()
        
    def edit_dataset1(self):
        self.groupbox1.dataset.set_writeable() # This is an activable dataset
        if self.groupbox1.dataset.edit():
            self.update_groupboxes()
    
    def edit_dataset2(self):
        if self.groupbox2.dataset.edit():
            self.update_groupboxes()

    def edit_dataset4(self):
        if self.groupbox4.dataset.edit():
            self.update_groupboxes()
        
if __name__ == '__main__':
    from guidata.qt.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())