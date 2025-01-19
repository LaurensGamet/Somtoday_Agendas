import requests
import os
import shutil

# Give simpler names
file1 = 'c5490491-11eb-4aca-a8f1-ea3f58e75d54.ics'
file2 = 'Final-File.ics'
klas = 'oga3b'

# Makes sure no duplicate files
if os.path.exists(file2):
  os.remove(file2)
else:
  print("The file does not exist")

# Gets original file
url = 'https://api.somtoday.nl/rest/v1/icalendar/stream/58405be0-5611-4aba-be66-9894a1009f12/c5490491-11eb-4aca-a8f1-ea3f58e75d54'
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
            if i + 10 < len(lines):
                # Check if the fourth line in the block contains the keyword
                if f"SUMMARY:{keyword}" in lines[i + 4]:
                    #print(f"Deleting VEVENT block starting at line {i}")  # Debugging
                    # Skip the 11 lines of this VEVENT block
                    i += 12
                    continue  # Skip appending these lines to the result
            # If the block is too short, just append it (avoid breaking the structure)
        result_lines.append(lines[i])
        i += 1

    # Write the remaining lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(result_lines)

# Test the function
remove_events_with_summary(file1, file2, 'Studiedag')

with open(file2, 'r') as file:
  filedata = file.read()

# Naam agenda
filedata = filedata.replace('NAME:Somtoday agenda', 'NAME:Somtoday Madelief')

with open(file2, 'w') as file:
  file.write(filedata)

# Define subject replacements
subject_replacements = {
    f'{klas}ak': 'Aardrijkskunde',
    f'{klas}bl': 'Begeleidingslessen',
    f'{klas}du': 'Duits',
    f'{klas}ec': 'Economie',
    f'{klas}en': 'Engels',
    f'{klas}fa': 'Frans',
    f'{klas}gs': 'Geschiedenis',
    f'{klas}lo': 'Lichamelijke Opvoeding',
    f'{klas}mentor': 'Mentor',
    f'{klas}na': 'Natuurkunde',
    f'{klas}ne': 'Nederlands',
    f'{klas}o&o': 'Onderzoeken en Ontwerpen',
    f'{klas}sk': 'Scheikunde',
    f'{klas}wi': 'Wiskunde',
    f'oga3.tmc1, oh3.tmc1': 'TMC',
    f'oga3.tmc1\, oh3.tmc1' : 'TMC',
    f'oh3.tmc1, oga3.tmc1': 'TMC',
    f'oh3.tmc1\, oga3.tmc1' : 'TMC',
    f'oga3.bl2' : 'Begeleidingslessen',
    f'oga3.mentor2' : 'Mentor',
    f'Les - en' : 'Engels',
    f'Les - wi' : 'Wiskunde',
    f'Les - fa' : 'Frans',
    f'Les - ne' : 'Nederlands',
    f'Les - ec' : 'Economie',
    f'Les - sk' : 'Scheikunde',
    f'Les - na' : 'Natuurkunde',
    f'Les - gs' : 'Geschiedenis',
    f'Les - du' : 'Duits',
    f'Les - ak' : 'Aardrijkskunde',
}

# Perform all replacements
for old, new in subject_replacements.items():
    filedata = filedata.replace(old, new)

# Write the modified data back to the file
with open(file2, 'w') as file:
    file.write(filedata)

# Lokalen

# Define the ranges for replacements
ranges = {
    "be": (1, 300),
    "tm": (1, 300),
    "cc": (1, 99),
    "cb": (1, 200)
}

# Perform range-based replacements
for prefix, (start, end) in ranges.items():
    for i in range(start, end + 1):
        formatted_number = f"{i:03d}" if prefix in ["be", "tm", "cb"] else f"{i:02d}"
        filedata = filedata.replace(f"SUMMARY:{prefix}{formatted_number} - ", 'SUMMARY:')

# Define specific replacements
specific_replacements = [
    "SUMMARY:beuk3_gym - ",
    "SUMMARY:tm047_gym - ",
    "SUMMARY:tm046_gym - ",
    "SUMMARY:tm116_binask - ",
    "SUMMARY:tm128_tmc - ",
    "SUMMARY:tm145_o&o - ",
    "SUMMARY:tm146_o&o - ",
    "SUMMARY:cb012_gym - ",
    "SUMMARY:tm116_binask\, tm115_binask - ",
    "SUMMARY:tm034\, tm035 - ",
    "SUMMARY:tm208\, tm214\, tm137\, tm215 - ",
    "SUMMARY:tm208\, tm137\, tm214\, tm215 - ",
]

# Perform specific replacements
for replacement in specific_replacements:
    filedata = filedata.replace(replacement, 'SUMMARY:')

# Write the modified data back to the file
with open(file2, 'w') as file:
    file.write(filedata)

# Delete temporary file

if os.path.exists(file1):
  os.remove(file1)
else:
  print("The file does not exist")
