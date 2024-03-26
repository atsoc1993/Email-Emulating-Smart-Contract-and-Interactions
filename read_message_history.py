import base64
import requests

node_url = 'https://testnet-idx.algonode.cloud'
transactions_endpoint = '/v2/transactions?'
app_id = 628544102
application_endpoint = f'application-id={app_id}'

complete_url = node_url + transactions_endpoint + application_endpoint

response = requests.get(complete_url)
transactions = response.json()['transactions']

original_message = ''
index_cursor = -1
for t in transactions:
    app_transaction = t.get('application-transaction', {})
    app_args = app_transaction.get('application-args', [])
    if app_args and app_args[0] == '8A7DRA==':
        last_index = int.from_bytes(base64.b64decode(t['logs'][0]),'little')
        if last_index <= index_cursor:
            index_cursor = 0
            original_message = ''
            print(original_message)
            break
        index_cursor += 1
        full_message = base64.b64decode(t['logs'][1])
        original_message += full_message.decode()
        
print(original_message)

