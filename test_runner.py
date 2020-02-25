import unittest
import test_http_api

httpTestSuite = unittest.TestSuite()
httpTestSuite.addTest(unittest.makeSuite(test_http_api.HttpApiTests))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(httpTestSuite)