import requests
import os
import shutil
import sys
import re
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.append('/mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/')
import Custom

# ================= CONFIG =================
BASE_PATH = '/mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/Laurens'
SOURCE_FILE = f'{BASE_PATH}/original.ics'
FINAL_FILE  = f'{BASE_PATH}/Final-File.ics'

URL = 'https://elo.somtoday.nl/services/webdav/calendarfeed/58405be0-5611-4aba-be66-9894a1009f12/4fc988ad-6d4d-4c2a-aaf0-8207665bf69b'

REMOVE_KEYWORDS = ['Studiedag', 'Sneeuwvrij', 'Lesvrij', 'Studiemiddag', 'Studieochtend', 'Goede_vrijdag']

# Formaat: (Weekdag, Starttijd, Eindtijd) 
# Weekdagen: 0=Maandag, 1=Dinsdag, 2=Woensdag, 3=Donderdag, 4=Vrijdag
REMOVE_TIMESLOTS = [
    (0, "09:15", "10:00"), # Maandag
    (0, "13:45", "14:30"), # Maandag
    (0, "15:15", "16:00"),  # Maandag
    (1, "14:30", "15:15"), # Dinsdag
    (2, "08:30", "09:15"), # Woensdag
    (2, "09:15", "10:00"),   # Woensdag
    (3, "09:15", "10:00"), # Donderdag
    (3, "15:15", "16:00"), # Donderdag
    (4, "09:15", "10:00"), # Vrijdag
]

# ================= DOWNLOAD =================
if os.path.exists(FINAL_FILE):
    os.remove(FINAL_FILE)

r = requests.get(URL)
with open(SOURCE_FILE, 'wb') as f:
    f.write(r.content)

shutil.copyfile(SOURCE_FILE, FINAL_FILE)

# ================= HELPER FUNCTIE DATUM/TIJD =================
def parse_ics_datetime(dt_str):
    """Zet een ICS datumblob (bijv. 20231016T071500Z) om naar lokale Nederlandse tijd."""
    match = re.search(r'(\d{8}T\d{6})(Z?)', dt_str)
    if not match:
        return None
    
    time_str, is_utc = match.groups()
    dt = datetime.strptime(time_str, "%Y%m%dT%H%M%S")
    
    # Reken UTC om naar de Nederlandse tijdzone
    if is_utc == 'Z':
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
        dt = dt.astimezone(ZoneInfo("Europe/Amsterdam"))
    else:
        # Als er geen Z staat, gaan we uit van lokale tijd
        dt = dt.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
        
    return dt

# ================= VEVENT FILTER =================
def filter_events(filename, keywords, timeslots):
    """Filtert events op basis van de lijst met keywords én specifieke tijdsblokken."""
    with open(filename, 'r') as f:
        lines = f.readlines()

    result = []
    i = 0

    while i < len(lines):
        if lines[i].strip() == "BEGIN:VEVENT":
            block = []
            remove = False
            dtstart = None
            dtend = None

            while i < len(lines):
                line = lines[i]
                block.append(line)

                # 1. Check op keywords in SUMMARY
                if line.startswith("SUMMARY") and any(k in line for k in keywords):
                    remove = True

                # 2. Extract de start- en eindtijd voor de timeslot check
                if line.startswith("DTSTART"):
                    dtstart = parse_ics_datetime(line)
                elif line.startswith("DTEND"):
                    dtend = parse_ics_datetime(line)

                if line.strip() == "END:VEVENT":
                    break
                i += 1
            
            # 3. Check of de les in een van de verboden tijdsblokken valt
            if not remove and dtstart and dtend:
                weekday = dtstart.weekday()
                start_time = dtstart.strftime("%H:%M")
                end_time = dtend.strftime("%H:%M")
                
                for (w, st, et) in timeslots:
                    if weekday == w and start_time == st and end_time == et:
                        remove = True
                        break

            if not remove:
                result.extend(block)
        else:
            result.append(lines[i])

        i += 1

    with open(filename, 'w') as f:
        f.writelines(result)

# ================= CLEAN EVENTS =================
filter_events(FINAL_FILE, REMOVE_KEYWORDS, REMOVE_TIMESLOTS)

# ================= TEXT REPLACEMENTS =================
with open(FINAL_FILE, 'r') as f:
    filedata = f.read()

# Naam agenda
filedata = filedata.replace(
    'NAME:Somtoday agenda',
    'NAME:Somtoday Laurens'
)

# Lesnamen
for old, new in Custom.Lessen.items():
    filedata = filedata.replace(old, new)

# Lokalen (ranges)
ranges = {
    "be": (1, 300),
    "tm": (1, 300),
    "cc": (1, 99),
    "cb": (1, 200)
}

for prefix, (start, end) in ranges.items():
    for i in range(start, end + 1):
        num = f"{i:03d}" if prefix in ["be", "tm", "cb"] else f"{i:02d}"
        filedata = filedata.replace(f"SUMMARY:{prefix}{num} - ", 'SUMMARY:')

# Lokalen (Custom)
for loc in Custom.Lokalen:
    filedata = filedata.replace(f"SUMMARY:{loc} - ", 'SUMMARY:')

with open(FINAL_FILE, 'w') as f:
    f.write(filedata)

# ================= CLEANUP =================
os.remove(SOURCE_FILE)

print("✅ Agenda succesvol opgeschoond en specifieke lessen verwijderd!")