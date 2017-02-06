from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#class NewVisitorTest(unittest.TestCase):
class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        #self.browser = webdriver.Firefox()
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit();

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Ash has heard about a new online to-do list app.
        # He goes to check out its homepage.
        #self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)

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
        self.check_for_row_in_list_table('1: Buy some cat foods')

        # There is still text box to add another item.
        # He types in repair the car
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Repair the car')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again and shows both items in his list
        self.check_for_row_in_list_table('1: Buy some cat foods')
        self.check_for_row_in_list_table('2: Repair the car')

        # He wonders if the site will remember her list. Then he sees
        # the site has generated a unique URL for her. Text is explanatory
        self.fail('Finish the test')

        # He visits that url - his to do list still there

        # Satisfied, he goes back to sleep

# Comment below cause we use Django test runner now
# if __name__ == '__main__':
#     unittest.main()