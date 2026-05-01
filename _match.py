import pandas as pd
import revised.fast_score as fast_score
from tqdm import tqdm
import re

if __name__ == "__main__":
    url_df = pd.read_csv("schools_url.csv")
    university_urls = pd.read_csv('university_scores.csv')['University Name'].unique()
    url_df['University Name'] = university_urls
    print(url_df.head())
    for idx, row in tqdm(url_df.iterrows(), total=url_df.shape[0]):
        university_name_parts = row['University Name'].split()
        for word in ['University', 'College', 'Institute', 'School', 'Academy', 'of']:
            if word in university_name_parts:
                university_name_parts.remove(word)
        any_match = False
        for part in university_name_parts:
            if re.search(part, row['url'], re.IGNORECASE):
                any_match = True
                break
        if not any_match:
            print(f"URL: {row['url']} does not match University Name: {row['University Name']}")
    print(url_df.head())
    url_df.to_csv("schools_url_with_schools_name.csv", index=False, encoding="utf-8")