import json
import os
import scrapy
from scrapy.crawler import CrawlerProcess
import random
import string
from scraphtml import *
import requests
from scrapy.http import HtmlResponse
from dotenv import load_dotenv

load_dotenv()


EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
JOBS = ["~016ba20b6754868b82", "~016e9ab519a6d0bf5c", "~01efe7eeb3412b6261"]


class UpworkCrawler(scrapy.Spider):
    name = "upwork_crawler"
    start_urls = ['https://www.upwork.com/ab/account-security/login']
    csrf_token = None
    iovation = ''.join(random.choice(string.ascii_letters) for _ in range(120))
    allowed_domains = ["*.upwork.com", "upwork.com", "www.upwork.com"]
    custom_settings = {
        "HTTPERROR_ALLOWED_CODES": [403, 410, 401], 
        "LOG_ENABLED": False,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0"
    }

    def start_requests(self):
        if os.path.exists("mydata.pickle"):
            qookie = load_qookie("mydata.pickle")
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Alt-Used": "www.upwork.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "If-None-Match": 'W/"56232-kJh7vneWraHDwtkby+xKjpRIM6g"',
                "TE": "trailers"
            }
            header.update(qookie)
            for job in JOBS:
                response = requests.get(url=f"https://www.upwork.com/jobs/{job}", headers=header, allow_redirects=False)
                if response.status_code == 403 or response.status_code == 302:
                    os.remove("mydata.pickle")
                    header = {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Alt-Used": "www.upwork.com",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                        "TE": "trailers"
                    }
                    yield scrapy.Request(url="https://www.upwork.com/ab/account-security/login", callback=self.login_user, headers=header)
                else:
                    response = HtmlResponse(url="", body=response.text, encoding='utf-8')
                    self.process_result(response, job)
            print("-"*150)

        else:
            header = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Alt-Used": "www.upwork.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "TE": "trailers"
            }
            yield scrapy.Request(url="https://www.upwork.com/ab/account-security/login", callback=self.login_user, headers=header)


    def login_user(self, response):
        for k, v in response.headers.items():
            if k.decode('utf-8') == 'Set-Cookie':
                for xsrf in v:
                    if str(xsrf.decode('utf-8')).startswith('XSRF-TOKEN'):
                        self.csrf_token = xsrf.decode('utf-8').split(';')[0].split('=')[1]
                        break
        hdr = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.upwork.com/ab/account-security/login",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json",
            "X-Odesk-Csrf-Token": self.csrf_token,
            "Origin": "https://www.upwork.com",
            "Alt-Used": "www.upwork.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        data = {
            "login": {
                "mode": "username",
                "iovation": self.iovation,
                "username": EMAIL,
                "elapsedTime": 1809726
            }
        }
        yield scrapy.Request(method="POST", url="https://www.upwork.com/ab/account-security/login", headers=hdr, body=json.dumps(data), callback=self.login_pass_1)



    def login_pass_1(self, response):
        hdr = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.upwork.com/ab/account-security/login",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json",
            "X-Odesk-Csrf-Token": self.csrf_token,
            "Origin": "https://www.upwork.com",
            "Alt-Used": "www.upwork.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        data = {
            "login": {
                "mode": "password",
                "iovation": self.iovation,
                "username": EMAIL,
                "elapsedTime": 3223388,
                "password": PASSWORD
            }
        }
        yield scrapy.Request(method="POST", url="https://www.upwork.com/ab/account-security/login", headers=hdr, body=json.dumps(data), callback=self.login_pass_2)


    def login_pass_2(self, response):
        dt = json.loads(response.body)
        hdr = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.upwork.com/ab/account-security/login",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json",
            "X-Odesk-Csrf-Token": self.csrf_token,
            "Origin": "https://www.upwork.com",
            "Alt-Used": "www.upwork.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        payload = {
            "login": {
                "mode": "password",
                "iovation": self.iovation,
                "username": EMAIL,
                "elapsedTime": 32848,
                "password": PASSWORD,
                "securityCheckCertificate": dt["securityCheckCertificate"],
                "authToken": dt["authToken"]
            }
        }
        yield scrapy.Request(method="POST", url="https://www.upwork.com/ab/account-security/login", headers=hdr, body=json.dumps(payload), callback=self.attach_device_1)


    def attach_device_1(self, response):
        header = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.upwork.com/nx/find-work/",
            "x-odesk-user-agent": "oDesk LM",
            "x-requested-with": "XMLHttpRequest",
            "Alt-Used": "www.upwork.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }
        yield scrapy.Request(url="https://www.upwork.com/ab/find-work/api/nuxt/globals?deviceType=desktop", callback=self.attach_device_2, headers=header)


    def attach_device_2(self, response):
        header = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.upwork.com/nx/find-work/",
            "x-odesk-user-agent": "oDesk LM",
            "x-requested-with": "XMLHttpRequest",
            "Alt-Used": "www.upwork.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }
        yield scrapy.Request(url="https://www.upwork.com/api/v3/geo/ip/city", callback=self.find_job, headers=header)


    def find_job(self, response):
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Alt-Used": "www.upwork.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "If-None-Match": 'W/"56232-kJh7vneWraHDwtkby+xKjpRIM6g"',
            "TE": "trailers"
        }
        for job in JOBS:
            yield scrapy.Request(url=f"https://www.upwork.com/jobs/{job}", callback=self.result, headers=header)



    def result(self, response):
        save_qookie(response, 'mydata.pickle')
        self.process_result(response, response.url)


    def process_result(self, response, job):
        left_side = response.css('.cfe-ui-job-details-content')
        right_side= response.css('.job-details-sidebar')

        title = left_side.css('.up-card-header > h1 ::text').get().strip()
        description = left_side.css('.up-card-section')[1]
        description = description.css('div > div ::text').get().strip()

        job_features_list = get_job_features(left_side)
        skills_expertise, section_id = get_skills_expertise(left_side)
        activities = get_job_activities(left_side, section_id)
        titles_history = get_client_history(response)
        about_client = get_client_about(right_side, response)

        print("-"*50 + f" Scraping started for Job ID {job} " + "-"*50)
        print({
            "title": " ".join(title.split()),
            "job_description": " ".join(description.split()),
            "job_features": job_features_list,
            "skills_expertise": skills_expertise,
            "activities": activities,
            "client_histories": titles_history,
            "about_client": about_client
        })


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(UpworkCrawler)
    process.start()