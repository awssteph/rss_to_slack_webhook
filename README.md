# rss_to_slack_webhook

Python tool to read an RSS feed and selectively publish articles, based on keywords, to Slack via Webhook

This tool checks the AWS 'What's New' RSS feed every minute for announcements related to cost optimization. 

Code adapted from: https://timothybramlett.com/recieving_notifications_of_rss_feeds_matching_keywords_with_Python.html

Key word filter can be updated for your needs. 

Run this script with a cronjob every minute by adding the following to your crontab:

```
* * * * * /usr/bin/python3 /home/ec2-user/rss_webhook/rss_webhook.py
```
