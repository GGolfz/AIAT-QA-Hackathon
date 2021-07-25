import json
with open('test/test.json', 'r') as file:
    test = json.load(file)
yn =[]
for i in test:
    for j in range(len(i['qas'])):
        question_id = i['qas'][j]['question_id']
        if int(question_id) >= 5001 and int(question_id) <= 5500:
            yn.append([i['qas'][j]['question_id'],i['context'],i['qas'][j]['question']])
print(len(yn))

import pandas as pd

df = pd.DataFrame(yn,columns=['question_id','context','question'])

df.to_csv('yesorno.csv',index=False)