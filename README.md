# Weather Data Pipeline

A Python pipeline that pulls the current weather for Quezon City from the Open-Meteo API, saves it to a SQL Server table, and writes a report.

## How it works

1. **Extract:** call the Open-Meteo API with `requests` and get the response as JSON.
2. **Transform:** pick `timezone`, `time`, and `temperature_2m` out of the nested JSON.
3. **Load:** check if the reading already exists, then `INSERT` it into SQL Server only if it is new.
4. **Report:** `SELECT` all readings and write them to `output/weather_report.txt`.

## Tools used

- Python
- requests
- pyodbc
- SQL Server (SSMS)
- Open-Meteo API

## How to run it

1. Install the packages: `requests` and `pyodbc`.
2. Create the table in SSMS:

```sql
CREATE TABLE weather_reading (
    timezone VARCHAR(50),
    time_reading VARCHAR(50),
    temperature_2m DECIMAL(5, 1)
)
```

3. Open `config/database.py` and change the server name to your own SQL Server name.
4. Run the weather file (`weather_report.py`). Run it again later to add new readings.

## Sample output

```
Weather Report
====================
Asia/Manila 2026-10-25T13:15 32.90
Asia/Manila 2026-10-29T16:45 31.50
Asia/Manila 2026-10-29T17:30 30.60
```

## What I learned

- How to avoid duplicate rows by checking with `COUNT` before inserting
- How to read nested JSON responses
- When to use `fetchall()` and `fetchone()`
- Using `commit()` to save an `INSERT`
- Handling errors with `try/except`
