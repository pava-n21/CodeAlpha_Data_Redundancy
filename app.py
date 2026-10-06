from flask import Flask, render_template, request

from validator import validate_record

from duplicate_detector import (
    create_record_hash,
    check_duplicate,
    insert_record,
    log_validation
)

from database import get_db_connection


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()

    # STEP 1: Validate input
    valid, reason = validate_record(
        name,
        email,
        phone
    )

    if not valid:

        log_validation(
            name,
            email,
            phone,
            None,
            "INVALID",
            reason
        )

        return render_template(
            "index.html",
            message=f"❌ {reason}"
        )

    # STEP 2: Generate SHA-256 fingerprint
    data_hash = create_record_hash(
        name,
        email,
        phone
    )

    # STEP 3: Check for duplicate
    if check_duplicate(data_hash):

        log_validation(
            name,
            email,
            phone,
            data_hash,
            "DUPLICATE",
            "Identical data already exists."
        )

        return render_template(
            "index.html",
            message="❌ Duplicate data detected. Record was not added."
        )

    # STEP 4: Store unique record
    insert_record(
        name,
        email,
        phone,
        data_hash
    )

    # STEP 5: Log successful insertion
    log_validation(
        name,
        email,
        phone,
        data_hash,
        "UNIQUE",
        "New verified record added successfully."
    )

    return render_template(
        "index.html",
        message="✅ Unique data verified and added successfully!"
    )


@app.route("/records")
def view_records():

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            phone,
            status,
            created_at
        FROM records
        ORDER BY id DESC
        """
    )

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "records.html",
        records=records
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )