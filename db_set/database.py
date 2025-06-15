from pathlib import Path
from pydantic_settings import BaseSettings

Base_Dir = Path(__file__).parent.parent

class Settings(BaseSettings):
    DB_HOST: str = 
    DB_PORT: int = 
    DB_USER: str = 
    DB_PASS: str = 
    DB_NAME: str = 
    private_key : Path = Base_Dir / "key" / "jwt-private.pem"
    public_key : Path = Base_Dir / "key" / "jwt-public.pem"
    access_token_time : int = 3
    refresh_token_time : int = 30
    algorithms : str = "RS256"
    
    @property
    def DB_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    

setting = Settings()
