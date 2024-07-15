import base64
import json
import ctypes
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

def dpapi_decrypt(encrypted):
    # Decrypting using Windows DPAPI
    buffer_in = ctypes.c_buffer(encrypted, len(encrypted))
    buffer_out = ctypes.c_buffer(len(encrypted))
    length = ctypes.c_int(len(encrypted))
    result = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(buffer_in),
        None,
        None,
        None,
        None,
        0,
        ctypes.byref(buffer_out)
    )
    if not result:
        raise ValueError("Decryption using DPAPI failed")
    return buffer_out.raw

def aes_decrypt(encrypted_key):
    encrypted_key = base64.b64decode(encrypted_key)
    encrypted_key = encrypted_key[5:]  # remove DPAPI prefix
    decrypted_key = dpapi_decrypt(encrypted_key)
    return decrypted_key

def extract_master_key(local_state_path):
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = json.load(file)
    encrypted_key = local_state['os_crypt']['encrypted_key']
    decrypted_key = aes_decrypt(encrypted_key)
    return decrypted_key

if __name__ == '__main__':
    local_state_path = '/media/kali/CF48AD8E7F3395EC/Users/Owner/AppData/Local/Google/Chrome/User Data/Local State'
    try:
        master_key = extract_master_key(local_state_path)
        print("Master Key:", master_key)
    except Exception as e:
        print(f"An error occurred: {e}")
