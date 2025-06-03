from flask import Flask, request, send_file, jsonify
from weasyprint import HTML, CSS
import io
from clerk_auth import verify_clerk_token

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/render', methods=['POST'])
def render_pdf():
    html = request.form.get('html')
    css = request.form.get('css', '')

    if not html:
        return "Missing HTML content", 400
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing auth token"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = verify_clerk_token(token)
        user_id = payload['sub']
    except Exception as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 403


    pdf_file = io.BytesIO()
    HTML(string=html).write_pdf(pdf_file, stylesheets=[CSS(string=css)] if css else [])
    pdf_file.seek(0)

    return send_file(pdf_file, mimetype='application/pdf', as_attachment=False, download_name='document.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)
