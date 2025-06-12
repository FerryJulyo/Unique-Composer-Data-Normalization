import pandas as pd
from unidecode import unidecode
from tqdm import tqdm
import re

# Baca file Excel
df = pd.read_excel("master_song.xlsx")

# Fungsi deteksi bahasa dari song_id
def detect_language(song_id):
    str_id = str(song_id)
    if str_id.startswith("91"): return "ID"
    elif str_id.startswith("92"): return "EN"
    elif str_id.startswith("93"): return "CN"
    elif str_id.startswith("1"): return "ID"
    elif str_id.startswith("2"): return "EN"
    elif str_id.startswith("3"): return "CN"
    elif str_id.startswith("4"): return "JP"
    elif str_id.startswith("5"): return "KR"
    elif str_id.startswith("6"): return "IN"
    elif str_id.startswith("7"): return "PH"
    elif str_id.startswith("8"): return "TH"
    else: return "Unknown"

df["language"] = df["song_id"].apply(detect_language)

# Karakter pembatas untuk potong string
stop_chars = ['(', '"', "'", '[', '{', '|', '&', '“', '‘']

def clean_text(text):
    if pd.isnull(text):
        return ""
    text = unidecode(str(text))
    # Potong di karakter pembatas pertama
    for char in stop_chars:
        if char in text:
            text = text.split(char)[0]
    # Bersihkan dari karakter non-alfabet + angka + spasi
    text = re.sub(r'[^A-Za-z0-9 ]', '', text)
    return text.strip()

# 6 huruf pertama dari judul
def generate_title_code(title):
    clean_title = clean_text(title)
    words = clean_title.split()
    chars = [word[0].upper() for word in words if word]
    while len(chars) < 6:
        chars.append("0")
    return ''.join(chars[:6])

# 3 huruf dari composer
def extract_composer_code(composer_raw):
    clean_composer = clean_text(composer_raw)
    first_composer = clean_composer.split(",")[0].strip()
    parts = first_composer.split()
    if not parts:
        return "000"
    first = parts[0][0].upper() if len(parts[0]) > 0 else "0"
    last = parts[-1][0].upper() if len(parts) > 1 else parts[0][0].upper()
    middle = parts[1][0].upper() if len(parts) > 2 else "0"
    return f"{first}{last}{middle}"

# Tambahkan kolom kode
df["title_code"] = df["song"].apply(generate_title_code)
df["composer_code"] = df["composer"].apply(extract_composer_code)

# Gabungan language + title + composer untuk deteksi duplikat
df["key_combo"] = df["language"] + "0" + df["title_code"] + df["composer_code"]

# Hitung increment berdasarkan key_combo
increment_map = {}
new_ids = []

for key in df["key_combo"]:
    if key not in increment_map:
        increment_map[key] = 1
    else:
        increment_map[key] += 1
    new_ids.append(str(increment_map[key]).zfill(2))  # 01, 02, ...

df["increment"] = new_ids

# Final new_id
df["new_id"] = df["language"] + "0" + df["title_code"] + df["increment"] + df["composer_code"]

# Simpan ke file
df.to_excel("data_lagu_dengan_id_baru.xlsx", index=False)

print("✅ Selesai! File disimpan sebagai data_lagu_dengan_id_baru.xlsx")
