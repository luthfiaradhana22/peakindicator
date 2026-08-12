# Data 25 tile Bingo Peak Behavior — Revalue Academy
# Urutan & teks persis mengikuti bingo_peak_behavior_card.html

CATEGORIES = [
    ("K", "Keramaian"),
    ("M", "Media & Narasi"),
    ("D", "Pasar & Data"),
    ("G", "Greed o' Meter"),
    ("P", "Kepastian"),
]

TILES = [
    # Keramaian
    {"code": "K1", "cat": "K", "text": "Lingkar keluarga & teman dekat pada bahas saham"},
    {"code": "K2", "cat": "K", "text": "Banyak bahas saham di ruang publik"},
    {"code": "K3", "cat": "K", "text": "Profesi jauh dari finance ikut ngomongin saham"},
    {"code": "K4", "cat": "K", "text": "Newbie ngaku punya info A1"},
    {"code": "K5", "cat": "K", "text": "Banyak yang join & buka kelas saham"},
    # Media & Narasi
    {"code": "M1", "cat": "M", "text": "Artis gak nyambung bikin konten saham"},
    {"code": "M2", "cat": "M", "text": "Story isinya screenshot cuan tiap hari"},
    {"code": "M3", "cat": "M", "text": "Pidato Prabowo malah bikin pasar saham naik"},
    {"code": "M4", "cat": "M", "text": "Narasi mengerucut ke satu cerita yang sama"},
    {"code": "M5", "cat": "M", "text": "Pemerintah claim IHSG naik berkat mereka"},
    # Pasar & Data
    {"code": "D1", "cat": "D", "text": "Transaksi BUMI dominasi bursa"},
    {"code": "D2", "cat": "D", "text": "Transaksi di saham kapitalisasi kecil gede banget"},
    {"code": "D3", "cat": "D", "text": "Sekuritas Permudah Akses akun margin/leverage", "highlight": True},
    {"code": "D4", "cat": "D", "text": "Uang dari bisnis riil diputer di pasar saham"},
    {"code": "D5", "cat": "D", "text": "Banyak banget IPO & rights issue"},
    # Greed o' Meter
    {"code": "G1", "cat": "G", "text": "Tabungan pindah ke RDN, all-in tanpa sisa"},
    {"code": "G2", "cat": "G", "text": "Susah cari entry bagus, jadinya hajar kanan"},
    {"code": "G3", "cat": "G", "text": "Berat banget jual saham yang udah naik 100%+"},
    {"code": "G4", "cat": "G", "text": "Si paling funda ikut beli saham narasi"},
    {"code": "G5", "cat": "G", "text": "Cuan belum cair udah dibelanjain"},
    # Kepastian
    {"code": "P1", "cat": "P", "text": "Agenda saham narasi terbongkar, target price keluar"},
    {"code": "P2", "cat": "P", "text": "Mulai banyak yang kasih target price IHSG"},
    {"code": "P3", "cat": "P", "text": "\u201cKonglo X pasti bener, market cap minimal sekian T\u201d"},
    {"code": "P4", "cat": "P", "text": "Yang bilang hati-hati malah dibully"},
    {"code": "P5", "cat": "P", "text": "Hasrat pensiun kerja memuncak"},
]

TILES_BY_CODE = {t["code"]: t for t in TILES}

PHASES = [
    (0.25, "Akumulasi", "Pasar masih sepi. Barang bagus masih bisa ditawar."),
    (0.50, "Optimisme", "Udah rame tapi masih ada skeptis. Skeptis bikin kenaikan sehat."),
    (0.75, "Euforia", "Suara hati-hati hilang. Ukur risiko, bukan tambah target."),
    (1.01, "Puncak", "Semua yakin, gak ada sisa pembeli. Kurangi ukuran posisi."),
]


def get_phase(pct: float):
    """pct is a fraction 0..1"""
    for threshold, name, desc in PHASES:
        if pct <= threshold:
            return name, desc
    return PHASES[-1][1], PHASES[-1][2]
