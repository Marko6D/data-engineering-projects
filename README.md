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



# CSV Cleaner and Loader

A Python script that reads a messy CSV file, checks every row, loads the good rows into SQL Server, and saves the bad rows to a rejects file with the reason.

## How it works

1. **Read:** open `data/messy.csv` and read each row with `csv.DictReader`.
2. **Validate:** check each row with `validate_row()` (in `utils/csv_validate.py`). It returns a reason when a row is bad, or `None` when it is good.
3. **Skip duplicates:** skip an id that was already seen in the file, and an id that is already in the database.
4. **Load:** `INSERT` the good rows into the `csv_data` table.
5. **Reject:** write each bad row and its reason to `data/rejects.csv`.
6. **Summary:** print how many rows were loaded, rejected, and already in the database.

## Validation rules

| Field | Rule | Reason returned |
|---|---|---|
| id | not empty, digits only | Id is missing / Id is not a number |
| name | not empty | Name is missing |
| age | not empty, a number, not negative | Age is missing / Age is not a number / Age is negative |
| email | not empty, exactly one `@`, text before the `@`, a dot after the `@` with text after it | Email is missing / Email has no @ / Email domain is invalid |

## Project structure

```
config/database.py        connection to SQL Server
utils/csv_validate.py     validate_row()
projects/csv_cleaner.py   main script
data/messy.csv            input file
data/rejects.csv          rejected rows (created when you run it)
```

## Tools used

- Python
- csv module
- pyodbc
- SQL Server (SSMS)

## How to run it

1. Install `pyodbc`.
2. Create the table in SSMS:

```sql
CREATE TABLE csv_data (
    ID INT,
    NAMES VARCHAR(50),
    AGE INT,
    EMAIL VARCHAR(100)
)
```

3. Open `config/database.py` and change the server name to your own SQL Server name.
4. Put `messy.csv` in the `data` folder.
5. Run `csv_cleaner.py`.

You can run it again. Rows already in the table are not inserted twice.

## Sample output

First run:

```
3 Age is not a number
4 Email is missing
2 Duplicate
6 Name is missing
7 Age is negative
8 Email domain is invalid
Loaded 4 rows
Rejected 6 rows
Already 0 rows
```

Second run:

```
Loaded 0 rows
Rejected 5 rows
Already 5 rows
```

## What I learned

- How to read a CSV file as dictionaries with `csv.DictReader`
- How `writerow()` writes one row to a CSV file, and that it takes one list of values
- How to import functions from other files, like `validate_row` and `get_connection`
- How to use `if`, `else`, and `continue` so each row goes down the right path
- How to keep a small function for one job, and put the memory (the list of seen ids) in the loop
- How to stop the same row from being inserted twice by checking the database first
