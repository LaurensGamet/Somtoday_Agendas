import requests
import os
import shutil
import sys

sys.path.append('/home/laurens/Somtoday_Agendas')
import Custom_Loukas as Custom

from datetime import date, timedelta

# Huidige datum
vandaag = date.today()

# Huidig jaar en weeknummer
jaar, week, _ = vandaag.isocalendar()

# Volgende week (zelfde jaar/week systeem)
volgende_week_datum = vandaag + timedelta(weeks=1)
jaar_volgende, week_volgende, _ = volgende_week_datum.isocalendar()

# Alles samenplakken
resultaat = f"{jaar}{week:02d}-{jaar}{week_volgende:02d}"
# Give simpler names
file1 = f'/home/laurens/Somtoday_Agendas/Loukas/rooster-{resultaat}.txt'
file2 = '/home/laurens/Somtoday_Agendas/Loukas/Final-File.ics'

# Makes sure no duplicate files
if os.path.exists(file2):
  os.remove(file2)
else:
  print("The file does not exist")

# Gets original file
url = 'https://rsgrijks.zportal.nl/api/v3/ical?access_token=mc24jkscuoqntcvkuqom8nt8uh&startWeekOffset=0&endWeekOffset=1&valid=true&user=~me'
r = requests.get(url, allow_redirects=True)
open(file1, 'wb').write(r.content)

with open(file1, 'r') as file:
  filedata = file.read()

# Makes Final-File.ics from original
shutil.copyfile(file1, file2)

# Replaces text in original file

# Studiedag
def remove_events_with_summary(input_file, output_file, keyword):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    result_lines = []  # List to store lines to keep
    i = 0  # Line index

    while i < len(lines):
        # Check if a VEVENT block starts
        if lines[i].strip() == "BEGIN:VEVENT":
            # Check if the block is at least 11 lines long
            if i + 1 < len(lines):
                # Check if the fourth line in the block contains the keyword
                if f"SUMMARY:{keyword}" in lines[i + 3]:
                    #print(f"Deleting VEVENT block starting at line {i}")  # Debugging
                    # Skip the 11 lines of this VEVENT block
                    i += 11
                    continue  # Skip appending these lines to the result
            # If the block is too short, just append it (avoid breaking the structure)
        result_lines.append(lines[i])
        i += 1

    # Write the remaining lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(result_lines)

# Test the function
remove_events_with_summary(file1, file2, '[x]')


with open(file2, 'r') as file:
  filedata = file.read()

# Naam agenda
filedata = filedata.replace('BEGIN:VCALENDAR', 'BEGIN:VCALENDAR\nNAME:Zermelo Loukas\nX-WR-CALNAME:Zermelo Loukas')

with open(file2, 'w') as file:
  file.write(filedata)

# Dubbele shit
filedata = filedata.replace('END:VEVENT\nEND:VEVENT', 'END:VEVENT')

with open(file2, 'w') as file:
  file.write(filedata)

# Toetsen
filedata = filedata.replace('[o] [toets] ', '[TOETS]')

with open(file2, 'w') as file:
  file.write(filedata)

# Perform all replacements
for old, new in Custom.Lessen.items():
    filedata = filedata.replace(old, new)

# Write the modified data back to the file
with open(file2, 'w') as file:
    file.write(filedata)

# Lokalen

# Define the ranges for replacements
ranges = {
    "l": (1, 300),
    "d": (1, 300),
    "ska" :(1,300)
}

# Perform range-based replacements
for prefix, (start, end) in ranges.items():
    for i in range(start, end + 1):
        formatted_number = f"{i:03d}" if prefix in ["l", "d"] else f"{i:01d}"
        filedata = filedata.replace(f"SUMMARY:[>] ", f'SUMMARY:')
        filedata = filedata.replace(f"SUMMARY:{prefix}{formatted_number} ", f'LOCATION:{prefix}{formatted_number}\nSUMMARY:')

for prefix, (start, end) in ranges.items():
    for i in range(start, end + 1):
        formatted_number = f"{i:03d}" if prefix in ["l", "d"] else f"{i:01d}"
        filedata = filedata.replace(f"SUMMARY:[!] ", f'SUMMARY:')
        filedata = filedata.replace(f"SUMMARY:{prefix}{formatted_number} ", f'LOCATION:{prefix}{formatted_number}\nSUMMARY:')

for prefix, (start, end) in ranges.items():
    for i in range(start, end + 1):
        formatted_number = f"{i:03d}" if prefix in ["l", "d"] else f"{i:01d}"
        filedata = filedata.replace(f"SUMMARY:[>] ", f'SUMMARY:')
        filedata = filedata.replace(f"SUMMARY:[TOETS] {prefix}{formatted_number} ", f'LOCATION:{prefix}{formatted_number}\nSUMMARY:[TOETS] ')
# Perform specific replacements
#for replacement in Custom.Lokalen:
#    filedata = filedata.replace(replacement, 'SUMMARY:')

# Write the modified data back to the file
with open(file2, 'w') as file:
    file.write(filedata)

# Delete temporary file

if os.path.exists(file1):
  os.remove(file1)
else:
  print("The file does not exist")
