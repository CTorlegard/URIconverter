import pandas as pd
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO


# Load the CSV file into a DataFrame
df = pd.read_csv('results.csv')

# Get the name of the first column in the DataFrame
first_column = df.columns[0]

# Create a set to keep track of the image URIs that have already been processed
processed_images = set()

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Get the image URI from the row
    image_uri = row['image3']
    
    # Check if the image URI is not "null" or "nan"
    if pd.notnull(image_uri) and image_uri != "null":
        # Check if the image URI has not already been processed
        if image_uri not in processed_images:
            # Use the requests library to get the image data from the URI
            response = requests.get(image_uri)
            try:
                img = Image.open(BytesIO(response.content))
            except UnidentifiedImageError:
                print(f"Unable to open image: {image_uri}")
                continue
            
            # Get the value of the first column for this row
            first_column_value = row[first_column]
            
            # Convert the image to JPG and save it to a file with the same name as the first column value
            img.convert('RGB').save(f'G:/Shared drives/Shopify-images/{first_column_value}.jpg')
            
            # Update the row with the path to the saved image file
            df.at[index, 'image3'] = f'G:/Shared drives/Shopify-images/{first_column_value}.jpg'
            
            # Add the image URI to the set of processed images
            processed_images.add(image_uri)

# Save the updated DataFrame back to a CSV file
df.to_csv('G:/Shared drives/Shopify-images/converted csv/bq-dump-converted_19_06.csv', index=False)
