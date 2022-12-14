# Header Propagation Middleware

Middleware for propagating headers from incoming requests to outgoing requests for FastAPI.

## Installation

```bash
pip install header-propagation-middleware
```

## Setup

To setup the middleware, you need to add it to your FastAPI app.

### Adding Middleware

```python
from header_propagation_middleware import HeaderPropagationMiddleware

app = FastAPI()
app.add_middleware(HeaderPropagationMiddleware,header_names=["header1","header2"])
```

#### Configurable middleware argument

**header_names**

-   Type: `List[str]`
-   Default: `[]`
-   Description: The list of headers to propagate.

### Accessing propagated headers

You can access the propagated headers using the `propagated_headers` object.

```python
from header_propagation_middleware import propagated_headers

propagated_headers.get()
```

**propagated_headers**

-   Type: `dict`
-   Default: `{}`
-   Description: The dictionary of propagated headers.

## Tests

Running test

```bash
python -m pytest
```

Running test with coverage report

```bash
python -m pytest --cov --cov-report=html:reports/html_dir
```
