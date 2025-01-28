import pandas as pd
import numpy as np
import time , pymysql, re,os.path
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql
from tqdm import tqdm
import collections
import math
from bs4 import BeautifulSoup

def ts(num : int):
    time.sleep(num)

def get_path(path): 

    return driver.find_elements(by = By.CSS_SELECTOR, value = path)

def get_class(path): 
    
    return driver.find_elements(by = By.CLASS_NAME, value = path)


def get_Xpath(path): 

    return driver.find_elements(by = By.XPATH, value = path)

def get_class_name(path): 

    return list(map(lambda x : x.text, driver.find_elements(by = By.CLASS_NAME, value = path)))

def pattern_replace(df, col, ptrn, rpl):

    df[col] = df[col].apply(lambda x: re.sub(pattern = ptrn, repl = rpl, string = x))

    return df

def word_replace(df, col, before, after):

    df[col] = df[col].apply(lambda x:x.replace(before, after))

    return df



URL = 'https://www.10000recipe.com/ranking/home_new.html'

user_agent = 'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option('prefs', {'intl.accept_languages': 'ko,ko-KR'})
options.add_argument('--disable-translate')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-infobars")
options.add_argument("--enable-logging")
options.add_argument("--log-level=0")
options.add_argument("--single-process")
options.add_argument("--ignore-certificate-errors")
options.add_argument('--start-fullscreen')
options.add_argument('user-agent={0}'.format(user_agent))


host_id = socket.gethostname()

# 개발 DB 서버 관련 변수
host = 'host'
port = 3306
user = 'user'
passwd = 'passwd'
db = 'db' 
charset = 'utf8mb4'

# Container별 크롤링 인덱스 부여를 위한 개발 DB 연결
devdb_con = pymysql.connect(host = host, 
                        user = user, 
                        password = passwd, 
                        db = db, 
                        charset = charset,
                        cursorclass = pymysql.cursors.DictCursor
                    )

devdb_cur = devdb_con.cursor()
devdb_sql = 'SELECT * FROM docker_data WHERE status="start"'
devdb_cur.execute(devdb_sql)
docker_db = devdb_cur.fetchall()
docker_df = pd.DataFrame(docker_db)

devdb_sql = 'SELECT * FROM docker_data WHERE status="end"'
devdb_cur.execute(devdb_sql)
docker_db = devdb_cur.fetchall()
end_df = pd.DataFrame(docker_db)

if len(end_df):
    if len(end_df[end_df['container_id']==host_id]):
        print('크롤링이 완료되어 종료합니다.')
        exit()

orig_length = 3318
print('총 {}개의 데이터를 불러옵니다.'.format(orig_length))
new_length = 3318

