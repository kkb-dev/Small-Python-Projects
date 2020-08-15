import numpy
import tflearn
import tensorflow
import json, random, pickle
import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()
class Chatty():
    def __init__(self):
        with open('intents.json') as file:
            data = json.load(file)

        try: # If training completed
            with open("data.pickle","rb") as f:
                words, labels, training, output = pickle.load(f)
                    
        except: #If training doesn't exist
            words = []
            labels = []
            docs_x = []
            docs_y = []

            for intent in data["intents"]:
                for pattern in intent["patterns"]:
                    wrds = nltk.word_tokenize(pattern)
                    words.extend(wrds)
                    docs_x.append(wrds)
                    docs_y.append(intent["tag"])
                    
                    if intent["tag"] not in labels:
                        labels.append(intent["tag"])
                        
            # Create 'bag' for words
            words = [stemmer.stem(w.lower()) for w in words if w != '?']
            words = sorted(list(set(words)))
            labels=sorted(labels)
            
            training = []
            output = []

            out_empty = [0 for _ in range(len(labels))]

            for x,doc in enumerate(docs_x):
                bag = []

                wrds = [stemmer.stem(w) for w in doc]

                for w in words:
                    if w in wrds:
                        bag.append(1)
                    else:
                        bag.append(0)
                        
                output_row = out_empty[:]
                output_row[labels.index(docs_y[x])] = 1

                training.append(bag)
                output.append(output_row)

            training = numpy.array(training)
            output = numpy.array(output)
            
            with open("data.pickle","wb") as f:
                pickle.dump((words, labels, training, output), f)
          
        # Deep Learning 
        tensorflow.reset_default_graph()
        # Take input data and compute 
        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net,8)
        net = tflearn.fully_connected(net,8)
        # Use input to create best output 
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)

        model = tflearn.DNN(net)

        try: # Use saved training
            model.load("model.tflearn")
        except: # Conduct training
            # epoch = Train 1000 times, show_metric = Shows training data
            model = tflearn.DNN(net)
            model.fit(training,output, n_epoch=1000, batch_size=8, show_metric=True)
            model.save("model.tflearn")

        self.model = model
        self.words = words
        self.labels = labels
        self.data = data


    def chat(self,inp):
            model = self.model
            words = self.words
            labels = self.labels
            data = self.data
            
            results = model.predict([bag_of_words(inp,words)])[0]
            results_index = numpy.argmax(results)
            tag = labels[results_index]

            print(results[results_index],':',tag)
            if results[results_index] >= 0.91:
                for tg in data["intents"]:
                    if tg["tag"] == tag:
                        responses = tg["responses"]
                return tag
                
            else:
                return "huh?"
            


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


        

