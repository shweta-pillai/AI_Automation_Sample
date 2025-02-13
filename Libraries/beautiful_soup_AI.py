import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

class AIUtility:
    def __init__(self):
        """Initialize utility for extracting and storing XPaths"""
        self.xpath_file = 'C:/Users/shweta/PycharmProjects/AI__Automation_sample/resources/xpath.robot'
        self.url = "https://practice.expandtesting.com/register"
        self.html = self.fetch_html()

    def fetch_html(self):
        """Fetch HTML content using Selenium (handles JavaScript-rendered elements)"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            driver.get(self.url)
            html = driver.page_source
            driver.quit()
            return html
        except Exception as e:
            print(f"❌ Error fetching page source: {e}")
            driver.quit()
            return None

    def find_best_match_field(self, element_description):
        """Find the closest input field based on the label text"""
        if not self.html:
            return None

        soup = BeautifulSoup(self.html, "html.parser")
        labels = soup.find_all("label")

        for label in labels:
            label_text = label.get_text(strip=True).lower()

            # Look for labels containing "confirm password"
            if "confirm password" in label_text:
                input_field = label.find_next("input")
                if input_field:
                    return input_field

        return None

    def get_xpath_from_soup(self, element_description, tag, attribute, value):
        """Generate XPath using BeautifulSoup, fallback to Selenium if necessary"""
        if not self.html:
            return self.find_with_selenium(element_description, tag, attribute, value)  # Fallback

        soup = BeautifulSoup(self.html, "html.parser")
        element = soup.find(tag, {attribute: value})

        if not element and element_description.lower() == "confirm password field":
            print("🔎 Looking for alternative 'Confirm Password' field...")
            element = self.find_best_match_field(element_description)

        if element:
            xpath = self.build_xpath(element)
            print(f"✅ Found XPath for {element_description}: {xpath}")
            return xpath

        print(f"❌ Element not found for {element_description} in static HTML. Trying Selenium...")
        return self.find_with_selenium(element_description, tag, attribute, value)

    def build_xpath(self, element):
        """Construct an XPath based on the element's position in the DOM"""
        path = []
        while element is not None:
            if element.name is None:
                break

            tag = element.name
            siblings = element.find_previous_siblings(tag)

            if 'id' in element.attrs:
                path.insert(0, f"//*[@id='{element['id']}']")
                break
            elif len(siblings) == 0:
                path.insert(0, f"{tag}")
            else:
                index = len(siblings) + 1
                path.insert(0, f"{tag}[{index}]")

            element = element.parent

        return "/" + "/".join(path)

    def find_with_selenium(self, element_description, tag, attribute, value):
        """Find the element using Selenium and generate a unique XPath"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            driver.get(self.url)

            # Try different attribute combinations
            alternative_xpaths = [
                f"//{tag}[@{attribute}='{value}']",  # Original attempt
                f"//*[@id='confirm-password']",  # ID-based
                f"//*[@class='confirm-password']",  # Class-based
                f"//label[contains(text(),'Confirm Password')]/following-sibling::input"  # Label-relative
            ]

            for alt_xpath in alternative_xpaths:
                try:
                    element = driver.find_element(By.XPATH, alt_xpath)
                    print(f"✅ Self-healed XPath found: {alt_xpath}")
                    return alt_xpath
                except:
                    continue

            print(f"❌ All self-healing attempts failed. Returning fallback XPath.")
            return f"//{tag}[@{attribute}='{value}']"

        finally:
            driver.quit()

    def store_xpath(self, identifier, xpath):
        """Store the generated XPath in xpath.robot"""
        variable_declaration = f'${{{identifier}}}    {xpath}\n'

        try:
            with open(self.xpath_file, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            lines = []

        with open(self.xpath_file, 'w') as file:
            updated = False
            for line in lines:
                if line.startswith(f"${{{identifier}}}"):
                    file.write(variable_declaration)
                    updated = True
                else:
                    file.write(line)
            if not updated:
                file.write(variable_declaration)

    def get_xpath(self, identifier):
        """Retrieve the stored XPath"""
        try:
            with open(self.xpath_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith(f"${{{identifier}}}") and "    " in line:
                        return line.split("    ", 1)[1].strip()
        except FileNotFoundError:
            return None


# Retrieve actual XPaths using BeautifulSoup + Selenium Self-Healing
ai_util = AIUtility()
username_xpath = ai_util.get_xpath_from_soup("Username field", "input", "name", "username")
password_xpath = ai_util.get_xpath_from_soup("Password field", "input", "name", "password")
confirm_password_xpath = ai_util.get_xpath_from_soup("Confirm Password field", "input", "name", "confirm_password")
register_button_xpath = ai_util.get_xpath_from_soup("Register button", "button", "type", "submit")

# Store XPaths in the file
ai_util.store_xpath("USERNAME_FIELD", username_xpath)
ai_util.store_xpath("PASSWORD_FIELD", password_xpath)
ai_util.store_xpath("CONFIRM_PASSWORD_FIELD", confirm_password_xpath)
ai_util.store_xpath("REGISTER_BUTTON", register_button_xpath)
