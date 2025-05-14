import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from style import AllStyles as gui

# Check for CUDA GPU support
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents file
with open('intents.json', 'r') as td:
    intents = json.load(td)

# Load saved model data
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
model.eval()  # Set to evaluation mode

# Create the AI bot's name
ai_bot_name = "Techtara"


def get_response(message):
    # Tokenize the message and convert it to bag of words
    sentence = tokenize(message)
    x = bag_of_words(sentence, all_words)  # returns a numpy array
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x)

    # Get predictions - predicted tag
    output = model(x)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # Softmax prediction
    probability = torch.softmax(output, dim=1)
    probability_actual = probability[0][predicted.item()]

    # If probability is high, return responses
    if probability_actual.item() > 0.65:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    # Define the province-to-map mapping
    province_map = {
        "Western Province": "https://www.google.com/maps?q=Western+Province+private+IT+campus,Sri+Lanka",
        "Central Province": "https://www.google.com/maps?q=Central+Province+private+IT+campus,Sri+Lanka",
        "Southern Province": "https://www.google.com/maps?q=Southern+Province+private+IT+campus,Sri+Lanka",
        "Northern Province": "https://www.google.com/maps?q=Northern+Province+private+IT+campus,Sri+Lanka",
        "Eastern Province": "https://www.google.com/maps?q=Eastern+Province+private+IT+campus,Sri+Lanka",
        "North Western Province": "https://www.google.com/maps?q=North+Western+Province+private+IT+campus,Sri+Lanka",
        "North Central Province": "https://www.google.com/maps?q=North+Central+Province+private+IT+campus,Sri+Lanka",
        "Uva Province": "https://www.google.com/maps?q=Uva+Province+private+IT+campus,Sri+Lanka",
        "Sabaragamuwa Province": "https://www.google.com/maps?q=Sabaragamuwa+Province+private+IT+campus,Sri+Lanka"
    }

    # Define the intent patterns and responses
    province_intents = [
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
    for intent in province_intents:
        if any(pattern.lower() in message.lower() for pattern in intent["patterns"]):
            # If a province is found, fetch the relevant map URL
            for pattern in intent["patterns"]:
                if pattern.lower() in message.lower():
                    map_url = province_map.get(pattern, "https://www.google.com/maps?q=Colombo+Sri+Lanka")
                    # Return the map URL as a clickable link
                    return f"Sure! Here's the map for {pattern}: <a href='{map_url}' target='_blank'>{map_url}</a>"

    # Default response if no province is matched
    return "It seems like you're trying to find the location of a campus. Please make sure to mention the specific province correctly. If you're asking something else, feel free to rephrase your question and try again!"

# Example of using the function
if __name__ == "__main__":
    print("Type 'quit' to exit the chatbot")
    while True:
        user_input = input(f"{ai_bot_name}: ")
        if user_input.lower() == "quit":
            break
        response = get_response(user_input)
        print(f"{ai_bot_name}: {response}")
