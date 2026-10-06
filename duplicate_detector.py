import hashlib
from database import get_db_connection


def normalize_text(value):
    """Remove extra spaces and make text lowercase."""
    return " ".join(value.strip().lower().split())


def normalize_phone(phone):
    """Keep only digits from the phone number."""
    return "".join(character for character in phone if character.isdigit())


def create_record_hash(name, email, phone):
    """
    Create a unique SHA-256 fingerprint for the record.
    The same logical record will produce the same hash.
    """

    normalized_name = normalize_text(name)
    normalized_email = normalize_text(email)
    normalized_phone = normalize_phone(phone)

    combined_data = (
        normalized_name
        + "|"
        + normalized_email
        + "|"
        + normalized_phone
    )

    return hashlib.sha256(
        combined_data.encode("utf-8")
    ).hexdigest()


def check_duplicate(data_hash):
    """Check whether this record already exists in AWS RDS."""

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT id
        FROM records
        WHERE data_hash = %s
        LIMIT 1
    """

    cursor.execute(query, (data_hash,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None


def insert_record(name, email, phone, data_hash):
    """Insert a verified unique record into AWS RDS."""

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO records
        (name, email, phone, data_hash, status)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        name.strip(),
        email.strip().lower(),
        phone.strip(),
        data_hash,
        "UNIQUE"
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


def log_validation(
    name,
    email,
    phone,
    data_hash,
    result,
    reason
):
    """Store validation results in the validation_logs table."""

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO validation_logs
        (name, email, phone, data_hash, result, reason)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        name,
        email,
        phone,
        data_hash,
        result,
        reason
    )

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()