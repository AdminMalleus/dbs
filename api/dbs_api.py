from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from openai import OpenAI
import json
import requests
from groq import Groq
import anthropic
from text_analysis_prompts import ling_and_seman, logic_and_arg, prag_and_disct, bias_and_sub
endpoints_and_models = [{"openai": ["gpt-4-turbo"],
                          "perplexity":["llama-3-8b-instruct", "llama-3-70b-instruct"],
                          "groq":["llama3-8b-8192", "llama3-70b-8192"],
                          "anthropic": ["claude-3-5-sonnet-20240620"]
    }
                        
                        ]

PPX_KEY = "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"
API_KEY = "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"
CLAUDE_KEY = "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"
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
endpoints = dict(perplexity = OpenAI(api_key=PPX_KEY, base_url="https://api.perplexity.ai"),
                 groq = Groq(api_key="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"),
                 openai = OpenAI()
                 )

class Stream:
    def __init__(self, prompt,
                  system="you're a helpful assistant",
                  endpoints=endpoints):
        self.prompt, self.system, self.endpoints = prompt, system, endpoints 
       
    def __call__(self, model, temperature):
        response_stream = self.endpoints[self._get_endpoint(model)].chat.completions.create(
             model=model,
             temperature=temperature,
             messages=[{"role": "system", "content": self.system},
                       {"role": "user", "content": self.prompt}],
             stream=True,
         )
        for r in response_stream:
            token = r.choices[0].delta.content 
            if token == None:
                break
            yield token
            
    def _get_endpoint(self, model):
        return next((key for key, values in endpoints_and_models[0].items() if model in values), None)


client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=CLAUDE_KEY,
)

# message = client.messages.create(
#     model="claude-3-5-sonnet-20240620",
#     max_tokens=1024,
#     messages=[
#         {"role": "user", "content": "tell me main categories of languages"}
#     ],
#     stream=True
# )

# stream = Stream(prompt="tell me main categories of languages", endpoints=endpoints)
# messages = [m for m in stream("gpt-4-turbo", 0)]

prompts = {'Language Structure & Meaning':ling_and_seman,
           'Logic & Argumentation':logic_and_arg,
           'Context & Discourse':prag_and_disct,
           'Bias & Author Intent':bias_and_sub}

def get_key_index(key): return list(prompts.keys()).index(key) + 1

class StreamAnth:
    def __init__(self, prompt):
        self.client = anthropic.Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=CLAUDE_KEY,
        )
        self.prompt = prompt
    def __call__(self, model, temperature):
        response_stream = self.client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": self.prompt}
            ],
            stream=True
        ) 
        for r in response_stream:
            if type(r).__name__ == "RawContentBlockDeltaEvent":
                yield r.delta.text 

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    # print(data)
    # Start a background task for each prompt
    for prompt, model in data['promptModels'].items():
        socketio.start_background_task(process_prompt, prompt, model, data['text'], data['promptTexts'][prompt])
    
    return jsonify({'status': 'processing started'})

# @app.route('/process', methods=['POST'])
# def process():
#     data = request.get_json()
#     # print(data)

#     # Start a background task for each prompt
#     for prompt, model in data['promptModels'].items():
#         stream = Stream(prompt=prompts[prompt] +"\n here's the text to analyse \n" + data['text'], endpoints=endpoints)
#         result = ''.join([t for t in stream(model, 0)])
#         socketio.emit('response', {'prompt': prompt, 'response': result}, namespace=f'/prompt{get_key_index(prompt)}')

#         # socketio.start_background_task(process_prompt, prompt, model, data['text'], data['promptTexts'][prompt])
    
#     return jsonify({'status': 'processing started'})


# def process_prompt(prompt, model, text, prompt_text):
#     buffer = []
#     if 'claude' in model:
#         stream = StreamAnth(prompt=prompts[prompt] +"\n here's the text to analyse\n" + text)
#     else:
#         stream = Stream(prompt=prompts[prompt] +"\n here's the text to analyse \n" + text, endpoints=endpoints)
#     for token in stream(model, 0):
#         # print(buffer)
#         if token == "####" or token =="###" or 1 <= len(buffer) <= 10:
#             buffer.append(token)
#         if len(buffer) == 0:
#             socketio.emit('response', {'prompt': prompt, 'response': token}, namespace=f'/prompt{get_key_index(prompt)}')
#         if len(buffer) >= 10:
#             socketio.emit('response', {'prompt': prompt, 'response': ''.join(buffer)}, namespace=f'/prompt{get_key_index(prompt)}')
#             buffer = []
def process_prompt(prompt, model, text, prompt_text):
    # print(prompt)
    if 'claude' in model:
        stream = StreamAnth(prompt=prompts[prompt] +"\n here's the text to analyse\n" + text)
    else:
        stream = Stream(prompt=prompts[prompt] +"\n here's the text to analyse \n" + text, endpoints=endpoints)
    for token in stream(model, 0):
        socketio.emit('response', {'prompt': prompt, 'response': token}, namespace=f'/prompt{get_key_index(prompt)}')
    
    socketio.emit('response', {'prompt': prompt, 'response': '[DONE]'}, namespace=f'/prompt{get_key_index(prompt)}')

@app.route('/get_models', methods=['GET'])
def get_models():
    return jsonify({"models": [model for ep in endpoints_and_models for models in ep.values() for model in models]})

@app.route('/get_categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': list(prompts.keys())})

@app.route('/get_prompts', methods=['GET'])
def get_prompts():
    return jsonify({'prompts': prompts})

@socketio.on('connect', namespace='/prompt1')
def connect_prompt1():
    print("Client connected to prompt1")

@socketio.on('connect', namespace='/prompt2')
def connect_prompt2():
    print("Client connected to prompt2")

@socketio.on('connect', namespace='/prompt3')
def connect_prompt3():
    print("Client connected to prompt3")

@socketio.on('connect', namespace='/prompt4')
def connect_prompt4():
    print("Client connected to prompt4")

if __name__ == '__main__':
    socketio.run(app, debug=True)
