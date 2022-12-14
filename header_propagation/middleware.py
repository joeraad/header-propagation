from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List
from starlette.datastructures import Headers, MutableHeaders
from header_propagation.context import propagated_headers

import logging
logger = logging.getLogger('header_propagation')

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Message, Receive, Scope, Send
    
@dataclass
class HeaderPropagationMiddleware:
    app: 'ASGIApp'
    header_names: List= field(default_factory=list) 
    headers: dict = field(default_factory=dict)

    async def __call__(self, scope: 'Scope', receive: 'Receive', send: 'Send') -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        if(self.header_names != []):
            for header in self.header_names:
                self.headers[header] = Headers(scope=scope).get(header.lower())

        propagated_headers.set(self.headers)

        async def outgoing_request(message: 'Message') -> None:
            if message['type'] == 'http.response.start':
                headers = MutableHeaders(scope=message)
                for propagated_header in self.headers:
                    if(self.headers.get(propagated_header)):
                        headers.append(propagated_header, self.headers.get(propagated_header))

            await send(message)

        await self.app(scope, receive, outgoing_request)
        return
