# The future of marketing: Beat the competition with realtime analytics using AWS Kinesis, Spark and Amazon RDS
### Trends Marketplace Fall MSBA'19 - Team 2

## Project overview and objective
Due to social media outreach, identifying and leveraging social media influencers for business development has become crucial aspect of developing a successful marketing strategy for organisations. Below are some of the facts why influencer reach is of high importance:

![Influencer Importance](https://github.umn.edu/singh899/trends-project-team2/blob/master/Diagrams/Inf.PNG)

One of such popular social media platforms is twitter and various factors define how an influencer can be spotted:
1. Retweets: The number of retweets a person's tweet gets
2. Favourites: Number of accounts that have account under consideration as their favourite
3. Followers: Number of followers a person has
4. Depth: If a tweet is retweeted by another influencer then it is likeliy that the followers of that influencer will retweet the tweet. Hence it creates a second branch of retweets for the maub influencer which can create further layers of retweets. Depth signifies how farther is the reach of such non-primary retweets.

Our project aims to:
1. Understand what twitter users are talking about 
2. Important component of a marketing campaign
3. Identify influencer networks, leverage them for marketing
4. Optimize budget allocation in real-time using influencer efficiency, geographic penetration, etc.

## Architecture details

An iterative process flow to continually stream, process and generate insights has been implemented to gain information at the earliest:
![Methodology](https://github.umn.edu/singh899/trends-project-team2/blob/master/Diagrams/process.PNG)

The project pipeline consists of four main components. An amazon EMR instance is used to run the streaming script constantly while the data is sent to S3 using Amazon Kinesis Firehose. The data is batch processed and moved to Amazon RDS database using Spark and this dataset is further used to calculate influencer metric and build insightful visualizations in Tableau. Below is the detailed description of each of the component in the pipeline from streaming live data from twitter till storage and visualization.

![Project Architecture](https://github.umn.edu/singh899/trends-project-team2/blob/master/Diagrams/Arch2.PNG)

1. **Streaming Data Source:** The data collection began by implementing the streaming Twitter API using Python. We also implemented the TextBlob to understand and analyze the sentiment of the data being scraped. The script constantly ran on the cloud on an Amazon EMR instance.

EMR Configuration

![Configuration](https://github.umn.edu/singh899/trends-project-team2/blob/master/Diagrams/emr_config.PNG)

2. **Streaming Pipeline:** The streaming data was sent to Amazon S3, for convenient data storage using Amazon Kinesis Firehose. Amazon Kinesis Firehose provided an easy way to send streaming data into Amazon Web Services (AWS) to enable near real-time analytics with existing business tools.
3. **Data Storage and Processing:** The data stored on S3 was then batch processed using Apache Spark to ensure a scalable and reliable product for the clients of TwitterTalker. We used Spark to implement the majority of our analysis, e.g. calculate the influence score, etc. The data was processed every 15 minutes.
4. **Database:** The final output from our analysis in Spark was sent to Amazon RDS as a SQL table and updated every 15 minutes as mentioned earlier. The Python Flask App called the database to display the real time data to the client interface.

## Code walkthrough
Below are the details of key code components and their utility:
1. **create_aws_pipeline:** This python code is used to create Kinesis firehose pipeline based on the search term or tag we entered using boto3 library.
2. **data_producer:** This python code reads streaming data from Twitter API using Tweepy and also uses Textblob for the sentiment analysis and then creates the Kinesis Firehose pipeline to consumer data and store it in S3. The data is captured every 300 seconds or once the data reaches 5MB size limit, whichever reaches first and then dumped to S3 bucket.

Sample Output
```
{"rt_status_user_name": "Neil", "rt_status_user_friends_count": "140", "rt_status_created_at": "Sun Dec 09 21:20:06 +0000 2018", "rt_status_user_id": "1062071811066732544", "sentiment": "None", "status_id": "1071889854873657344", "rt_status_text": "A rare half hour zipping the drone about this evening before the rain kicked in again. #photooftheday #ThePhotoHour https://t.co/qGKP1lgepy", "rt_status_favorited": "False", "rt_status_retweeted": false, "rt_status_user_favourites_count": "354", "rt_status_user_screen_name": "MozMoz4000", "rt_status_user_profile_image": "http://pbs.twimg.com/profile_images/1062081627352907778/BoSB7NE5_normal.jpg", "status_created_at": "Sun Dec 09 22:10:30 +0000 2018", "rt_status_id": "1071877168978751488", "rt_status_user_statuses_count": "118", "searched_names": "photooftheday", "rt_status_user_followers_count": "68", "rt_status_favorite_count": "1", "rt_status_retweet_count": "1", "rt_status_user_location": "North West, England", "rt_status_user_listed_count": "0"}
```

3. **download_unzip_mysql_driver:** This shell script downloads and unzips the required MySQL driver. This driver was required to connect to mysql hosted on AWS RDS.
4. **run_analysis_updated:** This code moves json data from S3 and stores it in a database on RDS by processing it and taking the relevant columns. It collects various columns such as number of followers, number of friends, total number of tweets and retweets and number of favourites. This data is then appended to a table in RDS with specified paramteres. We can also do feature engineering and model fitting steps here to further enhance our solution.
5. **Execute code:** Run the below command to execute run analysis code. We can aslo schedule the code in a crontab file and run every hour or every day depending on our needs

```
spark-submit --jars ~/mysql-connector-java-5.1.42/mysql-connector-java-5.1.42-bin.jar run_analysis_updated.py
```

6. **delete_kinesis_pipeline:** This snippet drops the kinesis pipeline created in the first step


## Final Dashboard
https://public.tableau.com/profile/sidd.malik#!/vizhome/TopTwitter/Dashboard2

## References
1. https://nycdatascience.com/blog/student-works/web-scraping/build-near-real-time-twitter-streaming-analytical-pipeline-scratch-using-spark-aws/
2. https://nycdatascience.com/blog/student-works/creating-real-time-streaming-platform-identify-top-influencers-twitter/
3. https://github.com/casunlight/fusion_capstone_project
4. https://docs.aws.amazon.com/kinesis/index.html#lang/en_us
5. https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
6. https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
7. https://docs.aws.amazon.com/cli/index.html#lang/en_us


**********************************************************************************************************************************
