import re,os,string
from collections import defaultdict
from nltk import NaiveBayesClassifier
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk.classify
import codecs,random,mimetypes
from collections import Counter

def feature_extract(filst,tag,n_gram=1):
    lk = re.compile(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    feature_tag =[]
    wordLemtizer = WordNetLemmatizer()
    cmwords = stopwords.words('english')
    for f in filst:
        tk = []
        for line in nltk.sent_tokenize(codecs.open(f, 'r', 'latin-1').read()):
            for wd in nltk.word_tokenize(line):
                #lemword = wd

                if wd.isdigit():
                    tk.append("NUMBER")
                elif "." + wd in mimetypes.types_map.keys():
                    tk.append("ATTACHMENT")
                elif wd.upper()==wd:
                    tk.append("ALL_CAPS")
                    tk.append(wordLemtizer.lemmatize(wd.lower()).encode("utf-8"))
                elif lk.match(wd):
                    tk.append("HTML_LINK")
                else:
                    lemword = wordLemtizer.lemmatize(wd.lower())
                    if (lemword not in string.punctuation) and (lemword not in cmwords):
                        tk.append(lemword.encode("utf-8"))

        ngram_tk = nltk.ngrams(tk,n_gram,pad_right=True)
        feat = create_feat(ngram_tk);
        feature_tag.append((feat,tag))
    return feature_tag

def create_feat(listOfTokens):
    feat = defaultdict(list)
    for w in listOfTokens:
        feat[w] = True
    return feat

def getNBMClassifier(train_spam_files,test_spam_files,train_ham_files,test_ham_files,n_gram):

    train_spam_feature = feature_extract(train_spam_files, 'spam', n_gram)
    train_ham_feature = feature_extract(train_ham_files, 'ham', n_gram)
    combineset = train_spam_feature + train_ham_feature
    random.shuffle(combineset)

    test_spam_feature = feature_extract(test_spam_files, 'spam', n_gram)
    test_ham_feature = feature_extract(test_ham_files, 'ham', n_gram)
    return nbm_classifier(combineset, test_spam_feature, test_ham_feature)


def nbm_classifier(train_set, test_spam, test_ham):

    classifier = NaiveBayesClassifier.train(train_set)
    # print('Test Spam accuracy: {0:.2f} %'.format(100 * nltk.classify.accuracy(classifier, test_spam)))
    # print('Test Ham accuracy: {0:.2f} %'.format(100 * nltk.classify.accuracy(classifier, test_ham)))
    # #print classifier.most_informative_features(20)
    return classifier

def getProbDist(c1,c2,files,tag):
    prob_dist =[]
    train_spam_feature_one_gram = feature_extract(files,tag, 1)
    train_spam_feature_two_gram = feature_extract(files,tag, 2)
    for i in range(len(files)):
        prob_one_gram = c1.prob_classify(train_spam_feature_one_gram[i][0]).\
                        prob('spam')
        prob_two_gram = c2.prob_classify(train_spam_feature_two_gram[i][0]). \
                        prob('spam')
        prob_dist.append([prob_one_gram, prob_two_gram ])


    return prob_dist

def main():

    rd ="C:\\Users\\Bazingaaaa\\Desktop\\emailDataSet\\enron-preprocessed\\test"
    spam_files = []
    ham_files= []
    for dirs, subdrs, fls in os.walk(rd):

        if (os.path.split(dirs)[1] == 'spam'):
            for fl_name in fls:
                spam_files.append(os.path.join(dirs, fl_name))

        if (os.path.split(dirs)[1] == 'ham'):
            for fl_name in fls:
                ham_files.append(os.path.join(dirs, fl_name))

    no_of_spam_files = len(spam_files)
    no_of_ham_files = len(ham_files)
    print no_of_spam_files
    print no_of_ham_files

    train_spam_files = spam_files[int(no_of_spam_files*.7):]
    test_spam_files = spam_files[:int(no_of_spam_files*.7)]

    train_ham_files = ham_files[int(no_of_ham_files*.7):]
    test_ham_files = ham_files[:int(no_of_ham_files*.7)]

    # print len(train_spam_files)
    # print len(test_spam_files)
    # print len(train_ham_files)
    # print len(test_ham_files)

    nbm_one_gram = getNBMClassifier(train_spam_files,test_spam_files,train_ham_files,test_ham_files,1)
    nbm_two_gram = getNBMClassifier(train_spam_files,test_spam_files,train_ham_files,test_ham_files,2)

    spam_prob_dist = getProbDist(nbm_one_gram,nbm_two_gram,train_spam_files,'spam')
    print spam_prob_dist
    ham_prob_dist = getProbDist(nbm_one_gram,nbm_two_gram,train_ham_files,'ham')
    print ham_prob_dist








    #nbm_three_gram = getNBMClassifier(train_spam_files,test_spam_files,train_ham_files,test_ham_files,3)

    # msg1 = "Hello there sex master, I need cock right now. Ping me. Contact me."
    # msg2 = "Subject: meter 7266 daren - can you set up a deal for meter 7266 ? an accounting arrangement is " \
    #        "always created every month . it is used for the texas general land storage" \
    #        "deal , ( withholding 15 % on their injections only ) . it has been nominated in" \
    #        "pops on 012 - 41500 - 05 - 002 . please let me know , volume management wants to" \
    #        "get bammel allocated today .thanks . aimee"




    # words = word_tokenize(msg1)
    # features = create_feat(words)
    # print 'first',nbm_one_gram.classify(features)
    # print 'second', nbm_one_gram.prob_classify(features).samples();
    # print 'thrid', nbm_one_gram.prob_classify(features).prob(nbm_one_gram.prob_classify(features).samples()[0])
    # print 'fourth', nbm_one_gram.prob_classify(features).prob(nbm_one_gram.prob_classify(features).samples()[1])
    #
    #
    # words2 = word_tokenize(msg2)
    # features2 = create_feat(words2)
    # print 'first', nbm_one_gram.classify(features2)
    # print 'second', nbm_one_gram.prob_classify(features2).samples()
    # print 'thrid', nbm_one_gram.prob_classify(features2).prob(nbm_one_gram.prob_classify(features2).samples()[0])
    # print 'fourth', nbm_one_gram.prob_classify(features2).prob(nbm_one_gram.prob_classify(features2).samples()[1])













    # # Creating list of probability distributions to extract probabilities from
    # probDist = []
    # for i in range(0, len(test_feats)):
    #     probdist = cl.prob_classify(test_feats[i][0])
    #     probDist.append(probdist)
    #
    # # Creating list of the max probabilities for prediction
    # prob = []
    # for i in range(0, len(probDist)):
    #     prob.append(probDist[i].prob(probDist[i].max()))


if __name__ == '__main__':
        main()