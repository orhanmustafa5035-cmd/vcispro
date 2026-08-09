from flask import Flask, render_template, request, jsonify, send_from_directory
import json, os, time

app = Flask(__name__)
DATA_FILE = "C:/VCISPRO/data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html", v=int(time.time()))

@app.route("/api/areas", methods=["GET"])
def get_areas():
    return jsonify(load_data())

@app.route("/api/areas/add", methods=["POST"])
def add_area():
    areas = load_data()
    req = request.get_json()
    new_item = {
        "code": str(req.get("code")),
        "name": req.get("name"),
        "position": req.get("position", ""),
        "area": req.get("area", ""),
        "geometry": {}
    }
    areas.append(new_item)
    save_data(areas)
    return jsonify({"message": "Əlavə olundu"})

@app.route("/api/areas/<code_id>/geometry", methods=["GET", "POST"])
def area_geometry(code_id):
    areas = load_data()
    area = next((item for item in areas if str(item["code"]) == str(code_id)), None)
    if not area:
        return jsonify({"message": "Tapılmadı"}), 404

    if request.method == "GET":
        return jsonify(area.get("geometry") or {})

    if request.method == "POST":
        req_data = request.get_json()
        area["geometry"] = req_data
        save_data(areas)
        return jsonify({"message": "Uğurla saxlanıldı"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
