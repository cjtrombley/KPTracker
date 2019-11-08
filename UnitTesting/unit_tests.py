import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class KPBT_Chrome_Tests(unittest.TestCase):
	def setup(self):
		self.chrome = webdriver.Chrome()

	def test_home_page_title(self):
		self.chrome.get("localhost:8888/")
		self.assertIn("TEST", self.chrome.title)

	def tearDown(self):
		self.chrome.close()

class KPBT_Firefox_Tests(unittest.TestCase):
	def setup(self):
		self.firefox = webdriver.Firefox()

	def test_home_page_title(self):
		self.firefox.get("localhost:8888/")
		self.assertIn("TEST", self.firefox.title)

	def tearDown(self):
		self.firefox.close() 

class KPBT_Edge_Tests(unittest.TestCase):
	def setup(self):
		self.edge = webdriver.Edge()

	def test_home_page_title(self):
		self.edge.get("localhost:8888/")
		self.assertIn("TEST", self.edge.title)

	def tearDown(self):
		self.edge.close() 

if __name__ == '__main__':
	unittest.main()