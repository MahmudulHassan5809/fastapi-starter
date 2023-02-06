import json
from starlette.types import ASGIApp, Receive, Scope, Send, Message
from starlette.datastructures import MutableHeaders


class CustomResponseMiddleware:
    application_generic_urls = ['/api/v1/openapi.json', '/docs', '/docs/oauth2-redirect', '/redoc']
    
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and  not any([scope["path"].startswith(endpoint) for endpoint in CustomResponseMiddleware.application_generic_urls]):
            responder = MetaDataAdderMiddlewareResponder(self.app)
            await responder(scope, receive, send)
            return
        await self.app(scope, receive, send)


class MetaDataAdderMiddlewareResponder:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.initial_message: Message = {}

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.send = send
        await self.app(scope, receive, self.send_with_meta_response)

    async def send_with_meta_response(self, message: Message):
        message_type = message["type"]
        if message_type == "http.response.start":
            self.initial_message = message

        elif message_type == "http.response.body":
            response_body = json.loads(message["body"].decode())
            data = {}
            if self.initial_message['status'] in [200, 201, 204]:
                data["success"] = True
                data["message"] = "OK" 
            else:
                data["success"] = False
                data["message"] = response_body['detail']
            data['meta_info'] = response_body.get('meta_info')
            if self.initial_message['status'] == 403:
                data["data"] = response_body['detail']
            else:
                data["data"] = response_body['data'] if type(response_body.get('data')) == list else response_body
            data_to_be_sent_to_user = json.dumps(data, default=str).encode("utf-8")
            headers = MutableHeaders(raw=self.initial_message["headers"])
            headers["Content-Length"] = str(len(data_to_be_sent_to_user))
            message["body"] = data_to_be_sent_to_user
            await self.send(self.initial_message)
            await self.send(message)
