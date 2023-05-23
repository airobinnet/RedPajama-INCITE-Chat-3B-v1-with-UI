# RedPajama-INCITE-Chat-3B-v1 with UI

This repository contains a simple AI chatbot web application using Flask, Transformers, and PyTorch. The chatbot uses the [togethercomputer/RedPajama-INCITE-Chat-3B-v1](https://huggingface.co/togethercomputer/RedPajama-INCITE-Chat-3B-v1) model from Hugging Face.

https://github.com/airobinnet/RedPajama-INCITE-Chat-3B-v1-with-UI/assets/126980386/cc9be08a-66bc-4cae-b79b-01ab94bb88ca

**Note:** This application requires a GPU with 8GB memory or more and a valid CUDA installation.

## How the Chatbot Works

The chatbot uses the pre-trained [togethercomputer/RedPajama-INCITE-Chat-3B-v1](https://huggingface.co/togethercomputer/RedPajama-INCITE-Chat-3B-v1) model to generate text responses based on user input. The application maintains a chat history of 10 messages to provide context for the model's responses.

## Installation

1. Clone the repository:

```
git clone https://github.com/airobinnet/RedPajama-INCITE-Chat-3B-v1-with-UI.git
cd RedPajama-INCITE-Chat-3B-v1-with-UI
```

2. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

1. Start the Flask web application:

```
python app.py
```
(this may take a while depending on your computer's speed)

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. Start chatting with the AI chatbot!
