import itertools, re
from nltk.stem import StemmerI

class IndianNameStemmer(StemmerI):
    def stem(self, token):
        newtup=list()
        for i in token:
            i = i[:-1]+'v' if i.endswith('o') else i
            i = i[:-2] if i.endswith(['bi', 'ji']) else i            
            i = i[:-3] if i.endswith(['bai', 'ben', 'tai', 'sab', 'rao', 'rav']) else i
            i = i[:-4] if i.endswith(['bhai', 'sing']) else i
            i = i[:-5] if i.endswith(['saheb', 'singh' , 'shing']) else i
            
            for r in (("tha", "ta"), ("i", "e"), ("gi", "ji"), ("bh", "b"), ("v", "w"), ("yu", "u"), ("gh", "g"), 
                      ("dh", "d"), ("sh", "s") ):
                i = i.replace(*r)
                i = re.sub(r'(\w)\1+',r'\1', i)
            newtup.append(''.join(i for i, _ in itertools.groupby(i)))
        return tuple(newtup)