print('크롤링 할 인덱스를 확인합니다.')
if len(docker_df):
    if host_id in docker_df['container_id'].tolist():
        if docker_df[docker_df['container_id']==host_id]['ing_idx'].isna().sum():
            collector_cnt = docker_df['collector_cnt'].tolist()[0]
            if len(docker_df)!=collector_cnt:
                print('아직 확정되지 않아 종료합니다.')
                quit()
            else:
                print('데이터를 알맞게 분배합니다.')
                div_num = math.ceil(new_length/collector_cnt)
                split_df = []
                for i in range(1,(new_length//div_num)+2):
                    print((i-1)*div_num,'~',i*div_num,'개의 데이터를 분할합니다.')
                    split_df.append([(i-1)*div_num,i*div_num])
                idx = [i for i in docker_df[docker_df['container_id']==host_id].index]
                target_idx = split_df[idx[0]]
                print('할당된 인덱스는 {} ~ {}입니다.'.format(target_idx[0],target_idx[1]))
                devdb_con.ping(reconnect=True)
                sql = '''UPDATE `docker_data` SET `start_idx` = %s, `ing_idx` = %s, `end_idx` = %s WHERE `container_id` = %s'''
                devdb_cur.execute(sql,[target_idx[0],target_idx[0],target_idx[1],host_id])
                devdb_con.commit()
                start_idx = target_idx[0]
                end_idx = target_idx[1]
                if end_idx>new_length:
                    end_idx = new_length
        else:
            start_idx = docker_df[docker_df['container_id']==host_id]['ing_idx'].tolist()[0]
            end_idx = docker_df[docker_df['container_id']==host_id]['end_idx'].tolist()[0]
            if end_idx>new_length:
                    end_idx = new_length
    else:
        devdb_con.ping(reconnect=True)
        print('도커의 id가 없습니다.')
        print('크롤링 범위를 할당하기 위해 DB에 추가합니다.')
        sql = '''INSERT INTO `docker_data`(container_id) VALUES (%s)'''
        devdb_cur.executemany(sql,[host_id])
        devdb_con.commit()
        quit()
else:
    devdb_con.ping(reconnect=True)
    print('도커의 id가 없습니다.')
    print('크롤링 범위를 할당하기 위해 DB에 추가합니다.')
    sql = '''INSERT INTO `docker_data`(container_id) VALUES (%s)'''
    devdb_cur.executemany(sql,[host_id])
    devdb_con.commit()
    quit()

# ---------------------------------------------------------------------------------------------- #
print('크롤링을 위해 전체 데이터를 불러옵니다.')

menu_copy = pd.read_excel('menu_keyword.xlsx',index_col=0)

print('전체 데이터를 불러왔습니다.')

print('시작인덱스: ',start_idx,'종료 인덱스: ', end_idx)
menu_copy = menu_copy[start_idx:end_idx]


# 크롤링
driver = webdriver.Chrome(options=options); ts(5)
# driver.implicitly_wait(3)

product_label = {}
url = 'https://www.10000recipe.com'


print('크롤링을 시작합니다.')
new_df = pd.read_excel('form.xlsx')

for vals in tqdm(menu_copy.values):
    
    id = vals[0]
    menu_name = vals[1]
    descrp = vals[2]
    includes = vals[3]
    keyword_list = vals[4]
    
    # print('-----------------------')
    keyword = keyword_list.replace('(','').replace(')','')
    print('KEYWORD: ',keyword)
    total_url = url + '/recipe/list.html?q=' + keyword + '&order=accuracy'
    ingredient_list = []
    
    try:

        driver.get(total_url);ts(3)
        print('키워드 링크로 접속완료했습니다.')
        print('정확도순 상위 5개 크롤링 시작.')

        for i in range(1,6):

            print(i)

            try: # 5개 있으면

                get_path('#contents_area_full > ul > ul > li:nth-child({})'.format(i))[0].click();ts(3)
                print('{}번째 레시피로 들어갑니다.'.format(i))
                j = 3

                while True:

                    try: # 있는 재료 다 가져옴

                        ingredient = get_path('#divConfirmedMaterialArea > ul > li:nth-child({}) > a:nth-child(1)'.format(j))[0].text;ts(3) # 3,5,7,9,11
                        print(ingredient)
                        ingredient_list.append(ingredient)
                        
                        j += 2

                    except: # 없으면 뒤로 가서 정확순 확인
                        print('재료를 모두 크롤링했습니다. 이전 화면으로 이동합니다.')
                        driver.back(); ts(3)
                        break

            except: # 5개 없으면 끝나는 대로 for문 종료
                print('5개는 없지만 있는만큼 완료했습니다.')
                break
            

        print('정확도순 상위 n개 크롤링 완료.')
        


    except: # 해당 키워드에 대한 검색 결과가 없는 경우
        print('키워드에 대한 레시피 결과가 없습니다.')
        pass
    

    ingredient_list = list(map(lambda x:x.strip(), ingredient_list))

    product_label[id] = ingredient_list

    counter_dict_10 = collections.Counter(product_label[id]).most_common(10)

    for k in range(len(counter_dict_10)):
        
        label_name = counter_dict_10[k][0]
        label_cnt = counter_dict_10[k][1]

        tmp_df = pd.DataFrame(columns=['name','type','product_id','menu_name','description','includes','keyword','cnt'])
    
        tmp_df.loc[0,'name'] = label_name
        tmp_df.loc[0,'type'] = '주재료'
        tmp_df.loc[0,'product_id'] = id
        tmp_df.loc[0,'menu_name'] = menu_name
        tmp_df.loc[0,'description'] = descrp
        tmp_df.loc[0,'includes'] = includes
        tmp_df.loc[0,'keyword'] = keyword
        tmp_df.loc[0,'cnt'] = label_cnt

        new_df = pd.concat([new_df,tmp_df])

    new_df.to_excel('{}_{}.xlsx'.format(start_idx,end_idx),index=False)
    print(id,'까지에 대한 엑셀 파일을 생성했습니다.')

print('전체 과정을 완료했습니다.')

devdb_con = pymysql.connect(host = host, 
                        user = user, 
                        password = passwd, 
                        db = db, 
                        charset = charset,
                        cursorclass = pymysql.cursors.DictCursor
                    )
devdb_cur = devdb_con.cursor()

sql = '''UPDATE `docker_data` SET `status` = %s WHERE `container_id` = %s'''
devdb_cur.execute(sql,['end',host_id])
devdb_con.commit()

devdb_cur.close()
devdb_con.close()
driver.quit()
print('해당 container의 상태를 End로 변경하며, 코드를 종료합니다.')