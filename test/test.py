import unittest
from src.item import QuestionItem,AnswerItem,QAItem
from src.db import  MongoConnector
from src.backend import MongoQABackend
import config

from src.page import  KeywordQueryPage,HealthQuestionPage,PageUnderDepartment,Ask120HomePage


def create_qa_item(qid,title,description,answers):
    q = QuestionItem(qid,title,description)
    answers = [ AnswerItem(content,time,job)  for content,time,job  in answers]
    return QAItem(q,answers)

class WebPageParserTest(unittest.TestCase):

    def setUp(self):
        self.legal_page_file = './test/2.html'
        self.illegal_page_file = './test/1.html'
        self.listhome_page_file = './test/listhome.html'


    def test_parse_question_list(self):
        l = [('http://www.120ask.com/question/73715734.htm','73715734'),('http://www.120ask.com/question/26077691.htm','26077691')]
        with open('./test/q_list.html','r',encoding='utf-8') as f:
            src = f.read()
            lk,qi = zip(*l)
            lk,qi = list(lk),list(qi)
            page = KeywordQueryPage(src)
            links = list(page.parse_question_links())[0:2]
            qids = list(page.parse_question_ids())[0:2]
            self.assertEqual(lk,links)
            self.assertEqual(qi,qids)
            self.assertEqual('http://so.120ask.com/?kw=%E5%B0%BF%E7%97%85%E8%A9%B2&page=2',page.parse_next_page_link())

    def test_parse_singel_question_page(self):
        with open(self.legal_page_file ,'r',encoding='utf-8') as f:
            page = HealthQuestionPage(f.read())
            title = page.parse_title()
            descirption = page.parse_description()
            answers = list(page.parse_responses())

            self.assertEqual(title,'糖尿病该如何治愈呢？')
            self.assertEqual(descirption,'去年我的糖尿病已经治愈了，控制的一直都是很好，但是这一段时间我的血压有高了，不知道是怎么回事，饮食一直都是很忙有规律的，去医院检查，医生说要打针治疗。')
            self.assertEqual(answers[0]['job'],'爱心医生')
            self.assertEqual(answers[0]['time'],'2014-10-28 09:54:58')
            self.assertEqual(answers[0]['answer'][0:10],'你好,进食过多,体力')
            self.assertEqual(("糖尿病","https://www.120ask.com/list/tangniaobing/"),page.parse_nearest_department())
        

    def test_valid_single_question_page(self):
        with open(self.legal_page_file ,'r',encoding='utf-8') as f:
            page = HealthQuestionPage(f.read())
            self.assertEqual(True,page.is_valid_single_question())
        with open(self.illegal_page_file ,'r',encoding='utf-8') as f:
            page = HealthQuestionPage(f.read())
            self.assertEqual(False,page.is_valid_single_question())


    def test_parse_department_url(self):
        with open(self.listhome_page_file,'r',encoding='utf-8' ) as f:
            page = Ask120HomePage(f.read())
            urls = list(page.parse_department_hrefs())
            names = list(page.parse_department_names())
            self.assertEqual(len(urls),len(names))
            self.assertEqual(len(urls),23)
            self.assertIn('http://www.120ask.com/list/wuguanke/',urls)
            self.assertIn('http://www.120ask.com/list/zxmrk/',urls)
            self.assertIn('五官科',names)
            self.assertIn('整形美容科',names)
        

           
    def test_parse_department_page(self):
        with open('./test/waiko.html','r',encoding='utf-8' ) as f:
            page = PageUnderDepartment('外科',f.read())
            l = page.parse_diseases()
            self.assertEqual(len(l),8)
            l2 = page.parse_questions()
            self.assertEqual(len(l2),20)
            href = page.parse_next_link()
            self.assertEqual(href,"http://www.120ask.com/list/waike/2/")


