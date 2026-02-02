import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) 
sys.path.insert(0, project_root)

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    github_token: str
    autogen_use_docker: bool = False
    api_url: str = "http://localhost:8000"
    
    # Path Management
    base_dir: Path = Path(__file__).parent.parent
    data_dir: Path = base_dir / "data"
    db_dir: Path = base_dir / "chroma_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    def setup_directories(self):
        self.data_dir.mkdir(exist_ok=True, parents=True)
        self.db_dir.mkdir(exist_ok=True, parents=True)

settings = Settings()
settings.setup_directories()