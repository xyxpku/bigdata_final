#!usr/bin/env python
# -*- coding:utf8 -*-
# @TIME   :2020-12-01 19:35
# @Author :Xu Yongxin
# @File   :catch_imdb.py

import re
import requests
import time
import csv
#from selenium import webdriver
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import sys
sys.path.append('/home1/xyx/SparkHomework')
from utils.data_utils import load_pkl_file

def catch_IMDB_review(movie_id):
    NETWORK_STATUS = True  # 判断状态变量
    URL = "https://www.imdb.com/title/tt"+str(movie_id)+"/reviews?spoiler=hide&sort=helpfulnessScore&dir=desc&ratingFilter=0"
    print("URL：",URL)
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            original_html = response.text
            soup = BeautifulSoup(original_html,'lxml')

            reviews = soup.select('.review-container')

            movie_list=[]

            for review in reviews:
                single_review_list=[]
                content = review.select_one('.content')
                user_review = content.select('.text.show-more__control')
                dr = re.compile(r'<[^>]+>', re.S)
                user_review=str(user_review[0])
                movie_review = dr.sub('', user_review)
                single_review_list.append(movie_id)
                single_review_list.append(movie_review)
                movie_list.append(single_review_list)
                #print("用户评论：",movie_review)

            return movie_list
    except Exception:
        print("Request Failed")
        return None
    # except requests.exceptions.Timeout:
    #     NETWORK_STATUS = False  # 请求超时改变状态
    #     if NETWORK_STATUS == False:
    #         #'''请求超时'''
    #         driver.close()  # 关闭网页
    #         print('请求超时，重复请求')
    #         catch_IMDB_review(URL, movie_id)

if __name__ == "__main__":
    imdb_list=load_pkl_file("../data/imdb_list.pkl")
    movie_list=[]
    with open('../data/movie_review_info.csv', 'w', newline="", encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["movieId", "movieReview"])
        for i in range(0,len(imdb_list)):
            print("第"+str(i)+"个电影")
            movie_list=catch_IMDB_review(imdb_list[i])
            try:
                for j in range(len(movie_list)):
                    csvwriter.writerow(movie_list[j])
            except Exception:
                print("第" + str(i) + "个电影出错")
	  
