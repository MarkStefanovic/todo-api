import fastapi
import uvicorn
from fastapi import HTTPException
from starlette.middleware.cors import CORSMiddleware

from src import core, api


logger = core.logger.getChild("main")


def create_app() -> fastapi.FastAPI:
    config = core.EnvironConfig()
    app = fastapi.FastAPI(title="todo-api", debug=config.debug, version="0.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.add_event_handler("startup", create_start_app_handler(app))
    # app.add_event_handler("shutdown", create_stop_app_handler(app))
    app.add_exception_handler(HTTPException, api.http_error_handler)
    # app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.include_router(api.router, prefix="/api")
    return app


if __name__ == "__main__":
    import webbrowser

    webbrowser.open("http://localhost:8000/docs")

    import dotenv

    dotenv.load_dotenv(dotenv.find_dotenv())

    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=8000)
