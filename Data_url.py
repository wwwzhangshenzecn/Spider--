from bs4 import BeautifulSoup
import requests
from selenium import webdriver


'''
获取图书书名以及地址
'''

url_part_1 = 'http://search.dangdang.com/?key=%CE%C4%D1%A7&act=input&page_index='
url_part_2 = ''

def format_htref(url):
    return 'http://'+url

def JD_html_url(min,max):
    '''
    :param min: 页面号下限
    :param max: 页面号上限
    :return:
    '''
    JD_html_url = []

    for i in range(min,max+1):
        JD_html_url.append(url_part_1+str(i))

    all_href_list = []
    for url in JD_html_url:
        # print(url)
        resp = requests.get(url)

        bs = BeautifulSoup(resp.text)
        a_list = bs.find_all('a',attrs={'dd_name':'单品标题'})

        need_list = []

        #获取所有的 书名和链接
        for h in a_list:
            if 'href' in h.attrs :
                href_val = h['href']

                title_val = h.text
                title = h['title']

                if [title_val,format(href_val)] not in need_list and h.text!="":
                    need_list.append([str(title).replace(" ",'').strip(),format(href_val).replace(" ",'').strip()])

        all_href_list += need_list

    all_href_file = open('all_hrefs.txt','a',encoding='utf-8')

    for v in all_href_list:
        all_href_file.write('\t'.join(v)+'\n')

    all_href_file.close()

import multiprocessing

def Multiple_threading_pool(m):
    '''
    使用m个进程池
    :param m:CPU个数
    :return:
    '''
    pool = multiprocessing.Pool(m)

    for k in range(0,m):
        pool.apply_async(JD_html_url,(30*k+1,30*(k+1)))

    pool.close()
    pool.join()



if __name__=='__main__':
    import time
    t1 = time.time()
    Multiple_threading_pool(3) #要把线程池放入 __mian__中，否则抛出异常
    print(time.time()-t1)