# type User struct {
# Id          int    `json:"id"`
# AccessToken string `json:"access_token"`
# IdToken     string `json:"id_token"`
# Ids         string `json:"ids"`
# Phone       string `json:"phone"`
# Email       string `json:"email"`
# Password    string `json:"password"`
# Name        string `json:"name"`
# PhotoUrl    string `json:"photo_url"`
# Blocked     bool   `json:"blocked"`
# Role        string `json:"role"`
# Region      string `json:"region"`
# Device      string `json:"device"`
# CreatedAt   string `json:"created_at"`
# UpdatedAt   string `json:"updated_at"`
# Token       string `json:"token"`
# }
from pydantic import BaseModel


class User(BaseModel):
    id: int
    access_token: str
    id_token: str
    ids: str
    phone: str
    email: str
    password: str
    name: str
    photo_url: str
    blocked: bool
    role: str
    region: str
    device: str
    created_at: str
    updated_at: str
    token: str
