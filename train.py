import json
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from model import NeuralNet

# ! Open intents.json file in read mode
with open('intents.json', 'r') as td:
    intents = json.load(td)

# ! Collect all words for words in intents
all_words = []
tags = []
xy = []  # holds patterns and tags

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))  # append the pattern and the corresponding tag


# ! Lower and stem the collected words / exclude punctuation characters
ignore_words = ['?', '!', '.', ',']
# list comprehension
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))  # remove duplicates and sort
tags = sorted(set(tags))


# ! Create bag of words
X_train = []
y_train = []

for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)

    label = tags.index(tag)
    y_train.append(label)  # CrossEntropyLoss

# !* Create training data
# Convert to numpy array
X_train = np.array(X_train)
y_train = np.array(y_train)

# print(X_train)
# exit()

# ! Create pytorch dataset from training data
class ChatDataset(Dataset):
    def __init__(self):
        self.number_of_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # dataset[index]
    # magic methods call
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.number_of_samples


# Hyper parameters
batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(X_train[0])
learning_rate = 0.001
num_of_epochs = 1000

# print(output_size)
# print(input_size)
# exit()

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

# * Check for CUDA GPU support
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ! Create the model
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# ! Loss and optimizer
criterion = nn.CrossEntropyLoss()  # difference between two probability distributions -  loss between input and target
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# ! Training Loop
for epoch in range(num_of_epochs):
    # * Training loader
    for (words, labels) in train_loader:  # x,y
        words = words.to(device)
        labels = labels.to(device, dtype=torch.int64)

        # Forward pass
        outputs = model(words)
        loss = criterion(outputs, labels)  # loss between input and target

        # Backward pass and optimizer
        optimizer.zero_grad()   # empty the gradient
        loss.backward()         # calc back propagation
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f"Progress {(epoch + 1)/10}%, loss={loss.item():.4f}")
        # print(f"epoch {epoch + 1}/{num_of_epochs / epoch + 1}, loss={loss.item():.4f}")

print(f"Final loss = {loss.item():.4f}")

# ! Save trained data
data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"   # define save file name
torch.save(data, FILE)    # save to file

print(f"Training completed, file saved to {FILE}")
