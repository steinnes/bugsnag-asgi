import bugsnag
import os
import uvicorn

from bugsnag_asgi import BugsnagMiddleware
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse

bugsnag.configure(api_key=os.environ['BUGSNAG_API_KEY'], project_root=os.getcwd())

app = Starlette()
app.add_middleware(BugsnagMiddleware)


@app.route("/")
def index(req):
    return PlainTextResponse("hello")


@app.route("/raise")
def raiser(req):
    raise ValueError("Arghh!")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
