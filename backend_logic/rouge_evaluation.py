
import pickle
import numpy as np
import ann_summarize
import textrank_summarize
import cnn_preprocess
from rouge import *
import matplotlib.pyplot as plt



rouge_eval_in =open('../data/checkpoints/rouge_eval_set.pickle','rb')
rouge_eval_set=pickle.load(rouge_eval_in)


rouge=Rouge(metrics=["rouge-1","rouge-2"])


# word_embeddings = {}
# f = open('../data/glove/glove.6B.300d.txt', encoding='utf-8')
# for line in f:
#     values = line.split()
#     word = values[0]
#     coefs = np.asarray(values[1:], dtype='float32')
#     word_embeddings[word] = coefs
#
# f.close()

word_embeddings=cnn_preprocess.load_word_embeddings()



ann_rouge_scores = []
ann_rouge2_scores = []

tr_rouge_scores=[]
tr_rouge2_scores=[]



for story_highlight in rouge_eval_set:
    # sentence_vectors = []
    #
    # for sentence in story_highlight['story']:
    #     if len(sentence)>0:
    #         v = sum([word_embeddings.get(w, np.zeros((300,))) for w in sentence.split()]) / (len(sentence.split()) + 0.001)
    #     else:
    #         print("len sentence not greater than 0")
    #         v = np.zeros((300,))
    #     sentence_vectors.append(v)
    sentence_vectors=cnn_preprocess.get_sentence_vectors(word_embeddings,story_highlight['story'])

    ann_summary=cnn_preprocess.get_summary_from_indices(ann_summarize.get_summary(sentence_vectors),story_highlight['story'])

    tr_summary= textrank_summarize.get_summary(sentence_vectors,story_highlight['story'])

    if len(ann_summary)==0:
        continue

    print(ann_summary)
    actual_summary = '.'.join(story_highlight['highlights'])

    print(actual_summary)
    score=rouge.get_scores(ann_summary, actual_summary)[0]
    ann_score1=score['rouge-1']
    ann_score2=score['rouge-2']

    ann_rouge_scores.append([ann_score1[metric] for metric in ['r','p','f']])
    ann_rouge2_scores.append([ann_score2[metric] for metric in ['r','p','f']])

    score=rouge.get_scores(tr_summary, actual_summary)[0]
    tr_score1=score['rouge-1']
    tr_score2=score['rouge-2']

    tr_score1 = rouge.get_scores(tr_summary, actual_summary)[0]['rouge-1']
    tr_score2 = rouge.get_scores(tr_summary, actual_summary)[0]['rouge-2']

    tr_rouge_scores.append([tr_score1[metric] for metric in ['r', 'p', 'f']])
    tr_rouge2_scores.append([tr_score2[metric] for metric in ['r', 'p', 'f']])

    # ann_rouge_scores.append(rouge.get_scores(ann_summary, actual_summary)[0]['rouge-1']['r'])
    #
    # tr_rouge_scores.append(rouge.get_scores(tr_summary, actual_summary)[0]['rouge-1']['r'])

    print(ann_rouge_scores)

ann_rouge_scores= np.array(ann_rouge_scores)
ann_rouge2_scores= np.array(ann_rouge2_scores)

tr_rouge_scores= np.array(tr_rouge_scores)
tr_rouge2_scores=np.array(tr_rouge2_scores)


print("\t\t\t\tann\t\t\t\t\ttr ")
print("Rouge1 r:",np.mean(ann_rouge_scores[:,0]),"  ",np.mean(tr_rouge_scores[:,0]))
print("Rouge1 p:",np.mean(ann_rouge_scores[:,1]),"  ",np.mean(tr_rouge_scores[:,1]))
print("Rouge1 f:",np.mean(ann_rouge_scores[:,2]),"  ",np.mean(tr_rouge_scores[:,2]))
print()
print("Rouge2 r:",np.mean(ann_rouge2_scores[:,0]),"  ",np.mean(tr_rouge2_scores[:,0]))
print("Rouge2 p:",np.mean(ann_rouge2_scores[:,1]),"  ",np.mean(tr_rouge2_scores[:,1]))
print("Rouge2 f:",np.mean(ann_rouge2_scores[:,2]),"  ",np.mean(tr_rouge2_scores[:,2]))

print("ann avg precision: ",np.mean(np.array(ann_rouge_scores)))
plt.figure(1)

plt.plot(ann_rouge_scores)
plt.show()

print("Tr avg precision: ",np.mean(np.array(tr_rouge_scores)))

plt.figure(2)
plt.plot(tr_rouge_scores)
plt.show()

