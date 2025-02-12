import os
import re
import torch
from dotenv import load_dotenv
from transformers import GPT2LMHeadModel, GPT2Tokenizer


load_dotenv()

class AIUtility:
    def __init__(self):
        """Load pre-trained GPT-2 model and tokenizer"""
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.xpath_file = 'C:/Users/shweta/PycharmProjects/AI__Automation_sample/resources/xpath.robot'

    def generate_xpath(self, element_description, field_type):
        """Generate a unique XPath using GPT-2, considering element type."""
        prompt = (
            f"Got to website https://practice.expandtesting.com/register, Inspect the elements present in the website, look for the element type of the xpath required then Generate a unique and valid XPath for an HTML element which matches '{element_description}'"
        )

        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        attention_mask = torch.ones_like(input_ids)

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_length=70,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Improved regex for extracting XPath
        match = re.search(r'//\w+\[@[\w-]+=[\'"]\w+[\'"]\]', generated_text)

        extracted_xpath = match.group(0) if match else f"//input[@name='{element_description.lower().replace(' ', '_')}']"
        print(f"Generated XPath for {element_description}: {extracted_xpath}")  # Debugging output
        return extracted_xpath



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


ai_util = AIUtility()
username_xpath = ai_util.generate_xpath("Username field", "text")
password_xpath = ai_util.generate_xpath("Password field", "password")
confirm_password_xpath = ai_util.generate_xpath("Confirm Password field", "password")
register_button_xpath = ai_util.generate_xpath("Register button", "button")

ai_util.store_xpath("USERNAME_FIELD", username_xpath)
ai_util.store_xpath("PASSWORD_FIELD", password_xpath)
ai_util.store_xpath("CONFIRM_PASSWORD_FIELD", confirm_password_xpath)
ai_util.store_xpath("REGISTER_BUTTON", register_button_xpath)
