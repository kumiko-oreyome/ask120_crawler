import itertools,unicodedata,json
def remove_irrelated_questions(path,keyword):
    f = open(path,'r',encoding='utf-8') 
    filename,ext = path.split(".")
    wf = open(filename+"_rm."+ext,'w',encoding='utf-8')
    while True:
        title = f.readline().rstrip()
        print("t :%s"%(title))
        if len(title)<1:
            break
        answer = f.readline().rstrip()
        _ = f.readline().rstrip()
        if keyword not in title:
            continue
        wf.write(title+"\n")
        wf.write(answer+"\n")
        wf.write(_+"\n")
    f.close()
    wf.close()


def merge_qa_txts(paths,output_path):
    qas  =  list(itertools.chain(*[ read_qa_txt(path) for path in paths ]))
    with open(output_path,'w',encoding='utf-8') as f:
        for q,a in qas:
            qa_json = QAPair(q,a).to_json()
            f.write(json.dumps(qa_json,ensure_ascii=False)+"\n")



def read_qa_txt(path):
    ret = []
    with open(path,'r',encoding='utf-8') as f:
        while True:
            title = f.readline().rstrip()
            print(title)
            if len(title)<1:
                break
            answer = f.readline().rstrip()
            title = unicodedata.normalize("NFKD", title).replace(" ", "") #去掉空白 /xa0
            answer = unicodedata.normalize("NFKD", answer).replace(" ", "")
            _ = f.readline()
            ret.append((title,answer))
    return ret



class QAPair():
    def __init__(self,question,answer):
        self.question = question
        self.answer = answer
    
    def to_json(self):
        return {"question":self.question,"answer":self.answer}


merge_qa_txts(["問題和答案_分類1.csv","中風.txt","乳癌.txt","高血壓.txt","腦瘤.txt","糖尿病.txt"],"merge.jsonl")