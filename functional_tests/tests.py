import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 5

class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super(NewVisitorTest, cls).setUpClass()
        cls.server_url = cls.live_server_url

    def setUp(self):
        #self.browser = webdriver.Firefox()
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    def test_can_start_a_list_for_one_user(self):
        # Ash has heard about a new online to-do list app.
        # He goes to check out its homepage.
        #self.browser.get('http://localhost:8000')
        self.browser.get(self.server_url)

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
        #time.sleep(1)
        self.wait_for_row_in_list_table('1: Buy some cat foods')

        # There is still text box to add another item.
        # He types in repair the car
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Repair the car')
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(1)

        # The page updates again and shows both items in his list
        self.wait_for_row_in_list_table('1: Buy some cat foods')
        self.wait_for_row_in_list_table('2: Repair the car')

        # He wonders if the site will remember her list. Then he sees
        # the site has generated a unique URL for her. Text is explanatory
        #self.fail('Finish the test')

        # He visits that url - his to do list still there

        # Satisfied, he goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new list
        self.browser.get(self.server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegexpMatches(edith_list_url, '/lists/.+')

        # Now new user Francis comes along to the site

        # Use new browser session to ensure no Edith's info coming from cookies
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Francis visit the home page. No sign of Edith's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts new list by entering new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy a milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy a milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        #self.assertRegex(francis_list_url, '/lists/.+')
        self.assertRegexpMatches(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy a milk', page_text)

        # Satisfied, they both go back to sleep

    def test_layout_and_styling(self):
        #Edith goes to home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # She starts a new list and sees the input is nicely centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

# Comment below cause we use Django test runner now
# if __name__ == '__main__':
#     unittest.main()