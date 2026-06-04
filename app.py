from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    columns = []
    error = None

    # =========================
    # 1. ЗАГРУЗКА ФАЙЛА
    # =========================
    if request.method == "POST" and "file" in request.files:
        file = request.files["file"]

        if file.filename != "":
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            df = load_file(path)

            if df is None:
                error = "Unsupported format (use CSV or XLSX)"
            else:
                df_global = df
                columns = df.columns.tolist()
                table_html = df.to_html(classes="table table-striped", index=False)

    # =========================
    # 2. ФИЛЬТР ДАННЫХ
    # =========================
    if request.method == "POST" and df_global is not None:
        column = request.form.get("column")
        value = request.form.get("value")

        if column and value and column in df_global.columns:
            col_data = df_global[column]

            try:
                # если число
                if pd.api.types.is_numeric_dtype(col_data):
                    df_filtered = df_global[col_data > float(value)]
                else:
                    df_filtered = df_global[col_data.astype(str).str.contains(value)]

                table_html = df_filtered.to_html(classes="table table-striped", index=False)

            except:
                error = "Filter error"
    return render_template(
        "index.html",
        table=table_html,
        columns=columns,
        error=error
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)