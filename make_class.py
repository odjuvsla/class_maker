
from PyQt4 import QtGui, QtCore

class EncapsulationDelegate(QtGui.QItemDelegate):
  '''
  
  '''

  def __init__(self):
      QtGui.QItemDelegate.__init__(self)
      
  def createEditor(self, parent, option, index):
    
    editor = QtGui.QComboBox(parent)
    
    editor.addItem("public")
    editor.addItem("protected")
    editor.addItem("private")
    
    return editor
    
  def setEditorData(self, editor, index):
  
    t = index.model().data(index, QtCore.Qt.EditRole)
    if len(t) > 0:
      i = editor.findText(t)
      editor.setCurrentIndex(i)
      
    else:
      editor.setCurrentIndex(0)
    
  def setModelData(self, editor, model, index):
    model.setData(index, editor.currentText(), QtCore.Qt.EditRole)

  def setEditorGeometry(self, editor, option, index):
    
    editor.setGeometry(option.rect);
  
    
class member(QtGui.QTableWidgetItem):
  
  def __init__(self, encapsulation, t, name, default = 0):
    
    QtGui.QTableWidgetItem.__init__(self)
    
    self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled )
    self.encapsulation = encapsulation
    self.type = t
    self.name = name
    self.default = default

class MemberTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        
        self.public = []
        self.protected = []
	self.private = []
	
	self.members = []
        
    def setPublicMembers(self, members):
	self.public = members
	for m in members:
	  self.members.append(m)

    def setProtectedMembers(self, members):
	self.protected = members
	for m in members:
	  self.members.append(m)

    
    def setPrivateMembers(self, members):
	self.private = members
	for m in members:
	  self.members.append(m)
      
    def rowCount(self, parent):
        return len(self.members)

    def columnCount(self, parent):
        return 4

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
	  if index.column() == 0:
	      return self.members[index.row()].encapsulation
	  if index.column() == 1:
	      return self.members[index.row()].type
	  if index.column() == 2:
	      return self.members[index.row()].name
	  if index.column() == 3:
	      return self.members[index.row()].default
        return QtCore.QVariant()
    
    def setData(self, index, value, role):
	if index.row() < len(self.members):
	    if index.column() == 0:
	      self.members[index.row()].encapsulation = value
	    if index.column() == 1:
	      self.members[index.row()].type = value
	    if index.column() == 2:
	      self.members[index.row()].name = value
	    if index.column() == 3:
	      self.members[index.row()].default = value
	    self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), index, index);
	    return True
	return False
    
    def flags(self, index):
	return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable 
	
    def headerData(self, section, orientation, role):
	
	if role != QtCore.Qt.DisplayRole:
	  return QtCore.QVariant()
	if orientation == QtCore.Qt.Horizontal:
	  if section == 0:
	    return QtCore.QString('Member Type')
	  if section == 1:
	    return QtCore.QString('Type')
	  if section == 2:
	    return QtCore.QString('Name')
	  if section == 3:
	    return QtCore.QString('Default Value')
	else:
	  return QtCore.QString(section)
	  
    def insertRows(self, position, rows, index):
	
	self.beginInsertRows(QtCore.QModelIndex(), position, position+rows-1 )
	for row in range(rows):
	  m = member('','','','')
	  self.members.insert(position, m)
	self.endInsertRows();
	return True

    def removeRows(self, position, rows, index):
	
	self.beginRemoveRows(QtCore.QModelIndex(), position, position+rows-1 )
	for row in range(rows):
	  m = member('','','','')
	  if len(self.members) > position:
	    self.members.pop(position)
	self.endRemoveRows();
	return True

	  
