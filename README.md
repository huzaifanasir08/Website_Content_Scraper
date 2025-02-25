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
### 1. Prerequisites
Ensure Python is installed on your system. If not, download it from https://www.python.org/
### 2. Installation Steps
  #### 1. Clone the repository:
```python
git clone https://github.com/huzaifanasir08/Website_Content_Scraper.git
cd Website_Content_Scraper
```
  #### 2. Create a virtual environment:
```python
python -m venv .venv
```
  #### 3. Activate the virtual environment:
* On Windows:
```python
.venv\Scripts\activate
```
* On macOS/Linux::
```python
source .venv/bin/activate
```
  #### 4. Install dependencies:
```python
pip install -r requirements.txt
```
### 3. Configuration
Modify the list of websites in the scraping_task/task.py file at line 30, under the webs variable.

### 4. Running the Project
  #### 1. Create a superuser:
  ```python
python manage.py createsuperuser
```
#### 2. Start the Django server:
  ```python
python manage.py runserver
```
#### 3. Open your browser and go to:
  ```python
http://127.0.0.1:8000/admin
```
#### 4. Log in using the credentials created in step 1.
#### 5. Create and run a new scraping task.

#### Enjoy the power of Crawl4AI! 🚀
