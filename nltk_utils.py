import nltk
import numpy as np
# nltk.download('punkt')
# nltk.download('punkt_tab')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()


# NLP tokenization - breaking the raw text into small chunks
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# ! Testing tokenization  #
# text = "Hi there, what can I do for you?"
# print(text)
# text = tokenize(text)
# print(f"Output: {text}")
# exit()


# NLP stemming - lowers inflection in words to their root forms
def stem(word):
    return stemmer.stem(word.lower())

# eg:
# stem("Running")    # returns 'run'
# stem("Played")     # returns 'play'
# stem("Better")     # returns 'better' (PorterStemmer doesn't handle all inflections)



#! Testing stemming  #
# text = "Hello, looking for something?"
# print(f"Sentence: {text}")
#
# text = tokenize(text)
# print(f"Tokenized Sentence: {text}")
#
# stemmed_words = [stem(w) for w in text]
# print(f"Stemmed words: {stemmed_words}")
# exit()

# Creating NLP bag of words - representation of text that describes the occurrence of words within a document
def bag_of_words(tokenized_sentence, all_words):
    """
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog = [0, 1, 0, 1, 0, 0, 0]
    """
    tokenized_sentence = [stem(w) for w in tokenized_sentence]

    bag = np.zeros(len(all_words), dtype=np.float32)
    for index, word in enumerate(all_words):
        if word in tokenized_sentence:
            bag[index] = 1.0

    return bag


#! Testing tokenize and stemming  #
# a = "See you later, thanks for visiting."
# print(a)
#
# a = tokenize(a)
# print(a)
#
# stemmed_words = [stem(w) for w in a]
# print(stemmed_words)

# ! Testing bag of words  #
# sentence = ["hello", "how", "are", "you"]
# all_words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
# bag = bag_of_words(sentence, all_words)
# print(bag)
# print(f"Length of all word: {len(all_words)} \nLength of bag_of_words: {len(bag)}")
