class util(object):


    def getProbDistribution(self,c1,c2,c3,feature_one_gram,feature_two_gram,feature_three_gram,tag):
        prob_dist = []

        for i in range(len(feature_one_gram)):
            prob_one_gram = c1.prob_classify(feature_one_gram[i][0]). \
                prob(tag)
            prob_two_gram = c2.prob_classify(feature_two_gram[i][0]). \
                prob(tag)
            prob_three_gram = c3.prob_classify(feature_three_gram[i][0]). \
                prob(tag)
            prob_dist.append([prob_one_gram, prob_two_gram,prob_three_gram])

        return prob_dist


    def accuracy(self,c1,c2,c3,weight_onegram,weight_twogram,weight_threegram,testFeatureOnegram,testFeatureTwogram,testFeatureThreegram
        ,tag):
        actual_count =0
        total_count  = len(testFeatureOnegram)
        for i in range(total_count):
            tempDict  = {}
            tempDict['spam'] = self.weightedSpamProbability(c1,c2,c3,weight_onegram,weight_twogram,weight_threegram,testFeatureOnegram[i][0],
                                                            testFeatureTwogram[i][0],testFeatureThreegram[i][0])
            tempDict['ham'] = self.weightedHamProbability(c1,c2,c3,weight_onegram,weight_twogram,weight_threegram,testFeatureOnegram[i][0],
                                                            testFeatureTwogram[i][0],testFeatureThreegram[i][0])
            if tag==max(tempDict, key=tempDict.get):
                actual_count +=1

        return float(actual_count)/total_count

    def weightedSpamProbability(self,c1,c2,c3,weight_onegram,weight_twogram,weight_threegram,feature1,feature2,feature3):

        prob_one_gram = weight_onegram*(c1.prob_classify(feature1).prob('spam'))
        prob_two_gram = weight_twogram*(c2.prob_classify(feature2).prob('spam'))
        prob_three_gram = weight_threegram*(c3.prob_classify(feature3).prob('spam'))
        return prob_one_gram+prob_two_gram+prob_three_gram

    def weightedHamProbability(self, c1, c2, c3, weight_onegram, weight_twogram, weight_threegram, feature1,feature2,feature3):

        prob_one_gram = weight_onegram * (c1.prob_classify(feature1).prob('ham'))
        prob_two_gram = weight_twogram * (c2.prob_classify(feature2).prob('ham'))
        prob_three_gram = weight_threegram * (c3.prob_classify(feature3).prob('ham'))
        return prob_one_gram + prob_two_gram + prob_three_gram


    def maxLabel(self,dict):
        max((p, v) for (v, p) in dict)[1]


    def precision(self,truePostive,falsePositive):
        return float(truePostive)/(truePostive+falsePositive)

    def recall(self,truePositive,falseNegative):
        return float(truePositive)/(truePositive+falseNegative)

    def f_score(self,p,r):
        return float(2*p*r)/(p+r)
