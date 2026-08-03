from uuid import uuid4

def unique_repo_name(prefix: str = "api-test") -> str:
    return f"{prefix}-{uuid4().hex[:8]}"