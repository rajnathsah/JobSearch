import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import os
from multiprocessing import Pool
from multiprocessing import cpu_count


def generateUrlList(url):
    '''
    Generate list of url for scraping
    '''
    all_urls = []    
    for pageno in range(10):                  
        strpageno = ''
    
        if pageno == 0:
            strpageno = ''
        else:
            strpageno = '-{0}'.format(pageno)
                            
        purl = '{0}{1}'.format(url,strpageno)
        all_urls.append(purl)
    return all_urls    

def scrapeUrl(url):
    '''
    Attempts to get content at 'url' by making http get request.
    If the content-type of response is of html-xml, then return the text content, otherwise return None
    '''
    user_agent = {'User-agent': 'Mozilla/5.0'}    
    page = requests.get(url, headers=user_agent)    
    
    if is_good_response(page):
        return page
    else:
        return None
    
def is_good_response(resp):
    '''
    Returns True if the response seems to html, False otherwise
    '''
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code ==200
            and content_type is not None
            and content_type.find('html') >-1)


def getJobListing(url):
    '''
    scrape url and finds all div with link
    '''
    page = scrapeUrl(url)
    time.sleep(2)

    if page is not None:
        soup = BeautifulSoup(page.content, 'lxml')
        joblinks = soup.find_all('div', {'data-url':re.compile(r'http.*')}) 

        joburl = []
        skill = []
        designation = []
        orgnization = []
        experience = []
        loc = []
        moredesc = []
        salary = []
        recruiterdetails = []
        recruitername = []
        jobpostingdate = []
    
        for item in joblinks:
            try:              
                joburl.append(item.attrs['data-url'])
            except:
                joburl.append('')    
            try:        
                skill.append(item.find(class_='skill').get_text())
            except:
                skill.append('')
            try:        
                designation.append(item.find(class_='desig').get_text())
            except:
                designation.append('')
            try:
                orgnization.append(item.find(class_='org').get_text())
            except:
                orgnization.append('')
            try:        
                experience.append(item.find(class_='exp').get_text())
            except:
                experience.append('')
            try:
                loc.append(item.find(class_='loc').get_text())
            except:
                loc.append('')
            try:
                moredesc.append(item.find(class_='more desc').get_text())
            except:
                moredesc.append('')
            try:
                salary.append(item.find(class_='salary').get_text())
            except:
                salary.append('')
            try:        
                recruiterdetails.append(item.find(class_='rec_details').get_text())
            except:
                recruiterdetails.append('')
            try:
                recruitername.append(item.find(class_='rec_name').get_text())
            except:
                recruitername.append('')
            try:        
                jobpostingdate.append(item.find(class_="date").get_text())
            except:
                jobpostingdate.append('')        
            
        df = pd.DataFrame()    
        df['joburl'] = joburl
        df['skill'] = skill
        df['designation'] = designation
        df['orgnization'] = orgnization
        df['experience'] = experience
        df['location'] = loc
        df['moredesc'] = moredesc
        df['salary'] = salary
        df['recruitername'] = recruitername
        df['recruiterdetails'] = recruiterdetails
        df['jobpostingdate'] = jobpostingdate
        try:                    
            outdirpath = os.path.join((os.getcwd()), 'extract')
            filename = os.path.join(outdirpath, url.split('/')[3] + '.csv')    
            df.to_csv(filename)
        except FileNotFoundError as ex:
            print(ex)

    
def combineCSVData():
    '''
    combine all csv of extract directory and save it in output directory
    '''
    parent_dir = os.getcwd()        
    rootpath = os.path.join(parent_dir, 'extract')
    
    filenames = [os.path.join(path, name) for path, subdirs, files in os.walk(rootpath) for name in files]
    
    combined_csv = pd.concat([pd.read_csv(f) for f in filenames ])
    
    outputpath = os.path.join(parent_dir, 'output')
    outfilename = os.path.join(outputpath, 'output.csv')
       
    combined_csv.to_csv(outfilename, index=False)
        
    return outfilename    

def cleanOldFiles():
    '''
    Removes existing csv file from extract directory
    '''
    parent_dir = os.getcwd()        
    rootpath = os.path.join(parent_dir, 'extract')
    
    filenames = [os.path.join(path, name) for path, subdirs, files in os.walk(rootpath) for name in files]
    
    for f in filenames:
        os.remove(f)      