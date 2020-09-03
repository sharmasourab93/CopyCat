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

The Django application is a clone of the Hackerrank Website with additional personalized features & a dashboard. 

As per the requirement, 

1. Each news item has the following field 
    - Url 
    - Hacker News ID/Url  
    - Posted On
    - Upvotes 
    - Comments

2. The application also enable a script in the background which extracts the news items and adds them in the database. It updates upvote & comment count if the news item exits. 
3. The application provides a SignUp and a Login Dashboard
4. The dashboard Index lists all the news items in reverse chronological order. 
5. A User is provided with the personalized feature to bookmark news items. 
6. A user also has the ability to read or delete a news item from this dashboard. 

___

 #### File Structure
 
            ├───CopyCat
            │   ├───CopyCat
            │	│	├─── __init__.py
            │	│	├─── asgi.py
            │	│	├─── settings.py
            │	│	├─── urls.py
            │   │   └─── wsgi.py
            │	│
            │   ├───logs
            │	│	└─── debugger.log
            │	│	
            │   └───mainapp
            │   │   ├─── migrations
            │	│	│	 ├─── 000*.py
            │   │   │    └─── __init__.py
            │	│	│
            │   │   ├─── static
            │   │   │    └─── images
            │	│	│		   ├─── background.png
            │	│	│		   └─── favicon.png 
            │	│	│
            │   │   ├───templates
            │   │   │   ├───mainapp
            │	│	│	│	 ├─── base.html
            │	│	│	│	 ├─── bookmarks.html
            │	│	│	│	 ├─── history.html
            │	│	│	│	 ├─── index.html
            │	│	│	│	 └─── profile.html
            │	│	│	│
            │   │   │   └───registration
            │	│	│			├─── base.html 
            │	│	│			├─── details_page.html
            │	│	│			├─── login.html
            │	│	│			├─── logout.html
            │	│	│			├─── password.html
            │	│	│			└─── signup.html
            │	│	│
            │   │   ├───tests
            │	│	│    ├─── __init__.py
            │	│	│	 ├─── test_forms.py
            │	│	│	 ├─── test_models.py
            │	│	│	 ├─── 
            │	│	│	 └─── test_views.py
            │	│	│
            │	│	│
            │   │   ├─── __init__.py 
            │   │   ├─── admin.py 
            │   │   ├─── apps.py
            │   │   ├─── forms.py 
            │   │   ├─── models.py  
            │   │   ├─── urls.py 
            │   │   ├─── views.py 
            │	│	└─── parser.py 
            │	│
            │	├─── __init__.py 
            │	└─── manage.py 
            │	
            │	
            └───venv
            

___
### Details On the Application 

The Django application can be classified as follows 
    1. Urls/Paths 
    2. Views 
    3. Models 
    4. Templates
    5. External Logic
 
 Any other if exists
 
#### Urls 
 The application provides paths for view functions
 On the Project Urls, the application is routed to the following: 
1. `admin`          For Super User/Administrator 

2. `accounts`       For Login Related
 
3. ``               For Everything starting with None,
        
        
 On the app urls, the applications is meant to route as follows:
  
1. Creating Users/Sign Up           `accounts/signup`
2. Login View                       `accounts/login`
3. Logout View                      `accounts/logout`
4. Password Change View             `accounts/password-change`
5. Fill User Details View           `filldetails/`
6. Index View With News View        `index/`
7. User's Profile View              `profile/<user>` where <user> is specific to the registered user.
8. Marked As Read/Read History      `marked-read/`
9. All Bookmarks View               `bookmarks/`
    
From the above url routes, more logical views are written for 
    - Adding Bookmarks
    - Removing Bookmarks
    - Marking a news item as read,
    - Deleting a news item from a user's profile. 
    
    
#### Models 
The following models are the relationship with database. The database used for the application is `MySQL`.

1. `NewsFeed` (News Feed Details)
2. `Profile` (User's Personal Details)
3. `Bookmarks` (To hold the user specific Bookmark)
4. `UserRead` (Model to mark user's Read History)
5. `UserDelete` (Removed Items for a user)


For authentication, default `User` model from the module `django.contrib.auth.models` is utilized. 


#### Forms 

Following are the forms made use of in the application: 

1. `LoginForm`   # Form intended to login 
2. `FillUpForm` # Form intended to Fill in User's personal details like Name, DOB, email


The django forms that are imported are the following: 

1. `PasswordChangeForm` 
2. `UserCreationForm`


#### Templates 

There are primarily two sets of templates designed to uplift the look and feel of the website. 
What remains common is the usage of `static` files loaded into base templates in the form of `background.png` and `favicon.png`.

From the following two template sets `mainapp`(name of the app) and `registration`. 
The former's templates have been designed to meet the UI effects after login, and later's before login. 

Both sets have a common base template `base.html` but are segregated in the respective folders. 


#### External Logic 

Under the app `mainapp`, a certain file by the name `parser.py` is made use of by the `index` view of our application. 

This `parser.py` is a beautifulsoup `bs4` based module to act as the parsing engine for the [HackerNews](https://news.ycombinator.com) website. 
This  module can be used/reused or extended across various examples. 


#### More...

The application makes use of the following features to improve the standards for the application 

1. `Logging`
    The logging feature has been enabled to improve the standards of the application and utilize native features with more efficiency. 

2. `Paginator` 
    Paginator is used to limit the index page's News Item count to `30`. So the items are segragated in a Page number fashion based on Paginator index. 

3. Unittest case
    Unittest cases have been included to improve the code quality of the application and also to serve as a standard refernce point. 
    
    
#### What is more to come on the application?
To experiment and explore more standard tools used across the industry, the following activities are being  taken up with regards to this application. 

 1. Deploying `CopyCat` Django Application with `Gunicorn` & `Nginx`
 2. Exploring the deployment on to a `Docker` Container with the addition of `MySQL` container using a `docker-compose.yml` 
 3. Extending with `Kubernetes`/`Minikube`.  

---

<!--### Schedule Undertaken to Complete This Sample Django Application 
The following schedule was under taken to complete the project in it's first phase. 

The objective of the first phase was to develop a working application and get it ready to deploy with `Gunicorn` & `Nginx`.
The below given are serial numbers followed by date and the topics covered/implemented on the respective day in a block of 3 hours. 

1.  `24/08/2020` - Skeleton, Architecture
2.  `25/08/2020` - Update On Login, Logout, Sign Up, Bookmark Skeleton
3.  `26/08/2020` - DB & Migrations
4.  `27/08/2020` - UI Base template for Mainapp & Registration
5.  `28/08/2020` - Parser & DB Insertion logic
6.  `30/08/2020` - Index Page Population Logic & Parser Table Updation
7.  `31/08/2020` - Action Buttons On Index page, Reverse Chronological Order
8.  `01/09/2020` - Bookmarks & Delete Items
9.  `02/09/2020` - Mark as Read, Segregating Read Items, Password Change
10. `03/09/2020` - Explore Logging, Limit Views to 30 On a page
11. `04/09/2020` - Write Test cases
 -->
 
 The second phase will include a timeline undertaken to alter, develop, deploy code to do more as explore in the section above. 
 
 
 ### Possible Improvement Ideas For `Copy Cat` Django Application
 
 1. A Profile Picture For the User 
 2. Password Reset Using Email 
 
 
 ### Resources & References
 1. [Django Docs](https://docs.djangoproject.com/en/3.1/)
 2. [StackOverflow](https://stackoverflow.com/)
 