from nltk import NaiveBayesClassifier

class NBM(object):
    def __init__(self):
        self.classifier = None


    def train(self,features):
        self.classifier = NaiveBayesClassifier.train(features)

    def getClassifier(self):
        return self.classifier