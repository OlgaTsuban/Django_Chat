import requests

# # Assuming you have the authentication token
# token = "95ab01406ce7cbcda11665afaa7f797cccc85983"

# # Make a GET request to the profile endpoint with the token in the headers
# response = requests.get("http://127.0.0.1:8000/user/profile/", headers={"Authorization": f"Token {token}"})

# # Print the response status code and content
# print(response.status_code)
# if response.text:
#     print(response.text)
#     try:
#         print(response.json())
#     except ValueError as e:
#         print("Failed to parse JSON:", e)
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(os.path.join(BASE_DIR, 'img'))