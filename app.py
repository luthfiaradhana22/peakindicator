import streamlit as st
import requests
from datetime import datetime

from tiles import TILES, TILES_BY_CODE, CATEGORIES, get_phase
from icons import ICON_DEFS

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
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

# ikon-ikon dari kartu asli, ditaruh tersembunyi, direferensikan tiap tile via <use>
st.markdown(
    f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{ICON_DEFS}</defs></svg>',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
    .title-wrap {{
        font-family: 'Baloo 2', cursive;
        font-weight: 800;
        font-size: clamp(28px, 3vw, 42px);
        line-height: 1;
        letter-spacing: .005em;
        white-space: nowrap;
    }}
    .title-wrap .tb {{
        color: {ORANGE};
        -webkit-text-stroke: 5px #fff;
        paint-order: stroke fill;
        filter: drop-shadow(2px 2px 0 {ORANGE_DARK});
    }}
    .title-wrap .tp {{
        color: #fff;
        -webkit-text-stroke: 5px {ORANGE};
        paint-order: stroke fill;
        filter: drop-shadow(2px 2px 0 {ORANGE_SOFT});
        margin-left: 6px;
    }}
    .brand {{
        display: flex;
        align-items: center;
        gap: 9px;
        justify-content: flex-end;
    }}
    .brand .r {{
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: {INK};
        color: #fff;
        font-family: 'Baloo 2', cursive;
        font-weight: 800;
        font-size: 21px;
        display: flex;
        align-items: center;
        justify-content: center;
        line-height: 1;
        flex-shrink: 0;
    }}
    .brand .r i {{ font-style: normal; color: {ORANGE}; }}
    .brand .wm {{ line-height: 1.05; text-align: left; }}
    .brand .wm b {{
        display: block;
        font-family: 'Baloo 2', cursive;
        font-weight: 700;
        font-size: 15px;
        letter-spacing: .02em;
        color: {INK};
    }}
    .brand .wm span {{
        display: block;
        font-size: 9px;
        letter-spacing: .26em;
        color: {ORANGE};
        font-weight: 700;
    }}
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
        position: relative;
        border: 2.5px solid {ORANGE};
        border-radius: 9px;
        padding: 10px 12px;
        height: auto;
        min-height: 0;
        margin-bottom: 8px;
        background: #fff;
        color: {INK};
        display: flex;
        align-items: center;
        gap: 9px;
        transition: background .12s ease, transform .12s ease;
    }}
    .tile-box .txt {{
        flex: 1 1 auto;
        font-family: 'Baloo 2', cursive;
        font-weight: 700;
        font-size: 14px;
        line-height: 1.28;
        color: {INK} !important;
    }}
    .tile-box .art {{
        flex: 0 0 auto;
        width: 30px;
        height: 30px;
        opacity: .95;
    }}
    .tile-box .stamp {{
        display: none;
        position: absolute;
        top: 5px;
        right: 5px;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        border: 2px solid #fff;
        background: rgba(0,0,0,.18);
        align-items: center;
        justify-content: center;
        font-size: 9px;
        color: #fff;
        line-height: 1;
    }}
    .tile-box.on {{
        background: {ORANGE};
        color: #fff;
        border-color: {ORANGE_DARK};
        transform: rotate(-.5deg);
    }}
    .tile-box.on .txt {{ color: #fff !important; }}
    .tile-box.on .art {{ filter: brightness(0) invert(1); opacity: .9; }}
    .tile-box.on .stamp {{ display: flex; }}
    .tile-box.highlight {{
        background: {ORANGE_PALE};
        border-color: {ORANGE_DARK};
        color: {INK};
    }}
    .tile-box.highlight .txt {{ color: {INK} !important; }}
    .tile-box.highlight.on {{
        background: {ORANGE};
        color: #fff;
    }}
    .tile-box.highlight.on .txt {{ color: #fff !important; }}
    .cat-header {{
        box-sizing: border-box;
        text-align: center;
        font-family: 'Baloo 2', cursive;
        font-weight: 700;
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
            height: 92px;
            padding: 7px 9px;
            gap: 6px;
            align-items: flex-start;
        }}
        .tile-box .txt {{
            font-size: 11px;
            line-height: 1.22;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 5;
            overflow: hidden;
        }}
        .tile-box .art {{ width: 22px; height: 22px; margin-top: 1px; }}
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
            height: 80px;
            padding: 10px 14px;
            gap: 10px;
        }}
        .tile-box .txt {{
            font-size: 14.5px;
            line-height: 1.26;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 3;
            overflow: hidden;
        }}
        .tile-box .art {{ width: 38px; height: 38px; }}
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
    <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:20px;flex-wrap:wrap;">
        <div class="title-wrap">
            <span class="tb">BINGO</span><span class="tp">PEAK BEHAVIOR</span>
        </div>
        <div class="brand">
            <div class="r">R<i>.</i></div>
            <div class="wm"><b>REVALUE</b><span>ACADEMY</span></div>
        </div>
    </div>
    <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-top:2px;margin-bottom:10px;">
        <div style="font-size:13px;color:#8a6a55;font-weight:600;max-width:640px;">
            Centang yang udah kelihatan minggu ini — makin banyak kena, makin mahal harga optimisme yang lagi lo bayar.
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
            icon_id = t.get("icon", "")
            icon_html = (
                f'<svg class="art" viewBox="0 0 64 64" aria-hidden="true"><use href="#{icon_id}"></use></svg>'
                if icon_id
                else ""
            )
            st.markdown(
                f'<div class="{css_class}">'
                f'<span class="txt">{t["text"]}</span>'
                f"{icon_html}"
                f'<span class="stamp">&#10003;</span>'
                f"</div>",
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
