import requests
from pprint import pprint

# response = requests.get('http://127.0.0.1:8000/api/v0/regions/')
# response = requests.get('http://127.0.0.1:8000/api/v0/skillsarray/')
# response = requests.get('http://127.0.0.1:8000/api/v0/queries/', auth=('test', 'test1234'))

token = '972d5a48c7f464b48d2e793a93c1498180c8de44'
headers = {'Authorization': f'Token {token}'}
# headers = {'Authorization': token} - не работает так
response = requests.get('http://127.0.0.1:8000/api/v0/queries/', headers=headers)
# response = requests.get('http://127.0.0.1:8000/api/v0/queries/') - без headers не работает
pprint(response.json())
print('Status code:', response.status_code)
