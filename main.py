from google.cloud import bigquery
from google.cloud import storage
from PIL import Image, UnidentifiedImageError
import pandas as pd
import requests
from io import BytesIO

# Constants
BUCKET_NAME = 'shopify-converted-images'

def bq_to_gcs(event, context):
    # Authenticate with the service account using the Cloud Function's default service account
    bq_client = bigquery.Client()
    storage_client = storage.Client()

    # BigQuery query to fetch data
    query = """
    SELECT
        FORMAT(Product_Sku) AS sku,
        Product_title AS title,
        Product_Barcode AS barcode,
        Product_Variant_Title AS size,
        SPLIT(images, ',')[SAFE_ORDINAL(3)] AS image3
    FROM `alohas-shopify.ialohas_shopify.PRODUCTS_COREVIEW`
    LIMIT 500000
    OFFSET 178
    """
    df = bq_client.query(query).to_dataframe()

    # Create a set to keep track of the image URIs that have already been processed
    processed_images = set()

    # Create a Cloud Storage bucket object
    bucket = storage_client.bucket(BUCKET_NAME)

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
                first_column_value = row['sku']

                # Convert the image to JPG and upload it to Cloud Storage
                img_bytes_io = BytesIO()
                img.convert('RGB').save(img_bytes_io, format='JPEG')
                img_bytes_io.seek(0)
                blob = bucket.blob(f'converted-images/{first_column_value}.jpg')
                blob.upload_from_file(img_bytes_io, content_type='image/jpeg')

                # Add the image URI to the set of processed images
                processed_images.add(image_uri)

    print("Images uploaded to Google Cloud Storage")

# Deploying function - Deployment details will be handled using the 'gcloud' CLI
