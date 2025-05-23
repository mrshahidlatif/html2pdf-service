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

## API Usage

Send a POST request to `http://localhost:5007/convert` with HTML content in the request body.

Example using curl:

```bash
curl -X POST -H "Content-Type: text/html" --data-binary @input.html http://localhost:5007/convert --output output.pdf
```

## Development

### Project Structure

```
html2pdf-service/
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── service.py
└── README.md
```

### Version Management

This project uses `pyproject.toml` for version management and package configuration. The version can be updated in the `pyproject.toml` file.

## License

MIT
