#1
# Sets a default curve (secp256k1)
import random, io, json, shelve, base64
from pprint import pprint
from umbral import pre, keys, config, signing
from PIL import Image

config.set_default_curve()

#2
# Generate an Umbral key pair
# ---------------------------
# First, Let's generate two asymmetric key pairs for Alice:
# A delegating key pair and a Signing key pair.

#alices_private_key = "empty"
#alices_public_key = "empty"
try:
    with open("python/proxy/privateKey.txt") as f:
        # alices_private_key = keys.UmbralPrivateKey.gen_key()
        # alices_public_key = alices_private_key.get_pubkey()
        # alpkey_bytes = bytes(alices_private_key)
        # f.write(alpkey_bytes)
        # f.write("%d\r\n" % alices_public_key)
        fl = f.readlines()
        for x in fl:
            pprint(x)
except IOError as x:
    pprint("!!!!python/proxy/privateKey.txt  does not exist" )
    with open("python/proxy/privateKey.txt",'w+',encoding = 'utf-8') as fnew:
        alices_private_key = keys.UmbralPrivateKey.gen_key()
        alices_public_key = alices_private_key.get_pubkey()
        fnew.write(alices_private_key)
        fnew.write("%d\r\n" % alices_public_key)

alices_private_key = keys.UmbralPrivateKey.gen_key()
alices_public_key = alices_private_key.get_pubkey()
alices_signing_key = keys.UmbralPrivateKey.gen_key()
alices_verifying_key = alices_signing_key.get_pubkey()
alices_signer = signing.Signer(private_key=alices_signing_key)
#3
# Encrypt some data for Alice
# ---------------------------
# Now let's encrypt data with Alice's public key.
# Invocation of `pre.encrypt` returns both the `ciphertext`,
# and a `capsule`. Anyone with Alice's public key can perform
# this operation.
with open("python/proxy/23.jpg", "rb") as imageFile:
  f = imageFile.read()
  plaintext = bytes(f) 

# plaintext = b'Proxy Re-encryption is cool!' 
# print(plaintext)
ciphertext, capsule = pre.encrypt(alices_public_key, plaintext) 

#4
# Decrypt data for Alice
# ----------------------
# Since data was encrypted with Alice's public key,
# Alice can open the capsule and decrypt the ciphertext with her private key.

cleartext = pre.decrypt(ciphertext=ciphertext,
                        capsule=capsule,
                        decrypting_key=alices_private_key)

image_cleartext = Image.open(io.BytesIO(cleartext))
image_cleartext.save("python/proxy/232.jpg")
# print(cleartext)

#5
# Bob Exists
# -----------

bobs_private_key = keys.UmbralPrivateKey.gen_key()
bobs_public_key = bobs_private_key.get_pubkey()

#6
# Bob receives a capsule through a side channel (s3, ipfs, Google cloud, etc)
bob_capsule = capsule

 
#8
# Alice grants access to Bob by generating kfrags 
# -----------------------------------------------
# When Alice wants to grant Bob access to open her encrypted messages, 
# she creates *threshold split re-encryption keys*, or *"kfrags"*, 
# which are next sent to N proxies or *Ursulas*. 
# She uses her private key, and Bob's public key, and she sets a minimum 
# threshold of 10, for 20 total shares

kfrags = pre.generate_kfrags(delegating_privkey=alices_private_key,
                             signer=alices_signer,
                             receiving_pubkey=bobs_public_key,
                             threshold=10,
                             N=20)
 
#9
# Ursulas perform re-encryption
# ------------------------------
# Bob asks several Ursulas to re-encrypt the capsule so he can open it. 
# Each Ursula performs re-encryption on the capsule using the `kfrag` 
# provided by Alice, obtaining this way a "capsule fragment", or `cfrag`.
# Let's mock a network or transport layer by sampling `threshold` random `kfrags`,
# one for each required Ursula.

import random

kfrags = random.sample(kfrags,  # All kfrags from above
                       10)      # M - Threshold

# Bob collects the resulting `cfrags` from several Ursulas. 
# Bob must gather at least `threshold` `cfrags` in order to activate the capsule.

bob_capsule.set_correctness_keys(delegating=alices_public_key,
                                 receiving=bobs_public_key,
                                 verifying=alices_verifying_key)
# print("kfrags:", f'{kfrags}')
# for line in sys.stdin:
# dict = [{'delegating': alices_public_key},{'receiving': bobs_public_key},{'verifying': alices_verifying_key}]
alic_pub_byte = io.BytesIO(alices_public_key)
apb_64 = base64.encodestring(alic_pub_byte)
# dict = [alices_public_key, bobs_public_key, alices_verifying_key]
# print  str (dict)
# t = json.dumps(dict) # '[1, 2, [3, 4]]'
# pprint(t)
# pprint(str(dict))
# print(json.dumps(json.loads(text)) 
# pprint(r)
# pprint(json.dumps(json.loads(str({"('delegating',)": alices_public_key}))) 
# pprint(json.dumps(json.loads(str(bobs_public_key)))
# pprint(f'{"delegating": {alices_public_key}}')
# pprint(f'{"receiving": {bobs_public_key}}')
# pprint(f'{"verifying": {alices_verifying_key}}')
# pprint(f"capsule: bob_capsule")
shelf = shelve.open('mydata')  # open for reading and writing, creating if nec
shelf.update({'one':1, 'two':2, 'three': {'three.1': 3.1, 'three.2': 3.2 }})
shelf.close()

shelf = shelve.open('mydata')
# print shelf
shelf.close()