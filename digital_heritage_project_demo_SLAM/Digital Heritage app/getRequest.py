import requests

def send_get_request(url):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the content of the response
            print("Response from", url, ":")
            print(response.text)
        else:
            print("Failed to get response from", url, ". Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

# Example usage:
if __name__ == "__main__":
    url = "http://127.0.0.1:8080/updatecurrent"  # Replace this URL with the one you want to request
    send_get_request(url)