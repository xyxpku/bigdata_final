#!usr/bin/env python
# -*- coding:utf8 -*-
# @TIME   :2020-12-02 13:09
# @Author :Xu Yongxin
# @File   :sentiment_avereage.py

from textblob import TextBlob
import sys
import numpy as np
from utils.data_utils import csv_map_key,csv_map_key_list,write_csv_new

if __name__ == "__main__":
    result_dict=csv_map_key_list("../data/movie_sentiment.csv")
    idmap_dict=csv_map_key("../ml-latest-small/links.csv",reverse=True)

    #print(result_dict)
    average_list=[]
    average_list.append(["movieId","average_score"])
    for key in result_dict.keys():
        row_list=[]
        row_list.append(idmap_dict[key])
        row_list.append(np.mean(result_dict[key]))
        average_list.append(row_list)

    #print(average_list)
    write_csv_new("../data/movie_score.csv",average_list)