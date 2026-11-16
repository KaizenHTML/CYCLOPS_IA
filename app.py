import time
import os
from flask import Flask, render_template, request, jsonify
from cyclops_engine import RobustScalerService, AIClassifierService, EmailMetadata, Incident, SOCAnalystService

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

scaler_service = RobustScalerService()
classifier_service = AIClassifierService(scaler_service)
history_service = SOCAnalystService()

demo_meta_1 = EmailMetadata("Aviso urgente de actualizacion de datos de nomina. Ingrese a https://portal-nomina-rrhh-corporativo.com para confirmar.")
demo_eval_1 = classifier_service.predict(demo_meta_1)
demo_incident_1 = Incident(demo_meta_1.raw_text, "emp.usr.089", demo_meta_1, demo_eval_1)
demo_incident_1.status = "ANALYZED"
demo_incident_1.alert_level = "MEDIO"
history_service.add_incident(demo_incident_1)

demo_meta_2 = EmailMetadata("URGENTE: Su clave corporativa ha sido vulnerada. Ingrese inmediatamente a https://seguridad-accesos-ti.net/auth.")
demo_eval_2 = classifier_service.predict(demo_meta_2)
demo_incident_2 = Incident(demo_meta_2.raw_text, "emp.usr.042", demo_meta_2, demo_eval_2)
demo_incident_2.status = "ANALYZED"
demo_incident_2.alert_level = "CRITICO"
history_service.add_incident(demo_incident_2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    start_time = time.time()
    payload = request.get_json() or {}
    raw_text = payload.get("raw_text", "")
    reporter_id = payload.get("reporter_id", "emp.usr.001")

    metadata = EmailMetadata(raw_text)
    evaluation = classifier_service.predict(metadata)

    incident = Incident(raw_text, reporter_id, metadata, evaluation)
    incident.alert_level = evaluation["risk_level"]
    incident.status = "ANALYZED"
    history_service.add_incident(incident)

    elapsed_ms = round((time.time() - start_time) * 1000.0, 2)

    return jsonify({
        "status": "success",
        "incident_id": incident.id,
        "execution_time_ms": elapsed_ms,
        "metadata": metadata.to_dict(),
        "evaluation": evaluation
    })

@app.route("/api/incidents", methods=["GET"])
def get_incidents():
    all_incidents = history_service.get_all_incidents()
    return jsonify({
        "total_count": len(all_incidents),
        "pending_count": 0,
        "incidents": all_incidents
    })

@app.route("/api/incidents/<incident_id>/resolve", methods=["POST"])
def resolve_incident(incident_id):
    return jsonify({"status": "resolved"}), 200

if __name__ == "__main__":
    print("Iniciando CYCLOPS SENTINEL MVP en http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
