from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is asked to enter the first to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types in buy some cat foods
        inputbox.send_keys('Buy some cat foods')

        # When he hits enter, the page updates and now the page lists
        # "1. Buy some cat foods"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(
        #     any(row.text == '1: Buy some cat foods' for row in rows),
        #     "New to-do item did not appear in table - its text was: \n %s" % (
        #     table.text,
        #     )
        # or with this:
        self.assertIn('1: Buy some cat foods', [row.text for row in rows])
        #)
        # There is still text box to add another item.
        # He types in repair the car
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Repair the car')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again and shows both items in his list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy some cat foods', [row.text for row in rows])
        self.assertIn('2: Repair the car', [row.text for row in rows])

        # He wonders if the site will remember her list. Then he sees
        # the site has generated a unique URL for her. Text is explanatory
        self.fail('Finish the test')

        # He visits that url - his to do list still there

        # Satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main()