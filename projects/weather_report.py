from turtledemo.sorting_animate import start_ssort

import requests
import sys
sys.path.append('..')
from config.database import get_connection


def run_weather_reading():
    conn = get_connection()

    try:
        if not conn:
            print('Connection error')
            return

        response = requests.get(
            'https://api.open-meteo.com/v1/forecast?latitude=14.65&longitude=121.05&current=temperature_2m,wind_speed_10m&timezone=Asia/Manila')
        cursor = conn.cursor()

        if response.status_code == 200:
            data = response.json()
            current = data['current']
            print(f'Timezone: {data['timezone']}')
            print(f'Time: {current['time']}')
            print(f'Temperature: {current['temperature_2m']}')

            cursor.execute('''SELECT COUNT(*) FROM weather_reading WHERE time_reading = ?''', (current['time'],))

            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute('''
                           INSERT INTO weather_reading(timezone, time_reading, temperature_2m) VALUES(?,?,?)''',
                           (data['timezone'], current['time'], current['temperature_2m'])
                           )
                cursor.commit()
                cursor.execute('''SELECT * FROM weather_reading ORDER BY time_reading''')
                result = cursor.fetchall()

                with open('../output/weather_report.txt', 'w') as file:
                    file.write('Weather Report\n')
                    file.write('=' * 20 +'\n')
                    for row in result:
                            file.write(f'{row[0]} {row[1]} {row[2]:.1f}\n')
                print('Weather report inserted')
            else:
                print('\nReading already saved')

        else:
            print('Failed to connect')

    except Exception as e:
        print(f'Error: {e}')

    finally:
        conn.close()

if __name__ == '__main__':
    run_weather_reading()