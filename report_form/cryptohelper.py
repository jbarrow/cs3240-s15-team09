from Crypto.Hash import MD5
import os, random, struct
from report_form.models import File
from Crypto.Cipher import AES

def get_file_checksum(filename):
	h= MD5.new()
	chunk_size = 8192
	with open(filename, 'rb') as f:
		while True:
			chunk = f.read(chunk_size)
			if len(chunk) == 0:
				break
			h.update(chunk)
		return h.hexdigest()

def encrypt_file_helper(in_file, key):
	#http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto
# she is using the file objects directly, which explains why it doesn't work
# trying to read the file early on with the call to read to get the bytes of the object
	output_name = os.path.basename(in_file) # this is actually the full path for retrieval
	output_name = output_name + ".enc"
	filesize = os.path.getsize(in_file)
	#iv = ''.join(chr(random.randint(0, 0xFF))) for i in range(16))
	encryptor = AES.new(key, AES.MODE_CBC, iv)
	with open(in_file, 'rb') as input_file:
		with open(out_file, 'wb') as output_file:
			output_file.write(struct.pack('<Q', filesize)) # little endian unsigned long long
			output_file.write(iv)
			while True:
				chunk= input_file.read()