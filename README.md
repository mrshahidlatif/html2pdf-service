# HTML to PDF Service

A lightweight microservice that converts HTML content to PDF using WeasyPrint.

## Features

- Converts HTML to PDF
- RESTful API endpoint
- Docker support
- Production-ready with Gunicorn

## Installation

### Using Docker

```bash
# Build the Docker image
docker build -t html2pdf-service .

# Run the container
docker run -p 5007:5007 html2pdf-service
```

### Local Development

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the service:

```bash
gunicorn service:app
```

## Running Tests

1. Activate your virtual environment:

```bash
source .venv/bin/activate
```

2. (Optional, but recommended) Install dev dependencies and your package in editable mode:

```bash
pip install -r requirements-dev.txt
pip install -e .
```

3. Run the tests with coverage:

```bash
pytest tests/ -v --cov=src
```

You should see output similar to:

```
tests/test_service.py::test_health_check PASSED
tests/test_service.py::test_render_pdf PASSED
tests/test_service.py::test_render_pdf_missing_html PASSED

---------- coverage: platform darwin, python 3.13.3-final-0 ----------
Name              Stmts   Miss  Cover
-------------------------------------
src/__init__.py       3      0   100%
src/service.py       19      1    95%
-------------------------------------
TOTAL                22      1    95%
```

## API Usage

Send a POST request to `http://localhost:5007/render` with HTML content in the request body.

Example using curl:

```bash
curl -X POST -F "html=<html><body><h1>Test</h1></body></html>" http://localhost:5007/render --output output.pdf
```

## Development

### Project Structure

```
html2pdf-service/
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── src/
│   ├── __init__.py
│   └── service.py
├── tests/
│   └── test_service.py
├── README.md
└── ...
```

### Version Management

This project uses `pyproject.toml` for version management and package configuration. The version can be updated in the `pyproject.toml` file.

## License

MIT
