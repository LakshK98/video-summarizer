import torch
import sys
# sys.path.append('models')
from tsum_1000 import Model
import numpy as np
import math


# print(sys.path)
model=Model()
# model.load_state_dict(torch.load('models/weights/model_1000_itr100_final.pt',map_location=torch.device('cpu')))
model.load_state_dict(torch.load('/Users/lakshkotian/Documents/VidSum/backend_logic/models/weights/model_1000_itr100_final.pt',map_location=torch.device('cpu')))

model.eval()



def get_summary(sentence_vectors,as_indices=True):


    total_len=len(sentence_vectors)
    batch_len=10
    sentence_batches = [sentence_vectors[i * batch_len:(i + 1) * batch_len] for i in range((len(sentence_vectors) + batch_len - 1) // batch_len)]



    if len(sentence_batches[-1]) < batch_len:
        for i in range(batch_len - len(sentence_batches[-1])):
            sentence_batches[-1].append(np.zeros((300,)))

    full_summary=[]
    for batch in sentence_batches:
        summary_vector=model(torch.from_numpy(np.array(batch)).reshape(1,3000).float())
        full_summary.append(summary_vector)


    full_summary = torch.stack(full_summary)

    full_summary = full_summary.reshape(1, -1).squeeze()

    full_summary = full_summary.detach().numpy()


    # 1
    # full_summary = np.where(full_summary > 0.5, 1, 0)

    full_summary=full_summary[:total_len]
    print("shape", full_summary.shape)

    if not as_indices:
        return full_summary

    summary_indices=full_summary.argsort()[-(math.ceil(len(sentence_vectors)*0.25)):][::-1]


    # 2
    # for i, sentence in enumerate(story_list):
    #     if full_summary[i]==1:
    #         ann_summary.append(sentence)

    # if as_indices:
    return summary_indices

    # ann_summary = []
    #
    # for i, sentence in enumerate(story_list):
    #     if i in summary_indices:
    #         ann_summary.append(sentence)
    #
    # ann_summary = '.'.join(ann_summary)
    #
    #
    # return ann_summary




