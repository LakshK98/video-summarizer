import decimal
import numpy as np

def create_knapsack_matrix(scores,lens,budget):

    matrix = [[0 for y in range((budget + 1))]
              for x in range((len(scores) + 1))]
    for i in range(1, len(scores) + 1):
        for j in range(1, budget + 1):
            #         print(i,j)
            matrix[i][j] = max(matrix[i - 1][j], matrix[i - 1][j - (lens[i - 1])] + scores[i - 1]) if j >= lens[i - 1] else matrix[i - 1][j ]


    return matrix

def knapsack_indices(scores,lens,budget,matrix):
    # print(lens)
    res = decimal.Decimal(matrix[len(scores)][budget])

    w = budget
    selected_indices = []
    for i in range(len(scores), 0, -1):
        if res <= 0:
            break
        # for matrixx in matrix:
        #     print(matrixx)
        # either the result comes from the
        # top (K[i-1][w]) or from (val[i-1]
        # + K[i-1] [w-wt[i-1]]) as in Knapsack
        # table. If it comes from the latter
        # one/ it means the item is included.
        # print("weights",w)
        # print(len(matrix),len(matrix[0]))
        # print(i,w)

        if res == matrix[i - 1][w]:
            continue
        else:

            # This item is included.
            # print(lens[i - 1])
            selected_indices.append(i - 1)

            # Since this weight is included
            # its value is deducted
            res = res - scores[i - 1]
            w = w - (lens[i - 1])
    return selected_indices



def drop_and_forward_algo(total_seconds,compression_ratio,shots):

    budget =int(total_seconds*compression_ratio)

    max_score=-1
    selected_shots=[]
    selected_spoken_speed=1
    selected_silent_speed=1

    # ps spoken 1,1.05,1.1....1.5
    # ps silent 1,1.5,2....6

    for ps_spoken in [round(x*0.05,2) for x in range(20,31)]:
        for ps_silent in [y*0.5 for y in range(2,13)]:
            # print(ps_spoken,ps_silent)
            shot_lens=[]
            shot_scores=[]
            for shot in shots:
                shot_len=shot['spoken_len']/ps_spoken + shot['silent_len']/ps_silent
                shot_lens.append(int(shot_len))
                shot_scores.append(shot['spoken_score']*(-1*(ps_spoken-1)+1)+ shot['silent_score']*(-0.1*(ps_silent-1)+1))
            shot_scores=[decimal.Decimal(score).quantize(decimal.Decimal('0.00000')) for score in shot_scores]
            knapsack_matrix=create_knapsack_matrix(shot_scores,shot_lens,budget)
            if knapsack_matrix[len(shot_scores)][budget]>max_score:
                # print("max changing")
                # print("shot lens: ",shot_lens)
                # print("shot scores:",shot_scores)
                max_score=knapsack_matrix[len(shot_scores)][budget]
                # print("max_score:",max_score)

                selected_shots=knapsack_indices(shot_scores,shot_lens,budget,knapsack_matrix)
                selected_spoken_speed=ps_spoken
                selected_silent_speed=ps_silent


    compressed_len=0
    for shot in shots:
        compressed_len=shot['spoken_len']/selected_spoken_speed+shot['silent_len']/selected_silent_speed
    print(total_seconds,compressed_len)
    # print("spoken:",selected_spoken_speed)
    # print("silent:",selected_silent_speed)
    # print(selected_shots)

    return  selected_shots,selected_spoken_speed,selected_silent_speed