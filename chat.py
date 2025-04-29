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

# print(model_state)
# print(input_size)
# print(output_size)
# print(hidden_size)
# print(all_words)
# print(tags)
# exit()

# Create the model
model = NeuralNet(input_size, hidden_size, output_size).to(device)
# Load model state dictionary
model.load_state_dict(model_state)
model.eval()  # set to evaluation mode

# ! Create the Chat

ai_bot_name = "Halsey"
print(f"{'='*49}\n|{gui.BOLD}{gui.HEADER} Let's have a chat!, what do you want to know. {gui.ENDC}|\n{'-'*49}\n| Type 'quit' to exit the chat.{' '*17}|\n{'='*49}")

while True:
    sentence = input(f"{' '*3}You: ")
    if sentence.lower() == "quit":
        break

    # Tokenize the sentence
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)   # returns a numpy array
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    # get predictions - predicted tag
    output = model(X)
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
                print("\n")
                print(f"{gui.WARNING}{ai_bot_name}: {gui.OKCYAN}{random.choice(intent['responses'])}{gui.ENDC}")
                print("\n")

    else:
        print("\n")
        print(f"{gui.WARNING}{ai_bot_name}: {gui.ENDC}I don't understand your question...")
        print("\n")
