from fastapi import FastAPI, File, UploadFile
import hashlib
app = FastAPI()

hashMethodsDictionary = {
    'sha1'   : hashlib.sha1,
    'sha224' : hashlib.sha224,
    'sha256' : hashlib.sha256,
    'sha384' : hashlib.sha384,
    'sha512' : hashlib.sha512,
    'blake2b': hashlib.blake2b,
    'blake2s': hashlib.blake2s,
    'md5'    : hashlib.md5
}

@app.post("/hash/{hashType}")
async def HashFile(hashType: str, file: UploadFile = File(...)):
    token = ""
    codigoerror = 0
    mensajeerror = ""
    if hashType not in hashMethodsDictionary:
        token      = ""
        mensajeerror = "Not valid hash type"
        codigoerror  = 1
    
    contents = await file.read()
    
    hashMethod = hashMethodsDictionary[hashType]()
    hashMethod.update(contents)
    token = hashMethod.hexdigest()

    print(token)
        
    return {'codigoerror': codigoerror, 'mensajeerror': mensajeerror, 'token': token}
