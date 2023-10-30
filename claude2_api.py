import openai
import os

class GPT3TurboAPI:
    def __init__(self):
        self.api_key = ""

    def send_message(self, messages):
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message['content']

        # Check if the request was successful
        if response['choices'][0]['finish_reason'] == 'stop':
            # Return the message from the response
            return response['choices'][0]['message']['content']

        else:
            # If the request was not successful, return an error message
            return "Error: Could not send message"