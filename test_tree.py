"""
  REFERENCES

  1. https://www.adamsmith.haus/python/examples/1293/unittest-add-test-cases-to-a-test-suite

  2. https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python

"""
import unittest
class Test(unittest.TestCase):  
    def __init__(self,ExpressionValidation,**kwargs):
        super(Test, self).__init__()
        self.expression = kwargs['expression']
        self.index = kwargs['index']
        self.isTestcase = kwargs['debug']
        self.actualResults = kwargs['results']
        self.val = ExpressionValidation(self.expression)

    def runTest(self):
        resultText = f'\ntest passed'
        try:
            results = self.val.isValidExpression(isTestcase=self.isTestcase)
            self.assertEqual(results,self.actualResults)
        except AssertionError:
            resultText = f'\ntest failed'
        finally:
            print('\n'+'-'*20)
            print(f'\n| case {self.index}: |')
            print(f'\nexpression -- {self.expression} ')
            print(f'\nOutput: {results}')
            print(f'\nExpected Output: {self.actualResults} ')
            print(resultText)


def testTreeMain(ExpressionValidation):
    testCases = [
        #   expression || validexpression ?
            ('(4*3*2)'   ,False ),
            ('(4*(2))'   ,False ),
            ('(4*(3+2)*(2+1))',False ), 
            ('(2*4)*(3+2)', False ), 
            ('((2+3)*(4*5)', False ), 
            ('(2+5)*(4/(2+2)))',False ), 
            ('(((2+3)*(4*5))+(1(2+3)))',False),
        ]
    suite = unittest.TestSuite()
    for index,(expression,result) in enumerate(testCases):
        info = {'results':result,'expression':expression,'index':index+1,'debug':True}
        suite.addTest(Test(ExpressionValidation,**info))
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    pass
    print('Hello test')
    #testTreeMain(ExpressionValidation)
