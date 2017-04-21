import re,string
from collections import defaultdict
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk.classify
import codecs,random,mimetypes
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures


class featExtract(object):

    def __init__(self,spamFiles,hamFiles,n_gram,prop=.7):
        print str('\n[featExtract] Extracting features for ') + str(n_gram) + str(' gram...')
        self.spam_files = spamFiles
        self.ham_files = hamFiles
        self.n_gram = n_gram
        self.proportion  = prop
        self.trainSpamFeature= None
        self.testSpamFeature = None
        self.trainHamFeature = None
        self.testHamFeature = None


    def getTrainSpamFeature(self):
        no_of_spam_files  = len(self.spam_files)
        train_spam_files = self.spam_files[int(no_of_spam_files * self.proportion):]
        self.trainSpamFeature = self.feature_extract(train_spam_files,'spam',self.n_gram)
        return self.trainSpamFeature


    def getTestSpamFeature(self):
        no_of_spam_files = len(self.spam_files)
        test_spam_files = self.spam_files[:int(no_of_spam_files * self.proportion)]
        self.testSpamFeature = self.feature_extract(test_spam_files, 'spam', self.n_gram)
        return self.testSpamFeature


    def getTrainHamFeature(self):
        no_of_ham_files = len(self.ham_files)
        train_ham_files = self.ham_files[int(no_of_ham_files * self.proportion):]
        self.trainHamFeature = self.feature_extract(train_ham_files, 'ham', self.n_gram)
        return self.trainHamFeature

    def getTestHamFeature(self):
        no_of_ham_files = len(self.ham_files)
        test_ham_files = self.ham_files[:int(no_of_ham_files * self.proportion)]
        self.testHamFeature = self.feature_extract(test_ham_files, 'ham', self.n_gram)
        return self.testHamFeature

    def getTrainFeature(self):
        return self.getTrainSpamFeature() + self.getTrainHamFeature()

    def getTestFeature(self):
        return self.getTestHamFeature() + self.getTestSpamFeature()

    def feature_extract(self,filst, tag, n_gram=1):
        lk = re.compile(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        feature_tag = []
        wordLemtizer = WordNetLemmatizer()
        cmwords = stopwords.words('english')
        for f in filst:
            tk = []
            for line in nltk.sent_tokenize(codecs.open(f, 'r', 'latin-1').read()):
                for wd in nltk.word_tokenize(line):
                    # lemword = wd

                    if wd.isdigit():
                        tk.append("NUMBER")
                    elif "." + wd in mimetypes.types_map.keys():
                        tk.append("ATTACHMENT")
                    elif wd.upper() == wd:
                        tk.append("ALL_CAPS")
                        tk.append(wordLemtizer.lemmatize(wd.lower()).encode("utf-8"))
                    elif lk.match(wd):
                        tk.append("HTML_LINK")
                    else:
                        lemword = wordLemtizer.lemmatize(wd.lower())
                        if (lemword not in string.punctuation) and (lemword not in cmwords):
                            tk.append(lemword.encode("utf-8"))
            # if(n_gram==2):
            #     bigram_finder = BigramCollocationFinder.from_words(tk)
            #     bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 200)
            #     feat = dict([(ngram, True) for ngram in itertools.chain(tk, bigrams)])
            #     feature_tag.append((feat, tag))
            #
            # else:
            ngram_tk = nltk.ngrams(tk, n_gram, pad_right=True)
            feat = self.create_feat(ngram_tk);
            feature_tag.append((feat, tag))
        return feature_tag

    def create_feat(self,listOfTokens):
        feat = defaultdict(list)
        for w in listOfTokens:
            feat[w] = True
        return feat