""" IMPORTS """
from tools import BinaryTree,Stack
from test_tree import testTreeMain
from collections import Counter
import pickle

class ExpressionValidation:

    def __init__(self,exp) -> None:
        self.string = exp
        self.stringLength = len(self.string)
        self.isOperator = lambda char: True if char in {'/','*','-','+'} else False

    def insertToString(self,string:str,index: int,value :any):
        stringList = [i for i in string]
        stringList.insert(index,value)
        return ''.join(i for i in stringList)

    def missmatched(self,string:str = None) -> bool: 
        """ 
        returns True or False for both operator and bracket missmatch
        """
        if string is None:
            string = self.string
        bracketStorage = Counter()
        bracketStorage['('] = 0 
        bracketStorage[')'] = 0 
        OperatorMissmatch = False
        for index,char in enumerate(string):
            if char in {'(',')'} :
                bracketStorage[char] += 1 
            """ This part checks for operandmissmatch"""
            if char.isdigit():
                try:
                    if self.string[index+1] == '(':
                        OperatorMissmatch = True
                except IndexError:
                    pass
        """ This part checks for bracketMissmatch"""            
        bracketMissMatch = bracketStorage['('] == bracketStorage[')']
        """ if len ( and len ) is equal return True"""
        return  bracketMissMatch ,OperatorMissmatch

    def bracketAndContent(self,string: str =None) -> list:
        """ 
        this function returns 2 lists. One is what is actually contained in everybracket
        another is the indexes of the brackets
        for example 
        expresssion: ((1+3)/(3*5))
        returns ([((1+3)/(3*5)),(1+3),(3*5)], [[0,12],[1,5],[7,11]])
        """
        string = self.string if string is None else string
        bracketList = []
        bracketListIndex = []
        stack = Stack()
        for pointCounter,char in enumerate(string):
            if char == '(':
                bracketListIndex.append([pointCounter])
                stack.append(pointCounter)
            elif char == ')':
                try:
                    value = stack.pop()
                    for index,item in enumerate(bracketListIndex):
                        if item[0] == value:
                            bracketListIndex[index].append(pointCounter)
                except IndexError:
                    pass
            # if stack isempty and we at the last element
            if stack.isEmpty() and char == string[-1]:
                for lists in bracketListIndex:
                    if len(lists) > 1:
                        start,end =lists[0],lists[1]+1
                        bracketList.append(string[start:end])
                    else:
                        a = lists[0]
                        bracketList.append(string[a]) 
                break
        return bracketList,bracketListIndex

    def operandOutofRange(self) -> bool:
        """ (1+2) - > False
            (1+4+5) -> True
            returns True if the expression is not contained in brackets,
            if spaces are available or  if a bracket contains numbers greated than 3
            returns True if its wrong else False
        """
        operandOutOfRange = False
        spacing = False
        bracketList,bracketListIndex = self.bracketAndContent()
        if [0,len(self.string)-1] not in bracketListIndex:
            operandOutOfRange = True
            return True,spacing
        for expression in bracketList:
            brackets = '' 
            isdigitCount = 0
            for index,char in enumerate(expression):
                if char == '(' or char == ')':
                    brackets += char
                if char.isdigit():
                    isdigitCount += 1
                if char == ' ':
                    spacing = True
                    return operandOutOfRange,spacing
            if len(brackets) == 2 and (isdigitCount > 2 or isdigitCount < 2):
                operandOutOfRange = True
                return operandOutOfRange,spacing

        return operandOutOfRange,spacing

    def preprocessExpression(self,string:str):
        """ 
        this function takes an expression,
        finds a mid point of the expression and 
        returns a tuple of the left,the right 
        and the operator of that expression
        for example:
            1.expression: ((1+3)*(5+7))
              returns left: (1+3), operator: * , right: (5+7)
            2.expression: (4*(5+6))
              returns left: 4 , operator: * , right: (5+6)
        """
        currentString = string
        currentStringLength = len(currentString)
        while True:
            bracketList,bracketListIndex = self.bracketAndContent(currentString)
            content = [0,currentStringLength-1]
            if content in bracketListIndex:
                start,end = content
                currentString = currentString[start+1:end]
                currentStringLength = len(currentString)
            else:
                break
        for index,char in enumerate(currentString):
            if self.isOperator(char):
                mid = index
                left = currentString[:mid]
                right = currentString[mid+1:]
                bracketMissMatch = self.missmatched
                if bracketMissMatch(left)[0] and bracketMissMatch(right)[0]:
                    return left,currentString[mid],right
        return None

    def isValidExpression(self,isTestcase=False) -> bool:
        """returns True if the expression passed all the error checks"""
        results = True
        outputText = ''
        bracketMissMatch ,OperatorMissmatch = self.missmatched()
        operandOutOfRange,spacing = self.operandOutofRange()
        if not bracketMissMatch or self.isOperator(self.string[-1]):
            outputText = 'Not a valid expression, brackets mismatched.'
            results = False
        if OperatorMissmatch:
            outputText = 'Not a valid expression, operator missing.'
            results = False
        if operandOutOfRange :
            outputText = 'Not a valid expression, wrong number of operands.'
            results = False
        if spacing:
            outputText = 'Spaces available. Try to eliminate the spacing from the expression'
            results = False
        if not isTestcase:
            print(outputText)
        return results
 
def saveObject(object,filename):
    print('Saved....')
    with open(filename,'wb') as file:
        pickle.dump(object,file)

def loadObject(filename):
    print('Loading....')
    with open(filename,'rb') as file:
        return pickle.load(file)

def BuildTree(expression):  
    # STRING = '((2+5)*(4/((7-2)+2)))'
    # STRING2 = '(((5+2)*(2-1))/((2+9)+((7-2)-1))*8)'
    # expression= STRING2
    val = ExpressionValidation(expression)
    if val.isValidExpression():
        print(f'Expression: {expression}')
        print(f'result: {eval(expression)}')
        binarytree = BinaryTree()
        binarytree.createExpressionTree(expression,val.preprocessExpression)
        """ 
        use print on the binary tree
        object to visualize the tree  
        """
        print(binarytree)
        """ Saving the Binary Tree object """
        saveAs ='savedBinaryTree/binarytreedata.pkl'
        saveObject(binarytree,saveAs)


def main():
    while True:
        print('-'*55)
        print('Type "help" for a list of commands. Type "quit" to end.')
        print('\tOR\nPlease "type" in an expression: ')
        command = input('>>> ').lower()
        if command == 'quit' or command == 'clear':
            print('Quiting now')
            break
        elif command == 'help':
            print('quit: \n -- To quit\n')
            print('help: \n -- To display a list of commands\n')
            print('v : \n   -- To visualize the previous saved binary tree\n')
            print('v -a or v -animate : \n   -- To visualize the previous saved binary tree in an animated fashion\n')
            print('test: \n -- To run some test\n')
            print('Type an expression directly: \nTo create, save and visualize the a new binary Tree \n')
        elif command == 'test':
            testTreeMain(ExpressionValidation)
        elif command == 'v' :
            loadAs = 'savedBinaryTree/binarytreedata.pkl'
            binarytree = loadObject(loadAs)
            print(binarytree)
        elif command.split(' ') == ['v','-animate'] or command.split() == ['v','-a']:
            loadAs = 'savedBinaryTree/binarytreedata.pkl'
            binarytree = loadObject(loadAs)
            binarytree.animate = True
            print(binarytree)
        else:
            if len(command) > 1:
                BuildTree(command)
            else:
                print('Invalid command ')
        
if __name__ == '__main__':
    main()
