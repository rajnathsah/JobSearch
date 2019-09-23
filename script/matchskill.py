import pandas as pd
from fuzzywuzzy import fuzz
import os

def matchSkillGenRep(skills,datafile):
    '''
    Read datafile and match skill and add % match skill column in dataframe.
    Generates csv and html as output.
    '''
    if datafile is not None:
        pd.set_option('display.max_colwidth',-1)
        parent_dir = os.getcwd()        
        rootpath = os.path.join(parent_dir, 'output')
    
        df = pd.read_csv(datafile)
        df.drop(df.columns[[0]],axis=1, inplace=True)
        
        exp_year = pd.DataFrame(df.experience.str.split(' ', expand=True))[0].str.split('-', expand=True)
        columns = ['start', 'end']
        exp_year.columns = columns  
        updated_df = pd.concat([df, exp_year], axis=1)
        updated_df = updated_df.drop('experience', 1)
        
        match_perc = []
        for index, row in df.iterrows(): 
            match_perc.append(fuzz.token_set_ratio(row['skill'], skills))        
               
        match_perc = pd.DataFrame(match_perc)
        match_col = ['Match Percentage(%)']
        match_perc.columns = match_col
        updated_df = pd.concat([updated_df, match_perc], axis=1)
        
        updated_df.drop_duplicates(keep=False, inplace=True)       
        updated_df.sort_values(by=['Match Percentage(%)'], ascending=False, inplace=True)
        
        updated_df.rename(columns={'joburl':'Job Link','skill':'Skills','designation':'Designation','orgnization':'Orgnization',
                           'experience':'Experience','location':'Location','salary':'Salary','moredesc':'More Description',
                           'recruitername':'Recruiter Name','recruiterdetails':'Recruiter Details',
                           'jobpostingdate':'Job Posting Date'}, inplace=True)
        
        outcsvfile = os.path.join(rootpath, 'pythonjob.csv')
        updated_df.to_csv(outcsvfile, index=False)        
        updated_df['Job Link']=updated_df['Job Link'].map(lambda x : '<a target="_blank" href="{}">{}</a>'.format(x,x))
        outhtmlfile = os.path.join(rootpath, 'pythonjob.html')        
        updated_df.to_html(outhtmlfile, escape=False, index=False)
    else:
        pass