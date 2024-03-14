import requests

def send_get_request(url, show):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the content of the response
            if show:
                print("Response from", url, ":")
                print(response.text)
            data = interpret_data(response, show)
            return data
        else:
            print("Failed to get response from", url, ". Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

def interpret_data(response, show):
    data = response.json()

    if show:
        for item in data:
            if 'location_name' in item:
                for item in data:
                    # Depending on the structure of each item, handle it accordingly
                    if 'location_name' in item:
                        # This item represents location information
                        print("Location Name:", item['location_name'])
                        print("Description:", item['description'])
                        print("Voice Message:", item['voice_message'])
                        print("Coordinates (x, y, yaw):", item['x'], item['y'], item['yaw'])
                    else:
                        # This item represents coordinates
                        print("Coordinates (x, y, yaw):", item['x'], item['y'], item['yaw'])
    return data

# Example usage:
if __name__ == "__main__":
    url = "http://127.0.0.1:8080/locations"  # Replace this URL with the one you want to request
    response = send_get_request(url, True)