


def create_qa_item(qid,title,description,answers):
    q = QuestionItem(qid,title,description)
    answers = [ AnswerItem(content,time,job)  for content,time,job  in answers]
    return QAItem(q,answers)


class QAItem():
    def __init__(self,question,answers):
        self.question = question
        self.answer_list = []
        for a in answers:
            self.append_answer(a)
    def append_answer(self,answer):
        self.answer_list.append(answer)
    def find_newest_answer(self):
        pass
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
    def to_dict(self):
        return {'job':self.job,'content':self.content,'time':self.time}


class QuestionItem():
    def __init__(self,qid,title,description):
        self.qid = qid
        self.title = title
        self.description = description
    def to_dict(self):
        return {'qid':self.qid,'title':self.title,'description':self.description}