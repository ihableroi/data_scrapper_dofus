import csv

def calculate_recipe_prices(recipes_file, prices_file, output_file):
    # Load resource prices and current market prices from the prices file
    resource_prices = {}
    item_market_prices = {}

    with open(prices_file, 'r', encoding='utf-8') as prices_csv:
        prices_reader = csv.reader(prices_csv, delimiter=',')
        next(prices_reader)  # Skip the header row
        for row in prices_reader:
            if len(row) < 5:
                continue  # Skip invalid rows
            try:
                resource = row[0].strip()
                price = float(row[4].replace(',', '.'))  # Handle comma as decimal separator
                resource_prices[resource] = price
                item_market_prices[resource] = price
            except ValueError:
                print(f"Skipping invalid price entry: {row}")

    # Process recipes and calculate total prices
    with open(recipes_file, 'r', encoding='utf-8') as recipes_csv, open(output_file, 'w', encoding='utf-8', newline='') as output_csv:
        recipes_reader = csv.reader(recipes_csv, delimiter=',')
        output_writer = csv.writer(output_csv, delimiter=',')

        # Write header for the output file
        output_writer.writerow(["Item Name", "Total Price", "Current Market Price", "Margin", 
                               "Resource Type 1", "Unit Price 1", "Quantity 1", "Resource Cost 1",
                               "Resource Type 2", "Unit Price 2", "Quantity 2", "Resource Cost 2",
                               "Resource Type 3", "Unit Price 3", "Quantity 3", "Resource Cost 3",
                               "Resource Type 4", "Unit Price 4", "Quantity 4", "Resource Cost 4"])

        for row in recipes_reader:
            if len(row) < 3:
                continue  # Skip invalid rows

            item_name = row[0].strip()
            total_price = 0
            resource_details = []  # List to store resource details for the current item

            # Check for current market price
            current_market_price = item_market_prices.get(item_name, None)

            if current_market_price is None:
                print(f"Current market price not found for: {item_name}")

            # Collect the detailed information for each resource used in the recipe
            for i in range(1, len(row), 2):
                resource_type = row[i].strip()
                if i + 1 >= len(row):
                    break  # No quantity specified
                try:
                    quantity = int(row[i + 1])
                except ValueError:
                    quantity = 0  # Default to 0 if quantity is invalid

                if resource_type in resource_prices:
                    unit_price = resource_prices[resource_type]
                    resource_cost = unit_price * quantity
                    total_price += resource_cost

                    # Append the resource details to the resource_details list
                    resource_details.append([resource_type, f"{unit_price:.2f}", quantity, f"{resource_cost:.2f}"])
                else:
                    print(f"Resource '{resource_type}' not found in prices file.")

            # Prepare the output row with the item name, total price, current market price, and margin
            output_row = [item_name, f"{total_price:.2f}", 
                          f"{current_market_price:.2f}" if current_market_price is not None else 'N/A',
                          f"{(current_market_price- total_price) / total_price:.2%}" if current_market_price is not None and total_price > 0 else 'N/A']

            # Add resource details as additional columns
            for detail in resource_details:
                output_row.extend(detail)

            # Pad the output row with empty strings if there are fewer details than expected
            while len(output_row) < 20:  # Adjust based on the number of expected columns
                output_row.append('')

            # Write the single row to the output file
            output_writer.writerow(output_row)

# Example usage:
calculate_recipe_prices('recipes.csv', 'prices.csv', 'output.csv')
