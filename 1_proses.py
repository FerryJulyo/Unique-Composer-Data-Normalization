import pandas as pd
from rapidfuzz import fuzz

# Baca data dari file Excel
df = pd.read_excel("master_vod.xlsx")
df = df[['SongID', 'Song', 'csong']]

# Ubah ke string
df['csong'] = df['csong'].fillna('').astype(str)
df['Song'] = df['Song'].fillna('').astype(str)

# Bagi dua: dengan dan tanpa csong
df_with_csong = df[df['csong'].str.strip() != ''].copy()
df_without_csong = df[df['csong'].str.strip() == ''].copy()

# Gabungkan untuk df_with_csong
df_with_csong['combined'] = df_with_csong['Song'].str.strip() + " - " + df_with_csong['csong'].str.strip()

# Fungsi normalisasi fuzzy
def normalize_pairs(pairs, threshold=95):
    unique_list = []
    mapping = {}
    total = len(pairs)
    bar_width = 20

    for i, pair in enumerate(pairs, start=1):
        pair = str(pair).strip()
        matched = False

        for unique in unique_list:
            score = fuzz.ratio(pair.lower(), unique.lower())
            if score >= threshold:
                mapping[pair] = unique
                matched = True
                break

        if not matched:
            unique_list.append(pair)
            mapping[pair] = pair

        percent = int(i / total * 100)
        filled = int(bar_width * percent / 100)
        bar = "[" + "=" * filled + " " * (bar_width - filled) + f"] {percent}%"
        print(bar, end='\r', flush=True)

    print()
    return mapping

# Normalisasi hanya untuk baris dengan csong
mapping = normalize_pairs(df_with_csong['combined'])
df_with_csong['normalized_pair'] = df_with_csong['combined'].map(mapping)
df_with_csong = df_with_csong.groupby('normalized_pair', as_index=False).first()
df_with_csong[['song_normalized', 'csong_normalized']] = df_with_csong['normalized_pair'].str.split(' - ', n=1, expand=True)

# Gabungkan lagi dengan baris yang tidak punya csong
df_without_csong = df_without_csong.rename(columns={'Song': 'song_normalized', 'csong': 'csong_normalized'})
df_all = pd.concat([
    df_with_csong[['SongID', 'song_normalized', 'csong_normalized']],
    df_without_csong[['SongID', 'song_normalized', 'csong_normalized']]
])

# Format kolom akhir
df_output = df_all.rename(columns={
    'SongID': 'song_id',
    'song_normalized': 'song',
    'csong_normalized': 'composer'
})[['song_id', 'song', 'composer']]

# Simpan ke file
df_output.to_excel("new_data.xlsx", index=False)
print("✅ Semua data termasuk csong kosong berhasil dimasukkan ke 'new_data.xlsx'")
