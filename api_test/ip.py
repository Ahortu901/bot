import requests

ip = requests.get('https://api.ipify.org').text
print(f"My current IP address is: {ip}")
