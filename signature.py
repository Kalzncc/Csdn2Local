import requests as rq
import random as rd
import hmac
import hashlib
import base64
import json




def get_articles_list_signature(router: str, xca_key: str, once_key: str):
    router_and_param = router.split('?')
    url, param = '', ''
    url = router_and_param[0]
    if len(router_and_param) > 1:
        param = router_and_param[1] 
    _url = url + ('' if '' == param else '?' + param)
    
    return  f"GET\napplication/json, text/plain, */*\n\n\n\nx-ca-key:{xca_key}\nx-ca-nonce:{once_key}\n{_url}"
    
    

def get_articles_content_signature(router: str, xca_key: str, once_key: str):
    return f"GET\n*/*\n\n\n\nx-ca-key:{xca_key}\nx-ca-nonce:{once_key}\n{router}"





def to_base64_encode(e_key, to_enc):
    hmac_sha256 = hmac.new(e_key.encode('utf-8'), to_enc.encode('utf-8'), hashlib.sha256)
    digest = hmac_sha256.digest()
    return base64.b64encode(digest)
    


