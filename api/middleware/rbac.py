from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.core.security import decode_access_token

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Mock retrieving user from DB
    return {"id": user_id, "email": "admin@nexra.com"}

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = Security(get_current_user)):
        # In a real app, query WorkspaceMember here to verify role
        # Mocking role access check
        user_role = "Admin" # Mock role
        
        if user_role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return user

# Pre-configured dependencies
require_owner = RoleChecker(["Owner"])
require_admin = RoleChecker(["Owner", "Admin"])
require_analyst = RoleChecker(["Owner", "Admin", "Analyst"])
require_viewer = RoleChecker(["Owner", "Admin", "Analyst", "Viewer"])
