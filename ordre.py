import csv

def sort_csv_by_margin(input_csv, output_csv, margin_field_index=3):
    # Read the CSV file and sort it by the margin field (field 4, index 3) in descending order
    with open(input_csv, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=',')
        header = next(reader)  # Read the header
        data = list(reader)  # Read the rest of the data

        # Sort the data
        # If the margin is "N/A", put it at the end of the list
        data.sort(key=lambda row: (row[margin_field_index] == "N/A", 
                                   float(row[margin_field_index].replace('%', '')) if row[margin_field_index] != "N/A" else -1), 
                  reverse=True)

    # Write the sorted data to a new CSV file
    with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(header)  # Write the header
        writer.writerows(data)  # Write the sorted data

# Example usage
sort_csv_by_margin('output.csv', 'sorted_output.csv')
