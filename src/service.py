from flask import Flask, request, send_file, jsonify
from weasyprint import HTML, CSS
import io, json
from clerk_auth import verify_clerk_token

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/render', methods=['POST'])
def render_pdf():
    html = request.form.get('html')
    css = request.form.get('css', '')
    options_raw = request.form.get('options', '{}')

    if not html:
        return "Missing HTML content", 400

    # Token auth
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing auth token"}), 401
    token = auth_header.split(" ")[1]

    try:
        payload = verify_clerk_token(token)
        user_id = payload['sub']
    except Exception as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 403

    try:
        options = json.loads(options_raw)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid options JSON"}), 400

    # Optional write_pdf args
    write_pdf_args = {
        "stylesheets": [CSS(string=css)] if css else None,
        "media_type": options.get("media_type"),
        "attachments": options.get("attachments"),
        "pdf_identifier": options.get("pdf_identifier", "").encode() if options.get("pdf_identifier") else None,
        "pdf_variant": options.get("pdf_variant"),
        "pdf_version": options.get("pdf_version"),
        "pdf_forms": options.get("pdf_forms"),
        "uncompressed_pdf": options.get("uncompressed_pdf"),
        "custom_metadata": options.get("custom_metadata"),
        "presentational_hints": options.get("presentational_hints"),
        "srgb": options.get("srgb"),
        "optimize_images": options.get("optimize_images"),
        "jpeg_quality": options.get("jpeg_quality"),
        "dpi": options.get("dpi"),
        "full_fonts": options.get("full_fonts"),
        "hinting": options.get("hinting"),
        "cache": options.get("cache")
    }

    # Remove None values (write_pdf doesn't accept them)
    write_pdf_args = {k: v for k, v in write_pdf_args.items() if v is not None}

    pdf_file = io.BytesIO()
    HTML(string=html).write_pdf(target=pdf_file, **write_pdf_args)
    pdf_file.seek(0)

    return send_file(pdf_file, mimetype='application/pdf', as_attachment=False, download_name='document.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)
