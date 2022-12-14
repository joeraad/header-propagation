import logging
from typing import TYPE_CHECKING
from uuid import uuid4

import pytest
from fastapi import Response
from httpx import AsyncClient
from starlette.testclient import TestClient

from tests.conftest import (
    default_app,
    one_header_app, 
    two_headers_app, 
    same_header_app,
    HEADER_1_NAME,
    HEADER_1_VALUE,
    HEADER_2_NAME,
    HEADER_2_VALUE,
)

if TYPE_CHECKING:
    from starlette.websockets import WebSocket

logger = logging.getLogger('header_propagation')

apps = [default_app, one_header_app, two_headers_app, same_header_app]

pytestmark = pytest.mark.asyncio

async def test_returned_response_headers():

    @default_app.get('/test')
    async def test_view() -> Response:
        return Response(status_code=200)

    async with AsyncClient(app=default_app, base_url='http://test') as client:
        response = await client.get('test')
        assert response.headers.get(HEADER_1_NAME) == None
        assert response.headers.get(HEADER_2_NAME) == None
    
    @one_header_app.get('/test')
    async def test_view() -> Response:
        return Response(status_code=200)

    async with AsyncClient(app=one_header_app, base_url='http://test') as client:
        response = await client.get('test', headers={HEADER_1_NAME: HEADER_1_VALUE})
        assert response.headers.get(HEADER_1_NAME) == HEADER_1_VALUE
        assert response.headers.get(HEADER_2_NAME) == None
    
    @two_headers_app.get('/test')
    async def test_view() -> Response:
        return Response(status_code=200, )
    
    async with AsyncClient(app=two_headers_app, base_url='http://test') as client:
        response = await client.get('test', headers={HEADER_1_NAME: HEADER_1_VALUE, HEADER_2_NAME: HEADER_2_VALUE})
        assert response.headers.get(HEADER_1_NAME) == HEADER_1_VALUE
        assert response.headers.get(HEADER_2_NAME) == HEADER_2_VALUE

    @same_header_app.get('/test')
    async def test_view() -> Response:
        return Response(status_code=200)
    
    async with AsyncClient(app=same_header_app, base_url='http://test') as client:
        response = await client.get('test', headers={HEADER_1_NAME: HEADER_1_VALUE, HEADER_1_NAME: HEADER_2_VALUE})
        assert response.headers.get(HEADER_1_NAME) == HEADER_2_VALUE
        assert response.headers.get(HEADER_2_NAME) == None