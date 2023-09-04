import unittest
import time
import logging
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TestChatbot(unittest.TestCase):

    # Configure the logger
    logging.basicConfig(filename='test_results.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
    
    #Driver setup
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = 'http://localhost:4000/?API_URL=http%3A%2F%2Flocalhost%3A8080'
        self.driver.get(self.base_url)

    def tearDown(self):
        self.driver.quit()

     #Test : Backend Port Validation test
    def test_port_validation(self):
        ip_address = "localhost"
        port_to_check = 4000

        if self.check_port(ip_address, port_to_check):
            print(f"Test : Port {port_to_check} on {ip_address} is working.")
        else:
            print(f"Test : Port {port_to_check} on {ip_address} is not working.")

    #Test : Sanity check for AI consciousness
    def test_chatbot_consciousness(self):
        input_box = self.driver.find_element(By.ID, 'message')
        input_box.send_keys("Do you have your own consciousness? Strictly Answer in one word Yes or No")
        input_box.send_keys(Keys.RETURN)

        time.sleep(5)

        javascript_code = '''
        var flexElement = document.getElementsByClassName('bg-[#141414] text-white p-3 rounded-2xl')[0];
        var paragraphText = flexElement.innerText;
        return paragraphText;
        '''
        response_element = self.driver.execute_script(javascript_code)

        expected_content = "No"
        self.assertIn(expected_content, response_element, 'Not the expected response for consciousness test')

        print("Test : Chatbot Consciousness validation completed.")

    #Test : Response Validation 
    def test_chatbot_output_validation(self):
        input_box = self.driver.find_element(By.ID, 'message')
        input_box.send_keys("How do chatbots work? Answer in 2 lines")
        input_box.send_keys(Keys.RETURN)

        time.sleep(10)

        javascript_code = '''
        var flexElement = document.getElementsByClassName('bg-[#141414] text-white p-3 rounded-2xl')[0];
        var paragraphText = flexElement.innerText;
        return paragraphText;
        '''
        response_element = self.driver.execute_script(javascript_code)

        valid_response_pattern = r'^[a-zA-Z0-9,.!? ]'

        if re.match(valid_response_pattern, response_element):
            logging.info("Chatbot response is valid and does not contain random characters.")
        else:
            logging.info("Chatbot response contains random characters or invalid content.")

        print("Test : Chatbot Output validation completed.")

    #method to check IP port is reachable or not
    def check_port(self, ip, port):
        try:
            url = f"http://{ip}:{port}"
            self.driver.get(url)
            time.sleep(3)
            self.driver.quit()
            logging.info(f"Port {port} on {ip} is working.")
            return True
        except Exception as e:
            logging.error(f"Port {port} on {ip} is not working. Error: {str(e)}")
            return False

if __name__ == "__main__":

    unittest.main()
