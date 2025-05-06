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


import random

#ad to test
import random

def get_response(user_input):
    # Define the province-to-map mapping
    province_map = {
        "Western Province": "https://www.google.com/maps?q=Western+Province,Sri+Lanka",
        "Central Province": "https://www.google.com/maps?q=Central+Province,Sri+Lanka",
        "Southern Province": "https://www.google.com/maps?q=Southern+Province,Sri+Lanka",
        "Northern Province": "https://www.google.com/maps?q=Northern+Province,Sri+Lanka",
        "Eastern Province": "https://www.google.com/maps?q=Eastern+Province,Sri+Lanka",
        "North Western Province": "https://www.google.com/maps?q=North+Western+Province,Sri+Lanka",
        "North Central Province": "https://www.google.com/maps?q=North+Central+Province,Sri+Lanka",
        "Uva Province": "https://www.google.com/maps?q=Uva+Province,Sri+Lanka",
        "Sabaragamuwa Province": "https://www.google.com/maps?q=Sabaragamuwa+Province,Sri+Lanka"
    }

    # Define the intent patterns and responses
    intents = [
        {
            "tag": "Province",
            "patterns": [
                "Western Province",
                "Central Province",
                "Southern Province",
                "Northern Province",
                "Eastern Province",
                "North Western Province",
                "North Central Province",
                "Uva Province",
                "Sabaragamuwa Province"
            ],
            "responses": ["__show_map__"]
        }
    ]

    # Check if the input matches any province
    for intent in intents:
        if any(pattern.lower() in user_input.lower() for pattern in intent["patterns"]):
            # If a province is found, fetch the relevant map URL
            for pattern in intent["patterns"]:
                if pattern.lower() in user_input.lower():
                    map_url = province_map.get(pattern, "https://www.google.com/maps?q=Colombo+Sri+Lanka")
                    # Return the map URL as a clickable link
                    return f"Sure! Here's the map for {pattern}: <a href='{map_url}' target='_blank'>{map_url}</a>"

    # Default response if no province is matched
    return "I don't understand your question. Can you ask about a specific province?"
