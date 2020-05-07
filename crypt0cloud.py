import crypt0
import requests
import json

class CryptoCloud:
    def __init__(self, endpoint):
        self.client = Client(endpoint)
        self.cry = crypt0.Crypt0graphy()

    def CreateUser(self, user):
        b1 = self.client.getCurrentBlock()
        nid = self.client.getNodeId()

        kp = self.cry.newSigningKey()

        t = dict([
            ("AppID", self.cry.base64Encode(bytes(kp.verify_key))),
            ("Payload", user),
            ("SignKind", "NewUser"),
            ("SignerKinds", ["NewUser"]),
            ("FromNode", nid),
            ("ToNode", nid),

            ("Callback", "demo"),
            ("Creation", self.cry.currentMilis()),
            ("BlockSign", b1["Sign"])
        ])
        t["Signer"] = t["AppID"]

        self.client.PostSingleTransaction(t, kp)

        return kp, t

    def InsertTransaction(self, payload, userkp, appkey):
        b1 = self.client.getCurrentBlock()
        nid = self.client.getNodeId()


        t = dict([
            ("AppID", self.cry.base64Encode(bytes(appkey.verify_key))),
            ("Signer", self.cry.base64Encode(bytes(userkp.verify_key))),
            ("Payload", payload),
            ("SignKind", ""),
            ("SignerKinds", [""]),

            ("FromNode", nid),
            ("ToNode", nid),

            ("Callback", "demo"),
            ("Creation", self.cry.currentMilis()),
            ("BlockSign", b1["Sign"])
        ])

        t = self.client.PostSingleTransaction(t, userkp)

        return t

    def CreateGroup(self, payload, kinds, appkeys, callback):
        nid = self.client.getNodeId()

        t = dict([
            ("AppID", self.cry.base64Encode(bytes(appkeys.verify_key))),
            ("Payload", payload),
            ("SignKind", "__NEWCONTRACT"),
            ("SignerKinds", kinds),

            ("FromNode", nid),
            ("ToNode", nid),

            ("Callback", callback),
            ("Creation", self.cry.currentMilis()),

        ])
        t["Signer"] = t["AppID"]

        t = self.client.CreateGroup(t, appkeys)

        return t

    def CreateSigningRequest(self, payload, signkind, kinds, parent, appkeys, callback):
        nid = self.client.getNodeId()

        t = dict([
            ("AppID", self.cry.base64Encode(bytes(appkeys.verify_key))),
            ("SignKind", signkind),
            ("SignerKinds", kinds),
            ("Parent", parent),
            ("FromNode", nid),
            ("Callback", callback),
            ("Payload", payload)

        ])

        t = self.client.CreateSigningRequest(t)

        return t

    def GetSigningRequest(self, idval):
        return self.client.GetSigningRequest(idval)

    def SignSigningRequest(self, t, userkp):
        b1 = self.client.getCurrentBlock()

        t["Signer"] = self.cry.base64Encode(bytes(userkp.verify_key))
        t["ToNode"] = t["FromNode"]
        t["BlockSign"] = b1["Sign"]

        return self.client.SignSigningRequest(t, userkp)



class Client:
    def __init__(self, edp):
        self._endpoint = edp
        self.cry = crypt0.Crypt0graphy()

    def getNodeId(self):
        if self._endpoint == "":
            return None
        urlstring = "https://" + self._endpoint + "/api/v1/node_id"
        r = requests.get(urlstring)
        if r.status_code != 200:
            return None
        return json.loads(r.content)

    def getCurrentBlock(self):
        if self._endpoint == "":
            return None
        urlstring = "https://" + self._endpoint + "/api/v1/block/get_lasts"
        r = requests.get(urlstring)
        if r.status_code != 200:
            return None
        return json.loads(r.content)[0]

    def PostSingleTransaction(self, t, key):
        if self._endpoint == "":
            return None
        t = self.cry.signTransaction(t, key)
        jsont = json.dumps(t)

        r = requests.post("https://" + self._endpoint + "/api/v1/post_single_transaction", data=jsont, headers={'Content-Type': 'application/json'})
        if r.status_code != 200:
            return None
        return json.loads(r.content)

    def CreateGroup(self, t, key):
        if self._endpoint == "":
            return None
        t = self.cry.signTransaction(t, key)
        jsont = json.dumps(t)

        r = requests.post("https://" + self._endpoint + "/api/v1/create_group", data=jsont)
        if r.status_code != 200:
            return None
        return json.loads(r.content)

    def CreateSigningRequest(self, t):
        if self._endpoint == "":
            return None
        jsont = json.dumps(t)

        r = requests.post("https://" + self._endpoint + "/api/v1/create_signingRequest", data=jsont)
        if r.status_code != 200:
            return None
        return json.loads(r.content)

    def GetSigningRequest(self, transactionrequest):
        if self._endpoint == "":
            return None
        urlstring = "https://" + self._endpoint + "/api/v1/get_signingRequest?id="+transactionrequest
        r = requests.get(urlstring)
        if r.status_code != 200:
            return None
        return json.loads(r.content)

    def SignSigningRequest(self, t, key):
        if self._endpoint == "":
            return None
        t = self.cry.signTransaction(t, key)
        jsont = json.dumps(t)

        r = requests.post("https://" + self._endpoint + "/api/v1/sign_signingRequest", data=jsont)
        if r.status_code != 200:
            return None
        return json.loads(r.content)
