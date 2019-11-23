import unittest
import glob

loader = unittest.TestLoader()
files = "unit"
suite = loader.discover(files)
runner = unittest.TextTestRunner()
runner.run(suite)
