import requests
import csv
from io import StringIO
def get_water_price(total_water_volume):
    # Get the input amount from the user and convert it to a float
    #input_amount = float(input("Please input how much water (ml) do you use: "))

    csv_url = "https://www.water.gov.tw/opendata/prop8.csv"

    try:
        response = requests.get(csv_url)
        response.raise_for_status()  # Check for a successful response

        csv_content = response.text
        csv_file = StringIO(csv_content)

        # Use the csv.reader to parse the CSV content
        csv_reader = csv.reader(csv_file)

        # Use list comprehension to extract the last row as a list
        content_list = [row for row in csv_reader]

        # Extract the desired element (e.g., the third element from the last row)
        desired_element = float(content_list[-1][2])

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch CSV: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Perform the calculation with the converted input_amount
    return float(total_water_volume * 0.001 * 0.001) * desired_element