import os
import psycopg
import pandas as pd
from fastapi import FastAPI, HTTPException

DATABASE_URL = os.environ["DATABASE_URL"]

app = FastAPI(title="Employee Performance API", version="1.0.0")


def query_df(sql: str, params=None) -> pd.DataFrame:
    with psycopg.connect(DATABASE_URL) as conn:
        return pd.read_sql(sql, conn, params=params)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/reports/top-employees")
def top_employees():
    df = query_df("""
        SELECT full_name, department,
               ROUND(AVG(efficiency_score),2) AS avg_eff,
               COUNT(*) AS activities
        FROM v_efficiency
        GROUP BY full_name, department
        ORDER BY avg_eff DESC;
    """)
    return df.to_dict(orient="records")


@app.get("/reports/dept-trend")
def dept_trend():
    df = query_df("""
        SELECT activity_date, department,
               ROUND(AVG(efficiency_score),2) AS dept_avg_efficiency
        FROM v_efficiency
        GROUP BY activity_date, department
        ORDER BY activity_date, department;
    """)
    return df.to_dict(orient="records")


@app.get("/employee/{employee_code}/efficiency")
def employee_efficiency(employee_code: str):
    df = query_df("""
        SELECT *
        FROM v_efficiency
        WHERE employee_id = (
            SELECT id FROM employees WHERE employee_code = %(code)s
        )
        ORDER BY activity_date;
    """, params={"code": employee_code})

    if df.empty:
        raise HTTPException(status_code=404, detail="Employee not found or no data")

    return df.to_dict(orient="records")
