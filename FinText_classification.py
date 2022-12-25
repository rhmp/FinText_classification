# -*- coding: utf-8 -*-
"""git1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GyU--z7EbihsR9GolHGkg1wz-lAYmKnF
"""

#installing reqiured modules
!pip install finbert-embedding==0.1.4         #for sentence embedding
 
#importing required modules
import torch
import numpy
import pandas as pd
import nltk
from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as prf
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from statistics import mean, stdev
from sklearn.metrics import precision_recall_fscore_support
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from finbert_embedding.embedding import FinbertEmbedding
from matplotlib import pyplot as plt
import seaborn as sn




#Loading the data set - training data.
#you can load your own training data set if you have one.
train = pd.read_csv("/content/trainingdata.csv")
train_x = train['Message'].tolist()
train_y = train['Category'].tolist()

train_yi = []          #integer target list. unknown = 1 , event = 0
test_yi = []

for i in range(len(train_y)):
  if train_y[i] == 'unknown':
    train_yi.append(1)
  else:
    train_yi.append(0)


#finbert_encoder 
'''
word_embeddings = finbert.word_vector(text)
sentence_embedding = finbert.sentence_vector(text)
 '''
finbert = FinbertEmbedding()

X_train_fb = []           #finbert senetnce embedding list of train_x
np_zeros = numpy.zeros((768,))

for i in range(len(train_x)):
  try:
    emb = finbert.sentence_vector(train_x[i])   #emb is torch.tensor
    np_arr = emb.cpu().detach().numpy()
    X_train_fb.append(np_arr)
  except:
    X_train_fb.append(np_zeros)


#Converting finbert embedding list into matrix
'''
X_train_fb = [{-768},{},{}........x21]

we want, matrix of shape (21,768)
'''
X_train_fb_mat = numpy.matrix([list(i) for i in X_train_fb])



# Multinomial classification doesn't work with finbert embedding, because the embedding matrix has negative values.
#So creating TF-IDF matrix for the purpose of Multinomial classification
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_fb)
X_train_tfidf.shape

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_test_tfidf = tfidf_transformer.fit_transform(X_test_fb)
X_test_tfidf.shape


#Training Classification models

# Training Naive Bayes (NB) classifier on training data.
clf_nb = MultinomialNB(alpha=0.1).fit(X_train_tfidf, train_yi)
print("NB model score",clf_nb.score(X_test_fb, test_yi))

# Training LogisticRegression classifier on training data.
clf_lr = LogisticRegression(multi_class='ovr', max_iter= 1000)
print("LR model score",clf_lr.score(X_test_fb, test_yi))

#Model testing 

#Read data as dataframe
nltk.download('punkt')
df1 = pd.read_csv('/content/k-jan_sum-head-100.csv') 
print(len(df1))         
#df = df1.iloc[3000:4169]

news_para = df1.summary.values    #Taking news content(paragraph) from df to a list

#sentence tokenisation
sentences1 = []
for para in news_para:
  news_sent = nltk.sent_tokenize(str(para))
  sentences1.append(news_sent)                    # sentences1 will be a list of lists, need to flatten the list

#flattening the sentences1 list
sentences = []                      #flatten the list of sentences
for sublist in sentences1:
    for item in sublist:
        sentences.append(item)



# Read data stored as sentence 
import pandas as pd
df = pd.read_csv('/content/kalash_1169newscsv.csv')         #25696 sentences
df.sample(5)
sentences1 = df['news_sent'].tolist()
len(sentences1)


# model prediction
prediction_labels_sent = clf_lr.predict(sentences_fb) 
print("model predicted labels on test data",prediction_labels_sent)


#predictions to csv file

k = 0
for i in prediction_labels_sent:
  if i == 0:
    k+=1

print('No of events =', k)

events_from_news = []
unknown_from_news = []
for i in range(len(prediction_labels_sent)):
  if prediction_labels_sent[i] == 0:
    events_from_news.append(sentences[i])
  else:
    unknown_from_news.append(sentences[i])

print(len(events_from_news))
print(len(unknown_from_news))

dict = {'Predicted Events': events_from_news }
dfs = pd.DataFrame(dict) 
dfs.to_csv('predicted_events.csv')

dict= {'Predicted unknown': unknown_from_news }
dfs2 = pd.DataFrame(dict)
dfs2.to_csv('predicted_unknowns.csv')


#confusion matrix
predicted = model_1995.predict(sentences_fb)
test_yia = numpy.array(test_yi)
cm = confusion_matrix(test_yia, predicted)
#cm = [[14,0],[8,89]]
metrics = prf(test_yia, predicted)
print(cm)
print(metrics)
plt.figure(figsize= (10,7))
cat = ['Event','Unknown']
sn.heatmap(cm, annot= True,fmt = 'd', xticklabels = cat, yticklabels = cat,annot_kws={"size":30} )
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('FinBERT_emb, logReg')


#Stratified k fold CV


train_yia = numpy.array(train_yi)
X_train_fba = numpy.array(X_train_fb)

# Create StratifiedKFold object.
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=1)
lst_accu_stratified = []    #accuracy list
lst_metrics = []            #precision, recall, f1 score and support as array, list of arrays.
  
