import pandas as pd
from unidecode import unidecode
from tqdm import tqdm

# Baca file Excel
df = pd.read_excel("master_song.xlsx")

# Deteksi bahasa dari song_id
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

df["language"] = df["song_id"].apply(detect_language)

# Ambil 6 huruf awal dari judul (dari kata dalam tanda kurung jika ada), setelah di-unidecode
def generate_title_code(title):
    if pd.isnull(title):
        return "000000"
    
    if '(' in title:
        content = title.split('(')[-1].replace(')', '').strip()
    else:
        content = title.strip()

    content_ascii = unidecode(content)
    words = content_ascii.split()
    chars = [word[0].upper() for word in words if word]
    while len(chars) < 6:
        chars.append("0")
    return ''.join(chars[:6])

# Ambil 3 huruf dari composer pertama setelah transliterasi dan sebelum tanda "("
def extract_composer_code(composer_raw):
    if pd.isnull(composer_raw) or composer_raw.strip() == "":
        return "000"
    
    composer_clean = composer_raw.split('(')[0]
    first_composer = composer_clean.split(",")[0].split("&")[0].split("|")[0].strip()
    first_composer = unidecode(first_composer)
    
    parts = first_composer.split()
    if not parts:
        return "000"

    first = parts[0][0].upper() if len(parts[0]) > 0 else "0"
    last = parts[-1][0].upper() if len(parts) > 1 else parts[0][0].upper()
    middle = parts[1][0].upper() if len(parts) > 2 else "0"

    return f"{first}{last}{middle}"

# Tambahkan kolom kode judul dan composer
df["title_code"] = df["song"].apply(generate_title_code)
df["composer_code"] = df["composer"].apply(extract_composer_code)

# Hitung increment berdasarkan kombinasi unik (title_code + composer_code)
df["key_combo"] = df["language"] + "0" + df["title_code"] + df["composer_code"]

increment_map = {}
new_ids = []

for key in df["key_combo"]:
    if key not in increment_map:
        increment_map[key] = 1
    else:
        increment_map[key] += 1
    new_ids.append(str(increment_map[key]).zfill(2))  # e.g. 01, 02

df["increment"] = new_ids
df["new_id"] = df["language"] + "0" + df["title_code"] + df["increment"] + df["composer_code"]

# Simpan ke Excel
df.to_excel("data_lagu_dengan_id_baru.xlsx", index=False)