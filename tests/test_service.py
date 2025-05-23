import pytest
from src import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_render_pdf(client):
    html_content = "<html><body><h1>Test</h1></body></html>"
    response = client.post('/render', data={'html': html_content})
    assert response.status_code == 200
    assert response.mimetype == 'application/pdf'

def test_render_pdf_missing_html(client):
    response = client.post('/render')
    assert response.status_code == 400
    assert response.data.decode() == "Missing HTML content" 