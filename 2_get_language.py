import pandas as pd

# Baca file Excel
df = pd.read_excel("data_lagu.xlsx")

# Fungsi untuk menentukan bahasa
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

# Tambahkan kolom language
df["language"] = df["song_id"].apply(detect_language)

# Simpan ke file baru
df.to_excel("data_lagu_dengan_bahasa.xlsx", index=False)

print(df)
