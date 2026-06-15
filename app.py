from flask import Flask, request, redirect
from html import escape

app = Flask(__name__)

# --------------------------------------------------
# Midlertidig lokal data
# Rahma din patient-side skal senere gemme data her
# --------------------------------------------------

patients = [
    {
        "id": 1,
        "name": "Ali Hassan",
        "age": 55,
        "blood_pressure": [
            {"date": "2026-06-10", "systolic": 145, "diastolic": 90},
            {"date": "2026-06-12", "systolic": 138, "diastolic": 85},
            {"date": "2026-06-15", "systolic": 142, "diastolic": 88}
        ],
        "feedback": []
    },
    {
        "id": 2,
        "name": "Sara Jensen",
        "age": 43,
        "blood_pressure": [
            {"date": "2026-06-10", "systolic": 120, "diastolic": 78},
            {"date": "2026-06-12", "systolic": 118, "diastolic": 76},
            {"date": "2026-06-15", "systolic": 122, "diastolic": 80}
        ],
        "feedback": []
    },
    {
        "id": 3,
        "name": "Mads Nielsen",
        "age": 61,
        "blood_pressure": [
            {"date": "2026-06-10", "systolic": 160, "diastolic": 96},
            {"date": "2026-06-12", "systolic": 155, "diastolic": 94},
            {"date": "2026-06-15", "systolic": 158, "diastolic": 95}
        ],
        "feedback": []
    }
]


# --------------------------------------------------
# Hjælpefunktioner
# --------------------------------------------------

def find_patient(patient_id):
    for patient in patients:
        if patient["id"] == patient_id:
            return patient
    return patients[0]


def calculate_average(patient):
    measurements = patient["blood_pressure"]

    if len(measurements) == 0:
        return "-", "-"

    avg_systolic = sum(m["systolic"] for m in measurements) / len(measurements)
    avg_diastolic = sum(m["diastolic"] for m in measurements) / len(measurements)

    return round(avg_systolic, 1), round(avg_diastolic, 1)


def get_status(avg_systolic, avg_diastolic):
    if avg_systolic == "-":
        return "Ingen data", "gray", "Der findes ingen blodtryksmålinger endnu."

    if avg_systolic >= 140 or avg_diastolic >= 90:
        return "Forhøjet blodtryk", "orange", "Patientens blodtryk er forhøjet. Lægen bør give feedback."

    return "Normalt blodtryk", "green", "Patientens blodtryk ser stabilt ud."


# --------------------------------------------------
# Lægeside
# --------------------------------------------------

@app.route("/")
def home():
    return redirect("/doctor")


@app.route("/doctor")
def doctor_page():
    patient_id = request.args.get("patient_id", 1, type=int)
    patient = find_patient(patient_id)

    avg_systolic, avg_diastolic = calculate_average(patient)
    status, status_color, status_text = get_status(avg_systolic, avg_diastolic)

    html = f"""
    <!DOCTYPE html>
    <html lang="da">
    <head>
        <meta charset="UTF-8">
        <title>Lægeside</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f2f5f9;
                margin: 0;
                padding: 30px;
            }}

            .container {{
                max-width: 900px;
                margin: auto;
            }}

            h1 {{
                background-color: #1e3a5f;
                color: white;
                padding: 20px;
                border-radius: 10px;
            }}

            .card {{
                background-color: white;
                padding: 20px;
                margin-top: 20px;
                border-radius: 10px;
                box-shadow: 0 3px 8px rgba(0,0,0,0.1);
            }}

            select, input, textarea, button {{
                width: 100%;
                padding: 10px;
                margin-top: 8px;
                margin-bottom: 15px;
                font-size: 15px;
            }}

            button {{
                background-color: #1e3a5f;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }}

            button:hover {{
                background-color: #2c5282;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }}

            th {{
                background-color: #dbeafe;
            }}

            .status {{
                border-left: 8px solid {status_color};
            }}

            .feedback {{
                background-color: #eef6ff;
                padding: 12px;
                margin-top: 10px;
                border-left: 5px solid #1e3a5f;
                border-radius: 6px;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            <h1>Lægeside - Blodtryksdata</h1>

            <div class="card">
                <h2>Vælg patient</h2>

                <form method="GET" action="/doctor">
                    <select name="patient_id" onchange="this.form.submit()">
    """

    for p in patients:
        selected = "selected" if p["id"] == patient["id"] else ""
        html += f"""
                        <option value="{p['id']}" {selected}>
                            {escape(p['name'])}
                        </option>
        """

    html += f"""
                    </select>
                </form>
            </div>

            <div class="card">
                <h2>Patientinformation</h2>
                <p><strong>Navn:</strong> {escape(patient["name"])}</p>
                <p><strong>Alder:</strong> {patient["age"]}</p>
            </div>

            <div class="card status">
                <h2>Blodtryksstatus</h2>
                <p><strong>Status:</strong> {status}</p>
                <p>{status_text}</p>
                <p><strong>Gennemsnit systolisk:</strong> {avg_systolic}</p>
                <p><strong>Gennemsnit diastolisk:</strong> {avg_diastolic}</p>
            </div>

            <div class="card">
                <h2>Patientens blodtryksmålinger</h2>

                <table>
                    <tr>
                        <th>Dato</th>
                        <th>Systolisk</th>
                        <th>Diastolisk</th>
                    </tr>
    """

    for measurement in patient["blood_pressure"]:
        html += f"""
                    <tr>
                        <td>{measurement["date"]}</td>
                        <td>{measurement["systolic"]}</td>
                        <td>{measurement["diastolic"]}</td>
                    </tr>
        """

    html += f"""
                </table>
            </div>

            <div class="card">
                <h2>Giv feedback til patienten</h2>

                <form method="POST" action="/add_feedback">
                    <input type="hidden" name="patient_id" value="{patient["id"]}">

                    <label>Dato</label>
                    <input type="date" name="date" required>

                    <label>Feedback</label>
                    <textarea name="message" rows="5" placeholder="Skriv feedback til patienten..." required></textarea>

                    <button type="submit">Send feedback</button>
                </form>
            </div>

            <div class="card">
                <h2>Tidligere feedback</h2>
    """

    if len(patient["feedback"]) == 0:
        html += "<p>Der er endnu ingen feedback til denne patient.</p>"
    else:
        for feedback in patient["feedback"]:
            html += f"""
                <div class="feedback">
                    <strong>{escape(feedback["date"])}</strong>
                    <p>{escape(feedback["message"])}</p>
                </div>
            """

    html += """
            </div>
        </div>
    </body>
    </html>
    """

    return html


# --------------------------------------------------
# Gem feedback fra lægen
# --------------------------------------------------

@app.route("/add_feedback", methods=["POST"])
def add_feedback():
    patient_id = int(request.form["patient_id"])
    patient = find_patient(patient_id)

    new_feedback = {
        "date": request.form["date"],
        "message": request.form["message"]
    }

    patient["feedback"].append(new_feedback)

    return redirect(f"/doctor?patient_id={patient_id}")


# --------------------------------------------------
# Start programmet
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)