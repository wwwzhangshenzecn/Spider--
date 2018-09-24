import xlwt
import requests
from bs4 import BeautifulSoup

with open('all_hrefs.txt','r',encoding='utf-8') as f:
    href_list = []
    for h in f:
        href_list.append(h.split('\t')[1].replace("\n",""))


def List(m,n,k):
    '''
    抓取数据
    :param hrefs: 链接列表
    :return:
    '''
    hrefs = href_list[m:n]
    all_rec = []  # 存下所有的记录
    all_rec.append(["标题","作者","出版时间","出版社","价格/RMB"])

    for url in hrefs:
        resp = requests.get(url)
        bs = BeautifulSoup(resp.text)

        procduct = bs.find_all('div',attrs={'id':'product_info'})

        title =''
        author= ''
        price =''
        time = ''
        publish = ''

        for p in procduct:
            try:
                title = p.find('h1')['title']
            except:pass
            try:
                author = p.find('span',id='author').find('a').text
            except:pass

        procduct = bs.find_all('span',attrs={'class':'t1'})

        try:
            publish = str(procduct[1]).split('_blank">')[1].split('</a>')[0]
        except:
            pass

        try:
            time = str(procduct[2]).split('出版时间:')[1].split('</')[0]
        except:
            pass

        procduct = bs.find_all('p', attrs={'id':'dd-price'})

        try:
            price = str(procduct[0]).replace('\n',"").replace(' ','').split('n>')[1].split('<')[0]
        except:
            pass
        print(title,author,time,publish,price,'')
        all_rec.append([title,author,time,publish,price])

    all_href_file = open('all_book.txt', 'a', encoding='utf-8')

    for v in all_rec:
        all_href_file.write('\t'.join(v) + '\n')

    all_href_file.close()
    Writer_xls(all_rec,k)

def Writer_xls(rec,k):
    '''
    追写入xls文件
    :param rec: 信息表
    :return:
    '''
    import xlrd
    from xlutils.copy import copy
    st = '图书信息'+str(k)+'.xls'

    wb = xlwt.Workbook(st)
    sheet = wb.add_sheet('图书信息一览表')
    for i in range(0,len(rec)):
        for j in range(0,len(rec[i])):
            sheet.write(i,j,rec[i][j])
    wb.save(st)


def MongoDB_Save(rec):
    import pymongo
    import json

    ip = '127.0.0.1'
    port = 27017
    db_name = 'zz'
    collection_name = 'col'

    conn = pymongo.MongoClient(ip,port)
    db = conn[db_name]
    collection = db[collection_name]

    Json_data = json.loads(rec)

    collection.save(Json_data)

if __name__=='__main__':
    import time
    t1 =time.time()

    print( 100 //3)
    import multiprocessing

    lenght = len(href_list)
    l = lenght // 3

    pool = multiprocessing.Pool(3)

    pool.apply_async(List, (0,l,1))
    pool.apply_async(List, (l,2*l,2))
    pool.apply_async(List, (2*l,lenght,3))

    pool.close()
    pool.join()

    print("时间：",time.time()-t1)