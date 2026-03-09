from fastapi import FastAPI
import psycopg2

app = FastAPI(title="Bank Data Platform API")

def get_connection():
    return psycopg2.connect(
        host="bank_postgres",
        dbname="bank",
        user="data",
        password="data"
    )

@app.get("/")
def home():
    return {"message": "Bank Data Platform API is running"}

@app.get("/kpi/by-type")
def kpi_by_type():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT type, nb_transactions, montant_total, montant_moyen
        FROM vw_kpi_by_type
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "type": row[0],
            "nb_transactions": row[1],
            "montant_total": float(row[2]),
            "montant_moyen": float(row[3])
        })

    return result

@app.get("/kpi/daily")
def kpi_daily():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT date, nb_transactions, montant_total, montant_moyen
        FROM vw_daily_kpi
        ORDER BY date
        LIMIT 100
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "date": str(row[0]),
            "nb_transactions": row[1],
            "montant_total": float(row[2]),
            "montant_moyen": float(row[3])
        })

    return result

@app.get("/kpi/top-customers")
def top_customers(limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT customer_id, nb_transactions, montant_total, montant_moyen
        FROM vw_kpi_by_customer
        ORDER BY montant_total DESC
        LIMIT {limit}
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "customer_id": row[0],
            "nb_transactions": row[1],
            "montant_total": float(row[2]),
            "montant_moyen": float(row[3])
        })

    return result

