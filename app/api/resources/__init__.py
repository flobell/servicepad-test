from .auth import api as api_auth
from .publications import api as api_publications
from .users import api as api_users
from .files import api as api_files

API_NAMESPACES = [
    api_auth,
    api_publications,
    api_users,
    api_files
]