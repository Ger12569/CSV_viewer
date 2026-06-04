from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

df_global = None


def load_file(path):
    if path.endswith(".csv"):
        return pd.read_csv(path)
    elif path.endswith(".xlsx"):
        return pd.read_excel(path)
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    global df_global

    table_html = None
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        # ================= UPLOAD =================
        if action == "upload":
            file = request.files.get("file")

            if file and file.filename:
                path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(path)

                df_global = load_file(path)

                if df_global is None:
                    error = "Unsupported file format"
                else:
                    table_html = df_global.to_html(index=False)

        # ================= FILTER =================
        elif action == "filter":
            if df_global is None:
                error = "Upload file first"
            else:
                column = request.form.get("column")
                value = request.form.get("value")

                if column in df_global.columns:
                    col = df_global[column]

                    try:
                        if pd.api.types.is_numeric_dtype(col):
                            df_filtered = df_global[col > float(value)]
                        else:
                            df_filtered = df_global[col.astype(str).str.contains(value)]

                        table_html = df_filtered.to_html(index=False)

                    except Exception as e:
                        error = f"Filter error: {e}"

        # ================= PLOT =================
        elif action == "plot":
            if df_global is not None:
                num_cols = df_global.select_dtypes(include="number")

                if not num_cols.empty:
                    plt.figure()
                    num_cols.plot(kind="bar")
                    plt.tight_layout()

                    path = os.path.join(STATIC_FOLDER, "plot.png")
                    plt.savefig(path)
                    plt.close()

    return render_template("index.html", table=table_html, error=error)


@app.route("/plot")
def plot():
    return send_file("static/plot.png", mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)