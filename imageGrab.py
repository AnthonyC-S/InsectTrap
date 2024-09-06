import requests
import csv

# Define the API endpoint for iNaturalist
api_url = "https://api.inaturalist.org/v1/observations"

insectDict = {'Asian Lady Beetle':'48484',
    'Stink Bug':'47742',
    'Japanese Beetle':'67760',
    'Spotted Lanternfly':'324726',
    'Potato Beetle':'84189',
    'Common House Fly':'120156',
    'Common House Spider':'120583',
    'Wolf Spider':'47416',
    'Bee':'630955',
    'Hoverfly':'49995',
    'Earwigs':'47793',
    'Gypsy Moth':'47802',
    'Corn Earworm Moth':'118492',
    'Grasshopper':'47651',
    'Ground Beetle':'49567',
    'Wasp':'52747',
    'Harvestman':'47367',
    'Crane Fly':'179916',
    'Root Maggot':'49996',
    'Apple Maggot':'366909'}

def writeCSV():
    wa = 'w' # read or write variable
    for taxonName in insectDict:
        taxonID = insectDict[taxonName]
        # Parameters to filter research-grade observations and limit to 100 results
        params = {
            'taxon_id': taxonID,
            'quality_grade': 'research',
            'page': 1,
            'per_page': 100,
            'order_by': 'date_added',
            'order': 'desc',
            'photos': []
        }
        # Send a GET request to the API
        response = requests.get(api_url, params=params)
        data = response.json()
        openCSV(data, wa, taxonName)
        wa = 'a'
        print(f"Added {taxonName} to CSV file")

def openCSV(data, wa, taxonName):
    # Open a CSV file to save the image links
    csv_name = 'inaturalist_images.csv'
    with open(csv_name, wa, newline='') as csvfile:
        writer = csv.writer(csvfile)
        if wa == 'w':
            writer.writerow(['Image URL', 'Taxon'])  # Add the column headers
        if True:
            # Loop through each observation and extract the image URLs and taxon names
            for observation in data['results']:
                if observation.get('photos'):
                    for photo in observation['photos']:
                        image_url = photo.get('url')
                        if image_url:
                            # Replace the suffix in the URL to get the medium-sized image
                            medium_image_url = image_url.replace('square', 'medium')
                            taxon_id = taxonName#observation['taxon']['id']  # Get the taxon ID
                            # Write the image URL and taxon name to the CSV file
                            writer.writerow([medium_image_url, taxon_id])