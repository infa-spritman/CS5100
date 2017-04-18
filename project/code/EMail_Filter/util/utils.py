class util(object):


    def getProbDistribution(self,c1,c2,c3,feature_one_gram,feature_two_gram,feature_three_gram):
        prob_dist = []
        for i in range(len(feature_one_gram)):
            prob_one_gram = c1.getClassifier().prob_classify(feature_one_gram[i][0]). \
                prob('spam')
            prob_two_gram = c2.getClassifier().prob_classify(feature_two_gram[i][0]). \
                prob('spam')
            prob_three_gram = c3.getClassifier().prob_classify(feature_three_gram[i][0]). \
                prob('spam')
            prob_dist.append([prob_one_gram, prob_two_gram,prob_three_gram])

        return prob_dist