for train_index, test_index in skf.split(X_train_fb, train_yi):
    x_train_fold, x_test_fold = X_train_fba[train_index], X_train_fba[test_index]
    y_train_fold, y_test_fold = train_yia[train_index], train_yia[test_index]
    model_l.fit(x_train_fold, y_train_fold)
    lst_accu_stratified.append(model_l.score(x_test_fold, y_test_fold))
    pr = model_l.predict(x_test_fold)
    lst_metrics.append(precision_recall_fscore_support(y_test_fold, pr, average='macro'))

# Print the output.
print('List of possible accuracy:', lst_accu_stratified)
print('\nMaximum Accuracy That can be obtained from this model is:',
      max(lst_accu_stratified)*100, '%')
print('\nMinimum Accuracy:',
      min(lst_accu_stratified)*100, '%')
print('\nOverall Accuracy:',
      mean(lst_accu_stratified)*100, '%')
print('\nStandard Deviation is:', stdev(lst_accu_stratified))


##Model performance metrics
#precision, recall, f1, =>  ((p,r,f),  (), ...)


precision =[]
recall = []
f1 = [] 
fold = []

for i in range(10):
  fold.append(i)
  precision.append(lst_metrics[i][0])
  recall.append(lst_metrics[i][1])
  f1.append(lst_metrics[i][2])

dict = {'Fold': fold, 'Precision': precision, 'recall': recall, 'F1 score': f1, 'accuracy': lst_accu_stratified }

df = pd.DataFrame(dict)

df.to_csv('10cv-metrics.csv')

##Additonal models

#SGD
clf_svm = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, max_iter=5, random_state=42).fit(X_train_fb_mat, train_yi)
predicted_svm = clf_svm.predict(X_test_fb_mat)
print(numpy.mean("SGD model score",predicted_svm == test_yia))


#SVM
# Training Support Vector Machines - SVM and calculating its performance
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
text_clf_svm = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
                         ('clf-svm', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, max_iter=5, random_state=42))])

text_clf_svm = text_clf_svm.fit(X_train_fb_mat, train_yi)
predicted_svm = text_clf_svm.predict(X_test_fb_mat)
print("SVM model score",numpy.mean(predicted_svm == test_yi)

# Grid Search
# Here, we are creating a list of parameters for which we would like to do performance tuning. 
# All the parameters name start with the classifier name (remember the arbitrary name we gave). 
# E.g. vect__ngram_range; here we are telling to use unigram and bigrams and choose the one which is optimal.

from sklearn.model_selection import GridSearchCV
parameters = {'vect__ngram_range': [(1, 1), (1, 2)], 'tfidf__use_idf': (True, False), 'clf__alpha': (1,1e-1,1e-2, 1e-3)}

# To see the best mean score and the params, run the following code
#gs_clf.best_score_
#gs_clf.best_params_



# Similarly doing grid search for SVM
from sklearn.model_selection import GridSearchCV
parameters_svm = {'vect__ngram_range': [(1, 1), (1, 2)], 'tfidf__use_idf': (True, False),'clf-svm__alpha': (1,0.1,1e-2, 1e-3)}

gs_clf_svm = GridSearchCV(text_clf_svm, parameters_svm, n_jobs=-1)
gs_clf_svm = gs_clf_svm.fit(train_x, train_yi)


# To see the best mean score and the params, run the following code
# gs_clf_svm.best_score_
# gs_clf_svm.best_params_


# NLTK
# Removing stop words
from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer(stop_words='english')), ('tfidf', TfidfTransformer()), 
                     ('clf', MultinomialNB())])


# Stemming Code

import nltk
nltk.download()

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english", ignore_stopwords=True)

class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])
    
stemmed_count_vect = StemmedCountVectorizer(stop_words='english')

text_mnb_stemmed = Pipeline([('vect', stemmed_count_vect), ('tfidf', TfidfTransformer()), 
                             ('mnb', MultinomialNB(fit_prior=False))])

text_mnb_stemmed = text_mnb_stemmed.fit(twenty_train.data, twenty_train.target)

predicted_mnb_stemmed = text_mnb_stemmed.predict(twenty_test.data)

np.mean(predicted_mnb_stemmed == twenty_test.target)


#classification metrics

import numpy as np
from sklearn.metrics import precision_recall_fscore_support

rbf_met = precision_recall_fscore_support(test_yia, ml_predictions_s_rbf, average= None)

# print((rbf_met[0]))
# print((rbf_met[1]))
# print((rbf_met[2]))
# print((rbf_met[3]))

cat = []
pr = []
re = []
f = []


for i in range(10):
  pr.append(rbf_met[0][i])
  re.append(rbf_met[1][i])
  f.append(rbf_met[2][i])

cat.append(rbf_met[3])
print(len(pr))
print(len(re))
print(len(f))
print(len(cat[0]))

dict = {'precison': pr, 'recall':re, 'f1': f}
dfm = pd.DataFrame(dict)
dfm.to_csv('multi-rbfsvm-metrics.csv')

dfm
