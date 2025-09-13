import csv
import io
import ssl
import base64
import requests
from typing import List, Dict
from flask import Flask, render_template, request, send_file
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from io import BytesIO

app = Flask(__name__)

STATUS_URL = "https://castcertificatewb.gov.in/application_search"
DOWNLOAD_URL = "https://castcertificatewb.gov.in/downlaod_signcertificate"

# -------- SSL Adapter for Legacy TLS --------
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        self.poolmanager = PoolManager(*args, ssl_context=ctx, **kwargs)

session = requests.Session()
session.mount("https://", SSLAdapter())

# -------- Fetch Application Status --------
def check_status(app_no: str) -> Dict[str, str]:
    try:
        resp = session.get(STATUS_URL, params={"applid": app_no}, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("recordsTotal", 0) > 0:
            return data["data"][0]
        else:
            return {"applid": app_no, "status_desc": "No record found"}
    except Exception as e:
        return {"applid": app_no, "status_desc": f"Error: {e}"}

def bulk_check(app_numbers: List[str]) -> List[Dict[str, str]]:
    return [check_status(app.strip()) for app in app_numbers if app.strip()]

# -------- Download Certificate Server-Side --------
@app.route("/download/<path:applid>")
def download_certificate(applid):
    applname = request.args.get("applname", "")
    try:
        response = session.post(DOWNLOAD_URL, data={"applno": applid, "applname": applname}, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "success" and data.get("pdf"):
            pdf_bytes = base64.b64decode(data["pdf"])
            return send_file(
                BytesIO(pdf_bytes),
                as_attachment=True,
                download_name=f"{applid}.pdf",
                mimetype="application/pdf"
            )
        else:
            return f"Certificate not ready for {applid}", 404
    except Exception as e:
        return f"Error downloading certificate for {applid}: {e}", 500

# -------- Main Web Route --------
@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        app_numbers = []

        # Manual input
        manual_input = request.form.get("app_numbers")
        if manual_input:
            app_numbers.extend([x.strip() for x in manual_input.splitlines()])

        # CSV upload
        if "csv_file" in request.files:
            file = request.files["csv_file"]
            if file and file.filename.endswith(".csv"):
                stream = io.StringIO(file.stream.read().decode("utf-8"))
                reader = csv.reader(stream)
                for row in reader:
                    if row and row[0] != "ApplicationNumber":  # skip header
                        app_numbers.append(row[0].strip())

        if app_numbers:
            results = bulk_check(app_numbers)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
