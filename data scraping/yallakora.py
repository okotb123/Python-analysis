import requests
from bs4 import BeautifulSoup
import csv

date = input("please enter a date in the following format MM/DD/YYYY")
page = requests.get(f"https://www.yallakora.com/match-center/%d9%85%d8%b1%d9%83%d8%b2-%d8%a7%d9%84%d9%85%d8%a8%d8%a7%d8%b1%d9%8a%d8%a7%d8%aa?date{date}")

def main (page):
    src = page.content
    soup =BeautifulSoup(src, "lxml")
    matches_details = []
     
    championships = soup.find_all("div" , {'class': "matchCard"})
    
    def get_match_info(championships):

        championship_title = championships.contents[1].find('h2').text.strip()
        all_matches = championships.contents[3].find_all('li')
        number_of_match = len(all_matches)
        
        for i in range(number_of_match):
            #get teams name
            Team_A = all_matches[i].find('div' , {'class' : 'teamA'}).text.strip()
            Team_B = all_matches[i].find('div' , {'class' : 'teamB'}).text.strip()
            
            #get_match_result
            match_result = all_matches[i].find('div', {'class' : 'MResult'}).find_all('span' , {"class" : 'score'})
            score = f"{match_result[0].text.strip()}  - {match_result[1].text.strip()}"

            #get_match_time
            match_time = all_matches[i].find('div', {'class' : 'MResult'}).find('span' , {'class' : 'time'}).text.strip()

            #add match info to match details 
            matches_details.append({"نوع البطوله":championship_title , "ألفريق الاول" : Team_A , "ألفريق الثاني" : Team_B, "ميعاد المباره" : match_time , "النتيجه":score})

    for i in range(len(championships)):
        get_match_info(championships[i])

    keys = matches_details[0].keys()

    with open("C:/Users/dell/Desktop/Data Analyst/data scraping/New Microsoft Excel Worksheet.csv" , 'w' ) as outptfile:
        dict_writer = csv.DictWriter(outptfile, keys )
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("file created")

main(page)
