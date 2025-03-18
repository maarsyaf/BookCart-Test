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

    def test1_valid_login(self):
        """Uji skenario login sukses di berbagai browser"""
        for browser in self.browsers:
            with self.subTest(browser=browser):
                driver = self.initialize_driver(browser)
                driver.maximize_window()
                print(f"\n Running valid login test on {browser.capitalize()}...")

                try:
                    # Buka website
                    driver.get('https://bookcart.azurewebsites.net/')
                    print(f"1. Website Opened")
                    driver.implicitly_wait(5)

                    # Klik tombol login
                    driver.find_element(By.XPATH, get_xpath(driver, 'OIoqDBj0pCWLHTO')).click()

                    # Isi username & password (valid)
                    driver.find_element(By.XPATH, get_xpath(driver, '9jLX4IRGXNUivnV')).send_keys('testabdb9')
                    driver.find_element(By.XPATH, get_xpath(driver, 'MG5MHyvBnjDYiRv')).send_keys('T3st@bdb9', Keys.ENTER)
                    
                    # Tunggu hingga elemen profil pengguna muncul
                    driver.implicitly_wait(5)
                    user_profile = driver.find_element(By.XPATH, get_xpath(driver, '3x19vu0GEL7PpsM'))
                    self.assertTrue(user_profile.is_displayed(), f"Login failed on {browser}")
                    print(f" 2. Login Success")

                except Exception as e:
                    print(f"❌ Test Failed on {browser.capitalize()}! Error: {e}")
                    self.fail(f"Test failed on {browser}: {e}")

                finally:
                    driver.quit()

    def test2_invalid_login(self):
        """Uji skenario login gagal dengan kredensial yang salah"""
        for browser in self.browsers:
            with self.subTest(browser=browser):
                driver = self.initialize_driver(browser)
                driver.maximize_window()
                print(f"\n Running invalid login test on {browser.capitalize()}...")

                try:
                    # Buka website
                    driver.get('https://bookcart.azurewebsites.net/')
                    print("1. Website Opened")
                    driver.implicitly_wait(5)

                    # Klik tombol login
                    driver.find_element(By.XPATH, get_xpath(driver, 'OIoqDBj0pCWLHTO')).click()

                    # Isi username & password (invalid)
                    driver.find_element(By.XPATH, get_xpath(driver, '9jLX4IRGXNUivnV')).send_keys('testabdb9')
                    driver.find_element(By.XPATH, get_xpath(driver, 'MG5MHyvBnjDYiRv')).send_keys('test123', Keys.ENTER)
                    
                    # Tunggu hingga pesan error muncul
                    driver.implicitly_wait(5)
                    error_message = driver.title
                    self.assertTrue(error_message.is_displayed("Login"), f"Error message not displayed on {browser}")
                    print(f"2. Invalid login correctly rejected")

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
