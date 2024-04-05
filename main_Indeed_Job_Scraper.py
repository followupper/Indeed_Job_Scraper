import os
import csv
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
# import resume
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class INDEED:
    def __init__(self, indeed_target_urls) -> None:
        
        self.json_file_path = os.path.join(os.getcwd(), 'indeed_jobs.json')

        # Headers for the request 
        self.headers = {
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
        self.reference_url_dict = indeed_target_urls  
        self.base_url = 'https://www.indeed.com'


        # login(self):

        # Create a new instance of the Firefox driver
        self.driver = webdriver.Firefox()
        # self.driver.get(target_url)
        
        # '''SETUP TOR BROWSER (NOT WORKING ON INDEED THOUGH)''' 
        # # Set the location of the Tor browser
        # tor_path = '/Applications/Tor Browser.app/Contents/MacOS/firefox'

        # # Set the profile to use with Tor
        # profile = webdriver.FirefoxProfile()

        # # Set the network proxy to use Tor
        # profile.set_preference('network.proxy.type', 1)
        # profile.set_preference('network.proxy.socks', '127.0.0.1')
        # profile.set_preference('network.proxy.socks_port', 9150)
        # profile.set_preference("network.proxy.socks_remote_dns", False)

        # # Set the options to use with Tor
        # options = Options()
        # options.binary_location = tor_path
        # options.profile = profile  # Set the profile in options

        # # Create the WebDriver with the Tor options
        # self.driver = webdriver.Firefox(options=options)
        # input("is tor browser connected? press enter to continue...")




        #<<<<<<<<get rid of cookies
        # cookie_button = self.driver.find_element( By.XPATH , "//*[text()='Agree and Proceed']")
        # cookie_button = self.driver.find_element(By.XPATH, "//*[text()='Required Only']")
        # cookie_button.click()
        #for now accept cookies manually
        time.sleep(5)  # 4
    # define destructor
    def __del__(self):
        self.driver.quit()

    #TODO not sure if this is the right way to check if the page is a CAPTCHA page
    def check_captcha(self, target_url):
        counter = 0
        try:
            WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Widget containing a Cloudflare security challenge']")))
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.ctp-checkbox-label"))).click()
            print("Captcha solved")
            time.sleep(random.randint(5, 10))
            # self.driver.switch_to.default_content()
            return True
        except Exception as e:
            print("Error: ", e)
            print("No CAPTCHA found.")
            return False
        
        #     indeed_captcha_title = self.driver.find_element(By.ID, 'challenge-running')
        #     if "you are human" in indeed_captcha_title.text:
        #         # self.driver.refresh()
        #         # Check if the page is a CAPTCHA page
        #         captcha_element = self.driver.find_element(By.CLASS_NAME, 'ctp-checkbox-label')
        #         if captcha_element:
        #             # click the checkbox
        #             checkbox = captcha_element.click()
        #             # wait for 5 seconds
        #             time.sleep(4)
        #             self.driver.get(target_url)
        #             return True
        #         else:   
        #             input("Please solve the CAPTCHA and press Enter to continue...")
            
        # except Exception as e:
        #     print("Error: ", e)
        #     print("No CAPTCHA found.")
        #     # input("Please solve the CAPTCHA and press Enter to continue...")
        #     return True
        # return True

    def get_jobs(self, all_jobs, skill, location='Germany', no_of_pages=5):
        recent_jobs = {}
        # find latest internall job_id
        #TODO we general approach to store jobs for each candidate, ID must be unique for each job, platform and candidate
        if '0' in all_jobs: #TODO check if this is the right way to check if the dictionary is empty
            self.latest_job_id = max([int(job_id) for job_id in all_jobs.keys()])+1
        else:
            self.latest_job_id = 0
        self.current_job = {self.latest_job_id: {}}  # create a new job

        # Creating the Main Directory
        main_dir = os.getcwd() + '\\'
        if not os.path.exists(main_dir):
            os.mkdir(main_dir)
            print('Base Directory Created Successfully.')


        # Name of the CSV File
        # file_name = skill.title() + '_' + place.title() + '_Jobs.csv'
        # Path of the CSV File
        # file_path = main_dir + file_name

        # Writing to the CSV File
        # with open(file_path, mode='w') as file:
        #     writer = csv.writer(file, delimiter=',', lineterminator='\n')
        #     # Adding the Column Names to the CSV File
        #     writer.writerow(
        #         ['JOB_NAME', 'COMPANY', 'LOCATION', 'POSTED', 'APPLY_LINK'])

        # Requesting and getting the webpage using requests
        print(f'\nScraping in progress...\n')
        for page in range(no_of_pages):
            try:
                self.base_url = self.reference_url_dict[location]
                url = self.base_url + "jobs?q=" + skill + \
                    '&l=' + location + '&start=' + str(page * 10)
                response = requests.get(url, headers=self.headers)
                if response.status_code != 200:
                    print('Failed to load page', page)
                    print('Status Code:', response.status_code)
                    print("attempting to load via selenium")
                    self.driver.get(url)
                    time.sleep(random.randint(5, 10))
                    indeed.check_captcha(self.base_url)

                    html = self.driver.page_source
                else:
                    html = response.text

                # Scrapping the Web
                soup = BeautifulSoup(html, 'lxml')
                search_result = soup.find('div', attrs={'id': 'mosaic-provider-jobcards'})

                # html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                search_result = soup.find('div', attrs={'id': 'mosaic-provider-jobcards'})

                #css-5lfssm eu4oa1w0
                #css-5lfssm eu4oa1w0
                self.current_job_id = self.latest_job_id
                
                mosaics = search_result.find_all('li', class_='css-5lfssm eu4oa1w0')
            except Exception as e:
                print("Error: ", e)
                print("error in getting info:" + "mosaics", self.base_url)
                continue
            for job_ad in mosaics:
                try:
                    self.current_job[self.current_job_id] = {}
                    self.current_job[self.current_job_id]['job_id'] = self.current_job_id
                    self.current_job[self.current_job_id]['date_added'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                    #job_title = job_ad.select('[class*="jcs-JobTitle"]')
                    job_title = job_ad.find('a', class_='[class*="jcs-JobTitle"]')
                    job_title = job_ad.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0')
                    self.current_job[self.current_job_id]['job_title'] = job_title.text



                    job_link = self.base_url + job_title.get('href')
                    self.current_job[self.current_job_id]['job_link'] = job_link
                    print(job_link)
                    # check if a job with this link already in the dataset
                    job_links = [job.get('job_link') for job in all_jobs.values() if job.get('job_link') is not None]
                    if job_link in job_links:
                        print(f"'{job_title.text}' exists already in the dictionary.", job_link)
                        continue

                    print("<<<<<<<<<<<>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>")
                    print(job_ad.text)
                    self.current_job[self.current_job_id]['job_summary'] = job_ad.text

                    #``` get job details from the job_link```
                    response = requests.get(job_link, headers=self.headers)
                    if response.status_code != 200:
                        print('Failed to load page', page)
                        print('Status Code:', response.status_code)
                        print("attempting to load via selenium")
                        self.driver.get(job_link)
                        time.sleep(random.randint(5, 15))
                        html = self.driver.page_source
                    else:
                        html = response.text
                    
                    soup_job = BeautifulSoup(html, 'html.parser')
                    if soup_job:
                        visible_text = soup_job.get_text(strip=True)
                        # print(visible_text)

                    # COMPANY NAME
                    try:
                        company_name = soup_job.find('div', attrs={'data-testid': 'inlineHeader-companyName'}).getText()
                        # company_indeed_link = soup_job.find('div', attrs={'data-testid': 'inlineHeader-companyName'}).get('href')
                        # Find the div element
                        div_element = soup_job.find('div', attrs={'data-testid': 'inlineHeader-companyName'})

                        # Find all 'a' tags in the div element
                        subelements = div_element.find_all('a')

                        links = []
                        for subelement in subelements:
                            link = subelement.get('href')
                            if link:  # check if link is not None
                                links.append(link)
                        company_indeed_link = links[0]        
                        self.current_job[self.current_job_id]['company_indeed_link'] = company_indeed_link
                        print("company_name:  " + company_name)
                        self.current_job[self.current_job_id]['company'] = company_name
                    except Exception as e:
                        print("Error: ", e)
                        print("error in getting info:" + "company name")
                    

                    #LOCATION
                    try:
                        location = soup_job.find('div', attrs={'data-testid': 'inlineHeader-companyLocation'}).getText()
                        print("company location:  " + location)
                        self.current_job[self.current_job_id]['location'] = location
                    except Exception as e:
                        print("Error: ", e)
                        print("error in getting info:" + "company location")
                    
                    # check if already in the dataset
                    # Check if 'string_value' is equal to the value of any 'job_title' in the dictionary
                    if any(job.get('job_title') == self.current_job[self.current_job_id]['job_title'] for job in all_jobs.values()):
                        if any(job.get('company') == self.current_job[self.current_job_id]['company'] for job in all_jobs.values()):
                            if any(job.get('location') == self.current_job[self.current_job_id]['location'] for job in all_jobs.values()):
                                print(f"'{job_title.text}' from {self.current_job[self.current_job_id]['company']} in {self.current_job[self.current_job_id]['location']} exists already in the dictionary in the dictionary.")
                                continue
                    else:
                        print(f"'{job_title.text}' is not a job title in the dictionary.")  


                    try:
                        full_job_description = soup_job.find('div', id='jobDescriptionText').getText()
                        #print("company location:  " + location)
                        self.current_job[self.current_job_id]['full_job_description'] = full_job_description
                    except Exception as e:
                        print("Error: ", e)
                        print("error in getting info:" + "full_job_description")


                    recent_jobs.update(self.current_job)
                    self.current_job_id += 1
                    #for element in mosaics:
                except Exception as e:
                    print("Error: ", e)
                    print("error in getting info:" + "job_title")
                    continue
        return recent_jobs
                                            


                    # job_title = mosaic.find('h2', class_='jobTitle').text.strip()
                    # company = mosaic.find('span', class_='companyName').text.strip()
                    # location = mosaic.find('div', class_='companyLocation').text.strip()
                    # posted = mosaic.find('span', class_='date').text.strip()
                    # job_link = base_url + job_id
                    # print([job_title, company, location, posted, job_link])

                    # Writing to CSV File
                    # writer.writerow(
                    #    [job_title, company, location.title(), posted, job_link])
                
                # Find elements where class contains 'jcs-JobTitle'



        #         jobs = soup.find_all('a', class_='tapItem')

        #         for job in jobs:
        #             job_id = job['id'].split('_')[-1]
        #             job_title = job.find('span', title=True).text.strip()
        #             company = job.find('span', class_='companyName').text.strip()
        #             location = job.find('div', class_='companyLocation').text.strip()
        #             posted = job.find('span', class_='date').text.strip()
        #             job_link = base_url + job_id
        #             #print([job_title, company, location, posted, job_link])

        #             # Writing to CSV File
        #             writer.writerow(
        #                 [job_title, company, location.title(), posted, job_link])

        # print(f'Jobs data written to <{file_name}> successfully.')
        # file.close()

    def apply(self, applicant):
        pass

# test the class
if __name__ == "__main__":

    target_url_reference_dict = {'zürich' :"https://ch.indeed.com/",
                  'san francisco': "https://www.indeed.com/",
                  'germany': "https://de.indeed.com/",
                  'france': "https://fr.indeed.com/",
                  'london': 'https://www.uk.indeed.com/',
                  'search': 'https://www.indeed.com/',
                  'default': 'https://www.indeed.com/',
                  'seatle': 'https://www.indeed.com/',
                  'new york': 'https://www.indeed.com/',
                  'california': 'https://www.indeed.com/',
                   'boston': 'https://www.indeed.com/',
                     'chicago': 'https://www.indeed.com/',
                    'berlin': 'https://de.indeed.com/',
                    'münchen': 'https://de.indeed.com/',
                    'hamburg': 'https://de.indeed.com/',
                    'köln': 'https://de.indeed.com/',
                    'frankfurt': 'https://de.indeed.com/',
                    'stuttgart': 'https://de.indeed.com/',
                    }
    # Skills and Place of Work
    # skill = input('Enter your Skill: ').strip()
    # place = input('Enter the location: ').strip()
    # no_of_pages = int(input('Enter the #pages to scrape: '))
    # skill = "machine learning"
    # place = "zürich"
    no_of_pages = 4

    #load prev. jobs from dataset
    jobs = {}

    applicants_path = "/Users/alira/alisworld/followup/toolbox/myjob/myjob-ml/applicants/applicants.json"
    with open(applicants_path, 'r') as json_file:
        applicants = json.load(json_file)

    applicant = applicants["ali@ai-bridge.de"]
        # store jobs in a json file
        # with open('jobs.json', 'w') as json_file:
        #     json.dump(job, json_file)
    #shuffle the skills to avoid repeated searches from same starting point in case of failure, yeah sometimes i also think about the edge cases :P 
    random.shuffle(applicant['core_skills']['value'])
    random.shuffle(applicant['preferred_locations']['value'])

    # Load existing data
    # The path to the JSON file
    json_file_path = 'indeed_jobs.json'

    # Check if the file does not exist
    if not os.path.exists(json_file_path):
        # Create the file and write an empty JSON object to it
        with open(json_file_path, 'w') as json_file:
            json.dump({}, json_file)

    with open('indeed_jobs.json', 'r') as json_file:
        indeed_jobs = json.load(json_file)

    indeed = INDEED(indeed_target_urls=target_url_reference_dict)
    #indeed.check_captha(target_url)
    # latest_jobs = indeed.search(applicant, indeed_jobs)
    for skill in applicant['core_skills']['value']: 
        for location in applicant['preferred_locations']['value']:
            recent_jobs = indeed.get_jobs(all_jobs=indeed_jobs,skill=skill, location=location, no_of_pages=no_of_pages)
            indeed_jobs.update(recent_jobs)

            # store jobs in a json file
            with open('indeed_jobs.json', 'w') as json_file:
                    json.dump(indeed_jobs, json_file)

    # here a module to select which jobs to apply for
    # resume = resume.ResumeAnalyser()
    # selected_jobs = resume.select(applicant, latest_jobs)
    # here a module to apply for the selected jobs
    # indeed.apply(applicant=applicant, latest_jobs=selected_jobs)

