# CLass for extracting the data
import os
class DSRxtract(object):

    def __init__(self, path):
        print "[DsExtract] Extracting Dataset Files...."
        self.path = path
        self.spam_files = []
        self.ham_files = []
        self.create_files(self.path)
        print "[DsExtract]  Extraction process done..."

    def create_files(self,path):
        print "[DsExtract] Extracting Spam Dataset Files...."
        self.create_spam_files(path);
        print "[DsExtract] Extracting Ham Dataset Files...."
        self.create_ham_files(path);

    def create_spam_files(self,path):
        for dirs, subdrs, fls in os.walk(path):

            if (os.path.split(dirs)[1] == 'spam'):
                for fl_name in fls:
                    self.spam_files.append(os.path.join(dirs, fl_name))

    def create_ham_files(self,path):
        for dirs, subdrs, fls in os.walk(path):

            if (os.path.split(dirs)[1] == 'ham'):
                for fl_name in fls:
                    self.ham_files.append(os.path.join(dirs, fl_name))


    def getSpamFiles(self):
        return self.spam_files

    def getHamFiles(self):
        return self.ham_files