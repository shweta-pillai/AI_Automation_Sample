import openai
import os
from dotenv import load_dotenv
load_dotenv()
class AIUtility:

    def __init__(self):
        openai.api_key = os.getenv("API_KEY") # Replace with your API key



    def generate_xpath(self, element_description):
        prompt = f"Generate an XPath for '{element_description}' on a registration page."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        xpath = response['choices'][0]['message']['content'].strip()
        return xpath



    def store_xpath(self, identifier, xpath):
        """Store the generated XPath in xpath.robot."""
        variable_declaration = f'${{{identifier}}}    {xpath}\n'

        # Check if the variable already exists and update
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
        """Load XPath from xpath.robot."""
        try:
            with open(self.xpath_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith(f"${{{identifier}}}"):
                        return line.split("    ", 1)[1].strip()
        except FileNotFoundError:
            return None