class MakeClass:
  '''
  Create a class
  '''
  def __init__(self,name, inherits=''):
    
    self.name = name
    self.inherits = inherits
    self.license = ''
    self.public = []
    self.protected = []
    self.private = []
    self.createDefaultConstructor = True
    self.createCopyConstructor = True
    self.createAssignmentOp = True
    self.createEqualityOp = True
    self.createParameterConstructor = True
    
  def setPublicMembers(self, members):
    self.public = members
    
  def setProtectedMembers(self, members):
    self.protected = members
    
  def setPrivateMembers(self, members):
    self.private = members
  
  def getFunctionArg(self, member):
    return member.type +' ' + member.name + ', '
  def getInitListArg(self, member, first = False):
    if first:
      return ' _' + member.name + '(' + member.name + ')\n'
    else:
      return ',_' + member.name + '(' + member.name + ')\n'

  def getInitListArgZero(self, member, first = False):
    if first:
      return ' _' + member.name + '(0)\n'
    else:
      return ',_' + member.name + '(0)\n'

  def setCreateDefaultConstructor(self, state):
    print 'createDefaultConstructor: ' + str(state)
    self.createDefaultConstructor = state
  
  def setCreateParameterConstructor(self, state):
    print 'createParameterConstructor: ' + str(state)
    self.createParameterConstructor = state
  
  def setCreateCopyConstructor(self, state):
    print 'createCopyConstructor: ' + str(state)
    self.createCopyConstructor = state
  
  def setCreateAssignmentOperator(self, state):
    print 'createAssignmentOp: ' + str(state)
    self.createAssignmentOp = state
  
  def setCreateEqualityOperator(self, state):
    print 'createEqualityOp: ' + str(state)
    self.createEqualityOp = state
  
  def getDefaultConstructor(self, impl = False):
      if impl == False:
	content = '//! Default constructor\n'
	content += self.name + '();\n\n'
      else:
	content = self.name + '::' + self.name + '() : \n'
	firstMember = True
	for m in self.public:
	  content += self.getInitListArgZero(m, firstMember)
	  firstMember = False
	for m in self.protected:
	  content += self.getInitListArgZero(m, firstMember)
	  firstMember = False
	for m in self.private:
	  content += self.getInitListArgZero(m, firstMember)
	  firstMember = False
	content += '{}\n\n'

      return content
      
  def getParameterConstructor(self, impl = False):
      if impl == False:
	content = '//! Constructor\n'	
	content += self.name + '('
	for m in self.public:
	  content += self.getFunctionArg(m)
	for m in self.protected:
	  content += self.getFunctionArg(m)
	for m in self.private:
	  content += self.getFunctionArg(m)
	content = content.rstrip(', ')
	content += ');\n\n'
	return content
      else:
	content = self.name + '::' + self.name + '('
	for m in self.public:
	  content += self.getFunctionArg(m)
	for m in self.protected:
	  content += self.getFunctionArg(m)
	for m in self.private:
	  content += self.getFunctionArg(m)
	content = content.rstrip(', ')
	content += ') :\n'
	firstMember = True
	for m in self.public:
	  content += self.getInitListArg(m, firstMember)
	  firstMember = False
	for m in self.protected:
	  content += self.getInitListArg(m, firstMember)
	  firstMember = False
	for m in self.private:
	  content += self.getInitListArg(m, firstMember)
	  firstMember = False
	content += '{}\n\n'
	return content
  
  def getCopyConstructor(self, impl = False):
      content = '//! Copy constructor\n'
      content += self.name + '(const ' + self.name + ' &obj);\n\n'
      return content
  
  def getDestructor(self, impl = False):
      content = '//! Destructor\n'
      content += 'virtual ~' + self.name + ';\n\n'
      return content

  def getAssignmentOp(self, impl = False):
      content = '//! Assignment operator\n'
      content += self.name + '& operator=(const ' + self.name + '& obj);\n\n'
      return content
      
  def getEqualityOp(self, impl = False):
      content = '//! Equality operator\n'
      content += 'bool operator==(const ' + self.name + ' &obj) const;\n\n'
      return content

  def generateDefaultConstructorDef(self):
    
      return self.getDefaultConstructor()
  
  def generateParameterConstructorDef(self):
    
      return self.getParameterConstructor()
  		
  def generateCopyConstructorDef(self):
      content = '//! Copy constructor\n'
      content += self.name + '(const ' + self.name + ' &obj);\n\n'
      return content
  
  def generateDestructorDef(self):
      content = '//! Destructor\n'
      content += 'virtual ~' + self.name + ';\n\n'
      return content

  def generateAssignmentOpDef(self):
      content = '//! Assignment operator\n'
      content += self.name + '& operator=(const ' + self.name + '& obj);\n\n'
      return content
      
  def generateEqualityOpDef(self):
      content = '//! Equality operator\n'
      content += 'bool operator==(const ' + self.name + ' &obj) const;\n\n'
      return content
  
  def generateDefaultConstructorImpl(self):
    
      return self.getDefaultConstructor(True)
  
  def generateParameterConstructorImpl(self):
      content = self.getParameterConstructor(True)
      print content
      return content
  		
  def generateCopyConstructorImpl(self):
      content = '//! Copy constructor\n'
      content += self.name + '(const ' + self.name + ' &obj);\n\n'
      return content
  
  def generateDestructorImpl(self):
      content = '//! Destructor\n'
      content += 'virtual ~' + self.name + ';\n\n'
      return content

  def generateAssignmentOpImpl(self):
      content = '//! Assignment operator\n'
      content += self.name + '& operator=(const ' + self.name + '& obj);\n\n'
      return content
      
  def generateEqualityOpImpl(self):
      content = '//! Equality operator\n'
      content += 'bool operator==(const ' + self.name + ' &obj) const;\n\n'
      return content
    
  def generateHeaderFile(self):
    
      content = '#ifndef ' + self.name.upper() + '_H\n'
      content += '#define ' + self.name.upper() + '_H\n'
      content += self.license + '\n'
      if len(self.inherits) > 0:
	content += 'class ' + self.name+' : public ' + self.inherits + '\n'
      else:
	content += 'class ' + self.name+'\n'
      content += '{\n\n'
      content += 'public:\n\n'
      if self.createDefaultConstructor:
	content += self.getDefaultConstructor()
      if self.createParameterConstructor:
	content += self.getParameterConstructor()
      if self.createCopyConstructor:
	content += self.getCopyConstructor()
      content += self.getDestructor()
      if self.createAssignmentOp:
	content += self.getAssignmentOp()
      if self.createEqualityOp:
	content += self.getEqualityOp()
      content += '// Getters\n\n'
      for m in self.protected:
	content += m.type + ' ' + m.name + '() const { return _' + m.name +'; }\n\n' 
      for m in self.private:
	content += m.type + ' ' + m.name + '() const { return _' + m.name +'; }\n\n' 
      content += '// Setters\n\n'
      for m in self.protected:
	content += 'void set' + m.name.capitalize() + '(' + m.type + ' ' + m.name + ') { _' + m.name + ' = ' + m.name + '; }\n\n' 
      for m in self.private:
	content += 'void set' + m.name.capitalize() + '(' + m.type + ' ' + m.name + ') { _' + m.name + ' = ' + m.name + '; }\n\n'
	
      for m in self.public:
	content += '//! ' + m.name + '\n'
	content += m.type + ' _' + m.name + ';\n'
      content += '\nprotected:\n\n'
      for m in self.protected:
	content += '//! ' + m.name + '\n'
	content += m.type + ' _' + m.name + ';\n'
      content += '\nprivate:\n\n'
      for m in self.private:
	content += '//! ' + m.name + '\n'
	content += m.type + ' _' + m.name + ';\n'
      
      content += '};\n\n'
      content += '#endif //' + self.name.upper() + '_H'
      print content
      
  def generateImplementationFile(self):
      
      content = self.license
      content += '\n'
      content += '#include \"' + self.name.lower() + '.h\"\n\n'
      content += self.getDefaultConstructor(True)
      content += self.getParameterConstructor(True)
      print content
      
#c = myclass('test', 'ptest')
#c.setPublicMembers([member('float', 'a'), member('float', 'b'), member('char*', 'c')])
#c.setProtectedMembers([member('float', 'd'), member('float', 'e'), member('char*', 'f')])
#c.setPrivateMembers([member('float', 'g'), member('float', 'h'), member('char*', 'i')])
#c.generateHeaderFile()
#c.generateImplementationFile()
