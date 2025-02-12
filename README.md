# Website Content Scraper
Scraping the content of any available website in a minimum time, using Crawl4AI a powerfull crawl tool used for web crawling. You can get different kinds of output by its build-in functions. For more info about its output formates visit: https://crawl4ai.com/mkdocs/
# Why it is Better?
* Integration of Crawl4AI, a powerfull tool used of content scraping.
* Content fetching of dynamic websites.
* Celery implimentation for better controll of task also for parallel way.
* Significant modulization.
* Easy to understand.
# How to Use the Project?
* Make sure you have installed python on your system or install it from: https://www.python.org/
* Clone the repository.
* Make a vitual enviroment in project directory using command: python -m venv .enviroment_name
* Activate the enviroment by using command: .enviroment_name\Scripts\activate
* Install the requirements by using command: pip install -r req.txt
* Modify 'webs' (list of websites) under the application 'scraping_task' in the file 'task.py' at line 30
* Create superuser by using command: python manage.py createsuperuser
* Run the server by using command: python manage.py runserver
* Now go to: http://127.0.0.1:8000/admin
* Enter the username and password you just used during creating the superuser.
* Make a new task and run the task.
* Enjoy the power of crawl4AI
