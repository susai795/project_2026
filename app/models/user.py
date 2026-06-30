from pydantic import ConfigDict
from sqlmodel import SQLModel, Field #impostare modello database



class User(SQLModel, table=True):
    model_config = ConfigDict(strict=True)
    username : str = Field(primary_key=True) #collegamento class user con registration
    name : str
    email: str
