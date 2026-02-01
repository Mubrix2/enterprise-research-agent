import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) 
sys.path.insert(0, project_root)

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.
    
    Environment Variables:
        GITHUB_TOKEN: API token for the LLM service
        AUTOGEN_USE_DOCKER: Whether to use Docker for code execution
        API_URL: URL for the FastAPI server
    """
    # API Configuration
    github_token: str
    
    # Application Configuration
    autogen_use_docker: str = "False"
    api_url: str = "http://localhost:8000"
    
    # Path Configuration
    base_dir: Path = Path(__file__).parent.parent
    data_dir: Path = base_dir / "data"
    db_dir: Path = base_dir / "chroma_db"
    
    # Create directories if they don't exist
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure required directories exist
        self.data_dir.mkdir(exist_ok=True, parents=True)
        self.db_dir.mkdir(exist_ok=True, parents=True)
    
    @property
    def is_docker_enabled(self) -> bool:
        """Check if Docker execution is enabled."""
        return self.autogen_use_docker.lower() == "true"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",  # No prefix for environment variables
        case_sensitive=False
    )

# Global settings instance
settings = Settings()