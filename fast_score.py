from bs4 import BeautifulSoup as bs
import re
import requests
import fake_useragent as fu
import time
import random
import pandas as pd

def get_score(url):
    # time.sleep(random.uniform(1, 3))  # 短暫等待，避免過快請求
    try:
        response = requests.get(url,
                                headers={"User-Agent": fu.UserAgent().random},
                                timeout=3)
    except:
        return None, {}
    soup = bs(response.text, "html.parser")
    try:
        # Get school name
        school_name = ""
        h1 = soup.find("h1", class_="Heading-sc-1w5xk2o-0")
        if h1:
            school_name = h1.get_text(strip=True)
        else:
            return None, {}

        # Get discipline cluster
        results = {}
        bellow_divs = soup.find_all("div", class_="Bellow__BellowWrapper-sc-1wt7bw1-0")
   
        for bellow in bellow_divs:
            button = bellow.find("button")
            if not button:
                continue
            # Discipline name
            h3 = button.find("h3")
            if not h3:
                continue
            section_title = h3.get_text(strip=True)
            # print(f"Processing section: {section_title}")

            bellow_body = button.find_next_sibling("div", class_="Bellow__BellowBody-sc-1wt7bw1-2")
            if not bellow_body:
                continue


            # Get overall score
            content_div = bellow_body.find("div", class_="Bellow__Content-sc-1wt7bw1-3")
            if not content_div:
                continue

            data_rows = content_div.find_all("div", class_=lambda x: x and "DataRow__Row" in x)
            section_data = {}
            # Get overall ranking
            rank = bellow_body.find("strong").get_text(strip=True) if bellow_body.find("strong") else None
            rank = re.findall(r'[0-9]+', rank)[-1] if rank else None
            if rank:
                section_data["Rank"] = rank
            
            # Get label and value pairs
            for row in data_rows:
                ps = row.find_all("p")
                if len(ps) == 2:
                    label = ps[0].get_text(strip=True)
                    value = ps[1].get_text(strip=True)
                    if value.startswith("#"):
                        value = value[1:]
                    section_data[label] = value

            if section_data:
                results[section_title] = section_data
    
    except Exception as e:
        # print(f"Failed to fetch {url} → {e}")
        return None, {}
    # print(f"Finished fetching {url} in {end - start:.2f} seconds")
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
    
    url = "https://www.usnews.com/education/best-global-universities/university-of-oxford-503637"

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