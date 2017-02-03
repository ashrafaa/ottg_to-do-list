from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit();

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Ash has heard about a new online to-do list app.
        # He goes to check out its homepage.
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention to-do lists
        #assert 'To-Do' in browser.title, "Browser title was " + browser.title
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # He is asked to enter the first to-do item straight away

        # He types in buy some cat foods

        # When he hits enter, the page updates and now the page lists
        # "1. Buy some cat foods"

        # There is still text box to add another item.
        # He types in repair the car

        # The page updates again and shows both items in his list

        # He wonders if the site will remember her list. Then he sees
        # the site has generated a unique URL for her. Text is explanatory

        # He visits that url - his to do list still there

        # Satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main()