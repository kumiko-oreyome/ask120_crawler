import numpy as np
def extract_question_from_crawl_txt(path):
    with open(path,'r',encoding='utf-8') as f:
        lines = list(f.readlines())
        line_num = len(lines)
        line_array = np.array(lines,dtype='object')
        questions = line_array[range(0,line_num,3)].tolist()
        for q in questions:
            print(q.rstrip())
        #return questions
        