from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from openai import OpenAI
import json
import requests
from groq import Groq

endpoints_and_models = [{"openai": ["gpt-4-turbo"],
                          "perplexity":["llama-3-8b-instruct", "llama-3-70b-instruct"],
                          "groq":["llama3-8b-8192", "llama3-70b-8192"]
    }
                        
                        ]

PPX_KEY = "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"
API_KEY = "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"
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
endpoints = dict(perplexity = OpenAI(api_key=PPX_KEY, base_url="https://api.perplexity.ai"),
                 groq = Groq(api_key="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"),
                 openai = OpenAI()
                 )
PROMPT = """
Trustworthiness Assessment:

Evaluate overall trustworthiness based on evidence, consistency, and reliability.
Logical Fallacies Detection:

Identify fallacies such as ad hominem, straw man, false dilemmas, slippery slopes, and circular reasoning.
Insincere Statements:

Detect insincerity in generalized claims, avoidance, flattery, and sarcasm.
Vague Statements:

Highlight ambiguity, generalizations, and undefined terms.
Unnecessary Hype:

Spot hyperbolic statements, excessive superlatives, and emotional appeals lacking substance.
Avoidance Behavior:

Identify deflection, evasive language, and minimization of issues.
Lack of Straightforwardness:

Detect evasive phrasing, inconsistencies, and attempts to obscure truth.
Supporting Evidence:

Check for credible citations, logical reasoning, and factual support.
Bias and Subjectivity:

Spot bias, subjective opinions, and lack of balanced perspectives.
Language and Tone:

Analyze for neutral/objective language, professional/respectful tone, and consistency.
here is the text to evaluate:
"""




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
            
    def _get_endpoint(model):
        return next((key for key, values in endpoints_and_models[0].items() if model in values), None)
             
  
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    stream = Stream(prompt=PROMPT + data.get('text', ''),
                    endpoints=endpoints
                    )
    for token in stream(data.get('model', '') , 0):
        socketio.emit('response', {'response': token})
    return jsonify({'status': 'finished'})

@app.route('/get_models', methods=['GET'])
def get_models():
    return jsonify({"models": [model for ep in endpoints_and_models for models in ep.values() for model in models]})



if __name__ == '__main__':
    socketio.run(app, port=3003, debug=True)
