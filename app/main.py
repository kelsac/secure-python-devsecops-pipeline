"""Small API designed to demonstrate secure development practices."""
import os
from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        return response

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.post("/api/validate")
    def validate_message():
        if not request.is_json:
            return jsonify(error="Content-Type must be application/json"), 415
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not isinstance(data.get("message"), str):
            return jsonify(error="message must be a string"), 400
        message = data["message"].strip()
        if not 1 <= len(message) <= 200:
            return jsonify(error="message length must be 1-200 characters"), 400
        # We return only JSON and never interpolate the message into HTML or shell commands.
        return jsonify(valid=True, length=len(message))

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify(error="request too large"), 413

    return app


if __name__ == "__main__":
    # Local development only; production command is in Dockerfile.
    create_app().run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
