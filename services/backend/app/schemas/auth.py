from pydantic import BaseModel

class OTPSend(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str
    password: str
