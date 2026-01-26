from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # API Keys
    github_token: str
    
    # App Settings
    app_name: str = "Enterprise Research Agent"
    debug: bool = False
    
    # Paths
    base_dir: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = base_dir / "data"
    db_dir: Path = base_dir / "chroma_db"
    
    # Agent Settings
    use_docker: bool = True
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Global instance to be used across the project
settings = Settings()