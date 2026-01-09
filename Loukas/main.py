import requests
import os
import shutil
import sys
from datetime import date, timedelta

sys.path.append('/home/laurens/Somtoday_Agendas')
import Custom_Loukas as Custom

# ================= CONFIG =================
BASE_PATH = '/home/laurens/Somtoday_Agendas/Loukas'
FINAL_FILE = f'{BASE_PATH}/Final-File.ics'
SOURCE_FILE = f'{BASE_PATH}/source.ics'

URL = (
    'https://rsgrijks.zportal.nl/api/v3/ical'
    '?access_token=mc24jkscuoqntcvkuqom8nt8uh'
    '&startWeekOffset=0&endWeekOffset=1&valid=true&user=~me'
)

REMOVE_KEYWORDS = ['[x]']

# ================= DOWNLOAD =================
if os.path.exists(FINAL_FILE):
    os.remove(FINAL_FILE)

r = requests.get(URL)
with open(SOURCE_FILE, 'wb') as f:
    f.write(r.content)

shutil.copyfile(SOURCE_FILE, FINAL_FILE)

# ================= VEVENT CLEANER =================
def remove_events_with_keywords(filename, keywords):
    with open(filename, 'r') as f:
        lines = f.readlines()

    result = []
    i = 0

    while i < len(lines):
        if lines[i].strip() == "BEGIN:VEVENT":
            block = []
            remove = False

            while i < len(lines):
                line = lines[i]
                block.append(line)

                if line.startswith("SUMMARY") and any(k in line for k in keywords):
                    remove = True

                if line.strip() == "END:VEVENT":
                    break
                i += 1

            if not remove:
                result.extend(block)
        else:
            result.append(lines[i])

        i += 1

    with open(filename, 'w') as f:
        f.writelines(result)

remove_events_with_keywords(FINAL_FILE, REMOVE_KEYWORDS)

# ================= TEXT MODIFICATIONS =================
with open(FINAL_FILE, 'r') as f:
    data = f.read()

# Kalendernaam
data = data.replace(
    'BEGIN:VCALENDAR',
    'BEGIN:VCALENDAR\nNAME:Zermelo Loukas\nX-WR-CALNAME:Zermelo Loukas'
)

data = data.replace('\nREFRESH-INTERVAL:PT13M', '')

# Toetsen
data = data.replace('[o] [toets]', '[TOETS]')

# Lesnamen
for old, new in Custom.Lessen.items():
    data = data.replace(old, new)
    
# Lokalen (Custom)
for loc in Custom.Lokalen:
    data = data.replace(f"SUMMARY:{loc} - ", 'SUMMARY:')

# ================= LOKALEN =================
ranges = {
    "l": (1, 300),
    "d": (1, 300),
    "ska": (1, 300),
    "t": (1, 300),
    "s": (1,300)
}

def format_num(prefix, i):
    return f"{i:03d}" if prefix in ["l", "d"] else f"{i}"

for prefix, (start, end) in ranges.items():
    for i in range(start, end + 1):
        num = format_num(prefix, i)

        data = data.replace(
            f"SUMMARY:{prefix}{num} ",
            f"LOCATION:{prefix}{num}\nSUMMARY:"
        )

        data = data.replace("SUMMARY:[>] ", "SUMMARY:")
        data = data.replace("SUMMARY:[!] ", "SUMMARY:")
        data = data.replace(
            f"SUMMARY:[TOETS] {prefix}{num} ",
            f"LOCATION:{prefix}{num}\nSUMMARY:[TOETS] "
        )

# ================= WRITE FINAL =================
with open(FINAL_FILE, 'w') as f:
    f.write(data)

# ================= CLEANUP =================
os.remove(SOURCE_FILE)

print("✅ Zermelo agenda opgeschoond")
