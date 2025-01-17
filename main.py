import os
import uvicorn

if __name__ == "__main__":
    HOST = os.environ.get("HOST", "127.0.0.1")
    # PORT: int = os.environ.get("PORT", 8080)

    uvicorn.run("servidor.config:app", host=HOST, port=8888, reload=True)
