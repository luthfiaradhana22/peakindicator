import streamlit as st
import requests
from datetime import datetime

from tiles import TILES, TILES_BY_CODE, CATEGORIES, get_phase

st.set_page_config(
    page_title="Bingo Peak Behavior — Revalue Academy",
    page_icon="🎯",
    layout="wide",
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
        padding-top: 1.2rem;
        padding-bottom: 0.6rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }}
    .stApp {{ background-color: #FFFDFB; }}
    h1, h2, h3 {{ color: {INK}; }}
    [data-testid="stSidebar"] {{ padding-top: 1rem; }}
    .tile-box {{
        border: 2.5px solid {ORANGE};
        border-radius: 8px;
        padding: 6px 8px;
        min-height: 50px;
        margin-bottom: 3px;
        font-weight: 700;
        font-size: 11.5px;
        line-height: 1.15;
        color: {INK};
        background: #fff;
        display: flex;
        align-items: center;
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
        text-align: center;
        font-weight: 800;
        letter-spacing: .06em;
        text-transform: uppercase;
        font-size: 10.5px;
        color: {ORANGE_DARK};
        background: {ORANGE_PALE};
        border: 1.5px solid {ORANGE_SOFT};
        border-radius: 999px;
        padding: 3px 6px;
        margin-bottom: 5px;
    }}
    div.stButton > button {{
        width: 100%;
        border: 1.5px solid {ORANGE};
        background: #fff;
        color: {ORANGE_DARK};
        font-weight: 700;
        font-size: 10px;
        padding: 1px 0;
        min-height: 0;
        line-height: 1.6;
        margin-top: -1px;
        margin-bottom: 4px;
    }}
    div.stButton > button:hover {{
        background: {ORANGE_PALE};
        border-color: {ORANGE_DARK};
    }}
    .cat-count {{
        text-align: center;
        font-weight: 700;
        font-size: 11px;
        color: {ORANGE_DARK};
        margin-top: 2px;
    }}
    .thin-rule {{
        border: none;
        border-top: 1px solid {ORANGE_SOFT};
        margin: 8px 0;
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
    <div style="display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;margin-bottom:6px;">
        <div>
            <span style="font-family:sans-serif;font-weight:800;font-size:26px;color:{ORANGE};">
            BINGO PEAK BEHAVIOR</span>
            <div style="font-size:11.5px;color:#8a6a55;font-weight:600;">
            Centang yang udah kelihatan minggu ini — makin banyak kena, makin mahal harga optimisme yang lagi lo bayar.
            </div>
        </div>
        <div style="text-align:right;min-width:260px;">
            <span style="font-weight:800;font-size:20px;color:{INK};">{total_checked} / {total} kena</span>
            <span style="font-weight:700;font-size:12.5px;color:{ORANGE_DARK};"> ({pct*100:.0f}%)</span>
            <div style="font-size:12px;font-weight:700;color:{ORANGE_DARK};">Fase pasar: {phase_name} — {phase_desc}</div>
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
        st.markdown(f'<div class="cat-header">{cat_name}</div>', unsafe_allow_html=True)
        cat_tiles = [t for t in TILES if t["cat"] == cat_code]
        cat_checked = sum(state[t["code"]] for t in cat_tiles)
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
        st.markdown(
            f'<div class="cat-count">{cat_checked} / {len(cat_tiles)} kena</div>',
            unsafe_allow_html=True,
        )

st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)
st.markdown(
    f'<div style="font-size:10.5px;color:#8a6a55;">'
    f"Alat observasi, bukan sinyal jual-beli. Data tersimpan bareng untuk semua member — "
    f"hanya admin yang bisa mengubah status centang.</div>",
    unsafe_allow_html=True,
)
