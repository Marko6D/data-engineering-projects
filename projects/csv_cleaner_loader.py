import csv
import sys
sys.path.append("..")
from utils.csv_validate import validate_row
from config.database import get_connection


def run_csv_cleaner():
    conn = get_connection()
    if not conn:
        print('Connection error')
        return

    cursor = conn.cursor()
    try:
        with open('../data/messy.csv', newline='') as messy_file, open('../data/rejects.csv', 'w', newline='') as reject_file:
            reader = csv.DictReader(messy_file)
            writer = csv.writer(reject_file)
            loaded = 0
            rejected = 0
            already_in_db = 0
            processed_id = []
            writer.writerow(['id', 'name', 'age', 'email', 'reason'])
            for row in reader:
                reason = validate_row(row)
                if reason:
                    print(row['id'], reason)
                    rejected += 1
                    writer.writerow([row['id'], row['name'], row['age'], row['email'], reason])
                    continue
                if row['id'] in processed_id:
                    print(row['id'], 'Duplicate')
                    rejected += 1
                    writer.writerow([row['id'], row['name'], row['age'], row['email'], 'Duplicate'])
                    continue
                else:
                    cursor.execute('''SELECT COUNT(*) FROM csv_data WHERE id = ?''', (row['id'],))
                    count = cursor.fetchone()[0]

                    if count == 0:
                        loaded += 1
                        processed_id.append(row['id'])
                        cursor.execute('''
                                        INSERT INTO csv_data(ID, NAMES, AGE, EMAIL) VALUES(?,?,?,?)''',
                                       (int(row['id']), row['name'], int(row['age']), row['email'])
                                   )
                    else:
                        already_in_db += 1
                        print(row['id'], 'Already in the database')




            conn.commit()
            print(f'Loaded {loaded} rows')
            print(f'Rejected {rejected} rows')
            print(f'Already {already_in_db} rows')



    except Exception as e:
        print('Error:', e)

    finally:
        conn.close()


if __name__ == '__main__':
    run_csv_cleaner()







