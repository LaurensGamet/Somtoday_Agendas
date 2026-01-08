import requests
import os
import shutil
import sys

sys.path.append('/home/laurens/Somtoday_Agendas')
import Custom

# ================= CONFIG =================
BASE_PATH = '/home/laurens/Somtoday_Agendas/Laurens'
SOURCE_FILE = f'{BASE_PATH}/original.ics'
FINAL_FILE  = f'{BASE_PATH}/Final-File.ics'

URL = 'https://elo.somtoday.nl/services/webdav/calendarfeed/58405be0-5611-4aba-be66-9894a1009f12/4fc988ad-6d4d-4c2a-aaf0-8207665bf69b'

REMOVE_KEYWORDS = ['Studiedag', 'Sneeuwvrij', 'Lesvrij']

# ================= DOWNLOAD =================
if os.path.exists(FINAL_FILE):
    os.remove(FINAL_FILE)

r = requests.get(URL)
with open(SOURCE_FILE, 'wb') as f:
    f.write(r.content)

shutil.copyfile(SOURCE_FILE, FINAL_FILE)

# ================= VEVENT FILTER =================
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

# ================= CLEAN EVENTS =================
remove_events_with_keywords(FINAL_FILE, REMOVE_KEYWORDS)

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

print("✅ Agenda succesvol opgeschoond")
