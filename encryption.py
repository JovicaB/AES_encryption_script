from cryptography.hazmat.primitives import hashes, hmac, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import json
import base64


class Encryption:
    def __init__(self, key):
        if isinstance(key, str):
            key = key.encode('utf-8')

        if len(key) not in (16, 24, 32):
            raise ValueError("AES key must be either 16, 24, or 32 bytes long.")

        self.key = key
        self.backend = default_backend()

    def encrypt(self, data: dict) -> dict:
        # Serijalizuj podatke u JSON i enkoduj u bajtove
        plaintext = json.dumps(data).encode('utf-8')

        # Dodaj padding (AES blok veličina je 128 bita = 16 bajtova)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        # Generiši slučajni IV
        iv = os.urandom(16)

        # Enkripcija
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # HMAC za proveru integriteta
        h = hmac.HMAC(self.key, hashes.SHA256(), backend=self.backend)
        h.update(iv + ciphertext)
        tag = h.finalize()

        # Vrati sve kao base64 stringove (da možeš da čuvaš ili šalješ)
        return {
            'iv': base64.b64encode(iv).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'hmac': base64.b64encode(tag).decode('utf-8')
        }

    def decrypt(self, encrypted_data: dict) -> dict:
        iv = base64.b64decode(encrypted_data['iv'])
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        tag = base64.b64decode(encrypted_data['hmac'])

        # Provera HMAC
        h = hmac.HMAC(self.key, hashes.SHA256(), backend=self.backend)
        h.update(iv + ciphertext)
        h.verify(tag)  # Baciće grešku ako verifikacija ne uspe

        # Dekripcija
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Ukloni padding
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return json.loads(plaintext.decode('utf-8'))



### usage ###
# key = "AbascuS@800144!!"
# encryptor = Encryption(key)

# data = {
#     "komitent": "Firma d.o.o.",
#     "invoice_number": "INV-2025-0001",
#     "date": "2025-04-11",
#     "invoice_value": "1250.00",
#     "note": "Plaćanje u roku od 15 dana."
# }

# encrypted = encryptor.encrypt(data)
# print("Encrypted:", encrypted)

# decrypted = encryptor.decrypt(encrypted)
# print("Decrypted:", decrypted)
