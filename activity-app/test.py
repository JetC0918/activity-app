import requests

url = 'http://localhost:5000/question'
question = "What materials do I need for the Family Picnic?"
data = {'question': question} 
 
response = requests.post(url, json=data)

# Print raw response details
print("Response status code:", response.status_code)
print("Response content:", response.text)  # Don't parse as JSON yet, just print raw text

# If status code is OK, only then parse JSON
if response.status_code == 200:
    try:
        print("Response JSON:", response.json())
    except requests.exceptions.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
