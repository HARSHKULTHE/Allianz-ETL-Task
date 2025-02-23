import json
import openpyxl
from openpyxl.styles import Font
from bs4 import BeautifulSoup

INPUT_FILE = "hockey_stats.json"
OUTPUT_FILE = "NHL_Stats.xlsx"

def write_nhl_stats_sheet(worksheet, team_stats):
    """Writes all hockey team statistics to 'NHL Stats 1990-2011' sheet."""
    worksheet.append(["Year", "Team Name", "Wins", "Losses"])  
    for row in team_stats:
        worksheet.append([row["year"], row["team_name"], row["wins"], row["losses"]])

    
    for cell in worksheet[1]:
        cell.font = Font(bold=True)


def compute_winners_and_losers(team_stats):
    """Computes the team with most and least wins per year."""
    yearly_data = {}

    for row in team_stats:
        year = row["year"]
        team = row["team_name"]
        wins = row["wins"]

        if year not in yearly_data:
            yearly_data[year] = {"winner": (team, wins), "loser": (team, wins)}
        else:
            if wins > yearly_data[year]["winner"][1]:
                yearly_data[year]["winner"] = (team, wins)
            if wins < yearly_data[year]["loser"][1]:
                yearly_data[year]["loser"] = (team, wins)

    return yearly_data


def write_winners_losers_sheet(worksheet, yearly_summary):
    """Writes the winners and losers per year to the second sheet."""
    worksheet.append(["Year", "Winner", "Winner Wins", "Loser", "Loser Wins"])  

    for year, data in sorted(yearly_summary.items()):
        worksheet.append([year, data["winner"][0], data["winner"][1], data["loser"][0], data["loser"][1]])

    
    for cell in worksheet[1]:
        cell.font = Font(bold=True)


def create_excel_report():
    """Main function to create the Excel file."""
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        team_stats = json.load(file)

    yearly_summary = compute_winners_and_losers(team_stats)

    wb = openpyxl.Workbook()
    worksheet1 = wb.active
    worksheet1.title = "NHL Stats 1990-2011"
    write_nhl_stats_sheet(worksheet1, team_stats)

    worksheet2 = wb.create_sheet("Winner and Loser per Year")
    write_winners_losers_sheet(worksheet2, yearly_summary)

    wb.save(OUTPUT_FILE)
    print(f"Excel file '{OUTPUT_FILE}' created successfully!")


if __name__ == "__main__":
    create_excel_report()

def extract_team_stats(html_content):
    """Extracts team statistics from HTML table."""
    soup = BeautifulSoup(html_content, "html.parser")
    team_stats = []

    for row in soup.find_all("tr", class_="team"):
        cells = row.find_all("td")
        if len(cells) == 4:  
            team_stats.append({
                "year": cells[0].text.strip(),
                "team_name": cells[1].text.strip(),
                "wins": int(cells[2].text.strip()),
                "losses": int(cells[3].text.strip())
            })

    return team_stats