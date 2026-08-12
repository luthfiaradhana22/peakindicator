# Bingo Peak Behavior — Streamlit Tracker

Versi trackable dari kartu **Bingo Peak Behavior — Revalue Academy**. Satu kartu
dipakai bareng: **4 admin** (lo + 3 orang lainnya) yang berhak nyentang tile,
sisanya (member) buka link yang sama dan cuma bisa **lihat** hasilnya —
lengkap dengan counter per kategori (baris) dan overall, plus fase pasar
(Akumulasi / Optimisme / Euforia / Puncak).

Data disimpan online pakai **JSONBin.io** (bukan security-wall, cuma tempat
nyimpen data biar gak ilang tiap kali app reload) — setupnya jauh lebih
simpel dibanding Google Sheets: gak perlu enable API, gak perlu bikin service
account, tinggal 1 API key + 1 bin.

---

## Bagian 0 — yang lo butuhkan sebelum mulai
- Akun [jsonbin.io](https://jsonbin.io) (gratis, cukup email)
- Akun GitHub (gratis, buat naro kode)
- Akun [share.streamlit.io](https://share.streamlit.io) (gratis, daftar pakai akun GitHub)

Total waktu: ±10 menit.

---

## Bagian 1 — Bikin tempat nyimpen data (JSONBin.io)

1. Daftar/login di [jsonbin.io](https://jsonbin.io).
2. Ke menu **API Keys** di dashboard → copy key yang namanya **X-MASTER-KEY**. Simpan dulu di notes.
3. Ke menu **Bins** → **Create Bin** (atau tombol **+**).
4. Kasih nama bebas (mis. "bingo-peak-behavior"), lalu di kotak isi JSON, paste konten ini apa adanya:

```json
{
  "K1": {"checked": false, "by": "", "at": ""},
  "K2": {"checked": false, "by": "", "at": ""},
  "K3": {"checked": false, "by": "", "at": ""},
  "K4": {"checked": false, "by": "", "at": ""},
  "K5": {"checked": false, "by": "", "at": ""},
  "M1": {"checked": false, "by": "", "at": ""},
  "M2": {"checked": false, "by": "", "at": ""},
  "M3": {"checked": false, "by": "", "at": ""},
  "M4": {"checked": false, "by": "", "at": ""},
  "M5": {"checked": false, "by": "", "at": ""},
  "D1": {"checked": false, "by": "", "at": ""},
  "D2": {"checked": false, "by": "", "at": ""},
  "D3": {"checked": false, "by": "", "at": ""},
  "D4": {"checked": false, "by": "", "at": ""},
  "D5": {"checked": false, "by": "", "at": ""},
  "G1": {"checked": false, "by": "", "at": ""},
  "G2": {"checked": false, "by": "", "at": ""},
  "G3": {"checked": false, "by": "", "at": ""},
  "G4": {"checked": false, "by": "", "at": ""},
  "G5": {"checked": false, "by": "", "at": ""},
  "P1": {"checked": false, "by": "", "at": ""},
  "P2": {"checked": false, "by": "", "at": ""},
  "P3": {"checked": false, "by": "", "at": ""},
  "P4": {"checked": false, "by": "", "at": ""},
  "P5": {"checked": false, "by": "", "at": ""}
}
```

5. Klik **Create** / **Save**. Lihat URL bin yang barusan dibuat, bentuknya:
   `https://jsonbin.io/.../b/`**`65f1a2...abcd`**
   → copy ID itu (deretan huruf-angka setelah `/b/`). Itu **Bin ID** lo, simpan di notes.

---

## Bagian 2 — Siapkan 4 nama & password admin

Tentukan nama + password buat lo dan 3 orang lainnya yang berhak nyentang tile. Bebas, contoh:

```
Rugassi = "orange123"
Budi    = "peakbehavior1"
Ani     = "cuan2026"
Cici    = "bearish99"
```

Password ini cuma dipegang 4 orang ini — member lain yang buka link tidak akan lihat opsi ini kalau mereka tidak tahu password-nya.

---

## Bagian 3 — Naro kode ke GitHub

1. Pastikan lo punya folder ini (`app.py`, `tiles.py`, `requirements.txt`, `README.md`, `.streamlit/secrets.toml.example`).
2. Buka [github.com/new](https://github.com/new) → kasih nama repo (mis. `bingo-peak-behavior`) → pilih **Private** atau **Public**, terserah → **Create repository**.
3. Upload semua file ke repo tsb via tombol **"uploading an existing file"** → drag semua file & folder → **Commit changes**.
   - Jangan upload file `secrets.toml` yang udah keisi API key asli — cukup upload `secrets.toml.example` yang masih placeholder (udah ada di folder ini, aman di-upload apa adanya).

---

## Bagian 4 — Deploy ke Streamlit Community Cloud

1. Buka [share.streamlit.io](https://share.streamlit.io) → login pakai GitHub → **Create app**.
2. Pilih **"Deploy a public app from GitHub"** → pilih repo tadi → branch `main` → **Main file path**: `app.py`.
3. **Sebelum klik Deploy**, klik **Advanced settings** → bagian **Secrets** → paste ini (edit dulu nilai-nilainya):

```toml
jsonbin_api_key = "PASTE_X-MASTER-KEY_DARI_BAGIAN_1"
jsonbin_bin_id  = "PASTE_BIN_ID_DARI_BAGIAN_1"

[admins]
Rugassi = "orange123"
Budi = "peakbehavior1"
Ani = "cuan2026"
Cici = "bearish99"
```

   (Kalau app udah kadung ke-deploy duluan: buka app di dashboard Streamlit Cloud → **⋮** → **Settings** → **Secrets** → paste di sana → **Save**, app otomatis restart.)

4. Klik **Deploy**. Tunggu 1–3 menit sampai status jadi hijau/"Running".
5. App lo sekarang punya URL publik (`https://xxxxx.streamlit.app`). **Ini link yang lo share ke semua member.**

---

## Bagian 5 — Coba pakai

- **Sebagai admin (lo/3 lainnya):** buka link → sidebar kiri → pilih nama dari dropdown → masukin password → **Login**. Tombol "Centang"/"Un-centang" muncul di bawah tiap tile. Klik untuk toggle — langsung tersimpan dan langsung kelihatan buat semua orang begitu mereka buka/refresh halaman. Tiap tile yang kecentang nunjukin siapa yang nyentang & kapan.
- **Sebagai member biasa:** buka link yang sama, langsung lihat kartu, counter per kategori, overall counter, dan fase pasar — tanpa perlu login apa pun, dan tanpa ada tombol apa pun buat diklik-klik asal.
- Tombol **🔄 Refresh data** di sidebar buat force-reload kalau merasa datanya belum ter-update.

---

## Troubleshooting singkat
- **"Gagal konek ke JSONBin"** → cek `jsonbin_api_key` dan `jsonbin_bin_id` di secrets, pastikan sama persis dengan yang ada di dashboard jsonbin.io.
- **Login admin gagal terus** → cek nama yang dipilih di dropdown sama persis (termasuk huruf besar/kecil) dengan key di `[admins]` pada secrets.
- **Perubahan tidak muncul di HP/browser lain** → klik tombol 🔄 Refresh data, atau tutup-buka lagi tab-nya.

## Kalau nanti mau ganti storage lagi
Fungsi `load_state()` / `save_toggle()` di `app.py` isinya cuma manggil JSONBin lewat `requests` — kalau nanti mau pindah ke Google Sheets/database lain, tinggal ganti isi dua fungsi itu, struktur datanya (`checked, by, at` per kode tile) tetap sama.
