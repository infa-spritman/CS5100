import random
class reliefAlgo(object):
    def __init__(self,spamlist,hamlist,count):
        self.spam = spamlist
        self.ham = hamlist
        self.count = count

    def relief(self):
        weights = []
        if len(self.spam) != len(self.ham):
            for index in range(len(self.spam[0])):
                weights.append(0)

            for turns in range(self.count):
                nearHit = None
                nearMiss = None
                Instance = None

                sOrH = random.randint(0,1)

                if sOrH==0:
                    indexInstance = random.randint(0,len(self.spam)-1)
                    Instance = self.spam[indexInstance]
                    nearHit = self.spam[self.searchHit(self.spam,indexInstance,Instance)]
                    nearMiss = self.ham[self.searchMiss(self.ham,indexInstance,Instance)]
                else:
                    indexInstance = random.randint(0, len(self.ham)-1)
                    Instance = self.ham[indexInstance]
                    nearHit = self.ham[self.searchHit(self.ham,indexInstance,Instance)]
                    nearMiss = self.spam[self.searchMiss(self.spam,indexInstance,Instance)]

                for ind in range(len(weights)):
                    weights[ind] = weights[ind] - ((Instance[ind] - nearHit[ind])**2)/self.count + ((Instance[ind] - nearMiss[ind])**2)/self.count

        return weights

    def searchHit(self,set,targetIndex,Target):
        nearestIndex = None
        bestDis = float("inf")
        for index in range(len(set)):
            if index == targetIndex:
                continue
            setIns = set[index]
            euclideanDis = self.euclideanDiff(setIns,Target)
            if euclideanDis < bestDis:
                nearestIndex = index
                bestDis = euclideanDis

        return nearestIndex

    def searchMiss(self,set,targetIndex,Target):
        nearestIndex = None
        bestDis = float("inf")
        for index in range(len(set)):
            setIns = set[index]
            euclideanDis = self.euclideanDiff(setIns,Target)
            if euclideanDis < bestDis:
                nearestIndex = index
                bestDis = euclideanDis

        return nearestIndex

    def euclideanDiff(self,I1,I2):
        ans = 0
        for fIndex in range(len(I1)):
            ans = ans + (I1[fIndex] - I2[fIndex])**2
        return ans**0.5
