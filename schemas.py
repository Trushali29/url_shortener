from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str
        # Setting this here means URL and URLInfo inherit it automatically
    model_config = {"from_attributes":True}

class URL(URLBase):
    is_active: bool
    clicks : int

class URLInfo(URL):
    url: str
    admin_url: str
    secret_key : str
    
class SecretKeyRequest(BaseModel):
    secret_key: str