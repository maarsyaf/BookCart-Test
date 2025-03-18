import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from elements_manager import *

class BookCartTest(unittest.TestCase):
    browsers = ["chrome", "firefox", "edge"]

    def initialize_driver(self, browser):
        """Inisialisasi WebDriver untuk masing-masing browser"""
        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            options.add_argument("--headless")
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

        elif browser == "edge":
            options = EdgeOptions()
            options.add_argument("--headless")
            return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

        else:
            self.fail(f"Browser {browser} tidak didukung!")

    def test_register(self):
        """Uji skenario register sukses di berbagai browser"""
        for browser in self.browsers:
            with self.subTest(browser=browser):
                driver = self.initialize_driver(browser)
                driver.maximize_window()
                print(f"\n Running valid register test on {browser.capitalize()}...")

                try:
                    # Buka website
                    driver.get('https://bookcart.azurewebsites.net/')
                    print(f"1. Website Opened")
                    driver.implicitly_wait(5)
                    # Menuju ke halaman register
                    driver.find_element(By.XPATH,get_xpath(driver,'OtgNS3rGe6xkjcT')).click()
                    driver.find_element(By.XPATH,get_xpath(driver,'DA27iRS8feMC4LJ')).click()
                    print(f"2. Register Menu Opened")
                    # Mengisi input register menu
                    driver.find_element(By.XPATH,get_xpath(driver,'MiCiWd5coqnzHht')).send_keys('abdillah') # Firstname
                    driver.find_element(By.XPATH,get_xpath(driver,'bdQrhcyvsdIg2jx')).send_keys('abdillah') # Lastname
                    driver.find_element(By.XPATH,get_xpath(driver,'injM1UNDUQsqA1Y')).send_keys('testabdb9') # Username
                    driver.find_element(By.XPATH,get_xpath(driver,'2PD5kkiZ1oFeCsf')).send_keys('T3st@bdb9') # Password
                    driver.find_element(By.XPATH,get_xpath(driver,'xBMzXjddosj7dH0')).send_keys('T3st@bdb9') # Confirm Password
                    # Pilih gender male
                    driver.find_element(By.XPATH,get_xpath(driver,'i5LC4xkooqLq0a4')).click() # female
                    driver.find_element(By.XPATH,get_xpath(driver,'fhJkCkv9vGfpOhY')).click() # male
                    # Klik register
                    driver.find_element(By.XPATH,get_xpath(driver,'xxMSQWqPCkwhmDY')).click()

                    # Tunggu hingga pesan error muncul
                    driver.implicitly_wait(5)
                    user_profile = driver.find_element(By.XPATH, get_xpath(driver, '3x19vu0GEL7PpsM'))
                    self.assertTrue(user_profile.is_displayed(), f"Login failed on {browser}")
                    print(f"3. Register Success")

                except NoSuchElementException:
                    print(f"❌ Error message not found on {browser.capitalize()}!")
                    self.fail(f"Error message not found on {browser}")

                except Exception as e:
                    print(f"❌ Test Failed on {browser.capitalize()}! Error: {e}")
                    self.fail(f"Test failed on {browser}: {e}")

                finally:
                    driver.quit()

    def tearDown(self):
        """Tidak ada teardown karena driver di-quit dalam finally"""
        pass

if __name__ == "__main__":
    unittest.main()
