import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Load the CSV file into a DataFrame
df = pd.read_csv('bq-dump3.csv')

# Get the name of the first column in the DataFrame
first_column = df.columns[0]

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Get the image URI from the row
    image_uri = row['main_image']
    
    # Use the requests library to get the image data from the URI
    response = requests.get(image_uri)
    img = Image.open(BytesIO(response.content))
    
    # Get the value of the first column for this row
    first_column_value = row[first_column]
    
    # Convert the image to JPG and save it to a file with the same name as the first column value
    img.convert('RGB').save(f'G:\My Drive/bq-dump-converted-images/{first_column_value}.png')
    
    # Update the row with the path to the saved image file
    df.at[index, 'main_image'] = f'G:\My Drive/bq-dump-converted-images/{first_column_value}.png'

# Save the updated DataFrame back to a CSV file
df.to_csv('G:\My Drive/bq-dump-converted-csv/bq-dump-png4-converted.csv', index=False)
