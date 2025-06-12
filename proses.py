import pandas as pd
from rapidfuzz import fuzz

# Baca data dari file Excel
df = pd.read_excel("master_vod.xlsx")  # Ganti dengan nama file Excel kamu

# Pastikan kolom yang dibaca bernama 'Song' dan 'csong'
df = df[['Song', 'csong']]

# Fungsi untuk menormalkan nama csong berdasarkan kemiripan
def normalize_csongs(csongs, threshold=90):
    unique_list = []
    mapping = {}

    print("=== Proses normalisasi nama csong ===")
    for csong in csongs:
        matched = False
        for unique in unique_list:
            score = fuzz.ratio(csong.lower(), unique.lower())
            print(f"Membandingkan '{csong}' dengan '{unique}' => Skor: {score}")
            if score >= threshold:
                mapping[csong] = unique
                print(f"➡️  '{csong}' dianggap sama dengan '{unique}' (skor {score})")
                matched = True
                break
        if not matched:
            unique_list.append(csong)
            mapping[csong] = csong
            print(f"✅  '{csong}' ditambahkan sebagai nama unik baru")
    print("=== Normalisasi selesai ===\n")
    return mapping

# Normalisasi nama csong
mapping = normalize_csongs(df['csong'])
df['csong_normalized'] = df['csong'].map(mapping)

# Ambil hanya data unik berdasarkan Song dan csong_normalized
df_unique = df.drop_duplicates(subset=['Song', 'csong_normalized'])

# Simpan hasil ke file baru
df_unique.to_excel("output_unique.xlsx", index=False)

print("✅ Data unik telah disimpan di 'output_unique.xlsx'")
