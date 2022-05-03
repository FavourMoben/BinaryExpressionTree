from dataclasses import dataclass
from typing import Any,List
import time
@dataclass
class Node:
    value: Any
    left: Any = None
    right: Any = None

class Queue:
    def __init__(self) -> None:
        self.qlist = []
        self.length = 0

    def append(self,value:any):
        self.qlist.append(value)
        self.length += 1

    def pop(self):
        return self.qlist.pop(0)
    
    def isEmpty(self):
        return self.qlist == []
    
    def clear(self):
        self.qlist = []
        return None

    def __str__(self) -> str:
        return str(self.qlist)

class Stack:
    def __init__(self) -> None:
        self.stack_list = []
        self.length = 0
    
    def append(self,value:any):
        self.stack_list.append(value)
        self.length += 1

    def pop(self,index=None):
        if index is not None:
            return self.stack_list.pop(index)
        return self.stack_list.pop()
    
    def isEmpty(self):
        return self.stack_list == []

    def __repr__(self) -> str:
        return str(self.stack_list)

class BinaryTree:
    def __init__(self) -> None:
        self.root = None
        self.Tlength = 0
        self.treeLists = []
        self.alreadyTraversed = False
        self.animate = False

    def createExpressionTree(self,exp:str,preprocessExpression):
        if self.Tlength < 1:
            self.root = Node(exp)
            self.Tlength += 1
        # Using a Queue
        queue = Queue()
        queue.append(self.root)
        left,value,right = None,None,None
        while True:
            currentNode = queue.pop()
            if currentNode.left is None and currentNode.right is None:
                try:
                    left,value,right = preprocessExpression(currentNode.value)
                except TypeError:
                    pass
                else:
                    currentNode.value = value
                    currentNode.left = Node(left)
                    currentNode.right = Node(right)
                    if len(left) > 1:
                        queue.append(currentNode.left)
                    if len(right) > 1:
                        queue.append(currentNode.right)
                    self.Tlength += 2
            if queue.isEmpty():
                break

    def inorderTraversal(self,currentNode,spacingLevel=0):
        if currentNode.left:
            self.inorderTraversal(currentNode.left, spacingLevel + 1)
        result = f"{' '*4*spacingLevel}     |{currentNode.value}|   "
        self.treeLists.append(result)
        if currentNode.right: 
            self.inorderTraversal(currentNode.right, spacingLevel + 1)

    def __repr__(self):
        """ for the visualization part the tree is only traversed once """
        print('Visualization: ')
        if not self.alreadyTraversed:
            self.treeLists = []
            self.alreadyTraversed = True
            self.inorderTraversal(self.root)
        for i in self.treeLists:
            if self.animate:
              time.sleep(0.2)          
            print(i)
        return ''

