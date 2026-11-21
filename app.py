
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)



def koneksi_database():
    conn = sqlite3.connect('health_assistant.db')
    conn.row_factory = sqlite3.Row
    return conn



def buat_tabel():
    conn = koneksi_database()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS riwayat_pemeriksaan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            usia INTEGER NOT NULL,
            celcius REAL NOT NULL,
            fahrenheit REAL NOT NULL,
            kelvin REAL NOT NULL,
            status TEXT NOT NULL,
            waktu DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()



def simpan_riwayat(nama, usia, celcius, fahrenheit, kelvin, status):

    conn = koneksi_database()

    conn.execute("""
        INSERT INTO riwayat_pemeriksaan
        (nama, usia, celcius, fahrenheit, kelvin, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nama, usia, celcius, fahrenheit, kelvin, status))

    conn.commit()
    conn.close()



def ambil_riwayat():

    conn = koneksi_database()

    data = conn.execute("""
        SELECT * FROM riwayat_pemeriksaan
        ORDER BY waktu DESC
    """).fetchall()

    conn.close()

    return data


buat_tabel()




@app.route('/', methods=['GET', 'POST'])
def index():

    hasil = None

    if request.method == 'POST':

        nama = request.form.get('nama')
        usia = int(request.form.get('usia'))
        celcius = float(request.form.get('suhu'))

        fahrenheit = (9/5) * celcius + 32
        kelvin = celcius + 273.15

        if celcius >= 36 and celcius < 37.5:
            status = "Suhu Tubuh Normal"

        elif celcius >= 37.5 and celcius < 39:
            status = "Suhu Tubuh Anda Sedang Demam"

        elif celcius >= 39:
            status = "Suhu Tubuh Anda Sangat Tinggi, Segera Periksa ke Dokter"

        else:
            status = "Suhu Tubuh Anda Rendah, Segera Periksa ke Dokter"


        simpan_riwayat(
            nama,
            usia,
            celcius,
            fahrenheit,
            kelvin,
            status
        )

        hasil = {
            'nama': nama,
            'usia': usia,
            'celcius': celcius,
            'fahrenheit': fahrenheit,
            'kelvin': kelvin,
            'status': status,
        }

    return render_template('index.html', hasil=hasil)




@app.route('/history')
def history():

    riwayat = ambil_riwayat()

    return render_template(
        'history.html',
        riwayat=riwayat
    )


if __name__ == '__main__':
    app.run(debug=True)
