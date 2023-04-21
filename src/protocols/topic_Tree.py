class Node:
    def __init__(self, name, parent):
        self.name = name
        self.nodeList = []
        self.parent = parent
        self.clientList = set()
        self.value = None

    def setValue(self, value):
        self.value = str(value)


    def add(self, conn):
        # add client
        self.clientList.add(conn)
    
    def getClients(self, clients):
        """Returns client and all associated parent clients"""
        clients = self.clientList.union(clients)
        if self.parent == None:
            return clients
        else:
            return self.parent.getClients(clients)


    def getNode(self,newNode):
        """Returns node if exists. Otherwise creates a new one"""
        if type(newNode) != list:
            newNode = newNode.split("/")
            if len(newNode) > 1:
                newNode.pop(0)
        
    
        node = self.returnInnerNode(newNode[0])
        if len(newNode) > 1:
            if(node != None):
               return node.getNode(newNode[1:])
            else:
                node = Node(newNode[0], self)
                self.nodeList.append(node)
                return node.getNode(newNode[1:])
        
        else:
            if(node != None):
                return node
            else:
                node = Node(newNode[0], self)
                self.nodeList.append(node)
                return node


    def returnInnerNode(self,name):
        for node in self.nodeList:
            if node.name == name:
                return node
        return None
    

    def unsubscribe(self, conn):
        for client in self.clientList:
            if client[1] == conn:
                break
        self.clientList.remove(client)

    def getTopicsWithValue(self):
        valueList = []
        if (self.value != None):
            valueList.append(self.getName())
        for child in self.nodeList:
            valueList = valueList + child.getTopicsWithValue()
        return valueList

        
    def getName(self):
        if self.parent == None:
            return ""
        return self.parent.getName() + "/" + self.name
            