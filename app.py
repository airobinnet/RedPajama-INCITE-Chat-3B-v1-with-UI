from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList

# Initialize Flask app
app = Flask(__name__)
CORS(app)

MIN_TRANSFORMERS_VERSION = '4.25.1'

# Check if transformers library version is compatible
assert transformers.__version__ >= MIN_TRANSFORMERS_VERSION, f'Please upgrade transformers to version {MIN_TRANSFORMERS_VERSION} or higher.'

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("togethercomputer/RedPajama-INCITE-Chat-3B-v1", cache_dir='models/tokenizers/')
model = AutoModelForCausalLM.from_pretrained("togethercomputer/RedPajama-INCITE-Chat-3B-v1", torch_dtype=torch.float16, cache_dir='models/')
model = model.to('cuda:0')

# Define custom stopping criteria for model generation
class StoppingCriteriaSub(StoppingCriteria):
    def __init__(self, stops=[], encounters=1):
        super().__init__()
        self.stops = [stop.to("cuda") for stop in stops]

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor):
        for stop in self.stops:
            if torch.all((stop == input_ids[0][-len(stop) :])).item():
                return True

        return False

# Define stop words and stopping criteria
stop_words = ["<human>:"]
stop_words_ids = [
    tokenizer(stop_word, return_tensors="pt")["input_ids"].squeeze()
    for stop_word in stop_words
]
stopping_criteria = StoppingCriteriaList([StoppingCriteriaSub(stops=stop_words_ids)])

# Initialize chat history
history = []

# Define route to clear chat history
@app.route('/clear_history', methods=['POST'])
def clear_history():
    global history
    history = []
    return jsonify({'status': 'success'})

# Define route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Define route for generating model response
@app.route('/generate', methods=['POST'])
def generate():
    global history
    data = request.get_json()
    pre_prompt = data['chat_input']
    history.append(f'<human>: {pre_prompt}')

    # Keep only the last 10 messages in the history
    if len(history) > 20:
        history.pop(0)
        history.pop(0)
    
    prompt = '\n'.join(history) + '\n<bot>:'

    print(f"Prompt: {prompt}")
    inputs = tokenizer(prompt, return_tensors='pt').to(model.device)
    input_length = inputs.input_ids.shape[1]
    outputs = model.generate(
        **inputs, max_new_tokens=512, do_sample=True, temperature=0.7, top_p=0.8, top_k=40, return_dict_in_generate=True, 
        stopping_criteria=stopping_criteria
    )
    token = outputs.sequences[0, input_length:]
    output_str = tokenizer.decode(token)
    output_str = output_str.replace("<human>:", "")
    history.append(f'<bot>: {output_str}')
    return jsonify({'response': output_str})

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')