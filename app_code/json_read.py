#https://www.geeksforgeeks.org/modify-json-fields-using-python/
#https://www.geeksforgeeks.org/read-json-file-using-python/

import json,os

def read_file():
    dir_json = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(dir_json, 'r') as file:
        data = json.load(file)

    return data

def change_scores(score,imgs):
    keys = ["A","B","C"]

    dir_json = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(dir_json, 'r') as json_file:
        data = json.load(json_file)

    pos,lst = high_score(score[3:],data,"A")
    score = score[:3]
    score.insert(2,imgs[0])
    score.insert(4,imgs[1])
    for e in lst:
        score.append(e)

    if pos == None:
        return
    
    print(score)
    data[pos] = score
    
    dir_json = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(dir_json, 'w') as file:
        json.dump(data,file,indent=2)


def high_score(score,data,pos):
    #If the anoted goals are more than the last place
    print(int(data[pos][6]),score[1])
    if int(data[pos][6]) < score[1]:
        print("Actual team best")
        return pos,score
    
    #If the goals are equal
    elif int(data[pos][6]) == score[1]:
        print("Hmmm equals")
        if int(data[pos][5]) > score[0]:
            print("Actual team less fails")
            return pos,score
        #If the fails are equal
        elif int(data[pos][5]) == score[0]:
            print("HMMM Equals X2")
            if pos == "C": return None, score
            if pos == "B": pos = "C"            
            if pos == "A": pos = "B"
            print("Vamos por acá")
            return high_score(score,data,pos)
        else:
            return None,score

    #If the goals are less than the last place
    else:
        print("Actual Team Looser")
        if pos == "C": return None,score
        if pos == "B": pos = "C"            
        if pos == "A": pos = "B"
        return high_score(score,data,pos)
        


