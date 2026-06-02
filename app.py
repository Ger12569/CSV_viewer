from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

df_global = None


@app.route("/", methods=["GET", "POST"])
def index():
    global df_global
    table_html = None
    columns = []
    if request.method == "POST":
        file = request.files.get("file")

        print("FILE OBJECT:", file)

        if file:
            print("FILENAME:", file.filename)

            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            print("SAVED TO:", path)

            df_global = pd.read_csv(path)

            table_html = df_global.to_html(index=False)

    # if request.method == "POST":
    #     file = request.files.get("file")
    #
    #     if file and file.filename.endswith(".csv"):
    #         path = os.path.join(UPLOAD_FOLDER, file.filename)
    #         file.save(path)
    #
    #         df_global = pd.read_csv(path)
    #
    #         columns = df_global.columns.tolist()
    #         table_html = df_global.to_html(
    #             classes="table table-striped",
    #             index=False
    #         )

    return render_template(
        "index.html",
        table=table_html,
        columns=columns
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)