# Website Content Scraper
Scrape the content of any publicly available website in minimal time using Crawl4AI, a powerful crawling tool for web scraping. This tool enables various output formats through built-in functions.
For more info about its output formates visit: https://crawl4ai.com/mkdocs/
## Why it is Better?
* Integration of Crawl4AI – A powerful tool for content scraping.
* Supports dynamic websites – Fetch content even from JavaScript-rendered pages.
* Celery implementation – Enables better task control and parallel execution.
* Modularized structure – Easy to extend and modify.
* User-friendly – Simple setup and easy to understand.
## How to Use the Project?
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
