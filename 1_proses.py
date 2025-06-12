import pandas as pd
from rapidfuzz import fuzz
import sys

# Baca data dari file Excel
df = pd.read_excel("master_vod.xlsx")
df = df[['SongID','Song', 'csong']]
df = df.dropna(subset=['csong'])

# Fungsi untuk menormalkan nama csong berdasarkan kemiripan
def normalize_csongs(csongs, threshold=92):
    unique_list = []
    mapping = {}

    total = len(csongs)
    bar_width = 20  # panjang progress bar

    for i, csong in enumerate(csongs, start=1):
        csong = str(csong).strip()
        matched = False
        for unique in unique_list:
            score = fuzz.ratio(csong.lower(), unique.lower())
            if score >= threshold:
                mapping[csong] = unique
                matched = True
                break
        if not matched:
            unique_list.append(csong)
            mapping[csong] = csong

        # Tampilkan progress bar
        percent = int(i / total * 100)
        filled = int(bar_width * percent / 100)
        bar = "[" + "=" * filled + " " * (bar_width - filled) + f"] {percent}%"
        print(bar, end='\r', flush=True)

    print()  # Baris baru setelah 100%
    return mapping

# Normalisasi nama csong
mapping = normalize_csongs(df['csong'])
df['csong_normalized'] = df['csong'].map(mapping)

# Ambil data unik berdasarkan Song dan composer yang sudah dinormalisasi
df_unique = df.drop_duplicates(subset=['Song', 'csong_normalized'])

# Simpan ke file teks
with open("insert_statements.txt", "w", encoding="utf-8") as f:
    for _, row in df_unique.iterrows():
        songID = str(row['SongID']).replace("'","''")
        song = str(row['Song']).replace("'", "''")
        composer = str(row['csong_normalized']).replace("'", "''")

        if composer.lower() in ['nan', '']:
            continue  # Lewati data tanpa composer

        f.write(f"INSERT INTO master_song (song_id,song, composer) VALUES ('{songID}','{song}', '{composer}');\n")

print("✅ Semua perintah INSERT telah disimpan ke 'insert_statements.txt'")
