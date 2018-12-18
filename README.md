# bugsnag-asgi

Bugsnag integration for ASGI frameworks.  Heavily based on [sentry-asgi](https://github.com/encode/sentry-asgi).

Installation:
```
pip install bugsnag-asgi
```

Usage:
```
from bugsnag_asgi import BugsnagMiddleware
import bugsnag

bugsnag.configure(...)

app = ...
app = BugsnagMiddleware(app)
```
