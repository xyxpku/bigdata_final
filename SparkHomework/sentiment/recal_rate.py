#!usr/bin/env python
# -*- coding:utf8 -*-
# @TIME   :2020-12-02 13:37
# @Author :Xu Yongxin
# @File   :recal_rate.py

from utils.data_utils import get_csv_list,write_csv_new
weight=0.8


if __name__ == "__main__":
    rating_list=get_csv_list("../ml-latest-small/ratings.csv")
    sentiment_list=get_csv_list("../data/movie_score.csv")
    score_dict={}
    for sentiment in sentiment_list[1:]:
        score_dict[sentiment[0]]=float(sentiment[1])
    # print(score_dict)
    # print(rating_list)

    write_list=[]
    write_list.append(rating_list[0])

    for rating in rating_list[1:]:
        #new_row_list=[]
        userId=rating[0]
        movieId=rating[1]
        rate_score=float(rating[2])
        time=rating[3]
        if movieId in list(score_dict.keys()):
            sentiment_score=score_dict[movieId]
            rate_score=weight*rate_score+(1-weight)*sentiment_score
            if rate_score<0.5:
                rate_score=0.5
            elif rate_score>5.0:
                rate_score=5.0

        new_row_list=[userId,movieId,rate_score,time]
        write_list.append(new_row_list)

    write_csv_new("../data/ratings_new.csv",write_list)



