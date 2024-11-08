"""
run wrapper to simplify packaging
Every will be handled by the uv package manager, all packages will be installed in the virtual environment
and the server will be started with the proper settings

run with:
uv run starter.py
"""
import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    uvicorn.run(
        app="server:app",
        host=str(os.getenv("HOST", "localhost")),
        port=int(os.getenv("PORT", "3000")),
        reload=bool(os.getenv("ENV", "test")!="live"),    )
