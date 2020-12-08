#!usr/bin/env python
# -*- coding:utf8 -*-
# @TIME   :2020-12-01 19:53
# @Author :Xu Yongxin
# @File   :data_utils.py

import csv
import pickle
from collections import defaultdict

def get_csv_list(file_path):
    with open(file_path, "r", encoding='utf-8') as csvreader:
        reader = csv.reader(csvreader)
        rowlist = [row for row in reader]
        return rowlist

def write_csv_new(file_path,row_list):
    with open(file_path, "w", newline='', encoding='utf-8') as csvwriter:
        writer=csv.writer(csvwriter)
        writer.writerows(row_list)

def csv_map_key_list(file_path):
    row_list=get_csv_list(file_path)
    result_dict=defaultdict(list)
    for row in row_list[1:]:
        result_dict[row[0]].append(float(row[1]))
    return result_dict

def csv_map_key(file_path,reverse=False):
    row_list=get_csv_list(file_path)
    result_dict={}
    for row in row_list[1:]:
        if reverse==False:
            result_dict[row[0]]=row[1]
        else:
            result_dict[row[1]] = row[0]
    return result_dict

def save_pkl_file(file_obj,file_path):
    with open(file_path, "wb") as f:
        pickle.dump(file_obj, f)  # 顺序存入变量

def load_pkl_file(file_path):
    with open(file_path, 'rb') as f:
        file_obj= pickle.load(f)
    return file_obj

if __name__ == "__main__":
     rowlist=get_csv_list("../ml-latest-small/links.csv")
     #print(rowlist)

     imdbIdList=[row[1] for row in rowlist[1:]]
     save_pkl_file(imdbIdList,"../data/imdb_list.pkl")
