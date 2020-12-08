#!usr/bin/env python
# -*- coding:utf8 -*-
# @TIME   :2020-12-02 14:55
# @Author :Xu Yongxin
# @File   :spark_train.py


import os
from pyspark import SparkContext,SparkConf
from pyspark.mllib.recommendation import ALS,Rating

#SparkContext
# conf = SparkConf().setMaster("spark://162.105.88.93:7077")
# #sc=SparkContext("spark://162.105.88.93:7077","Test")
# sc=SparkContext("local","Test")
#
# #text = sc.textFile("hdfs://localhost:9000/data/ratings.csv")
# #text = sc.textFile("/data/ratings.csv")
# text=sc.textFile("/Users/xyxljz/PycharmProjects/SparkHomework/ml-latest-small/ratings.csv")
# #text=sc.textFile("file:////home/ml-latest-small/ratings.csv")
# text = text.filter(lambda x: "movieId" not in x)
#
# print(text.count())
#
# movieRatings = text.map(lambda x: x.split(",")[:3])
# model = ALS.train(movieRatings, 10, 10, 0.01)
#
# model.save(sc, "als-model")

# conf = SparkConf().setMaster("spark://162.105.88.93:7077").setAppName("Fisrt") \
#         .set("spark.num.executors", "1")\
#         .set("spark.executor.cores", "1")\
#         .set("spark.executor.memory", "2G")\
#
# sc=SparkContext(conf=conf)
#
# text=sc.textFile("hdfs://localhost:9000/data/ratings.csv")
# print(text.count())

def prepare_data(spark_context):
    # ------------1.读取评分数据并解析 -------------
    raw_user_data = spark_context.textFile("../data/ratings_new.csv")
    raw_user_data = raw_user_data.filter(lambda x: "movieId" not in x)

    raw_ratings = raw_user_data.map(lambda line: line.split("\t")[:3])
    ratings_rdd = raw_ratings.map(lambda x: Rating(int(x[0]), int(x[1]), float(x[2])))

    # ------------2.数据初步统计 ----------------
    num_ratings = ratings_rdd.count()
    num_users = ratings_rdd.map(lambda x: x[0]).distinct().count()
    num_movies = ratings_rdd.map(lambda x: x[1]).distinct().count()
    print("总共: ratings: " + str(num_ratings) + ", User: " + str(num_users) + ", Moive: " + str(num_movies))

    return ratings_rdd

def save_model(spark_context,model):
    try:
        model.save(spark_context, "../datas/als-model")
    except Exception:
        print ("保存模型出错")

if __name__ == "__main__":
    spark_context = SparkContext("local", "Test")
    # sc=SparkContext("spark://162.105.88.93:7077","Test")
    ratings_rdd=prepare_data(spark_context)
    model = ALS.train(ratings_rdd, 10, 10, 0.01)
    save_model(spark_context,model)


