from selenium  import webdriver
import unicodedata




def rlstrip(s):
   return unicodedata.normalize("NFKD", s).strip().rstrip()

def read_txt_lines(path):
    lines = []
    with open(path,'r',encoding="utf-8") as f:
        for row in f:
            lines.append(row.rstrip('\n'))
    return lines


def expand_keywords(keywords,expands=[]):
    l = []
    l.extend(keywords)
    for exp_word in expands:
        l.extend( [ '%s_%s'%(kw,exp_word) for kw in keywords])
    return l
 

def get_browser_driver(driver_path,env_name):
    if env_name == 'DEBUG':
        driver  = webdriver.Chrome(driver_path,chrome_options=webdriver.ChromeOptions())
    elif env_name == 'DEPLOY':
        driver = webdriver.Firefox(driver_path)
    else:
        assert False
    return driver