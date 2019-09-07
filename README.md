# Scrape Python developer job posted on www.naukri.com

## Requirement
1. [Python 3.x](https://www.python.org/)
2. [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
3. [Pandas](https://pandas.pydata.org/)
4. [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)

All the dependencies can be installed using requirement file
```python
pip install -r requirements.txt
```

pythonnaukri.py contains the code to scrape the python job in a city. It includes bit of data cleaning and matching skills posted on website. For matching the skills, it uses Levenshtein distance algorithm. It add the match percentage in output as column.
Upon running, it scrape all python job available in city and generate csv and html report, it also opens new tabs for the job which have matching skills more than 50%.


