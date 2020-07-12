# CopyCat - A Personalized News Interface/Clone

A Clone of the HackerNews website which keeps tab of all the latest news coming in along with a personalized experience.

This is a sample project to explore: 
   
        - Building a scalable Web Application using Django
        - Exploring Django & It's Integration with Templates & Models
        - Integrating Django with MySQL 
        - Writing Unittests for Django Application
        - Deploying Django Application With Gunicorn 
        - Extending the application deployement with Nginx
        - Using Docker Container 
        - Using Kubernetes/Minikube


Idea is to have this project as a base reference for all Django projects.

### Problem Statement 
[HackerNews](https://news.ycombinator.com/) is very popular website among developers for latest news and projects. However sorting of the items is done via their own algorithms and we want to build a clone which keeps getting the top 90 articles and shows them in reverse chronological order. 

#### Requirements
Each news item will have the following fields: 
- Url
- Hacker news url
- Posted on
- Upvotes
- Comments
      
1. A script which crawls the first three pages, extracts the news items and adds in the database. If the news item already exists, it updates the upvote and comment counts.
2. A user can signup or login to the dashboard.
3. A dashboard where all news items are listed in reverse chronological order.
4. A user can bookmark an item in the list.
5. A user can mark a news item as read or delete it. Deleted items are not shown in his/her panel but are not deleted from the database.


___

## Solution 

**Tech Stack**: Python3 + Django3 + MySQL

 #### File Structure
 
 
 