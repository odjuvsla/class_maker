
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
	      self.members[index.row()].encapsulation = str(value)
	    if index.column() == 1:
	      self.members[index.row()].type = str(value.toString())
	    if index.column() == 2:
	      self.members[index.row()].name = str(value.toString())
	    if index.column() == 3:
	      self.members[index.row()].default = str(value.toString())
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

	  
class MakeClass(QtCore.QObject):
  '''
  Create a class
  '''
  def __init__(self, model, name, inherits='', parent=None):
    
    QtCore.QObject.__init__(self, parent)
    
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
    
    self.model = model
    
  def updateFromModel(self, u, b):
    
    self.private = []
    self.public = []
    self.protected = []
    for m in self.model.members:
      if m.encapsulation == 'public':
	self.public.append(m)
      if m.encapsulation == 'protected':
	self.protected.append(m)
      if m.encapsulation == 'private':
	self.private.append(m)
      
    
    
  def setClassName(self, n):
    self.name = str(n)

  def setInherits(self, i):
    self.inherits = str(i)
  
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

  def getInitListArgCopy(self, member, source, first = False):
    if first:
      return ' _' + member.name + '(' + source + '._' + member.name + ')\n'
    else:
      return ',_' + member.name + '(' + source + '._' + member.name + ')\n'

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
	content = self.name + '::' + self.name + '()'
	if (len(self.public) + len(self.protected) + len(self.private)) > 0:
	  content += ' :\n'
	else:
	  content += '\n'
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
	content += ')'
	if (len(self.public) + len(self.protected) + len(self.private)) > 0:
	  content += ' :\n'
	else:
	  content += '\n'
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
      if impl == False:
	content += self.name + '(const ' + self.name + ' &obj);\n\n'
      else:
	content += self.name + '::' + self.name + '(const ' + self.name + ' &obj)'
	if (len(self.public) + len(self.protected) + len(self.private)) > 0:
	  content += ' :\n'
	else:
	  content += '\n'
	firstMember = True
	for m in self.public:
	  content += self.getInitListArgCopy(m, 'obj',firstMember)
	  firstMember = False
	for m in self.protected:
	  content += self.getInitListArgCopy(m, 'obj',firstMember)
	  firstMember = False
	for m in self.private:
	  content += self.getInitListArgCopy(m, 'obj',firstMember)
	  firstMember = False
	content += '{}\n\n'
      return content
  
  def getDestructor(self, impl = False):
      content = '//! Destructor\n'
      content += 'virtual ' + self.name + '::~' + self.name + '\n' + '{}' + '\n\n'
      return content

  def getAssignmentOp(self, impl = False):
      
      content = '//! Assignment operator\n'
      if impl == False:
	content += self.name + '& operator=(const ' + self.name + '& other);\n\n'
      else:
	content += self.name + '& ' + self.name + '::operator=(const ' + self.name + ' &other)\n{\n'
	content += 'if (this != &other)\n'
	content += '{\n'
	for m in self.public:
	  content += '_'+m.name + ' = other._'+m.name + ';\n'
	for m in self.protected:
	  content += '_'+m.name + ' = other._'+m.name + ';\n'
	for m in self.private:
	  content += '_'+m.name + ' = other._'+m.name + ';\n'
	content += '}\n'
	content += '}\n\n'
      return content
      
  def getEqualityOp(self, impl = False):
      content = '//! Equality operator\n'
      if impl == False:
	content += 'bool operator==(const ' + self.name + ' &other) const;\n\n'
      else:
	content += 'bool ' + self.name + '::operator==(const ' + self.name + ' &other)\n{\n'
	content += 'if (this == &other) return true;\n'
	content += 'else if\n'
	content += '(\n'
	for m in self.public:
	  content += '_'+m.name + ' == other._'+m.name + ' &&\n'
	for m in self.protected:
	  content += '_'+m.name + ' == other._'+m.name + ' &&\n'
	for m in self.private:
	  content += '_'+m.name + ' == other._'+m.name + ' &&\n'
	content = content.rstrip('&&\n')
	content += '\n)\n'
	content += '{\n'
	content += 'return true;\n'
	content += '}\n'
	content += 'return false;\n'
	content += '}\n\n'
      
      return content

  def generateDefaultConstructorDef(self):
      
      self.emit(QtCore.SIGNAL('generatedCode'), self.getDefaultConstructor())
  
  def generateParameterConstructorDef(self):
    
      self.emit(QtCore.SIGNAL('generatedCode'), self.getParameterConstructor())
      
  def generateCopyConstructorDef(self):
      
      self.emit(QtCore.SIGNAL('generatedCode'), self.getCopyConstructor()())
      
      
  def generateDestructorDef(self):

      self.emit(QtCore.SIGNAL('generatedCode'), self.getDestructor())
      
  def generateAssignmentOpDef(self):

      self.emit(QtCore.SIGNAL('generatedCode'), self.getAssignmentOp())
      
  def generateEqualityOpDef(self):

      self.emit(QtCore.SIGNAL('generatedCode'), self.getEqualityOp())
      
  def generateDefaultConstructorImpl(self):
      self.emit(QtCore.SIGNAL('generatedCode'), self.getDefaultConstructor(True))
      
  def generateParameterConstructorImpl(self):
      self.emit(QtCore.SIGNAL('generatedCode'), self.getParameterConstructor(True))
      
  def generateCopyConstructorImpl(self):

      self.emit(QtCore.SIGNAL('generatedCode'), self.getCopyConstructor(True))
      
  def generateDestructorImpl(self):
    
      self.emit(QtCore.SIGNAL('generatedCode'), self.getDestructor(True))

  def generateAssignmentOpImpl(self):
      self.emit(QtCore.SIGNAL('generatedCode'), self.getAssignmentOp(True))
      
  def generateEqualityOpImpl(self):
      
      self.emit(QtCore.SIGNAL('generatedCode'), self.getEqualityOp(True))
    
  def generateGetter(self, m):
    
      return m.type + ' ' + m.name + '() const { return _' + m.name +'; }\n' 
  
  def generateSetter(self, m):
    
      return 'void set' + m.name.capitalize() + '(' + m.type + ' ' + m.name + ') { _' + m.name + ' = ' + m.name + '; }\n' 
      
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
      
      if len(self.protected) > 0 or len(self.private) > 0:
	content += '// Getters\n\n'
      for m in self.protected:
	#content += m.type + ' ' + m.name + '() const { return _' + m.name +'; }\n\n' 
	content += self.generateGetter(m)
	content+= '\n'
      for m in self.private:
	#content += m.type + ' ' + m.name + '() const { return _' + m.name +'; }\n\n' 
	content += self.generateGetter(m)
	content += '\n'
      if len(self.protected) > 0 or len(self.private) > 0:
	content += '// Setters\n\n'
      for m in self.protected:
	#content += 'void set' + m.name.capitalize() + '(' + m.type + ' ' + m.name + ') { _' + m.name + ' = ' + m.name + '; }\n\n' 
	content += self.generateSetter(m)
	content += '\n'
      for m in self.private:
	#content += 'void set' + m.name.capitalize() + '(' + m.type + ' ' + m.name + ') { _' + m.name + ' = ' + m.name + '; }\n\n'
	content += self.generateSetter(m)
	content += '\n'
      for m in self.public:
	content += '//! ' + m.name + '\n'
	content += m.type + ' _' + m.name + ';\n'
      if len(self.protected) > 0:
	content += '\nprotected:\n\n'
      for m in self.protected:
	content += '//! ' + m.name + '\n'
	content += m.type + ' _' + m.name + ';\n'
      if len(self.private) > 0:
	content += '\nprivate:\n\n'
      for m in self.private:
	content += '//! ' + m.name + '\n'
	content += m.type + ' _' + m.name + ';\n'
      if (self.createDefaultConstructor == False or self.createParameterConstructor == False or self.createCopyConstructor == False or self.createAssignmentOp == False or self.createEqualityOp == False):
	if len(self.private) == 0:
	  content += '\nprivate:\n\n'
      if self.createDefaultConstructor == False:
	content += '// Prohibited\n'
	content += self.getDefaultConstructor()
      if self.createParameterConstructor == False:
	content += '// Prohibited\n'
	content += self.getParameterConstructor()
      if self.createCopyConstructor == False:
	content += '// Prohibited\n'
	content += self.getCopyConstructor()
      if self.createAssignmentOp == False:
	content += '// Prohibited\n'
	content += self.getAssignmentOp()
      if self.createEqualityOp == False:
	content += '// Prohibited\n'
	content += self.getEqualityOp()
      content += '};\n\n'
      content += '#endif //' + self.name.upper() + '_H\n\n'
      
      self.emit(QtCore.SIGNAL('generatedCode'), content)

  def generateImplementationFile(self):
      
      content = self.license
      content += '\n'
      content += '#include \"' + self.name.lower() + '.h\"\n\n'
      if self.createDefaultConstructor:
	content += self.getDefaultConstructor(True)
      if self.createParameterConstructor:
	content += self.getParameterConstructor(True)
      if self.createCopyConstructor:
	content += self.getCopyConstructor(True)
      content += self.getDestructor(True)
      if self.createAssignmentOp:
	content += self.getAssignmentOp(True)
      if self.createEqualityOp:
	content += self.getEqualityOp(True)

      self.emit(QtCore.SIGNAL('generatedCode'), content)
      
#c = myclass('test', 'ptest')
#c.setPublicMembers([member('float', 'a'), member('float', 'b'), member('char*', 'c')])
#c.setProtectedMembers([member('float', 'd'), member('float', 'e'), member('char*', 'f')])
#c.setPrivateMembers([member('float', 'g'), member('float', 'h'), member('char*', 'i')])
#c.generateHeaderFile()
#c.generateImplementationFile()
