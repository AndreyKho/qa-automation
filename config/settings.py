import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

@dataclass(frozen=True)
class Settings:
    gitea_url: str
    gitea_user: str
    gitea_password: str

    @classmethod
    def from_env(cls):
        return cls( 
            gitea_url=os.environ["GITEA_URL"],
            gitea_user=os.environ["GITEA_USER"],
            gitea_password=os.environ["GITEA_PASSWORD"]
        )

settings = Settings.from_env()