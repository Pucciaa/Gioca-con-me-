from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import json
app=Flask(__name__,static_folder=".")
DATA=Path("locations.json")
@app.get("/")
def home(): return send_from_directory(".", "index.html")
@app.post("/api/location")
def receive():
    d=request.get_json(silent=True) or {}
    d={k:d.get(k) for k in ("latitude","longitude","accuracy","timestamp")}
    rows=json.loads(DATA.read_text()) if DATA.exists() else []
    rows.append(d); DATA.write_text(json.dumps(rows,indent=2))
    return jsonify(ok=True)
@app.get("/dashboard")
def dashboard():
    rows=json.loads(DATA.read_text()) if DATA.exists() else []
    return "<h1>Posizioni condivise</h1><ul>"+"".join(
      f"<li>{r['timestamp']} — <a target='_blank' href='https://www.google.com/maps?q={r['latitude']},{r['longitude']}'>Apri sulla mappa</a> (precisione ~{round(r['accuracy'])} m)</li>" for r in rows
    )+"</ul>"
