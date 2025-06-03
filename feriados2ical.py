import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime, time
import pytz
import re

def parse_date_from_text(text, year):
    """Parse date from Spanish text format."""
    # Spanish month names to numbers
    month_map = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }

    # Pattern for "día de mes" format
    date_match = re.search(r'(\d{1,2})\s+de\s+(\w+)', text.lower())
    if date_match:
        day = int(date_match.group(1))
        month_name = date_match.group(2)
        if month_name in month_map:
            month = month_map[month_name]
            return datetime(year, month, day)

    # Pattern for "1°" format (like "1° de enero")
    date_match = re.search(r'(\d{1,2})°?\s+de\s+(\w+)', text.lower())
    if date_match:
        day = int(date_match.group(1))
        month_name = date_match.group(2)
        if month_name in month_map:
            month = month_map[month_name]
            return datetime(year, month, day)

    return None





def scrape_argentina_holidays(year=2025):
    """Get holidays for 2025 from the official government page."""
    return scrape_from_website(year)

def scrape_from_website(year):
    """Extract holidays from the official government website JavaScript data."""
    url = f"https://www.argentina.gob.ar/interior/feriados-nacionales-{year}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        holidays = []

        # Look for the JavaScript variable containing holiday data
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and f'holidays{year}' in script.string:
                script_content = script.string

                # Extract the JavaScript object containing holidays
                # Look for the pattern: holidays2025 = { es: [...] }
                pattern = rf'holidays{year}\s*=\s*\{{[^}}]*es:\s*\[([^\]]*)\]'
                match = re.search(pattern, script_content, re.DOTALL)

                if match:
                    # Extract the array content
                    array_content = match.group(1)

                    # Parse each holiday object
                    holiday_pattern = r'\{\s*"date":\s*"([^"]+)",\s*"label":\s*"([^"]+)",\s*"type":\s*"([^"]+)"\s*\}'
                    holiday_matches = re.findall(holiday_pattern, array_content)

                    for date_str, label, holiday_type in holiday_matches:
                        # Skip only "días no laborables" but include tourist holidays
                        if holiday_type == 'no_laborable':
                            continue

                        # Parse date (format: "1/01/2025" or "03/03/2025")
                        try:
                            # Handle both formats: "1/01/2025" and "03/03/2025"
                            if date_str.count('/') == 2:
                                parts = date_str.split('/')
                                if len(parts) == 3:
                                    day = int(parts[0])
                                    month = int(parts[1])
                                    parsed_year = int(parts[2])

                                    if parsed_year == year:
                                        date = datetime(year, month, day)
                                        # Clean up the label (remove trailing periods and extra spaces)
                                        clean_label = label.strip().rstrip('.')
                                        holidays.append((date, clean_label))
                        except ValueError:
                            print(f"Could not parse date: {date_str}")
                            continue

                break

        if not holidays:
            print(f"No JavaScript holiday data found for {year}")

        return holidays

    except Exception as e:
        print(f"Error scraping website: {e}")
        return []

def create_ical(holidays, filename):
    """Create an iCal file from holiday list."""
    cal = Calendar()
    cal.add('prodid', '-//Argentina Holidays//argentina_holidays.py//ES')
    cal.add('version', '2.0')

    # Argentina timezone (UTC-3)
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')

    for date, name in holidays:
        event = Event()
        event.add('summary', name)

        # Create event from 8am to 10pm Argentina time
        start_datetime = argentina_tz.localize(datetime.combine(date.date(), time(8, 0)))
        end_datetime = argentina_tz.localize(datetime.combine(date.date(), time(22, 0)))

        event.add('dtstart', start_datetime)
        event.add('dtend', end_datetime)

        event.add('dtstamp', datetime.now(tz=pytz.UTC))
        event['uid'] = f"{date.strftime('%Y%m%d')}-{name.replace(' ', '_').replace('(', '').replace(')', '')}@argentina.holidays"

        cal.add_component(event)

    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

    print(f"Calendar saved to {filename}")

if __name__ == "__main__":
    year = 2025
    holidays = scrape_argentina_holidays(year)
    create_ical(holidays, f"argentina_holidays_{year}.ics")

    print(f"Found {len(holidays)} holidays for {year}:")
    for date, name in sorted(holidays):
        print(f"{date.strftime('%Y-%m-%d')}: {name}")
