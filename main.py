import csv
import pandas as pd
import re

# Open the text file and the output CSV files
with open('descriptions.txt', 'r') as txt_file, \
     open('subjects_output.csv', 'w', newline='') as subjects_csv_file, \
     open('styles_output.csv', 'w', newline='') as styles_csv_file, \
     open('core_output.csv', 'w', newline='') as core_csv_file, \
     open('punk_output.csv', 'w', newline='') as punk_csv_file, \
     open('wave_output.csv', 'w', newline='') as wave_csv_file, \
     open('resolution_output.csv', 'w', newline='') as resolution_csv_file, \
     open('real_output.csv', 'w', newline='') as real_csv_file, \
     open('quality_output.csv', 'w', newline='') as quality_csv_file, \
     open('additional_output.csv', 'w', newline='') as additional_csv_file:

    subjects_writer = csv.writer(subjects_csv_file)
    styles_writer = csv.writer(styles_csv_file)
    core_writer = csv.writer(core_csv_file)
    punk_writer = csv.writer(punk_csv_file)
    wave_writer = csv.writer(wave_csv_file)
    resolution_writer = csv.writer(resolution_csv_file)
    real_writer = csv.writer(real_csv_file)
    quality_writer = csv.writer(quality_csv_file)
    additional_writer = csv.writer(additional_csv_file)

    # Write the headers
    subjects_writer.writerow(['Subject'])
    styles_writer.writerow(['Style'])
    core_writer.writerow(['Core'])
    punk_writer.writerow(['Punk'])
    wave_writer.writerow(['Wave'])
    resolution_writer.writerow(['Resolution'])
    real_writer.writerow(['Real'])
    quality_writer.writerow(['Quality'])
    additional_writer.writerow(['Additional'])

    # Process each line in the text file
    for line in txt_file:
        # Skip blank lines
        if not line.strip():
            continue

        # Initialize additional info as empty
        additional_info = ''
        core_info = ''
        punk_info = ''
        wave_info = ''
        resolution_info = ''
        real_info = ''
        quality_info = ''
        # Check if '--ar' is in the line and split the line to exclude it
        if '--ar' in line:
            line, _ = line.split('--ar', 1)
        # Check if 'in the style of' is in the line
        if 'in the style of' in line:
            # Split the line into subject, style, and additional info at 'in the style of'
            subject_part, rest_of_line = line.split('in the style of', 1)
            style_part, additional_info = rest_of_line.split(',', 1)
            # Write the subject and style information into the respective CSV files
            subjects_writer.writerow([subject_part.strip()])
            styles_writer.writerow(['in the style of ' + style_part.strip()])

            # Search for phrases containing "hd", "uhd", "quality", "photo"
            words = additional_info.split(',')
            keywords = ['hd', 'uhd', 'quality', 'photo']
            for word in words:
                if any(keyword in word for keyword in keywords):
                    quality_info += word.strip() + ','
                    words.remove(word)
                elif 'core' in word:
                    core_info = word.strip()
                    words.remove(word)
                elif 'punk' in word:
                    punk_info = word.strip()
                    words.remove(word)
                elif 'wave' in word:
                    wave_info = word.strip()
                    words.remove(word)
                elif re.search(r'\d+k', word.strip()):
                    resolution_info = word.strip()
                    words.remove(word)
                elif 'real' in word:
                    real_info = word.strip()
                    words.remove(word)
            additional_info = ','.join(words).strip()
            quality_info = quality_info.rstrip(',')
        else:
            # If 'in the style of' is not in the line, write the whole line to the subjects file
            subjects_writer.writerow([line.strip()])
            continue  # Skip writing to the additional file if 'in the style of' is not present

        # Write the core, punk, wave, resolution, real, and quality information into the respective CSV files
        core_writer.writerow([core_info])
        punk_writer.writerow([punk_info])
        wave_writer.writerow([wave_info])
        resolution_writer.writerow([resolution_info])
        real_writer.writerow([real_info])
        quality_writer.writerow([quality_info])
        # Write the additional information into the additional CSV file
        additional_writer.writerow([additional_info])

# Load the data from the CSV files
df1 = pd.read_csv('subjects_output.csv')
df2 = pd.read_csv('styles_output.csv')
df3 = pd.read_csv('core_output.csv')
df4 = pd.read_csv('punk_output.csv')
df5 = pd.read_csv('wave_output.csv')
df6 = pd.read_csv('resolution_output.csv')
df7 = pd.read_csv('real_output.csv')
df8 = pd.read_csv('quality_output.csv')
df9 = pd.read_csv('additional_output.csv')

# Use the concat() function to combine the dataframes along the column axis
combined_df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9], axis=1)

# Save the combined dataframe to a new CSV file
combined_df.to_csv('combined.csv', index=False)