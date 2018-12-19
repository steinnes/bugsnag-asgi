import functools
import bugsnag
import urllib


class BugsnagMiddleware:
    def __init__(self, app):
        bugsnag.before_notify(self.add_context_to_notification)
        self.app = app

    def __call__(self, scope):
        return functools.partial(self.asgi, asgi_scope=scope)

    async def asgi(self, receive, send, asgi_scope):
        bugsnag.configure_request(asgi_scope=asgi_scope)
        inner = self.app(asgi_scope)
        try:
            await inner(receive, send)
        except Exception as exc:
            bugsnag.configure_request(last_frame_locals=self.get_locals(exc))
            bugsnag.notify(exc)
            raise exc from None
        finally:
            bugsnag.clear_request_config()

    def get_locals(self, exception):
        try:
            tb = exception.__traceback__
            while True:
                if tb.tb_next is not None:
                    tb = tb.tb_next
                else:
                    break
            return tb.tb_frame.f_locals
        except Exception as e:
            return {'error': 'Could not collect locals ({})'.format(e)}

    def add_context_to_notification(self, notification):
        scope = notification.request_config.asgi_scope

        notification.add_tab("request", {
            "url": self.get_url(scope),
            "query": self.get_query(scope),
            "headers": self.get_headers(scope),
        })
        notification.add_tab("locals", notification.request_config.last_frame_locals)

    def get_url(self, scope):
        """
        Extract URL from the ASGI scope, without also including the querystring
        """
        scheme = scope.get("scheme", "http")
        server = scope.get("server", None)
        path = scope.get("root_path", "") + scope["path"]

        for key, value in scope["headers"]:
            if key == b"host":
                host_header = value.decode("latin-1")
                return "%s://%s%s" % (scheme, host_header, path)

        if server is not None:
            host, port = server
            default_port = {"http": 80, "https": 443, "ws": 80, "wss": 443}[scheme]
            if port != default_port:
                return "%s://%s:%s%s" % (scheme, host, port, path)
            return "%s://%s%s" % (scheme, host, path)
        return path

    def get_query(self, scope):
        """
        Extract querystring from the ASGI scope, in the format that the Sentry protocol expects.
        """
        return urllib.parse.unquote(scope["query_string"].decode("latin-1"))

    def get_headers(self, scope):
        """
        Extract headers from the ASGI scope, in the format that the Sentry protocol expects.
        """
        headers = {}
        for raw_key, raw_value in scope["headers"]:
            key = raw_key.decode("latin-1")
            value = raw_value.decode("latin-1")
            if key in headers:
                headers[key] = headers[key] + ", " + value
            else:
                headers[key] = value
        return headers
