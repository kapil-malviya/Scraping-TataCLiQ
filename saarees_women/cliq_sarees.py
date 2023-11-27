'''
sarees_for_women

'''


import subprocess
import csv
import json

for i in range(0, 350):

    # Define the base curl command
    curl_command = [
        'curl',
        f'https://searchbff.tatacliq.com/products/mpl/search?searchText=%3Arelevance%3Acategory%3AMSH1012102%3AinStockFlag%3Atrue&isKeywordRedirect=false&isKeywordRedirectEnabled=false&channel=WEB&isMDE=true&isTextSearch=false&isFilter=false&qc=false&test=invizbff.qpsv3-inviz.ab&page={i}&mcvid=40428844743522272003612757795264414381&customerId=&isSuggested=false&isPwa=true&pageSize=40&typeID=all',

    ]

    # Run the curl command using subprocess
    response = subprocess.run(curl_command, capture_output=True, text=True)

    # Check if the curl command was successful (return code 0)
    if response.returncode == 0:
        data = json.loads(response.stdout)  # Parse JSON data
        results = []  # Define the 'results' list

        # Process the data as needed
        if 'searchresult' in data:
            products = data['searchresult']

            # Iterate through the list of products
            for product in products:
                brand = product.get('brandname', '')
                title = product.get('productname', '')
                selling_price = product.get('price', {}).get('sellingPrice', {}).get('formattedValue', '')
                mrp_price = product.get('price', {}).get('mrpPrice', {}).get('formattedValue', '')
                average_rating = product.get('averageRating', '')
                rating_count = product.get('ratingCount', '')
                web_url = product.get('webURL', '')

                # Create a dictionary for each product and add it to the results list
                result = {
                    "Brand": brand,
                    "Title": title,
                    "Selling Price": selling_price,
                    "MRP Price": mrp_price,
                    "Average Rating": average_rating if average_rating else 0,
                    "Rating Count": rating_count,
                    "Web URL": "https://www.tatacliq.com" + web_url
                }
                results.append(result)

            # Save the extracted data to a CSV file
            with open("sarees_for_women.csv", "a", newline='', encoding="utf-8") as csvfile:
                fieldnames = ["Brand", "Title", "Selling Price", "MRP Price", "Average Rating", "Rating Count", "Web URL"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Do not write header in each iteration, write it only once outside the loop
                if i == 0:
                    writer.writeheader()

                # Write each product's data to the CSV file
                for product in results:
                    writer.writerow(product)

            print(f"Data for page {i} has been saved")

        else:
            print(f"Response format for page {i} is not as expected")

    else:
        print(f"curl command for page {i} failed with error:\n{response.stderr}")
