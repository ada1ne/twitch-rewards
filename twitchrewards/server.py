""""Starts uvicorn server for the app."""

import uvicorn

from twitchrewards.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "twitchrewards.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        ssl_keyfile=settings.SSL_KEY_PATH,
        ssl_certfile=settings.SSL_CERTIFICATE_PATH,
    )
