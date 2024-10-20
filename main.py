import phonenumbers
from opencage.geocoder import OpenCageGeocode
import folium
from coordinates import coordinates  # Ensure this file has a valid coordinates dictionary

default_region = "IN"
api_key = 'c1af42d5c2c24dff8ad301b140c52503'  # Replace with your actual API key

def main():
    # Get user input for the phone number
    number = input("Enter a phone number (e.g., +917676164663): ")
    try:
        # Parse the phone number
        pepnumber = phonenumbers.parse(number, default_region)
        print(f"Country Code: {pepnumber.country_code}, National Number: {pepnumber.national_number}")

        # Get the region based on the phone number
        region = phonenumbers.region_code_for_number(pepnumber)
        print(f'The region for the phone number is: {region}')

        # Get coordinates for the region
        if region in coordinates:
            latitude, longitude = coordinates[region]
        else:
            print("Region not found in coordinates.Defaulting to provided coordinates.")
            latitude, longitude = 0,0 # Default to India's central coordinates

        # Geocoding the coordinates
        geocoder = OpenCageGeocode(api_key)
        result = geocoder.reverse_geocode(latitude, longitude)

        if result:
            place = result[0]
            print(f"Address: {place['formatted']}")

            # Creating a map centered around the coordinates
            myMap = folium.Map(location=[latitude, longitude], zoom_start=6)
            folium.Marker([latitude, longitude], popup=place['formatted']).add_to(myMap)

            # Save the map
            myMap.save("mylocation.html")
            print("Map saved as 'mylocation.html'.")
        else:
            print("No results found for the given coordinates.")
    except phonenumbers.NumberParseException as e:
        print(f'Error parsing phone number: {e}')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
