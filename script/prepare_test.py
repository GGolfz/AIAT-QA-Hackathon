from numpy.core.fromnumeric import reshape
import pandas as pd
import numpy as np
import json
from lxml import etree

parser = etree.XMLParser(recover=True)

def get_test_data_with_type(df):
    for i in df.itertuples():
        id = i[1]
        article_id = i[2]
        try:
            filename = str(int(article_id))
            type = 'wiki'
        except:
            filename = article_id[3:]
            type = 'scg'
        df.loc[df.index[df['id'] == id], 'type'] = type
        df.loc[df.index[df['id'] == id], 'filename'] = filename
    return df
    
def findAnswerStartFromContext(context,answer):
    try:
        answer_start = context.index(answer)
    except:
        answer_start = -1
    return answer_start
def extract_text(body):
    tree = etree.fromstring(body, parser=parser)
    try:
        text = tree.text
    except:
        text = -1
    return text
def modifyWikiDataFrameToQAformat(df):
    data = dict()
    qa_format = []
    for i in df.itertuples():
        id = str(int(i[1]))
        filename = str(int(i[6]))
        question = i[3]
        if filename not in data:
            data[filename] = [filename,[]]
        data[filename][1].append((id,question))
    for i in data:
        filename = data[i][0]
        f = open('datasets/wiki/wiki-documents-nsc/'+filename+'.txt','r')
        context = f.read()
        f.close()
        context = extract_text(context)
        if extract_text != -1:
            qas = []
            for j in data[i][1]:
                id = j[0]
                question = j[1]
                qas.append({"id":len(qas)+1,"question":question,"question_id":id})
            qa_format.append({"context":context,"qas":qas})
    return qa_format
def modifySCGDataFrameToQAformat(df):
    data = dict()
    qa_format = []
    for i in df.itertuples():
        id = str(int(i[1]))
        filename = str(int(i[6]))
        question = i[3]
        if filename not in data:
            data[filename] = [filename,[]]
        data[filename][1].append((id,question))
    for i in data:
        filename = data[i][0]
        f = open('datasets/scg/data/SCG'+filename+'.txt','r')
        context = f.read()
        f.close()
        context = context.replace('\n',' ')
        context = context.replace('\t',' ')
        context = context
        qas = []
        for j in data[i][1]:
            id = j[0]
            question = j[1]
            qas.append({"id":len(qas)+1,"question":question,"question_id":id})
        qa_format.append({"context":context,"qas":qas})
    return qa_format
def modifyDataFrameToQaFormat(df):
    scgdf = df[df['type'] == 'scg']
    wikidf = df[df['type'] == 'wiki']
    scg_qa_format = modifySCGDataFrameToQAformat(scgdf)
    wiki_qa_format = modifyWikiDataFrameToQAformat(wikidf)
    return scg_qa_format + wiki_qa_format

def writeDataToFile(df):
    qa_data = modifyDataFrameToQaFormat(df)
    f = open('test/test.json','w')
    jsonString = json.dumps(qa_data, ensure_ascii=False).encode('utf8')
    f.write(jsonString.decode())
    f.close()

df = pd.read_csv('test/test.csv')
df = get_test_data_with_type(df)
writeDataToFile(df)