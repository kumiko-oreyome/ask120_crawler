from src import backend,db,crawler,util
import argparse
import config


arg_parser = argparse.ArgumentParser(description='')
arg_parser.add_argument('--kw_file',default='./datas/disease_list.txt')
args = arg_parser.parse_args()
#arg_parser.add_argument('host')
#arg_parser.add_argument('db_name')
#arg_parser.add_argument('--password',default='')
 
if __name__=='__main__':
    connector =   db.MongoConnector(config.DB_HOST,config.DB_USER_NAME,config.DB_PASSWORD,config.DB_NAME)
    backend =  backend.MongoQABackend(connector,config.QA_COLLECT_NAME)
    crawler = crawler.Ask123Crawler(util.get_browser_driver(config.DRIVER_PATH,config.ENV),backend)
    keywords = util.read_txt_lines(args.kw_file)
    keywords = util.expand_keywords(keywords,['飲食'])
    crawler.crawl_by_keywords(keywords)

    