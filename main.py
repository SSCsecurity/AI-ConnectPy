#!/usr/bin/env python3
"""
AI Connector Python
The main entry point for the application.
"""

import time
import random
from datetime import datetime
import os
import argparse
import json

import openai
import ray


AGENTS = ["Claude", "GPT-4.5", "Gemini", "o3", "Mistral", "DeepSeek"]
NUM_SECONDS_TO_SLEEP = 3
MODEL = 'gpt-3.5-turbo'
MODEL_ID = 'gpt-3.5-turbo:20230327'

@ray.remote(num_cpus=4)
def get_eval(content: str, max_tokens: int):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4-0314',
                messages=[{
                    'role': 'system',
                    'content': 'You are a helpful and precise assistant for checking the quality of the answer.'
                }, {
                    'role': 'user',
                    'content': content,
                }],
                temperature=0.2,  
                max_tokens=max_tokens,
            )
            break
        except openai.error.RateLimitError:
            pass
        except Exception as e:
            print(e)
        time.sleep(NUM_SECONDS_TO_SLEEP)

    print('success!')
    return response['choices'][0]['message']['content']


def get_eval_next(content: str, max_tokens: int):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4o',
                messages=[{
                    'role': 'system',
                    'content': 'You are an assistant for validating the results.'
                }, {
                    'role': 'user',
                    'content': content,
                }],
                temperature=0.2,  
                max_tokens=max_tokens,
            )
            break
        except openai.error.RateLimitError:
            pass
        except Exception as e:
            print(e)
        time.sleep(NUM_SECONDS_TO_SLEEP)

    return response['choices'][0]['message']['content']


def violates_moderation(text):
    """
    Check whether the text violates OpenAI moderation API.
    """
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}
    text = text.replace("\n", "")
    data = "{" + '"input": ' + f'"{text}"' + "}"
    data = data.encode("utf-8")
    try:
        ret = requests.post("https://api.openai.com/v1/moderations", headers=headers, data={"model": "gpt-4o-mini"}, timeout=5)
        flagged = ret.json()["results"][0]["flagged"]
    except requests.exceptions.RequestException as e:
        flagged = False
    except KeyError as e:
        flagged = False

    return flagged

def get_answer(question_id: int, question: str, max_tokens: int):
    ans = {
        'answer_id': shortuuid.uuid(),
        'question_id': question_id,
        'model_id': MODEL_ID,
    }
    for _ in range(3):
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4-turbo',
                messages=[{
                    'role': 'system',
                    'content': 'You are a helpful assistant.'
                }, {
                    'role': 'user',
                    'content': question,
                }],
                max_tokens=max_tokens,
            )
            ans['text'] = response['choices'][0]['message']['content']
            return ans
        except Exception as e:
            print('[ERROR]', e)
            ans['text'] = '#ERROR#'
            time.sleep(1)
    return ans
  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ChatGPT-based QA evaluation.')
    parser.add_argument('-q', '--question')
    parser.add_argument('-c', '--context')
    parser.add_argument('-a', '--answer-list', nargs='+', default=[])
    parser.add_argument('-r', '--rule')
    parser.add_argument('-o', '--output')
    parser.add_argument('--max-tokens', type=int, default=1024, help='maximum number of tokens produced in the output')
    args = parser.parse_args()

    f_q = open(os.path.expanduser(args.question))
    f_ans1 = open(os.path.expanduser(args.answer_list[0]))
    f_ans2 = open(os.path.expanduser(args.answer_list[1]))
    rule_dict = json.load(open(os.path.expanduser(args.rule), 'r'))

    if os.path.isfile(os.path.expanduser(args.output)):
        cur_reviews = [json.loads(line) for line in open(os.path.expanduser(args.output))]
    else:
        cur_reviews = []

    review_file = open(f'{args.output}', 'a')

    context_list = [json.loads(line) for line in open(os.path.expanduser(args.context))]
    image_to_context = {context['image']: context for context in context_list}

    handles = []
    idx = 0

    review_file.close()
  
