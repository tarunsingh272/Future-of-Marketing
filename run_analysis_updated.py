from __future__ import print_function
import sys
import re
from operator import add
import pandas as pd
from pyspark.sql.types import StructField, StructType, StringType
from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql import SQLContext
import json
import boto
import boto3
from boto.s3.key import Key
import boto.s3.connection
from pyspark.sql import SparkSession, SQLContext
from pyspark import SparkContext, SparkConf
from pyspark.ml.feature import MinMaxScaler
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql.functions import *
import credentials
from pyspark.sql.types import IntegerType


#aws keys
aws_key_id = 'XXXXXXXXXXXXXXXXXXXXXXXX'
aws_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'

#day = date | awk '{print $3}'
#hour = date | awk '{print $4}' | awk -F ":" '{print $1}'

def main():
    sc=SparkContext()
    sqlContext = SQLContext(sc)
    bucket = "trends-project-team2"
    prefix = "2018/12/*/*/*/" #These parameters need to be changed dynamically depending on date and time. Use crontab to autocreate these values
    filename = "s3a://{}/photooftheday/{}".format(bucket, prefix)
    print(filename)

    rdd = sqlContext.read.json(filename)


    data_rm_na = rdd.filter(rdd["status_id"]!='None')
    features_of_interest = ('rt_status_user_followers_count','rt_status_user_friends_count','rt_status_user_statuses_count','rt_status_retweet_count','rt_status_user_listed_count','rt_status_user_id','rt_status_created_at','status_created_at','rt_status_user_name','rt_status_user_favourites_count','status_id', 'rt_status_text', 'rt_status_user_location', 'sentiment')
    df_reduce= data_rm_na.select(*features_of_interest)
    df_reduce = df_reduce.withColumn("rt_status_user_followers_count", df_reduce.rt_status_user_followers_count.cast(IntegerType()))
    df_reduce = df_reduce.withColumn("rt_status_user_friends_count", df_reduce.rt_status_user_friends_count.cast(IntegerType()))
    df_reduce = df_reduce.withColumn("rt_status_user_statuses_count", df_reduce.rt_status_user_statuses_count.cast(IntegerType()))
    df_reduce = df_reduce.withColumn("rt_status_retweet_count", df_reduce.rt_status_retweet_count.cast(IntegerType()))
    df_reduce = df_reduce.withColumn("rt_status_user_listed_count", df_reduce.rt_status_user_listed_count.cast(IntegerType()))
    df_reduce = df_reduce.withColumn("rt_status_user_favourites_count", df_reduce.rt_status_user_favourites_count.cast(IntegerType()))
    df_reduce = df_reduce.withColumn("sentiment", df_reduce["sentiment"].cast(IntegerType()))


    url_ = "jdbc:mysql://trends2018.cfpjuvl8yy9t.us-east-2.rds.amazonaws.com:3306/innodb"
    table_name_ = "trends1234"
    mode_ = "append"

    df_reduce.write.format("jdbc").option("url", url_)\
    .option("dbtable", table_name_)\
    .option("driver", "com.mysql.jdbc.Driver")\
    .option("user", "trends")\
    .option("password", "trends1234")\
    .mode(mode_)\
    .save()



if __name__ == "__main__":
    main()
