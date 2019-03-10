class MongoQABackend():
    def __init__(self,connector,qa_collect_name):
        self.connector = connector
        self.collection = self.connector.get_collect(qa_collect_name)

    def save_qa_instance(self,qa):
        d  = qa.to_dict()
        r = self.collection.insert_one(d)
        print(r.inserted_id)

    def check_question_duplicate(self,qid):
        return self.collection.find_one({'qid':qid}) is not None