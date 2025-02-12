import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import time
import chardet
import re
import mysql.connector
import asyncio
from datetime import datetime
from crawl4ai import AsyncWebCrawler
import os
import upload_to_drive
from asgiref.sync import sync_to_async
from mysql.connector import Error
import logging
import sys
import io
from django.db import connection, transaction, close_old_connections
from django.db.utils import OperationalError
import time





def get_web_list():
    try:
        webs = [[1, 'www.example.com', 'Example Web'], [2, 'www.example2.com', 'Example Web2']]
        return webs  # Convert QuerySet to a list
    except Exception as e:
        print(f'Error fetching weblist : {e}')
        return []


async def get_all_links(base_url):
    internal_links = []
    for attempt in range(2):
        try:
        # Create an instance of AsyncWebCrawler
            async with AsyncWebCrawler(verbose=False) as crawler:
            # Run the crawler on a URL
                result = await crawler.arun(url=base_url, fit_markdown = True)
                internal_links = result.links.get("internal", []) # adjust according to need i.e. use external to get external links
                return internal_links
        except Exception as e:
            time.sleep(2)
            print(f'Error: {e}')
    return internal_links       


async def get_link_content(url):
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler(verbose=False) as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url=url)
    if result.success:
        return result.html  # Complete HTML including headers, scripts, etc.
    else:
        return False




def save_text_to_single_file(memory_file, base_url, links, errored_links):
        pdf_links = []
        img_links = []
        other_links = []
        length = len(links)
        
        # adjust the allowed error number according to need & size of links
        if length > 10 and length < 21:
            count = 10
        elif length > 19 and length < 41:
            count = 20
        elif length > 40:
            count = 30
        else:
            count = 7
        # print(length)
        for i, link in enumerate(links, start=1):
            url = link["href"]
            if 'pdf' in url:
                        pdf_links.append(url)
                        # print('pdf')
                        continue
            if 'img' in url or 'png' in url or 'jpg' in url:
                        img_links.append(url)
                        # print('img')
                        continue
            if count == 0 :
                # print(f"Stoped due to too many faild requests")
                errored_links.append(base_url)
                return other_links, memory_file
            for attempt in range(2):  # Retry logic
                try:
                    # fetching site content  
                    html_content = asyncio.run(get_link_content(url))
                    if html_content == False:
                        print(f"Failed to fetch {url}")
                        count = count -1
                        continue
                    soup = BeautifulSoup(html_content, "html.parser")
                    text_content = soup.get_text()

                    # Write the text content to the file
                    memory_file.write(f"\n\n--- Page {i}: {url} ---\n\n")
                    memory_file.write("\n" + "-" * 80 + "\n")
                    memory_file.write(text_content.strip())
                    print(f"Added text content from page {i}")
                    time.sleep(2)
                    break

                except requests.exceptions.RequestException as e:
                    print(f"Retrying ({attempt + 1}/2) for link {link}: {e}")
                    count = count -1
                    time.sleep(2)  # Wait before retrying
                
                else:
                    # print(f"Skipping link: {url}")
                    break
        if len(pdf_links)>0:
            other_links.append(pdf_links)

        if len(img_links)>0:
            other_links.append(img_links)
        return other_links, memory_file



def clean_file(input_file, output_file):
    try:
        data = input_file.getvalue()
        # Remove any empty lines or lines containing only spaces
        content = '\n'.join([line.strip() for line in data.splitlines() if line.strip()])

        # Add exactly two empty lines before each "Page:" occurrence
        content = re.sub(r'(?=\n?)(?=Page:)', '\n\n', content)  # Insert two new lines before 'Page:'

        output_file.write(content)

        return output_file

    except Exception as e:
            print(f'Error in cleaning file : {e}')
            return input_file

