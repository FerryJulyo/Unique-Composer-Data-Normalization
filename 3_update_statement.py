import pandas as pd

# Baca file Excel
df = pd.read_excel('data_lagu_dengan_id_baru.xlsx', dtype=str)

# Ambil hanya kolom yang dibutuhkan
df = df[['new_id', 'song', 'composer']]

# Fungsi untuk escape kutip tunggal
def escape_sql(value):
    if pd.isna(value):
        return 'NULL'
    return "'" + str(value).replace("'", "''") + "'"

# Kumpulkan value sebagai batch insert
insert_values = []

for _, row in df.iterrows():
    song_id = escape_sql(row['new_id'])
    song = escape_sql(row['song'])
    composer = escape_sql(row['composer'])
    insert_values.append(f"({song_id}, {song}, {composer})")

# Gabungkan semua baris menjadi satu INSERT statement
sql = "INSERT INTO master_song (song_id, song, composer) VALUES\n" + ",\n".join(insert_values) + ";"

# Simpan ke file .txt
with open("insert_songs.txt", "w", encoding="utf-8") as f:
    f.write(sql)

print("✅ INSERT statement berhasil disimpan ke 'insert_songs.txt'")