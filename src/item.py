from datetime import datetime
class QAItem():
    @classmethod
    def create_from_document(cls,doc):
        q = QuestionItem(qid=doc['qid'],title=doc['title'],description=doc['description'])
        al = [AnswerItem(**ans) for ans in doc['answers']]
        return QAItem(q,al)

    def __init__(self,question,answers):
        self.question = question
        self.answer_list = []
        for a in answers:
            self.append_answer(a)

    def get_title(self):
        return self.question.title


    def append_answer(self,answer):
        self.answer_list.append(answer)

    def find_newest_answer(self):
        if len(self.answer_list) > 0 :
            argmax,_ =  sorted( [ (i,a.get_time()) for i,a in enumerate(self.answer_list)] ,key=lambda x:x[1],reverse=True)[0]
            return self.answer_list[argmax]
        else:
            return null_answer

    def to_dict(self):
        d = self.question.to_dict()
        d['answers'] = []
        for a in self.answer_list:
            d['answers'].append(a.to_dict())
        return d
    

class AnswerItem(): 
    def __init__(self,content,time,job):
        self.job = job
        self.content = content 
        self.time = time
    
    def get_time(self):
        return datetime.strptime(self.time,"%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {'job':self.job,'content':self.content,'time':self.time}


class QuestionItem():
    def __init__(self,qid,title,description):
        self.qid = qid
        self.title = title
        self.description = description
    def to_dict(self):
        return {'qid':self.qid,'title':self.title,'description':self.description}

null_answer  = AnswerItem('no-content','2019-01-01','no-job')