# clerk_auth.py
import requests
import jwt
from jwt import algorithms
from flask import request, abort
import os
from dotenv import load_dotenv

load_dotenv()

CLERK_ISSUER = os.getenv("CLERK_ISSUER")
CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")

# Cache JWKS for performance
_jwks = None
def get_jwks():
    global _jwks
    if _jwks is None:
        res = requests.get(CLERK_JWKS_URL)
        _jwks = res.json()
    return _jwks

def verify_clerk_token(token):
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header['kid']

    # Find the correct key
    key = next((k for k in jwks['keys'] if k['kid'] == kid), None)
    if key is None:
        raise Exception("Invalid token key")

    public_key = algorithms.RSAAlgorithm.from_jwk(key)

    # Verify and decode
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=None,  # Optional: can match your frontend client ID
        issuer=CLERK_ISSUER,
    )

    return payload
