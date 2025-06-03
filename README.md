# Feriados2iCal

A Python script that scrapes Argentina's official national holidays from the government website and converts them into an iCalendar (.ics) file that can be imported into any calendar application.

## What it does

This tool:
- Scrapes Argentina's national holidays from the official government website: https://www.argentina.gob.ar/interior/feriados-nacionales-2025
- Parses the JavaScript data containing holiday information
- Filters out non-working days ("días no laborables") and tourist days, keeping only official national holidays
- Generates an iCalendar (.ics) file with proper timezone support (America/Argentina/Buenos_Aires)
- Creates all-day events from 8:00 AM to 10:00 PM Argentina time

## Features

- **Official source**: Uses only the official Argentina government website
- **Smart parsing**: Extracts holiday data from JavaScript variables in the webpage
- **Timezone aware**: Properly handles Argentina timezone (UTC-3)
- **Filtered results**: Only includes official national holidays, excludes tourist days and non-working days
- **Standard format**: Generates RFC 5545 compliant iCalendar files

## Requirements

- Python 3.8+
- Dependencies (automatically installed from `requirements.txt`):
  - `requests` - For web scraping
  - `beautifulsoup4` - For HTML parsing
  - `icalendar` - For generating iCal files
  - `pytz` - For timezone handling

## Installation and Usage

### Option 1: Using DDEV (Recommended for development)

This project is configured to work with DDEV, which provides a containerized development environment.

1. **Prerequisites**: Install [DDEV](https://ddev.readthedocs.io/en/stable/)

2. **Start the environment**:
   ```bash
   ddev start
   ```

3. **SSH into the container**:
   ```bash
   ddev ssh
   ```

4. **Run the script** (dependencies are automatically installed):
   ```bash
   # The virtual environment and dependencies are automatically set up by the post-start hook
   python feriados2ical.py
   ```

### Option 2: Local Python Environment

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd feriados2ical
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the script**:
   ```bash
   python feriados2ical.py
   ```

## Output

The script generates a file named `argentina_holidays_2025.ics` containing all Argentina's national holidays for 2025. You can import this file into:

- Google Calendar
- Apple Calendar
- Outlook
- Thunderbird
- Any other calendar application that supports iCalendar format

## Example Output

```
Found 16 holidays for 2025:
2025-01-01: Año Nuevo
2025-03-03: Carnaval
2025-03-04: Carnaval
2025-03-24: Día Nacional de la Memoria por la Verdad y la Justicia
2025-04-02: Día del Veterano y de los Caídos en la Guerra de Malvinas
2025-04-18: Viernes Santo Festividad Cristiana
2025-05-01: Día del Trabajador
2025-05-25: Día de la Revolución de Mayo
2025-06-16: Paso a la Inmortalidad del Gral. Don Martín Miguel de Güemes
2025-06-20: Paso a la Inmortalidad del Gral. Manuel Belgrano
2025-07-09: Día de la Independencia
2025-08-17: Paso a la Inmortalidad del Gral. José de San Martín
2025-10-12: Día de la Raza
2025-11-24: Día de la Soberanía Nacional (20/11)
2025-12-08: Inmaculada Concepción de María
2025-12-25: Navidad
```

## DDEV Configuration

The project includes a complete DDEV setup:

- **Type**: Generic project
- **Python support**: Includes pip and python3-venv packages
- **Virtual environment**: Automatically created and upgraded via post-start hook
- **Dependencies**: Automatically installed from `requirements.txt` on startup
- **Additional tools**: Includes the pimp-my-shell addon for enhanced terminal experience

### DDEV Commands

```bash
# Start the project
ddev start

# SSH into the container
ddev ssh

# Stop the project
ddev stop

# Restart the project
ddev restart
```

## Customization

To modify the script for different years, edit the `year` variable in the `__main__` section:

```python
if __name__ == "__main__":
    year = 2026  # Change this to the desired year
    holidays = scrape_argentina_holidays(year)
    create_ical(holidays, f"argentina_holidays_{year}.ics")
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with DDEV: `ddev start && ddev ssh`
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you've activated the virtual environment and installed all dependencies
2. **Network errors**: Check your internet connection and verify the government website is accessible
3. **No holidays found**: The government website structure may have changed; check the JavaScript parsing logic

### DDEV Issues

1. **Container won't start**: Run `ddev restart` or `ddev stop && ddev start`
2. **Python not found**: The post-start hook should install Python; try `ddev restart`
3. **Virtual environment issues**: SSH into the container and manually run the post-start script: `.ddev/post-start.sh`
