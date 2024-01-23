import csv
import pandas as pd

# Open the text file and the output CSV files
with open('descriptions.txt', 'r') as txt_file, \
     open('subjects_output.csv', 'w', newline='') as subjects_csv_file, \
     open('styles_output.csv', 'w', newline='') as styles_csv_file, \
     open('additional_output.csv', 'w', newline='') as additional_csv_file:

    subjects_writer = csv.writer(subjects_csv_file)
    styles_writer = csv.writer(styles_csv_file)
    additional_writer = csv.writer(additional_csv_file)

    # Write the headers
    subjects_writer.writerow(['Subject'])
    styles_writer.writerow(['Style'])
    additional_writer.writerow(['Additional'])

    # Process each line in the text file
    for line in txt_file:
        # Initialize additional info as empty
        additional_info = ''
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
        else:
            # If 'in the style of' is not in the line, write the whole line to the subjects file
            subjects_writer.writerow([line.strip()])
            continue  # Skip writing to the additional file if 'in the style of' is not present

        # Write the additional information into the additional CSV file
        # Check if there is any additional info to write
        if additional_info:
            additional_writer.writerow([additional_info.strip()])

# Load the data from the CSV files
df1 = pd.read_csv('subjects_output.csv')
df2 = pd.read_csv('styles_output.csv')
df3 = pd.read_csv('additional_output.csv')

# Use the concat() function to combine the dataframes along the column axis
combined_df = pd.concat([df1, df2, df3], axis=1)

# Save the combined dataframe to a new CSV file
combined_df.to_csv('combined.csv', index=False)