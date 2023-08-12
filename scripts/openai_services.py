import os

import openai
import tiktoken

from .openai_decorator import retry_on_openai_errors

openai.api_key = os.environ.get(
    "OPENAI_API_KEY", ""
)

class AI:
    def __init__(self, encoding_model: str = "cl100k_base"):
        self.tt_encoding = tiktoken.get_encoding(encoding_model)

    def token_counter(self, passage):
        tokens = self.tt_encoding.encode(passage)
        total_tokens = len(tokens)
        return total_tokens

    @retry_on_openai_errors(max_retry=7)
    def extract_dialogue(self, transcript, history=[]):
        prompt = """
        Identify and extract dialogue involving a therapist and multiple children/teens from the provided text.
        Present the conversation in the following format:

        Therapist:
        Child 1:
        Child 2:
        ....
        """
        while True:
            try:
                if history:
                    messages = history
                else:
                    messages = [
                        {"role": "system", "content": prompt},
                    ]
                user_massagge = {"role": "user",
                                 "content": transcript.replace('\n', '')}
                messages.append(user_massagge)
                tokens_per_message = 4
                max_token = 4096 - (self.token_counter(prompt) + self.token_counter(
                    transcript) + (len(messages)*tokens_per_message) + 3)
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    max_tokens=max_token,
                    temperature=1,
                    top_p=1,
                    presence_penalty=0,
                    frequency_penalty=0,
                )
                bot_response = response["choices"][0]["message"]["content"].strip()
                return bot_response

            except openai.error.RateLimitError:
                messages.pop(1)
                continue