def check_similarity_in_file(status_info, file, base_url, web_name, other_links, threshold=80):
    try:
        file_content = file.getvalue()
        content_len = len(file_content)
        if content_len>200: 
            try:              
                content = file_content.lower()  # Read and convert content to lowercase for case-insensitive matching
                web_detail = f"Website: {web_name}\n Base URL: {base_url}\n"
                # Split the content into words or sentences
                lines = content.split('\n')
        
                # Check the similarity between the web name and each word or phrase in the content
                for line in lines:
                    try:
                        similarity = fuzz.partial_ratio(web_name.lower(), line.strip())  # Compute similarity percentage
                        
                        if similarity >= threshold:
                            # if the site name is same as required
                            file.seek(0)
                            file.write(web_detail)
                            details= f''' The visited website was a true website, because the provided name has a similarity 
                            with the visted one'''
                            try:                                                  
                                details = '''Scraping was successful with true website and the file also uploaded to drive successfully'''
                                # do any thing you want i.e. save the content in file and then to system, database, server or other kind of storage
                                with open('folder_name/file_path', "w", encoding="utf-8") as file:
                                    file.write(web_detail + file_content)
                                time.sleep(2)
                                return                                                 
                            except Exception as e:                               
                                print(f'Error : {e}')
                                return
                    except Exception as e:
                        print(f'Error : {e}')
                        return 
                print('Not Similer')
                return   
            except Exception as e: 
                print(f'Error : {e}')
                return 

    except Exception as e:
            print(f'Error : {e}')
            return 

def main_task_chunk(chunk_sized_list, errored_links, count, chunk):

    # recursion depth limit set to 2000, adjust to normal 1000 or higher according to need 
    sys.setrecursionlimit(2000) 
    for web in chunk_sized_list:
        try: 
            # build-in memory file to handle content instead of making on system's permanent storage 
            memory_file = io.StringIO()
            count = count - 1
            time.sleep(1)
            web_id = web[0]
            base_url = web[1]
            web_name = web[2]
            
            if "/" in web_name or "|" in web_name:
                web_name = web_name.replace("/", "").replace("|", "")
          
            # extract Base url and ensure the base url is not a social website.
            if 'www.facebook.com' not in base_url and 'www.instagram.com' not in base_url and 'www.x.com' not in base_url and 'www.youtube.com' not in base_url:
                parsed_url = urlparse(base_url)  # Parse the URL
                base_url =  f"{parsed_url.scheme}://{parsed_url.netloc}"          
            print(f'Working on: {web_name} ....')
            if base_url in errored_links:
                continue
            
            # get web's internal/external links
            links = asyncio.run(get_all_links(base_url)) 
            print(f'{len(links)} internal links found...')
            if(len(links)<1):
                url = {'href': base_url, 'text': 'home', 'title': ''}
                links = [url]

            print(f'Fetching site content...')
            other_links, memory_file  = save_text_to_single_file(memory_file, base_url, links, errored_links)
            if len(other_links)<1:
                flattened_list = 'None'
            else:
                try:
                    flattened_list = [item for sublist in other_links for item in sublist]
                    flattened_list = ','.join(flattened_list)
                except:
                    flattened_list = 'None'

            cleaned_memory_file = io.StringIO()
            output_file = clean_file(memory_file, cleaned_memory_file)
            check_similarity_in_file(output_file, base_url, web_name, flattened_list)
            
            try:
                del memory_file
                del cleaned_memory_file
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)


def run_task(start_index):
    try:
        errored_links = []
        webs_list = get_web_list(start_index)
        length_of_web_list = len(webs_list)
        chunks_count = length_of_web_list // 100 #assuming the length of weblist is a big number, spliting in chunks of 100
        i = 0
        while i<chunks_count:      
            try:
                start = i*100
                i = i + 1
                end = i*100
                main_task_chunk(webs_list[start:end], errored_links, 100, i )
            except Exception as e:
                print(f'Error : {e}')   

    except Exception as e:
            print(f'Error : {e}')
