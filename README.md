# bugsnag-asgi

Bugsnag integration for ASGI frameworks.  Heavily based on [sentry-asgi](https://github.com/encode/sentry-asgi).

Installation:
```
pip install bugsnag-asgi
```

Usage:
```python
from bugsnag_asgi import BugsnagMiddleware
import bugsnag

bugsnag.configure(...)

app = ...
app = BugsnagMiddleware(app)
```

Here's a more complete example using [Starlette](https://github.com/encode/starlette) and [uvicorn](https://github.com/encode/uvicorn):
```python

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
```

See [examples/](tree/master/examples) for more.
