import os
import re
import torch
from dotenv import load_dotenv
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

class AIUtility:
    def __init__(self):
        """Load pre-trained GPT-2 model and tokenizer"""
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.xpath_file = 'C:/Users/shweta/PycharmProjects/AI__Automation_sample/resources/xpath.robot'

    def get_actual_xpath(self, element_description, attribute, value):
        """Use Selenium to extract the correct XPath for a given element, with AI-powered self-healing"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            driver.get("https://practice.expandtesting.com/register")
            xpath = f"//{attribute}[{value}]"
            element = driver.find_element(By.XPATH, xpath)
            print(f"✅ Found XPath for {element_description}: {xpath}")
            return xpath  # Returning the valid XPath

        except Exception as e:
            print(f"❌ Error finding XPath for {element_description}: {e}")
            print("🔄 Attempting AI-powered self-healing...")

            # AI-Based Self-Healing Strategy
            alternative_xpaths = self.generate_alternative_xpaths(element_description)

            for alt_xpath in alternative_xpaths:
                try:
                    element = driver.find_element(By.XPATH, alt_xpath)
                    print(f"✅ Self-healed XPath found: {alt_xpath}")
                    return alt_xpath
                except:
                    continue

            print("❌ AI self-healing failed. Returning fallback XPath.")
            return f"//{attribute}[{value}]"  # Return fallback XPath if all AI attempts fail.

        finally:
            driver.quit()

    def generate_alternative_xpaths(self, element_description):
        """Use AI to generate alternative XPath suggestions"""
        prompt = (
            f"Generate possible alternative XPath locators for an HTML input field labeled '{element_description}'. "
            f"Provide multiple variations such as ID-based, class-based, and label-relative XPaths."
        )

        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        attention_mask = torch.ones_like(input_ids)

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_length=100,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Extract multiple XPath patterns using regex
        matches = re.findall(r'//[a-zA-Z]+(?:\[@[a-zA-Z0-9_-]+=[\'"][a-zA-Z0-9_-]+[\'"]\])?', generated_text)

        # Add predefined alternative strategies
        matches.extend([
            f"//*[@id='{element_description.lower().replace(' ', '-')}']",
            f"//*[@class='{element_description.lower().replace(' ', '-')}']",
            f"//label[text()='{element_description}']/following-sibling::input"
        ])

        return list(set(matches))  # Return unique alternative XPaths

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


# Retrieve actual XPaths using Selenium with AI-powered self-healing
ai_util = AIUtility()
username_xpath = ai_util.get_actual_xpath("Username field", "input", "@name='username'")
password_xpath = ai_util.get_actual_xpath("Password field", "input", "@name='password'")
confirm_password_xpath = ai_util.get_actual_xpath("Confirm Password field", "input", "@name='confirm_password'")
register_button_xpath = ai_util.get_actual_xpath("Register button", "button", "@type='submit'")

# Store XPaths in the file
ai_util.store_xpath("USERNAME_FIELD", username_xpath)
ai_util.store_xpath("PASSWORD_FIELD", password_xpath)
ai_util.store_xpath("CONFIRM_PASSWORD_FIELD", confirm_password_xpath)
ai_util.store_xpath("REGISTER_BUTTON", register_button_xpath)
