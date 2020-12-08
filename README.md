# 代码说明
1. **bigdata_homework：集群搭建代码**
   1. bigdata_homework/spark_master/Dockerfile:集群搭建的Dockerfile
   2. bigdata_homework/spark_master/*：集群搭建所需要的其他文件和脚本
   3. docker-compose.yml：集群搭建的docker-compose文件，包括一个master和两个worker；可动态调整
   4. spark-homework-xyx.tar：已经保存的镜像，可直接通过docker load命令加载，不需要重新build镜像
   
2. **SparkHomework：数据预处理&模型训练代码**
   1. SparkHomework/imdb_crawler/catch_imdb.py：爬取IMDB电影评论代码
   2. SparkHomework/sentiment/*：对评论进行情感分析以及重新计算得分代码
   3. SparkHomework/spark/*：模型训练以及预测代码
   4. SparkHomework/utils/*：数据预处理代码
   
3. **robot_communication-movie：Django前端可视化代码**
   1. robot_communication-movie/communication1/data/als_model：已经训练好的模型
   2. robot_communication-movie/communication1/db.sqlite3：数据库
   3. robot_communication-movie/robot_communication/models.py：数据库表schema
   4. robot_communication-movie/robot_communication/views.py：后端逻辑
   5. robot_communication-movie/static/*：静态内容，包括css和图片
   6. robot_communication-movie/template/*：前端可视化界面
   
