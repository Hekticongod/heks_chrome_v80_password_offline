import json
import base64

def extract_encrypted_key(local_state_path):
    with open(local_state_path, 'r') as file:
        local_state = json.load(file)
    
    encrypted_key = local_state['os_crypt']['encrypted_key']
    return encrypted_key

# Path to the Local State file
local_state_path = '/media/kali/CF48AD8E7F3395EC/Users/Owner/AppData/Local/Google/Chrome/User Data/Local State'

# Extract and print the encrypted key
encrypted_key = extract_encrypted_key(local_state_path)
print("Encrypted Key:", encrypted_key)
