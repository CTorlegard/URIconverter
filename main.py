import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Load the CSV file into a DataFrame
df = pd.read_csv('your_file.csv')

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Get the image URI from the row
    image_uri = row['image_uri']
    
    # Use the requests library to get the image data from the URI
    response = requests.get(image_uri)
    img = Image.open(BytesIO(response.content))
    
    # Convert the image to JPG and save it to a file
    img.convert('RGB').save(f'image_{index}.jpg')
    
    # Update the row with the path to the saved image file
    df.at[index, 'image_path'] = f'image_{index}.jpg'

# Save the updated DataFrame back to a CSV file
df.to_csv('your_file.csv', index=False)