class ItemTest(unittest.TestCase):
    def test_qa_item(self):
        def same_field(d1,d2,field_name):
            return self.assertEqual(d1[field_name],d2[field_name])

        qa = {'title':'hasaki','description':'fuck','qid':'8787',\
        'answers':[{'job':'fucker','content':'qwer','time':'2011-2-3 00:22:12'},{'job':'AAA','content':'BBB','time':'2012-11-3 00:00:00'}]}
        q_item = QuestionItem('8787','hasaki','fuck')
        a_items = [AnswerItem('qwer','2011-2-3 00:22:12','fucker'),AnswerItem('BBB','2012-11-3 00:00:00','AAA')]
        qa_item = QAItem(q_item,a_items)
        d = qa_item.to_dict()
        same_field(d,qa,'title')
        same_field(d,qa,'description')
        same_field(d,qa,'qid')
    
    def test_create_qa_item_from_document(self):
        doc = {'title':'hasaki','description':'fuck','qid':'8787',\
        'answers':[{'job':'fucker','content':'qwer','time':'2011-2-3 00:22:12'},{'job':'AAA','content':'BBB','time':'2012-11-3 00:00:00'}]}
        qa_item = QAItem.create_from_document(doc)
        self.assertEqual(qa_item.get_title(),'hasaki')
        self.assertEqual(qa_item.answer_list[0].job,'fucker')
       

    def test_find_newest_answer(self):
        q_item = QuestionItem('8787','hasaki','fuck')
        a_items = [AnswerItem('qwer','2011-2-3 00:22:12','fucker'),AnswerItem('BBB','2012-11-3 00:00:00','AAA')]
        qa_item = QAItem(q_item,a_items)
        self.assertEqual(qa_item.find_newest_answer().content,'BBB')


        
        
class MongoBackendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #create test db
        fake_datas = []
        fake_datas.append(create_qa_item('id1','title1','descirption1',[('content1_1','2012-2-3 00:22:14','job_1_1'),('content1_2','2012-2-3 00:22:12','job_1_2'),('content1_3','2011-2-3 00:22:13','job_1_3')]))
        fake_datas.append(create_qa_item('id2','title2','descirption2',[('content2_1','2011-2-3 00:22:12','job_2_1')]))
        fake_datas.append(create_qa_item('id3','title3','descirption3',[('content3_1','2017-2-3 00:22:12','job_3_1'),('content3_2','2011-2-3 00:22:12','job_3_2'),('content3_3','2011-2-2 00:22:12','job_3_3')]))
        fake_datas.append(create_qa_item('id4','title4','descirption4',[('content4_1','2017-2-3 00:22:12','job_4_1'),('content4_2','2011-2-3 00:22:13','job_4_2')]))
  
        connector =  MongoConnector(config.DB_HOST,config.TEST_DB_USER_NAME,config.TEST_DB_PASSWORD,config.TEST_DB_NAME)

        if  config.QA_COLLECT_NAME in connector.db.collection_names():
            connector.get_collect(config.QA_COLLECT_NAME).drop()
        connector.create_collect(config.QA_COLLECT_NAME)
        cls.fake_datas = fake_datas
        cls.connector = connector
    

    def test_retrieve_qas(self):
        backend = MongoQABackend(self.connector,config.QA_COLLECT_NAME)
        qas1 = backend.retrieve_qas(find_newest=True)
        qas2 = backend.retrieve_qas(find_newest=False)
        self.assertEqual(len(qas1),4)
        self.assertEqual(qas1,[('title1','content1_1'),('title2','content2_1'),('title3','content3_1'),('title4','content4_1')])
        self.assertEqual(len(qas2),4)
        self.assertEqual(qas2[0].answer_list[0].content,'content1_1')
        self.assertEqual(qas2[3].answer_list[1].job,'job_4_2')
        self.assertEqual(len(qas2[0].answer_list),3)

    
    def test_insert_qa(self):
        backend = MongoQABackend(self.connector,config.QA_COLLECT_NAME)
        for d in  self.fake_datas:
            backend.save_qa_instance(d)
        collect =  self.connector.get_collect(config.QA_COLLECT_NAME)
        qas = list(collect.find())
        self.assertEqual(len(qas),4)

        self.assertTrue(backend.check_question_duplicate('id4'))
        self.assertFalse(backend.check_question_duplicate('8787'))

    @classmethod
    def tearDownClass(cls):
        cls.connector.get_collect(config.QA_COLLECT_NAME).drop()


def suite():  
    suite = unittest.TestSuite()  
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ItemTest))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase( MongoBackendTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(  WebPageParserTest))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())