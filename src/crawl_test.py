from requests_html import HTMLSession


from lxml import etree,html
import requests
from urllib.parse import urljoin
import requests,time

session = HTMLSession()

def valid_question_link(url):
    print(url)
    if url.startswith("http://www.120ask.com/question"):
        return True
    return False

def request_page(url):
    r = session.get(url)
    r.html.render(wait=60)
    tree = html.fromstring(r.content)
    return tree

def parse_page(base_url):
    r = session.get(base_url)
    r.html.render(wait=60)
    base_root = html.fromstring(r.content)
    try:
        assert len(base_root.xpath("//div[@class='result_box']//ul//li")) and >0
    except :
        print('fuck...')
        yield next(parse_page(base_url))
    else:
        yield base_root
        for node in base_root.xpath("//div[@class='result_box']//ul//li"):
            title = node.xpath("string(.//h3/a)")
            link = node.xpath("./span/text()")
            if len(link)>0 and valid_question_link(link[0]):
                link = link[0]
                detail_page = urljoin(base_url,link)
                root = request_page(detail_page)
                title,answer = parse_answer(root)   
                yield title,link,answer

def parse_answer(html_root):
    title = html_root.xpath("//h1[@id='d_askH1']//text()")[0]
    answer  = 'No_Answer'  
    rl =  html_root.xpath("//div[@class='b_answerli']//div[@class='crazy_new']/p")
    if len(rl) > 0:
        answer = rl[0].xpath('string()').strip()
    return title,answer


keywords = ['高血壓+飲食','糖尿病+飲食','中風+飲食']



for keyword in keywords:
    start_url ='http://so.120ask.com/?kw=%s'%(keyword)
    current_url = start_url
    f = open('%s_v2.txt'%(keyword),'w',encoding='utf-8')
    while True:
        progress = parse_page(current_url)
        root = next(progress)
        for title,link,answer in progress:
            print(title)
            f.write(title+"\n")
            f.write(answer+"\n")
            f.write('- - - - '*30+"\n")
            f.flush()
        link = root.xpath("//div[@class='p_pagediv']//a[@title='下一页']/@href")
        if len(link)  == 0:
            break
        current_url =  urljoin(start_url,link[0])
    f.close()