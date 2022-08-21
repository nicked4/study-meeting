from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes


if __name__ == '__main__':
    # Common key
    plain_text = b'Hello, world!'
    print(plain_text, end='\n\n')

    common_key = get_random_bytes(16)
    print(f'common_key: {common_key}')

    common_cipher = AES.new(common_key, AES.MODE_EAX)
    common_decoder = AES.new(common_key, AES.MODE_EAX, common_cipher.nonce)

    common_encoded_text = common_cipher.encrypt(plain_text)
    common_decoded_text = common_decoder.decrypt(common_encoded_text)
    print(common_encoded_text)
    print(common_decoded_text, end='\n\n')

    # Public key
    private_key = RSA.generate(2048)
    public_key = private_key.public_key()
    print(f'private_key: {private_key.export_key()}')
    print(f'public_key : {public_key.export_key()}', end='\n\n')

    private_cipher = PKCS1_OAEP.new(private_key)
    public_cipher = PKCS1_OAEP.new(public_key)

    public_encoded_text = public_cipher.encrypt(plain_text)
    public_decoded_text = private_cipher.decrypt(public_encoded_text)
    print(public_encoded_text)
    print(public_decoded_text, end='\n\n')

    # Check failed to decode with invalid keys
    try:
        public_cipher.decrypt(common_encoded_text)
    except ValueError:
        print(f'Failed to decrypt common_encoded_text with public key')

    try:
        public_cipher.decrypt(public_encoded_text)
    except TypeError:
        print(f'Failed to decrypt public_encoded_text with public key')

    try:
        assert common_decoder.decrypt(public_encoded_text) == plain_text
    except AssertionError:
        print(f'Failed to decrypt public_encoded_text with common key')
