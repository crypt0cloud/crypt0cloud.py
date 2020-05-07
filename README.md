# crypt0cloud.py
To know how to use the library refer to the libraries [How to](https://github.com/crypt0cloud/howto).

## Installing
Copy the *.py files in your project and import them as this

## Init the library

### Import the library
```python
import crypt0
import crypt0cloud
```

### Create an instance of the client library
```python
crypto_node = "yournode.nodes.crypt0.cloud"
cc = crypt0cloud.CryptoCloud(crypto_node)
```

### Create an instance of the application keys
```python
appkey_publickeyb64 = "soIHp6EMj7g+TplELyAkfJbFasdfdJqsRDyas0u1zbU="
appkey_secretkeyb64 = "0s84RY+zPcaHfysh3nDrtFeDmbbys0AasdfixIbtAfmyggenoQyPuD5OmUQvICR8lsWm44t0mqxEPJqzS7XNtQ=="
appkey_callback = "https://www.un.org/crypt0cloud_callback"
appkey = cry.signingKeyFromBase64(appkey_publickeyb64,appkey_secretkeyb64)
```

## Create an signing key
```python
keys, insertion_transaction = cc.CreateKey("Key identifier")
# keys are the cryptographic keys
# insertion_transaction is the transaction where the keys was inserted in crypt0.cloud
```

## Groups

### Creation of a group
```python
payload = "Investigation id=12345"
kind_list = ["prove", "veredict", "filling", "notification"]
gr = cc.CreateGroup(payload, kind_list, appkey, appkey_callback)
```

### Creation of a Signing Request
```python
payload = "Notification sent to Judge"
srq = cc.CreateSigningRequest(payload, "notification", kind_list, gr["Sign"], appkey, appkey_callback)
# Where srq["IdVal"] is the Id of the Signing Request
```

### Get a Signing Request
```python
srq = cc.GetSigningRequest(id)
```

### Sign the Signing Request
```python
transaction = cc.SignSigningRequest(srq, keys)
# transaction is the signed transaction stored in crypt0.cloud
```
