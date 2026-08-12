import streamlit as st
import requests
from datetime import datetime

from tiles import TILES, TILES_BY_CODE, CATEGORIES, get_phase

st.set_page_config(
    page_title="Bingo Peak Behavior — Revalue Academy",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# THEME (mengikuti palet kartu asli)
# ---------------------------------------------------------------------------
ORANGE = "#E15A1D"
ORANGE_DARK = "#B8410F"
ORANGE_SOFT = "#F9D9C4"
ORANGE_PALE = "#FDEFE4"
INK = "#3A2418"

st.markdown(
    f"""
    <style>
    .block-container {{
        padding-top: 3.6rem;
        padding-bottom: 1.5rem;
        padding-left: 2.4rem;
        padding-right: 2.4rem;
        max-width: 100%;
    }}
    .stApp {{ background-color: #FFFDFB; }}
    h1, h2, h3 {{ color: {INK}; }}
    [data-testid="stSidebar"] {{ padding-top: 1rem; }}

    /* ---------- Mobile default (< 768px): 1 kolom, tinggi kotak nyesuain teks ---------- */
    .tile-box {{
        box-sizing: border-box;
        border: 2.5px solid {ORANGE};
        border-radius: 9px;
        padding: 12px 14px;
        height: auto;
        min-height: 0;
        margin-bottom: 8px;
        font-weight: 700;
        font-size: 14px;
        line-height: 1.3;
        color: {INK};
        background: #fff;
        display: block;
        transition: background .12s ease;
    }}
    .tile-box.on {{
        background: {ORANGE};
        color: #fff;
        border-color: {ORANGE_DARK};
    }}
    .tile-box.highlight {{
        background: {ORANGE_PALE};
        border-color: {ORANGE_DARK};
    }}
    .tile-box.highlight.on {{
        background: {ORANGE};
        color: #fff;
    }}
    .cat-header {{
        box-sizing: border-box;
        text-align: center;
        font-weight: 800;
        letter-spacing: .06em;
        text-transform: uppercase;
        font-size: 12px;
        color: {ORANGE_DARK};
        background: {ORANGE_PALE};
        border: 1.5px solid {ORANGE_SOFT};
        border-radius: 999px;
        padding: 6px 8px;
        margin-bottom: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    div.stButton > button {{
        width: 100%;
        border: 1.5px solid {ORANGE};
        background: #fff;
        color: {ORANGE_DARK};
        font-weight: 700;
        font-size: 12.5px;
        padding: 4px 0;
        min-height: 0;
        line-height: 1.6;
        margin-top: -3px;
        margin-bottom: 9px;
    }}
    div.stButton > button:hover {{
        background: {ORANGE_PALE};
        border-color: {ORANGE_DARK};
    }}
    .thin-rule {{
        border: none;
        border-top: 1px solid {ORANGE_SOFT};
        margin: 10px 0;
    }}

    /* ---------- Tablet / iPad portrait (768px–1279px): kolom mulai berdampingan,
       teks dikecilin & kotak dikasih tinggi TETAP biar rapi sebaris ---------- */
    @media (min-width: 768px) and (max-width: 1279px) {{
        .tile-box {{
            height: 96px;
            font-size: 11.5px;
            line-height: 1.25;
            padding: 8px 10px;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 4;
            overflow: hidden;
        }}
        .cat-header {{
            font-size: 9.5px;
            letter-spacing: .02em;
            padding: 5px 4px;
            min-height: 32px;
        }}
    }}

    /* ---------- Desktop lebar (>= 1280px): kolom lega, teks digedein
       biar rasio teks:kotak enak dibaca, tinggi kotak tetap biar sebaris ---------- */
    @media (min-width: 1280px) {{
        .tile-box {{
            height: 78px;
            font-size: 15.5px;
            line-height: 1.28;
            padding: 12px 16px;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 3;
            overflow: hidden;
        }}
        .cat-header {{
            font-size: 13px;
            letter-spacing: .05em;
            padding: 6px 10px;
            min-height: 30px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# JSONBIN.IO BACKEND
# ---------------------------------------------------------------------------
JSONBIN_URL = f'https://api.jsonbin.io/v3/b/{st.secrets.get("jsonbin_bin_id", "")}'
JSONBIN_HEADERS = {
    "X-Master-Key": st.secrets.get("jsonbin_api_key", ""),
    "Content-Type": "application/json",
}


def _default_data():
    return {t["code"]: {"checked": False, "by": "", "at": ""} for t in TILES}


def load_state():
    resp = requests.get(f"{JSONBIN_URL}/latest", headers=JSONBIN_HEADERS, timeout=10)
    resp.raise_for_status()
    record = resp.json().get("record", {})
    state, meta = {}, {}
    for t in TILES:
        entry = record.get(t["code"], {})
        state[t["code"]] = bool(entry.get("checked", False))
        meta[t["code"]] = {"by": entry.get("by", ""), "at": entry.get("at", "")}
    return state, meta


def save_toggle(code, new_value, by):
    # ambil data terbaru dulu biar gak nimpa perubahan admin lain
    resp = requests.get(f"{JSONBIN_URL}/latest", headers=JSONBIN_HEADERS, timeout=10)
    resp.raise_for_status()
    record = resp.json().get("record", {}) or _default_data()
    record[code] = {
        "checked": bool(new_value),
        "by": by,
        "at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    put = requests.put(JSONBIN_URL, headers=JSONBIN_HEADERS, json=record, timeout=10)
    put.raise_for_status()


# ---------------------------------------------------------------------------
# ADMIN LOGIN (sidebar)
# ---------------------------------------------------------------------------
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "admin_name" not in st.session_state:
    st.session_state.admin_name = ""

ADMINS = st.secrets.get("admins", {})  # {"Nama": "password", ...}

with st.sidebar:
    st.markdown("### Akses")
    if st.session_state.is_admin:
        st.success(f"Mode admin aktif — login sebagai **{st.session_state.admin_name}**.")
        if st.button("Logout admin"):
            st.session_state.is_admin = False
            st.session_state.admin_name = ""
            st.rerun()
    else:
        names = list(ADMINS.keys())
        if names:
            selected_name = st.selectbox("Nama", names)
        else:
            selected_name = st.text_input("Nama")
        pw = st.text_input("Password admin", type="password")
        if st.button("Login"):
            correct_pw = ADMINS.get(selected_name)
            if pw and correct_pw and pw == correct_pw:
                st.session_state.is_admin = True
                st.session_state.admin_name = selected_name
                st.rerun()
            else:
                st.error("Nama/password salah.")
        st.caption("Member lain cukup buka link ini tanpa login — mode lihat-lihat aja.")

    st.divider()
    if st.button("🔄 Refresh data"):
        st.rerun()

# ---------------------------------------------------------------------------
# LOAD STATE
# ---------------------------------------------------------------------------
try:
    state, meta = load_state()
except Exception as e:
    st.error(
        "Gagal konek ke JSONBin. Cek konfigurasi secrets "
        "(jsonbin_api_key, jsonbin_bin_id) — pastikan sudah diisi dan bin ID-nya benar."
    )
    st.exception(e)
    st.stop()

# ---------------------------------------------------------------------------
# HEADER (dipadetin jadi 1 baris biar hemat tempat)
# ---------------------------------------------------------------------------
total_checked = sum(state.values())
total = len(TILES)
pct = total_checked / total if total else 0
phase_name, phase_desc = get_phase(pct)

st.markdown(
    f"""
    <div style="display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;margin-bottom:10px;">
        <div>
            <span style="font-family:sans-serif;font-weight:800;font-size:32px;color:{ORANGE};">
            BINGO PEAK BEHAVIOR</span>
            <div style="font-size:13px;color:#8a6a55;font-weight:600;">
            Centang yang udah kelihatan minggu ini — makin banyak kena, makin mahal harga optimisme yang lagi lo bayar.
            </div>
        </div>
        <div style="text-align:right;min-width:280px;">
            <span style="font-weight:800;font-size:26px;color:{INK};">{total_checked} / {total} kena</span>
            <span style="font-weight:700;font-size:14px;color:{ORANGE_DARK};"> ({pct*100:.0f}%)</span>
            <div style="font-size:14px;font-weight:700;color:{ORANGE_DARK};">Fase pasar: {phase_name} — {phase_desc}</div>
        </div>
    </div>
    <hr class="thin-rule">
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# GRID
# ---------------------------------------------------------------------------
cols = st.columns(5)
for col, (cat_code, cat_name) in zip(cols, CATEGORIES):
    with col:
        cat_tiles = [t for t in TILES if t["cat"] == cat_code]
        cat_checked = sum(state[t["code"]] for t in cat_tiles)
        st.markdown(
            f'<div class="cat-header">{cat_name} · {cat_checked}/{len(cat_tiles)}</div>',
            unsafe_allow_html=True,
        )
        for t in cat_tiles:
            code = t["code"]
            is_on = state[code]
            css_class = "tile-box"
            if t.get("highlight"):
                css_class += " highlight"
            if is_on:
                css_class += " on"
            mark = "✅ " if is_on else ""
            st.markdown(
                f'<div class="{css_class}">{mark}{t["text"]}</div>',
                unsafe_allow_html=True,
            )
            if st.session_state.is_admin:
                label = "Un-centang" if is_on else "Centang"
                if st.button(label, key=f"btn_{code}", use_container_width=True):
                    save_toggle(code, not is_on, by=st.session_state.admin_name)
                    st.rerun()

st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)
st.markdown(
    f'<div style="font-size:10.5px;color:#8a6a55;">'
    f"Alat observasi, bukan sinyal jual-beli. Data tersimpan bareng untuk semua member — "
    f"hanya admin yang bisa mengubah status centang.</div>",
    unsafe_allow_html=True,
)
