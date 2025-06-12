import pandas as pd
from tqdm import tqdm

# Baca file Excel
df = pd.read_excel("master_song.xlsx")

# Fungsi untuk menentukan bahasa berdasarkan song_id
def detect_language(song_id):
    str_id = str(song_id)
    if str_id.startswith("91"):
        return "ID"
    elif str_id.startswith("92"):
        return "EN"
    elif str_id.startswith("93"):
        return "CN"
    elif str_id.startswith("1"):
        return "ID"
    elif str_id.startswith("2"):
        return "EN"
    elif str_id.startswith("3"):
        return "CN"
    elif str_id.startswith("4"):
        return "JP"
    elif str_id.startswith("5"):
        return "KR"
    elif str_id.startswith("6"):
        return "IN"
    elif str_id.startswith("7"):
        return "PH"
    elif str_id.startswith("8"):
        return "TH"
    else:
        return "Unknown"

# Deteksi bahasa
df["language"] = df["song_id"].apply(detect_language)

# Fungsi untuk buat 6 huruf dari huruf awal tiap kata judul lagu
def generate_title_code(title):
    words = title.strip().split()
    chars = [word[0].upper() for word in words if word]
    while len(chars) < 6:
        chars.append("0")
    return ''.join(chars[:6])

# Fungsi ambil 3 huruf dari composer pertama
def extract_composer_code(composer_raw):
    if pd.isnull(composer_raw) or composer_raw.strip() == "":
        return "000"
    
    # Ambil composer pertama (split dengan ",", "&", "|")
    first_composer = composer_raw.split(",")[0].split("&")[0].split("|")[0].strip()

    parts = first_composer.split()
    if not parts:
        return "000"
    
    first = parts[0][0].upper() if len(parts[0]) > 0 else "0"
    last = parts[-1][0].upper() if len(parts) > 1 else parts[0][0].upper()
    middle = parts[1][0].upper() if len(parts) > 2 else "0"
    
    return f"{first}{last}{middle}"

# Fungsi gabungan untuk membuat new_id
def generate_new_id(row, index):
    lang = row["language"]
    title_code = generate_title_code(row["song"])
    composer_code = extract_composer_code(row["composer"])
    increment = str(index + 1).zfill(2)  # Mulai dari 01
    return f"{lang}0{title_code}{increment}{composer_code}"

# Proses semua baris dan buat kolom new_id
df["new_id"] = [generate_new_id(row, idx) for idx, row in df.iterrows()]

# Simpan ke Excel baru
df.to_excel("data_lagu_dengan_id_baru.xlsx", index=False)
