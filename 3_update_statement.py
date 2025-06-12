import pandas as pd

# Ganti dengan path ke file Excel Anda
file_path = 'data_lagu_dengan_id_baru.xlsx'
output_file = 'update_master_song.txt'

# Baca file Excel
df = pd.read_excel(file_path, engine='openpyxl')

# Ambil kolom id dan new_id
df = df[['id', 'new_id']]

# Tulis update statement ke file
with open(output_file, 'w') as f:
    for index, row in df.iterrows():
        f.write(f"UPDATE master_song SET song_id = '{row['new_id']}' WHERE id = {row['id']};\n")

print(f"SQL update statements saved to {output_file}")
