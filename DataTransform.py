import os
import json
from bs4 import BeautifulSoup


HTML_DIR = "hockey_html"

def extract_team_stats(html_content):
    """Extracts hockey team statistics from a single HTML file."""
    soup = BeautifulSoup(html_content, "html.parser")
    teams_data = []
    
   
    table_rows = soup.select("tr.team")  
    
    for row in table_rows:
        columns = row.find_all("td")
        if len(columns) >= 4:
            team_data = {
                "year": columns[0].text.strip(),
                "team_name": columns[1].text.strip(),
                "wins": int(columns[2].text.strip()),
                "losses": int(columns[3].text.strip())
            }
            teams_data.append(team_data)
    
    return teams_data


def process_all_html_files():
    """Extracts data from all HTML files and aggregates it into a list."""
    all_teams = []

    for filename in sorted(os.listdir(HTML_DIR), key=lambda x: int(x.split('.')[0])):
        filepath = os.path.join(HTML_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            html_content = file.read()
            teams = extract_team_stats(html_content)
            all_teams.extend(teams)
    
    return all_teams


if __name__ == "__main__":
   
    all_team_stats = process_all_html_files()

   
    with open("hockey_stats.json", "w", encoding="utf-8") as json_file:
        json.dump(all_team_stats, json_file, indent=4)

    print("Data extraction complete! Check hockey_stats.json")
