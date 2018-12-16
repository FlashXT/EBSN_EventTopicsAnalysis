import os
import gensim.models as models
from gensim.test.utils import datapath
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary

##Train an LDA model using a Gensim corpus
# ① Create a corpus from a list of texts
print("common_texts:")
[print("\t",text) for text in common_texts]
common_dictionary = Dictionary(common_texts)
print(common_dictionary.token2id)
common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]
[print(item) for item in common_corpus]
# ② Train the model on the corpus.

lda = models.ldamodel.LdaModel(common_corpus, num_topics=3,id2word=common_dictionary)
print(lda.print_topics(num_topics=3,num_words=2))
# ③ Save a model to disk, or reload a pre-trained model
#Save model to disk.
temp_file = datapath(os.getcwd()+"\\..\\Data\\Model\\model")
lda.save(temp_file)
# Load a potentially pretrained model from disk.
lda = models.LdaModel.load(temp_file)

##Query, the model using new, unseen documents
# ④ Create a new corpus, made of previously unseen documents.
other_texts = [
                ['computer', 'time', 'graph'],
                ['survey', 'response', 'eps'],
                ['human', 'system', 'computer']
            ]
other_corpus = [common_dictionary.doc2bow(other_text) for other_text in other_texts]
unseen_doc = other_corpus[0]
vector = lda[unseen_doc] # get topic probability distribution for a document
## Update the model by incrementally training on the new corpus
lda.update(other_corpus)
vector = lda[unseen_doc]
## A lot of parameters can be tuned to optimize training for your specific case
print(lda.print_topics(num_topics=3,num_words=2))
# lda = models.LdaModel(common_corpus, num_topics=3, alpha='auto', eval_every=5)  # learn asymmetric alpha from data
# ⑤

# ⑥⑦⑧