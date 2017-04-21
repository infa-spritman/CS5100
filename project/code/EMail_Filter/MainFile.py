import nltk.classify
from data_extractor.DSExtract import DSRxtract
from feature_extractor.featExtract import featExtract
from classifier.NaiveBayesClassifier import NBM
from util.utils import util
from relief.relief import reliefAlgo
def main():

    print 'Main Program Starting...'
    rd ="dataset/enron-preprocessed/enron6"

    print '[MainFile] The root path is: ', rd
    print '[MainFile] Creating util object....'
    ut = util()
    print '\n'

    ds_extract = DSRxtract(rd)
    spam_files = ds_extract.getSpamFiles()
    print '\n'
    print "[MainFile] Size of Spam dataset: ", len(spam_files)
    ham_files= ds_extract.getHamFiles()
    print "[MainFile] Size of Ham dataset: ", len(ham_files)



    # 1 gram
    feature_object_one = featExtract(spam_files,ham_files,1,.7)
    print '[MainFile] Creating classifier for 1 gram...'
    c1 = NBM()
    print '[MainFile] Training 1 gram classifier...'
    c1.train(feature_object_one.getTrainFeature())
    print '[MainFile] Testing accuracy for 1 gram classifier...'
    print('Test accuracy: {0:.2f} %'.format
          (100 * nltk.classify.accuracy(c1.classifier, feature_object_one.getTestFeature())))
    truepositive_one = nltk.classify.accuracy(c1.classifier, feature_object_one.testSpamFeature)*\
                   len(feature_object_one.testSpamFeature)
    falsenegative_one = len(feature_object_one.testSpamFeature) - truepositive_one
    falsepositive_one = (1- nltk.classify.accuracy(c1.classifier, feature_object_one.testHamFeature))*\
                    len(feature_object_one.testHamFeature)
    print('Spam Precision: {0:.2f} %'.format
          (100 * ut.precision(truepositive_one,falsepositive_one) ))
    print('Spam Recall: {0:.2f} %'.format
          (100 * ut.recall(truepositive_one,falsenegative_one)))
    print('F-Score: {0:.2f} %'.format
          (100 * ut.f_score(ut.precision(truepositive_one,falsepositive_one) ,
                            ut.recall(truepositive_one,falsenegative_one))))


    # 2 gram
    feature_object_two = featExtract(spam_files, ham_files, 2, .7)
    print '[MainFile] Creating classifier for 2 gram...'
    c2 = NBM()
    print '[MainFile] Training 2 gram classifier...'
    c2.train(feature_object_two.getTrainFeature())
    print '[MainFile] Testing accuracy for 2 gram classifier...'
    print('Test accuracy: {0:.2f} %'.format
          (100 * nltk.classify.accuracy(c2.classifier, feature_object_two.getTestFeature())))
    truepositive_two = nltk.classify.accuracy(c2.classifier, feature_object_two.testSpamFeature) * \
                       len(feature_object_two.testSpamFeature)
    falsenegative_two = len(feature_object_two.testSpamFeature) - truepositive_two
    falsepositive_two = (1 - nltk.classify.accuracy(c2.classifier, feature_object_two.testHamFeature)) * \
                        len(feature_object_two.testHamFeature)
    print('Spam Precision: {0:.2f} %'.format
          (100 * ut.precision(truepositive_two, falsepositive_two)))
    print('Spam Recall: {0:.2f} %'.format
          (100 * ut.recall(truepositive_two, falsenegative_two)))
    print('F-Score: {0:.2f} %'.format
          (100 * ut.f_score(ut.precision(truepositive_two, falsepositive_two),
                            ut.recall(truepositive_two, falsenegative_two))))


    # 3 gram
    feature_object_three = featExtract(spam_files, ham_files, 3, .7)
    print '[MainFile] Creating classifier for 3 gram...'
    c3 = NBM()
    print '[MainFile] Training 3 gram classifier...'
    c3.train(feature_object_three.getTrainFeature())
    print '[MainFile] Testing accuracy for 3 gram classifier...'
    print('Test accuracy: {0:.2f} %'.format
          (100 * nltk.classify.accuracy(c3.classifier, feature_object_three.getTestFeature())))
    truepositive_three = nltk.classify.accuracy(c3.classifier, feature_object_three.testSpamFeature) * \
                       len(feature_object_three.testSpamFeature)
    falsenegative_three = len(feature_object_three.testSpamFeature) - truepositive_three
    falsepositive_three = (1 - nltk.classify.accuracy(c3.classifier, feature_object_three.testHamFeature)) * \
                        len(feature_object_three.testHamFeature)
    print('Spam Precision: {0:.2f} %'.format
          (100 * ut.precision(truepositive_three, falsepositive_three)))
    print('Spam Recall: {0:.2f} %'.format
          (100 * ut.recall(truepositive_three, falsenegative_three)))
    print('F-Score: {0:.2f} %'.format
          (100 * ut.f_score(ut.precision(truepositive_three, falsepositive_three),
                            ut.recall(truepositive_three, falsenegative_three))))


    # # Prob Distribution
    print '\n[MainFile] Getting spam probabilty for spam files...'
    spam_prob_dist = ut.getProbDistribution(c1.classifier,c2.classifier,c3.classifier,feature_object_one.trainSpamFeature,
                                            feature_object_two.trainSpamFeature,
                                            feature_object_three.trainSpamFeature,'spam')

    print '[MainFile] Getting spam probabilty for ham files...'
    ham_prob_dist = ut.getProbDistribution(c1.classifier, c2.classifier, c3.classifier,
                                           feature_object_one.trainHamFeature, feature_object_two.trainHamFeature,
                                           feature_object_three.trainHamFeature,'spam')

    #Relief Algorithm
    print '[MainFile] Creating object for Relief algo using above probablities...'
    a = reliefAlgo(spam_prob_dist,ham_prob_dist,len(spam_prob_dist) + len(ham_prob_dist))

    print '[MainFile] Learning weights...'
    factor = a.relief()

    print 'Learned weights are: ', factor
    print 'Calculating weighted accuracy...'

    #Testing
    weighted_spam_accuracy =ut.accuracy(c1.classifier,c2.classifier,c3.classifier,factor[0],factor[1],factor[2],feature_object_one.testSpamFeature,
                          feature_object_two.testSpamFeature,feature_object_three.testSpamFeature,'spam')

    weighted_ham_accuracy = ut.accuracy(c1.classifier,c2.classifier,c3.classifier,factor[0],factor[1],factor[2],feature_object_one.testHamFeature,
                          feature_object_two.testHamFeature,feature_object_three.testHamFeature,'ham')

    final_weighted_accuracy = (weighted_spam_accuracy+weighted_ham_accuracy)/2
    truepositive_weighted = weighted_spam_accuracy*len(feature_object_one.testSpamFeature)
    falsenegative_weighted = len(feature_object_one.testSpamFeature) - truepositive_weighted
    falsepositive_weighted = (1-weighted_ham_accuracy)*len(feature_object_one.testHamFeature)
    print('Test accuracy: {0:.2f} %'.format
          (100 * final_weighted_accuracy))
    print('Spam Precision: {0:.2f} %'.format
          (100 * ut.precision(truepositive_weighted, falsepositive_weighted)))
    print('Spam Recall: {0:.2f} %'.format
          (100 * ut.recall(truepositive_weighted, falsenegative_weighted)))
    print('F-Score: {0:.2f} %'.format
          (100 * ut.f_score(ut.precision(truepositive_weighted, falsepositive_weighted),
                            ut.recall(truepositive_weighted, falsenegative_weighted))))

    #
    # ###############################HAM################################################################333
    #
    # print '\n[MainFile] Getting ham probabilty for spam files...'
    # spam_prob_dist_1 = ut.getProbDistribution(c1.classifier, c2.classifier, c3.classifier,
    #                                         feature_object_one.trainSpamFeature, feature_object_two.trainSpamFeature,
    #                                         feature_object_three.trainSpamFeature, 'ham')
    #
    #
    # print '[MainFile] Getting ham probabilty for ham files...'
    # ham_prob_dist_1 = ut.getProbDistribution(c1.classifier, c2.classifier, c3.classifier,
    #                                        feature_object_one.trainHamFeature, feature_object_two.trainHamFeature,
    #                                        feature_object_three.trainHamFeature, 'ham')
    #
    # # Relief Algorithm
    # print '[MainFile] Creating object for Relief algo using above probablities...'
    # a_1 = reliefAlgo(spam_prob_dist_1, ham_prob_dist_1, len(spam_prob_dist_1) + len(ham_prob_dist_1))
    #
    # print '[MainFile] Learning weights...'
    # factor_1 = a_1.relief()
    #
    # print 'Learned weights are: ', factor_1
    #
    # print('Test Spam accuracy using ham probablity distribution for weights: {0:.2f} %'.format(
    #     100 * ut.accuracy(c1.classifier, c2.classifier, c3.classifier, factor_1[0], factor_1[1], factor_1[2],
    #                       feature_object_one.getTestSpamFeature(),
    #                       feature_object_two.getTestSpamFeature(), feature_object_three.getTestSpamFeature(), 'spam')))
    #
    # print('Test Ham accuracy using ham probablity distribution for weights: {0:.2f} %'.format(
    #     100 * ut.accuracy(c1.classifier,c2.classifier,c3.classifier,factor_1[0],factor_1[1],factor_1[2],
    #                       feature_object_one.getTestHamFeature(),
    #                       feature_object_two.getTestHamFeature(),feature_object_three.getTestHamFeature(),'ham')))

if __name__ == '__main__':
        main()