import pandas as pd
from fast_score import get_score
from tqdm import tqdm
import os
import datetime

columns = [ 'University_Name',
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

def _dict_to_dataframe(school_name, results):
    df = pd.DataFrame(columns=columns)
    for discipline, info in results.items():
        row = {'University_Name': school_name, 'Category': discipline}
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        for label, value in info.items():
            label_lowercase = label.lower().replace(' ', '_')
            for col in columns[2:]:
                if label_lowercase.endswith(col.lower()):
                    df.at[df.index[-1], col] = value
                    break
    return df
            

if __name__ == "__main__":
    url_csv = 'schools_url.csv'
    df_university_url = pd.read_csv(url_csv)

    yyyy_mm = datetime.datetime.now().strftime("%Y-%m")
    filename = os.path.join(f'usnews_{yyyy_mm}.csv')
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write(','.join(columns) + '\n')
    usnews = pd.read_csv(filename)
    pbar = tqdm(df_university_url.iterrows(),
                dynamic_ncols=True,
                total=len(df_university_url),
                desc="Collecting",
                unit=" universities",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
                colour='green')
    for idx, (school_name, url) in pbar:
        while True:
            if school_name in usnews['University_Name'].values:
                if not usnews[usnews['University_Name'] == school_name]['Rank'].isnull().any():
                    pbar.set_postfix_str("OK")
                    break
            pbar.set_postfix_str(f"Scraping {school_name}")
            university_name, results = get_score(url)
            if university_name == None and results == {}:
                pbar.set_postfix_str("Failed")
                continue
            pbar.set_postfix_str("DataFraming")
            current_school_df = _dict_to_dataframe(university_name, results)
            usnews = pd.concat([usnews, current_school_df], ignore_index=True)
            pbar.set_postfix_str("Saving")
            usnews.to_csv(filename, index=False, encoding='utf-8')
            pbar.set_postfix_str("Success")
            break
    print('Finished !!')
        
        
    