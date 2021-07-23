import pandas as pd
import json
from lxml import etree

parser = etree.XMLParser(recover=True)
def extract_text(body):
    tree = etree.fromstring(body, parser=parser)
    try:
        text = tree.text
    except:
        text = -1
    return text
def findAnswerStartFromContext(context,answer):
    try:
        answer_start = context.index(answer)
    except:
        answer_start = -1
    return answer_start

def getWikiDataToDataFrame():
    f = open('datasets/wiki/ThaiQACorpus-DevelopmentDataset.json','r')
    data = json.load(f)
    df = pd.DataFrame(data["data"])
    return df

def modifyWikiDataFrameToQAformat(df):
    data = dict()
    qa_format = []
    for i in df.itertuples():
        if i[2] == 1:
            filename = str(int(i[7]))
            question = i[3]
            answer = i[4]
            answer_start = i[5]
            if filename not in data:
                data[filename] = [filename,[]]
            data[filename][1].append((question, answer))
    for i in data:
        filename = data[i][0]
        f = open('datasets/wiki/wiki-documents-nsc/'+filename+'.txt','r')
        context = f.read()
        f.close()
        context = extract_text(context)
        if extract_text != -1:
            qas = []
            for j in data[i][1]:
                question = j[0]
                answer = j[1]
                answer_start = findAnswerStartFromContext(context,answer)
                qas.append({"id":len(qas)+1,"is_impossible":answer_start < 0, "question":question,"answer":[{"text":answer,"answer_start":answer_start}]})
            qa_format.append({"context":context,"qas":qas})
    return qa_format
df = getWikiDataToDataFrame()
wiki_qa_format = modifyWikiDataFrameToQAformat(df)
f = open('wiki.json','w')
jsonString = json.dumps(wiki_qa_format, ensure_ascii=False).encode('utf8')
f.write(jsonString.decode())
f.close()