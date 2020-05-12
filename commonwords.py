import nltk
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer
from nltk.probability import FreqDist

from nltk.corpus import stopwords, state_union
from nltk.stem import PorterStemmer


sample_text = state_union.raw("2006-GWBush.txt")
tokenizer = nltk.RegexpTokenizer(r"\w+")
nopunc = tokenizer.tokenize(sample_text)
# print(nopunc)
# fdist = FreqDist()
# for word in word_tokenize(sentance):
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

# words = word_tokenize(nopunc)
# print(words)
stemwords = []
for w in nopunc:
	stemwords.append(ps.stem(w))

# print(stemwords)
stemwords = [stemword for stemword in stemwords if stemword not in stop_words]
# print(stemwords)
fdist = FreqDist(stemwords)

# for word, frequency in fdist.most_common(5):
	# print(u'{};{}'.format(word, frequency))
