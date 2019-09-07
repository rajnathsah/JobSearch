import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from fuzzywuzzy import fuzz
import webbrowser

# define skills
myskill="Python, flask, restful api, scraping, sqlalchemy, sql, pl/sql, oracle database, shell script, bash, performance tuning, automation, data analysis, selenium"

# function to scrape python job and generate csv and html file
def scrapepythonnaukri():
    '''
    This function scrape python job listing from naukri.com for hyderabad location.
    Using fuzzy match
    '''
    user_agent = {'User-agent': 'Mozilla/5.0'}
    url = "https://www.naukri.com/python-jobs-in-hyderabad"
    page = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find_all('div', {'data-url':re.compile(r'http.*')})

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

    for item in data:
        try:              
            joburl.append(item.attrs['data-url'])
        except Exception as ex:
            joburl.append('')    
        try:        
            skill.append(item.find(class_='skill').get_text())
        except Exception as ex:
            skill.append('')
        try:        
            designation.append(item.find(class_='desig').get_text())
        except Exception as ex:
            designation.append('')
        try:
            orgnization.append(item.find(class_='org').get_text())
        except Exception as ex:
            orgnization.append('')
        try:        
            experience.append(item.find(class_='exp').get_text())
        except Exception as ex:
            experience.append('')
        try:
            loc.append(item.find(class_='loc').get_text())
        except Exception as ex:
            loc.append('')
        try:
            moredesc.append(item.find(class_='more desc').get_text())
        except Exception as ex:
            moredesc.append('')
        try:
            salary.append(item.find(class_='salary').get_text())
        except Exception as ex:
            salary.append('')
        try:        
            recruiterdetails.append(item.find(class_='rec_details').get_text())
        except Exception as ex:
            recruiterdetails.append('')
        try:
            recruitername.append(item.find(class_='rec_name').get_text())
        except Exception as ex:
            recruitername.append('')
        try:        
            jobpostingdate.append(item.find(class_="date").get_text())
        except Exception as ex:
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
    
    exp_year=pd.DataFrame(df.experience.str.split(' ',expand=True))[0].str.split('-',expand=True)
    columns=['start','end']
    exp_year.columns=columns  
    updated_df=pd.concat([df,exp_year], axis=1)
    updated_df=updated_df.drop('experience',1)
    
    match_perc = []
    for index, row in df.iterrows(): 
        match_perc.append(fuzz.token_set_ratio(row['skill'],myskill))
        if fuzz.token_set_ratio(row['skill'],myskill) > 50:  
            webbrowser.open_new_tab(row['joburl'])            
           
    match_perc = pd.DataFrame(match_perc)
    match_col = ['Match Percentage(%)']
    match_perc.columns=match_col
    updated_df = pd.concat([updated_df,match_perc], axis=1)
    updated_df = updated_df.sort_values(by=['Match Percentage(%)'], ascending=False) 
    
    updated_df.to_csv('pythonjob.csv')
    updated_df.rename(columns={'joburl':'Job Link','skill':'Skills','designation':'Designation','orgnization':'Orgnization',
                       'experience':'Experience','location':'Location','salary':'Salary','moredesc':'More Description',
                       'recruitername':'Recruiter Name','recruiterdetails':'Recruiter Details',
                       'jobpostingdate':'Job Posting Date'}).to_html('pythonjob.html')
