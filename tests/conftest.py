from fastapi import FastAPI
from starlette.middleware import Middleware

from header_propagation.middleware import HeaderPropagationMiddleware

HEADER_1_NAME = 'header1'
HEADER_1_VALUE = 'header1_value'
HEADER_2_NAME = 'header2'
HEADER_2_VALUE = 'header2_value'

default_app = FastAPI(middleware=[Middleware(HeaderPropagationMiddleware)])

one_header_app= FastAPI(middleware=[Middleware(HeaderPropagationMiddleware, header_names=[HEADER_1_NAME])])

two_headers_app = FastAPI(middleware=[Middleware(HeaderPropagationMiddleware, header_names=[HEADER_1_NAME, HEADER_2_NAME])])

same_header_app = FastAPI(middleware=[Middleware(HeaderPropagationMiddleware, header_names=[HEADER_1_NAME, HEADER_2_NAME])])