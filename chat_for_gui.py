import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from style import AllStyles as gui

# Check for CUDA GPU support
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# open intents file
with open('intents.json', 'r') as td:
    intents = json.load(td)

# load saved model data
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

# Create the model
model = NeuralNet(input_size, hidden_size, output_size).to(device)
# Load model state dictionary
model.load_state_dict(model_state)
model.eval()  # set to evaluation mode

# ! Create the Chat
ai_bot_name = "Halsey"


def get_response(message):
    sentence = tokenize(message)
    x = bag_of_words(sentence, all_words)  # returns a numpy array
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x)

    # get predictions - predicted tag
    output = model(x)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # softmax prediction
    probability = torch.softmax(output, dim=1)
    probability_actual = probability[0][predicted.item()]

    # if probability is high, find responses
    if probability_actual.item() > 0.9:
        # find responses for matching tags
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    return "I don't understand your question..."
