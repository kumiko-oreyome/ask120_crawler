from .item import QuestionItem,QAItem,AnswerItem
class MongoQABackend():
    def __init__(self,connector,qa_collect_name):
        self.connector = connector
        self.collection = self.connector.get_collect(qa_collect_name)

    def save_qa_instance(self,qa):
        d  = qa.to_dict()
        self.collection.insert_one(d)
 
    def check_question_duplicate(self,qid):
        return self.collection.find_one({'qid':qid}) is not None

    def retrieve_qas(self,find_newest=True):
        qas = self.collection.find()
        l = []
        for qa in qas:
            qa_item = QAItem.create_from_document(qa)
            l.append(qa_item)
        if find_newest:
            return [(item.get_title(),item.find_newest_answer().content) for item in l]
        return l