#!usr/bin/env python
# -*- coding:utf8 -*-
# @TIME   :2020-12-02 18:25
# @Author :Xu Yongxin
# @File   :spark_test.py

from pyspark import SparkContext, SparkConf
from pyspark.mllib.recommendation import MatrixFactorizationModel
import os
import sys

def prepare_data(spark_context):
    item_rdd = spark_context.textFile("../ml-100k/u.item")   # 读取 u.item 电影信息数据
    movie_title = item_rdd.map(lambda line: line.split("|")) .map(lambda a: (float(a[0]), a[1]))

    movie_title_dict = movie_title.collectAsMap() # 将RDD转换字典
    return movie_title_dict

def load_model(spark_context):                    # 加载模型
    try:
        model = MatrixFactorizationModel.load(spark_context, '../datas/als-model')
        print (model)
        return model
    except Exception:
            print ("加载模型出错")

def recommend_movies(als, movies, user_id):
    rmd_movies = als.recommendProducts(user_id, 10)
    print('推荐的电影为：{}'.format(rmd_movies))
    for rmd in rmd_movies:
        print("为用户{}推荐的电影为：{}".format(rmd[0], movies[rmd[1]]))
    return rmd_movies


def recommend_users(als, movies, movie_id):  # 为每个电影推荐10个用户
    rmd_users = als.recommendUsers(movie_id, 10)
    print('针对电影ID：{0},电影名:{1},推荐是个用户为:'.format(movie_id, movies[movie_id]))
    for rmd in rmd_users:
        print("推荐用户ID：{},推荐评分：{}".format(rmd[0], rmd[2]))


def recommend(als_model, movie_dic):
    if sys.argv[1] == '--U':  # 推荐电影给用户
        recommend_movies(als_model, movie_dic, int(sys.argv[2]))
    if sys.argv[1] == '--M':  # 推荐用户给电影
        recommend_users(als_model, movie_dic, int(sys.argv[2]))


if __name__ == "__main__":
    """
    1.数据准备
    2.加载模型
    3.预测推荐
    """

    spark_context = SparkContext("local", "Test")
    # 由于推荐的方式有两种，一个是依据用户的推荐，一个是基于商品的推荐
    if len(sys.argv) != 3:
        print("请输入2个参数, 要么是: --U user_id,  要么是: --M movie_id")
        exit(-1)

    # 数据准备，就是加载电影数据信息，转换字典
    print('============= 数据准备 =============')
    movie_title_dic = prepare_data(spark_context)
    print('============= 加载模型 =============')
    als_load_model = load_model(spark_context)
    print('============= 预测推荐 =============')
    recommend(als_load_model, movie_title_dic)