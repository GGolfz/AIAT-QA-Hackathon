from numpy.lib.shape_base import split
import pandas as pd
import json
import numpy as np
def findAnswerStartFromContext(context,answer):
    try:
        answer_start = context.index(answer)
    except:
        answer_start = -1
    return answer_start
def modifySCGDataFrameToQAformat(df):
    data = dict()
    qa_format = []
    for i in df.itertuples():
        filename = i[1].split('/')[1]
        question = i[2]
        answer = i[3]
        if filename not in data:
            data[filename] = [filename,[]]
        data[filename][1].append((question, answer))
    for i in data:
        filename = data[i][0]
        f = open('datasets/scg/data/SCG'+filename,'r')
        context = f.read()
        f.close()
        context = context.replace('\n',' ')
        context = context.replace('\t',' ')
        context = context
        qas = []
        for j in data[i][1]:
            question = j[0]
            answer = j[1]
            answer_start = findAnswerStartFromContext(context,answer)
            qas.append({"id":len(qas)+1,"is_impossible":answer_start < 0, "question":question,"answers":[{"text":answer,"answer_start":answer_start}]})
        qa_format.append({"context":context,"qas":qas})
    return qa_format
def writeDataFrameToQAJSONFile(df,filename):
    scg_qa_format = modifySCGDataFrameToQAformat(df)
    f = open('mod-datasets/scg/'+filename,'w')
    jsonString = json.dumps(scg_qa_format, ensure_ascii=False).encode('utf8')
    f.write(jsonString.decode())
    f.close()
def main():
    scgdf = pd.read_csv('datasets/scg/SCG-Train.csv')
    split_list = np.random.rand(scgdf.shape[0])
    scgdf.loc[split_list <= 0.8,'set'] = 'train'
    scgdf.loc[split_list > 0.8, 'set'] = 'eval'
    train_df = scgdf[scgdf['set'] == 'train']
    eval_df = scgdf[scgdf['set'] == 'eval']
    writeDataFrameToQAJSONFile(train_df,'train.json')
    writeDataFrameToQAJSONFile(eval_df,'eval.json')

if __name__ == '__main__':
    main()