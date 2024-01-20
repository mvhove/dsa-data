import csv

# maeve andersen
# 19 january 2024
# appends leading zeros to zips (dumb band-aid, fix this plz future me)
file_path = 'chapter_zips.csv'
output_rows = []

with open(file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        row['zip'] = row['zip'].zfill(5)
        output_rows.append(row)

with open(file_path, 'w', newline='') as file:
    fieldnames = ['zip', 'chapter']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the modified rows
    writer.writerows(output_rows)
