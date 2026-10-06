import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_contributions(username="mohitxcodes", output_path="data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Failed to fetch {url}: {res.status_code}")
        return
    
    soup = BeautifulSoup(res.text, "html.parser")
    # GitHub's contribution graph often uses <td> with tooltips, or 
    # we can find elements with 'data-date' and 'data-level'.
    # Actually the table cells usually have class 'ContributionCalendar-day'.
    days = soup.find_all("td", class_="ContributionCalendar-day")
    
    if not days:
        print("Warning: No days found with class 'ContributionCalendar-day'. GitHub might have updated their markup.")
        
    contributions = []
    total = 0
    longest_streak = 0
    current_streak = 0
    
    for day in days:
        date_str = day.get('data-date')
        if not date_str:
            continue
            
        level_str = day.get('data-level', '0')
        level = int(level_str)
        
        # Tooltip text contains the exact count, e.g. "5 contributions on Dec 1, 2023"
        # Or you can just use level for visual, but let's try to extract count from text
        # If text is inside, or tooltip. Since it's complex, let's just use level for color.
        # But wait, we can also scrape standard stats.
        
        contributions.append({
            "date": date_str,
            "level": level
        })
        if level > 0:
            total += 1 # We don't have exact counts easily without parsing tooltips, just counting days with >0 or we can parse the text.
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak
        else:
            current_streak = 0
            
    stats = {
        "total_active_days": total,
        "longest_streak": longest_streak,
        "current_streak": current_streak
    }
    
    data = {
        "stats": stats,
        "days": contributions
    }
    
    with open(output_path, "w") as f:
        f.write(json.dumps(data, indent=2))
        
    print(f"Saved {output_path}")

if __name__ == "__main__":
    fetch_contributions()
