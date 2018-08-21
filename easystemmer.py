import itertools, re
from nltk.stem import StemmerI

class IndianNameStemmer(StemmerI):
    def stem(self, token):
        newtup=list()
        for i in token:
            i = i[:-3] if i.endswith('bai') else i
            for r in (("tha", "ta"), ("i", "e")):
                i = i.replace(*r)
                i = re.sub(r'(\w)\1+',r'\1', i)
            newtup.append(''.join(i for i, _ in itertools.groupby(i)))
        return tuple(newtup)
