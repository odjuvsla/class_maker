'''
Documentation, License etc.

@package class_maker
'''
import sys
from PyQt4 import QtGui, uic, QtCore
import make_class

    
    

class ClassMaker(QtGui.QMainWindow):
  '''
  
  '''
  
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    
    self.mt = make_class.MemberTableModel()
    
    self.mc = make_class.MakeClass(self.mt,'')
    
    self.setupUi()
    
    self.window.show()
  
  def setupUi(self):
    
    self.window = uic.loadUi('class_maker.ui')
    self.window.memberView.setModel(self.mt)
    self.window.memberView.setItemDelegateForColumn(0, make_class.EncapsulationDelegate())
    #self.window.memberView.setEditTriggers(QtGui.QTableView.DoubleClicked)
    self.setupSignals()
    
  def setupSignals(self):
    
    self.connect(self.mt, QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), self.mc.updateFromModel )
    
    self.connect(self.window.classNameEdit, QtCore.SIGNAL("textChanged(const QString&)"), self.mc.setClassName )
    self.connect(self.window.inheritsEdit, QtCore.SIGNAL("textChanged(const QString&)"), self.mc.setInherits )

    self.connect(self.window.genDefPb, QtCore.SIGNAL("clicked()"), self.mc.generateHeaderFile )
    self.connect(self.window.genImplPb, QtCore.SIGNAL("clicked()"), self.mc.generateImplementationFile )
    
    self.connect(self.window.defConCb, QtCore.SIGNAL("stateChanged(int)"), self.mc.setCreateDefaultConstructor )
    self.connect(self.window.paramConCb, QtCore.SIGNAL("stateChanged(int)"), self.mc.setCreateParameterConstructor )
    self.connect(self.window.copyConCb, QtCore.SIGNAL("stateChanged(int)"), self.mc.setCreateCopyConstructor )
    self.connect(self.window.assOpCb, QtCore.SIGNAL("stateChanged(int)"), self.mc.setCreateAssignmentOperator )
    self.connect(self.window.eqOpCb, QtCore.SIGNAL("stateChanged(int)"), self.mc.setCreateEqualityOperator )
    
    self.connect(self.window.defConPbDef, QtCore.SIGNAL("clicked()"), self.mc.generateDefaultConstructorDef)
    self.connect(self.window.paramConPbDef, QtCore.SIGNAL("clicked()"), self.mc.generateParameterConstructorDef)
    self.connect(self.window.copyConPbDef, QtCore.SIGNAL("clicked()"), self.mc.generateCopyConstructorDef)
    self.connect(self.window.assOpPbDef, QtCore.SIGNAL("clicked()"), self.mc.generateAssignmentOpDef)
    self.connect(self.window.eqOpPbDef, QtCore.SIGNAL("clicked()"), self.mc.generateEqualityOpDef)
    
    self.connect(self.window.defConPbImpl, QtCore.SIGNAL("clicked()"), self.mc.generateDefaultConstructorImpl)
    self.connect(self.window.paramConPbImpl, QtCore.SIGNAL("clicked()"), self.mc.generateParameterConstructorImpl)
    self.connect(self.window.copyConPbImpl, QtCore.SIGNAL("clicked()"), self.mc.generateCopyConstructorImpl)
    self.connect(self.window.assOpPbImpl, QtCore.SIGNAL("clicked()"), self.mc.generateAssignmentOpImpl)
    self.connect(self.window.eqOpPbImpl, QtCore.SIGNAL("clicked()"), self.mc.generateEqualityOpImpl)
    
    self.connect(self.window.addRowPb, QtCore.SIGNAL("clicked()"), self.addRow)
    self.connect(self.window.removeRowPb, QtCore.SIGNAL("clicked()"), self.removeRow)
    
    self.connect(self.mc, QtCore.SIGNAL('generatedCode'), self.window.genOutputText.insertPlainText)
    
  def addRow(self):
    
    self.mt.insertRows(self.mt.rowCount(0), 1, QtCore.QModelIndex())

  def removeRow(self):
    r = self.window.memberView.currentIndex().row()
    self.mt.removeRows(r, 1, QtCore.QModelIndex())
    
    
app = QtGui.QApplication(sys.argv)
  #mw = QtGui.QMainWindow()

cm = ClassMaker()


  
app.exec_()  
  