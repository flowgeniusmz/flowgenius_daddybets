import json
import os
import requests

def write_json_to_file(json_data, file_path='odds.json'):
    """
    Writes the provided JSON data to the specified file.
    
    Parameters:
    json_data (dict): The JSON data to write to the file.
    file_path (str): The path to the file where the data will be written.
    """
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

def read_json_from_file(file_path='odds.json'):
    """
    Reads JSON data from the specified file and returns it as a Python dictionary.
    
    Parameters:
    file_path (str): The path to the file to read the data from.
    
    Returns:
    dict: The JSON data read from the file.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        return json_data
    return None

def get_or_fetch_json(url, file_path='odds.json'):
    """
    Checks if JSON data exists in the specified file. If not, fetches the data from the given URL,
    writes it to the file, and then returns the data.
    
    Parameters:
    url (str): The URL to fetch the JSON data from if not found in the file.
    file_path (str): The path to the file to check for existing data and to write new data.
    
    Returns:
    dict: The JSON data either read from the file or fetched from the URL.
    """
    json_data = read_json_from_file(file_path)
    if json_data is None:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            write_json_to_file(json_data, file_path)
        else:
            raise Exception(f"Failed to fetch data from URL: {url} (Status code: {response.status_code})")
    return json_data

# Example usage:
# url = 'https://api.example.com/odds'
# data = get_or_fetch_json(url)
# print(data)