import json 
import pandas as pd
import requests 
from io import StringIO

SBIR_URL = "https://api.www.sbir.gov/public/api/"
AGENCIES = {
    "DOD": "solicitations?keyword=sbir&agency=DOD&open=1",
    "NASA": "solicitations?keyword=sbir&agency=NASA&open=1",
    "NSF": "solicitations?keyword=sbir&agency=NSF&open=1",
    "DOE": "solicitations?keyword=sbir&agency=DOE&open=1",
    "DHS": "solicitations?keyword=sbir&agency=DHS&open=1"
}

class SbirContractsInfo:
    def __init__(self, solicitation_agency_url, topic_info): 
        self.topic_title = topic_info["topic_title"]
        self.solicitation_agency_url = solicitation_agency_url
    
    def __str__(self):
        return f"Title: {self.topic_title}, "\
               f"Url: {self.solicitation_agency_url}"
    
    def __repr__(self): 
        return f"type:<SbirContractsInfo>Title:<{self.topic_title}>URL:<{self.solicitation_agency_url}>"

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items()}
    
def main():
    sbir_contracts_objects = []
    sbir_by_agency = {}
    for agency, url in AGENCIES.items():
        sbir_by_agency[agency] = []
        search_url = SBIR_URL + url
        solicitations = requests.get(search_url)
        if solicitations.status_code == 404: 
            print(f'No data found for {agency}')
            continue
        solicitations = solicitations.json()
        for solicitation_ids in solicitations:
            df = pd.DataFrame.from_dict(solicitation_ids)
            release_date_query = df.query('release_date == "2025/07/02"')
            solicitation_basic_info = release_date_query.loc[:, ['solicitation_agency_url','solicitation_topics']]
            sbir_contracts_objects = [SbirContractsInfo(a.solicitation_agency_url, a.solicitation_topics).to_dict() for a in solicitation_basic_info.itertuples()]
            for item in sbir_contracts_objects:
                sbir_by_agency[agency].append(item)
    with open('sbir.json', 'w') as json_file: 
        # loaded_json = json.load(sbir_by_agency)
        json.dump(sbir_by_agency, json_file)

if __name__ == "__main__":
    main()