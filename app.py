from script import searchjob
from script import matchskill
import time
from multiprocessing import Pool, cpu_count

skills = "Python, flask, restful api, scraping, sqlalchemy, sql, pl/sql, oracle database, shell script, bash, performance tuning, automation, data analysis, selenium"

if __name__ == '__main__':   
    starttime = time.time()   
     
    # clean old csv files
    searchjob.cleanOldFiles()
    
    # generate url list
    url  = 'https://www.naukri.com/python-jobs-in-hyderabad'
    all_urls= searchjob.generateUrlList(url)    
        
    # create Pool with cpu count    
    pool = Pool(cpu_count())
    pool.map(searchjob.getJobListing,all_urls)            
    pool.close()
    pool.join()
    
    # mearge all csv files        
    outputfile = searchjob.combineCSVData()
    # match skill and generate csv and html file
    matchskill.matchSkillGenRep(skills, outputfile)
    print('Scraping time (in Sec) - {0}'.format(time.time() - starttime))
