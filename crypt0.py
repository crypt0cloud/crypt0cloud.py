import time
import nacl.signing
import base64
import json
import hashlib


class Crypt0graphy:
    def signTransaction(self, t, key):
        jsonstr = json.dumps(t)
        contentbytes = jsonstr.encode("UTF-8")
        t["Content"] = self.base64Encode(contentbytes)

        m = hashlib.sha256()
        m.update(contentbytes)
        hash = m.digest()
        t["Hash"] = self.base64Encode(hash)
        signature = key.sign(hash)
        t["Sign"] = self.base64Encode(signature[:64]) # 64 for the sign size, the stored value is the combined sign

        t["Signer"] = self.base64Encode(bytes(key.verify_key))
        return t

    def base64Encode(self, bytearray):
        base64_bytes = base64.b64encode(bytearray)
        return base64_bytes.decode("UTF-8")

    def base64Decode(self, str):
        message_bytes = str.encode("UTF-8")
        return base64.b64decode(message_bytes)

    def newSigningKey(self):
        return nacl.signing.SigningKey.generate()

    def signingKeyFromBase64(self, public, secret):
        return CCSigningKey(public, secret)

    def currentMilis(self):
        return round(time.time()*1000.0)

class CCSigningKey(nacl.signing.SigningKey):
    def __init__(self, public, secret):
        cry = Crypt0graphy()
        secret_key = cry.base64Decode(secret)
        public_key = cry.base64Decode(public)

        self._signing_key = secret_key
        self.verify_key = nacl.signing.VerifyKey(public_key)

    def __bytes__(self):
        return self._signing_key

    def __hash__(self):
        return hash(bytes(self))