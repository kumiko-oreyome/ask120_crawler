import re
from lxml import etree
from .util import rlstrip



class Ask120HomePage():
    def __init__(self,page_src):
        self.page_src = page_src
        self.base_root = etree.HTML(page_src)


    def _get_department_node(self):
        return self.base_root.xpath("//div[@class='keshi-part clears']")[0]

    def parse_department_hrefs(self):
        for node in self._get_department_node().xpath('./a'):
            href = node.xpath('./@href')[0]
            yield href
           
    def parse_department_names(self):
        for node in self._get_department_node().xpath('./a'):
            department_name = rlstrip(node.xpath('./text()')[0])
            yield department_name


class KeywordQueryPage():
    def __init__(self,page_src):
        self.page_src = page_src
        self.base_root = etree.HTML(page_src)

    def is_valid_question_link(self,url):
        if url.startswith("http://www.120ask.com/question"):
            return True
        return False
    

    def parse_question_links(self):
        for node in self.base_root.xpath("//div[@class='result_box']//ul//span[@class='c_url']"):
            link = node.xpath("./text()")[0]
            if self.is_valid_question_link(link):
                yield link

    def parse_question_ids(self):
        for link in self.parse_question_links():
            m = re.search(r'([0-9]+)\.htm',link)
            qid = m.group(1)
            yield qid        

    def parse_next_page_link(self):
        link = self.base_root.xpath("//div[@class='p_pagediv']//a[@title='下一页']/@href")
        if len(link) == 0:
            return None
        return link[0]


 

class PageUnderDepartment():
    def __init__(self,keyword,page_src):
        self.keyword = keyword
        self.base_root = etree.HTML(page_src)
    def parse_diseases(self):
        disease_div_node = self.base_root.xpath("//ul[@class='clears h-ul1']")[0]
        l = []
        for disease_node in disease_div_node.xpath('./li/a'):
            href = disease_node.xpath('./@href')[0]
            department_name = rlstrip(disease_node.xpath('./text()')[0])
            l.append((department_name,href))
        return l
    def parse_questions(self):
        question_div_node = self.base_root.xpath("//div[@class='t13 h-main']//ul[@class='clears h-ul3']")[0]
        l = []
        for question_node in question_div_node.xpath(".//p[@class='h-pp1']"):
            #a1,a2 =  question_node.xpath("./a")
            #department_tag_name = a1.xpath("./text()")[0]
            #department_href =  a1.xpath("./@href")[0]
            q_node = question_node.xpath("./a[@class='q-quename']")[0]
            qtitle = q_node.xpath('./text()')[0]
            q_href = q_node.xpath('./@href')[0]
            l.append(( qtitle,q_href))
            #print(( department_tag_name,department_href,qtitle,q_href))
        return l


class HealthQuestionPage():
    def __init__(self,page_src,qid=None):
        self.page_src = page_src
        self.html_root = etree.HTML(page_src)
        self.qid = qid

    def is_valid_single_question(self):  
        title = self.parse_title()
        description = self.parse_description()
        return  title != 'no-title' and not description.startswith(title)


    def parse_nearest_department(self):
        node = self.html_root.xpath("//div[@class='b_route']/a")
        assert len(node) > 1
        node = node[-1]
        url =  rlstrip(node.xpath('./@href')[0])
        if not url.startswith("https:"):
            url = "https:"+url
        name = node.xpath('.//text()')[0]
        return name,url


    def parse_responses(self):
        responses =  self.html_root.xpath("//div[@class='b_answerli']")
        for response in responses:
            try:
                profile_box_node = response.xpath(".//div[@class='b_answertl']")[0]
                answer_box =  response.xpath(".//div[@class='b_anscontc']")[0]
                job = "".join(profile_box_node.xpath(".//span[@class='b_sp1']/text()"))
                time = answer_box.xpath(".//span[@class='b_anscont_time']/text()")[0]
                answer = answer_box.xpath(".//div[@class='crazy_new']/p")[0].xpath('string()')
                yield {'job':rlstrip(job),'answer':rlstrip(answer),'time':rlstrip(time)}
            except :
                print('something wrong while parsing responses of qid %s'%(self.qid))        

    def parse_title(self):
        title = 'no-title'
        try :
            title = self.html_root.xpath("//h1[@id='d_askH1']//text()")[0]
        except:
             print('something wrong while parsing title of qid(%s)'%(self.qid))
        return title

    def parse_description(self):
        description = 'no-description'
        try:
            description_node = self.html_root.xpath("//div[@class='b_askbox']//div[@class='b_askcont']//p[@class='crazy_new']")[0]
            description = description_node.xpath("./text()")[1].strip()
        except:
             print('something wrong while parsing description of qid(%s)'%(self.qid))
        return description

   