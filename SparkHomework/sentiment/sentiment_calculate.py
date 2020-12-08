#!usr/bin/env python
# -*- coding:utf8 -*-
# @TIME   :2020-12-02 09:28
# @Author :Xu Yongxin
# @File   :sentiment_calculate.py

from textblob import TextBlob
import sys
sys.path.append('/home1/xyx/SparkHomework')
from utils.data_utils import get_csv_list,write_csv_new

# text = "I am happy today. I feel sad today."
# blob = TextBlob(text)
# print(blob.sentences)
#
# print(blob.sentences[0].sentiment)
#
# import nltk
# nltk.download()


if __name__ == "__main__":
    rowlist = get_csv_list("../data/movie_review_info.csv")
    contentlist = [row for row in rowlist[1:]]
    write_list=[]
    write_list.append(["movieId","movieSentiment"])
    for index,row in enumerate(contentlist):
        print("处理到第"+str(index)+"行")

        write_row_list=[]
        write_row_list.append(row[0])

        text=row[1]
        blob = TextBlob(text)
        write_row_list.append(float(blob.sentiment.polarity))

        #write_row_list.append(0.2)

        write_list.append(write_row_list)

    write_csv_new("../data/movie_sentiment.csv",write_list)




