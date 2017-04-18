import nltk.classify
from data_extractor.DSExtract import DSRxtract
from feature_extractor.featExtract import featExtract
from classifier.NaiveBayesClassifier import NBM
from util.utils import util


def main():

    rd ="dataset/enron-preprocessed/test"


    ds_extract = DSRxtract(rd)
    spam_files = ds_extract.getSpamFiles()
    ham_files= ds_extract.getHamFiles()

    # 1 gram
    feature_object_one = featExtract(spam_files,ham_files,1,.7)
    c1 = NBM()
    c1.train(feature_object_one.getTrainFeature())
    print('Test Spam accuracy: {0:.2f} %'.format(100 * nltk.classify.accuracy(c1.classifier, feature_object_one.getTestSpamFeature())))
    print('Test Ham accuracy: {0:.2f} %'.format(100 * nltk.classify.accuracy(c1.classifier, feature_object_one.getTestHamFeature())))

    # 2 gram
    feature_object_two = featExtract(spam_files, ham_files, 2, .7)
    c2 = NBM()
    c2.train(feature_object_two.getTrainFeature())
    print('Test Spam accuracy: {0:.2f} %'.format(
        100 * nltk.classify.accuracy(c2.classifier, feature_object_two.getTestSpamFeature())))
    print('Test Ham accuracy: {0:.2f} %'.format(
        100 * nltk.classify.accuracy(c2.classifier, feature_object_two.getTestHamFeature())))

    # 3 gram
    feature_object_three = featExtract(spam_files, ham_files, 3, .7)
    c3 = NBM()
    c3.train(feature_object_three.getTrainFeature())
    print('Test Spam accuracy: {0:.2f} %'.format(
        100 * nltk.classify.accuracy(c3.classifier, feature_object_three.getTestSpamFeature())))
    print('Test Ham accuracy: {0:.2f} %'.format(
        100 * nltk.classify.accuracy(c3.classifier, feature_object_three.getTestHamFeature())))

    # Prob Distribution
    ut = util()
    spam_prob_dist = ut.getProbDistribution(c1,c2,c3,feature_object_one.trainSpamFeature,feature_object_two.trainSpamFeature,
                                            feature_object_three.trainSpamFeature)
    print spam_prob_dist
    ham_prob_dist = ut.getProbDistribution(c1,c2,c3,feature_object_one.trainHamFeature,feature_object_two.trainHamFeature,
                                           feature_object_three.trainHamFeature)
    print ham_prob_dist


if __name__ == '__main__':
        main()