from bs4 import BeautifulSoup as bs
import re
import requests
import fake_useragent as fu
import time
import random
import pandas as pd

def get_score(url):
    try:
        response = requests.get(url,
                                headers={"User-Agent": fu.UserAgent().random},
                                timeout=3)
        if response.status_code != 200:
            if response.status_code == 404:
                print(f"URL not found: {url}")
            elif response.status_code == 410:
                print(f"URL gone: {url}")
                return -1, {}
            else:
                print(f"Fetched {url} with status code {response.status_code}")
                return None, {}
    except Exception as e:
        return None, {}
    soup = bs(response.text, "html.parser")
    # try:
    # Get school name
    school_name = ""
    content_div = soup.find("div", class_="villain-content")
    if content_div:
        h1 = content_div.find("h1")
    if h1:
        school_name = h1.get_text(strip=True)
    # Get discipline cluster
    results = {}
    # Accordion : 手風琴式展開
    accordion_box = soup.find("div", class_="accordion-box")
    if not accordion_box:
        print(f"No accordion box found for {school_name} at {url}")
        return school_name, results
    # Bellow : 風箱，手風琴式展開的每個區塊
    bellow_divs = accordion_box.find_all("div", class_=lambda x: x and "BellowWrapper" in x)
    for i, bellow in enumerate(bellow_divs):
        button = bellow.find("button")
        if not button:
            print(f"No button found in bellow {i} for {school_name} at {url}")
            continue
        # Discipline name
        h3 = button.find("h3")
        if not h3:
            print(f"No h3 found in button of bellow {i} for {school_name} at {url}")
            continue
        section_title = h3.get_text(strip=True)
        # Discipline data
        bellow_body = button.find_next_sibling("div")
        if not bellow_body:
            print(f"No bellow body found in bellow {i} for {school_name} at {url}")
            continue
        # Get overall score
        content_div = bellow_body.find("div")
        if not content_div:
            print(f"No content div found in bellow {i} for {school_name} at {url}")
            continue
        section_data = {}
        # Get overall ranking
        strong = bellow_body.find("strong").get_text(strip=True) if bellow_body.find("strong") else None
        rank = re.findall(r'[0-9]+', strong) if strong else None
        if rank:
            section_data["Rank"] = rank[-1]
        else:
            section_data["Rank"] = strong if strong else None
        # Get label and value pairs
        data_rows = content_div.find_all("div", class_=lambda x: x and "DataRow__Row" in x)
        # Unranked case
        if not data_rows:
            continue
        # Ranked case
        for row in data_rows:
            ps = row.find_all("p")
            if len(ps) == 2:
                label = ps[0].get_text(strip=True)
                value = ps[1].get_text(strip=True)
                if value.startswith("#"):
                    value = value[1:]
                section_data[label] = value
            else:
                print(f"Unexpected data row format in {section_title} for {school_name}")
                print(f"Row content: {[p.get_text(strip=True) for p in ps]}")

        if section_data:
            results[section_title] = section_data
    return school_name, results

if __name__ == "__main__":

    columns = ['University_Name',
               'Category',
               'Rank',
               'Score',
               'Global_Research_Reputation',
               'Regional_Research_Reputation',
               'Publications',
               'Books',
               'Conferences',
               'Normalized_Citation_Impact',
               'Total_Citations',
               'Number_of_publications_that_are_among_The_10%_Most_Cited',
               'Percentage_of_total_publications_that_are_among_The_10%_Most_Cited',
               'International_Collaboration_-_relative_to_Country',
               'International_Collaboration',
               'Number_of_Highly_Cited_Papers_that_are_among_The_Top_1%_Most_Cited',
               'Percentage_of_Highly_Cited_Papers_that_are_among_The_Top_1%_Most_Cited']
    
    df = pd.read_csv("schools_url.csv")
    url = df[df['University_Name'] == 'Adana Alparslan Turkes Science & Technology University']['URL'].values[0]
    print(f"Testing URL: {url}\n")

    school_name, result = get_score(url)
    print(f"School Name: {school_name}\n")
    # print(result)
    for discipline, info in result.items():
        for label, value in info.items():
            label
            print(f"{discipline}  |  {'ok' if sum([int(label.lower().replace(' ', '_').endswith(col.lower())) for col in columns[2:]]) > 0 else label }  |  {value}")
        print('=' * 50, '\n')
    '''
    all_urls = pd.read_csv("schools_url.csv")["url"].tolist()
    for url in all_urls:
        school_name, result = get_score(url)
        print(f"School Name: {school_name}")
        print(result)
        print('=' * 50, '\n')
        if school_name and result:
            pd.DataFrame([result]).to_json(f"{school_name}.json", indent=4)
            break
    '''