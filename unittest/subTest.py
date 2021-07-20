import unittest

class CustomTest(unittest.TestCase):
    def __init__(self, name, a,b):
        super().__init__()
        self.name = name
        self.a = a
        self.b = b
    def runTest(self):
        print("test", self.name)
        self.assertEqual(self.a, self.b)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(CustomTest("Foo", 1337, 1337))
    suite.addTest(CustomTest("Bar", 0xDEAD, 1337))
    unittest.TextTestRunner().run(suite)
