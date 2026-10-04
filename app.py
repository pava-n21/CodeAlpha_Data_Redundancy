from flask import Flask, render_template, request
from database import get_db_connection
import hashlib
import re

app = Flask(__name__)


def generate_hash(name, email, phone):
    data = f"{name.strip().lower()}|{email.strip().lower()}|{phone.strip()}"
    return hashlib.sha256(data.encode()).hexdigest()


def validate_data(name, email, phone):
    if not name.strip():
        return False, "Name cannot be empty."

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(email_pattern, email):
        return False, "Invalid email address."

    if not phone.isdigit() or len(phone) < 10:
        return False, "Invalid phone number."

    return True, "Valid data."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()

    # STEP 1: Validate input
    valid, reason = validate_data(name, email, phone)

    if not valid:
        save_validation_log(
            name,
            email,
            phone,
            "",
            "INVALID",
            reason
        )

        return render_template(
            "index.html",
            message=f"❌ {reason}"
        )

    # STEP 2: Generate SHA-256 hash
    data_hash = generate_hash(name, email, phone)

    connection = get_db_connection()
    cursor = connection.cursor()

    # STEP 3: Check whether this data already exists
    cursor.execute(
        "SELECT id FROM records WHERE data_hash = %s",
        (data_hash,)
    )

    existing_record = cursor.fetchone()

    if existing_record:

        cursor.close()
        connection.close()

        save_validation_log(
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

    # STEP 4: Store unique data
    cursor.execute(
        """
        INSERT INTO records
        (name, email, phone, data_hash, status)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (name, email, phone, data_hash, "UNIQUE")
    )

    connection.commit()

    cursor.close()
    connection.close()

    save_validation_log(
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


def save_validation_log(name, email, phone, data_hash, result, reason):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO validation_logs
        (name, email, phone, data_hash, result, reason)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (name, email, phone, data_hash, result, reason)
    )

    connection.commit()

    cursor.close()
    connection.close()


if __name__ == "__main__":
    app.run(debug=True)
