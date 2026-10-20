import pickle

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Smart Home Energy AI",
    page_icon="🏡",
    layout="wide",
)

# ------------------------------------------------------------------ model
@st.cache_resource
def load_model():
    with open("energy_model.pkl", "rb") as file:
        return pickle.load(file)


model = load_model()

# ------------------------------------------------------------------ theme
if "theme" not in st.session_state:
    st.session_state.theme = "dark"


def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"


THEMES = {
    "dark": {
        "bg": "#0e1a1f", "panel": "#16262d", "line": "#2a4249",
        "text": "#eaf2f1", "sub": "#cfe0df", "muted": "#9fb6b8",
        "heading": "#ffffff", "accent_text": "#f5b942", "bar": "#3fb8a5",
        "track": "#0e1a1f", "chip": "#1c3139", "chip_hover": "#2a4249",
        "input_bg": "#0e1a1f",
    },
    "light": {
        "bg": "#f3f7f7", "panel": "#ffffff", "line": "#cbd9da",
        "text": "#12262b", "sub": "#26414a", "muted": "#4a6468",
        "heading": "#0b1c20", "accent_text": "#b45309", "bar": "#13917f",
        "track": "#e4eded", "chip": "#e9f1f1", "chip_hover": "#d3e2e2",
        "input_bg": "#ffffff",
    },
}
t = THEMES[st.session_state.theme]
root_vars = ":root{" + "".join(f"--{k.replace('_', '-')}:{v};" for k, v in t.items()) + "}"

st.markdown(f"<style>{root_vars}</style>", unsafe_allow_html=True)

# ------------------------------------------------------------------ style
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;800&display=swap');

html, body, .stApp, [class*="css"] { font-family: 'Manrope', sans-serif; }
.stApp, [data-testid="stAppViewContainer"] { background: var(--bg); color: var(--text); }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { max-width: 1180px; padding-top: 1.5rem; padding-bottom: 3rem; }

/* ---- text ---- */
h1, h2, h3, h4, h5, p, span, li { color: var(--text); }
h4 { color: var(--heading); font-weight: 800; }
label, [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p {
    color: var(--sub) !important; font-weight: 600 !important; font-size: 0.88rem !important;
}
[data-testid="stCaptionContainer"], .stCaption, small { color: var(--muted) !important; }

/* ---- inputs ---- */
[data-baseweb="input"], [data-baseweb="base-input"],
[data-testid="stNumberInputContainer"], [data-testid="stNumberInput"] input {
    background: var(--input-bg) !important; color: var(--text) !important; border-radius: 10px !important;
}
[data-baseweb="input"] { border: 1px solid var(--line) !important; }
[data-baseweb="input"]:focus-within { border-color: var(--accent-text) !important; }
[data-testid="stNumberInput"] button { background: var(--chip) !important; color: var(--text) !important; }
[data-testid="stNumberInput"] button:hover { background: var(--chip-hover) !important; }
[data-testid="stNumberInput"] button svg { fill: var(--text) !important; }

/* ---- form panel ---- */
[data-testid="stForm"] {
    background: var(--panel); border: 1px solid var(--line);
    border-radius: 18px; padding: 1.4rem 1.4rem 1rem 1.4rem;
}

/* ---- predict button (same in both themes) ---- */
.stFormSubmitButton > button {
    background: #f5b942 !important; border: none !important; border-radius: 12px !important;
    width: 100%; padding: 0.8rem 1rem !important;
}
.stFormSubmitButton > button p { color: #1a1305 !important; font-weight: 800; font-size: 1rem; }
.stFormSubmitButton > button:hover { background: #ffd070 !important; }

/* ---- theme toggle ---- */
.st-key-theme_toggle { display: flex; justify-content: flex-end; }
.st-key-theme_toggle button {
    width: auto !important; height: 44px; min-height: 44px; padding: 0 18px !important;
    border-radius: 999px !important; background: var(--panel) !important;
    border: 1px solid var(--line) !important; white-space: nowrap;
}
.st-key-theme_toggle button:hover { border-color: var(--accent-text) !important; }
.st-key-theme_toggle button p { font-size: 0.88rem; font-weight: 700; color: var(--text) !important; }

/* ---- hero ---- */
.hero {
    border: 1px solid var(--line); border-left: 6px solid #f5b942; background: var(--panel);
    border-radius: 18px; padding: 26px 30px; margin-bottom: 22px;
}
.hero h1 { margin: 0 0 6px 0; font-size: 2.1rem; font-weight: 800; color: var(--heading); }
.hero p  { margin: 0; color: var(--muted); font-size: 1.02rem; max-width: 640px; }

/* ---- result card ---- */
.result { background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 26px; }
.result .label { color: var(--muted); font-size: 0.85rem; font-weight: 600; margin-bottom: 4px; }
.result .value { color: var(--accent-text); font-size: 3.4rem; font-weight: 800; line-height: 1.05; }
.result .value span { font-size: 1.3rem; color: var(--sub); margin-left: 6px; }
.result .verdict { color: var(--text); font-weight: 700; margin: 10px 0 18px 0; }
.track { position: relative; height: 12px; background: var(--track); border-radius: 99px; border: 1px solid var(--line); }
.fill  { height: 100%; background: var(--bar); border-radius: 99px; }
.avg   { position: absolute; top: -5px; width: 2px; height: 20px; background: var(--heading); }
.scale { display: flex; justify-content: space-between; color: var(--muted); font-size: 0.75rem; margin-top: 8px; }
.facts { margin-top: 18px; border-top: 1px solid var(--line); padding-top: 14px; color: var(--sub); font-size: 0.88rem; line-height: 1.7; }
.facts b { color: var(--heading); }
.empty {
    background: var(--panel); border: 1px dashed var(--line); border-radius: 18px;
    padding: 40px 26px; text-align: center;
}
.empty .t { color: var(--sub); font-weight: 700; margin: 8px 0 4px 0; }
.empty .d { color: var(--muted); margin: 0; }
.note { background: var(--chip); border-radius: 12px; padding: 12px 16px; color: var(--sub); font-size: 0.85rem; margin-top: 14px; }
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ data
# Input order must match the 25 training features
feature_names = [
    "lights", "T1", "RH_1", "T2", "RH_2",
    "T3", "RH_3", "T4", "RH_4", "T5", "RH_5",
    "T6", "RH_6", "T7", "RH_7", "T8", "RH_8",
    "T9", "RH_9", "T_out", "Press_mm_hg",
    "RH_out", "Windspeed", "Visibility", "Tdewpoint",
]

defaults = {
    "lights": 0, "T1": 21.7, "RH_1": 40.3,
    "T2": 20.3, "RH_2": 40.4, "T3": 22.3,
    "RH_3": 39.2, "T4": 20.9, "RH_4": 39.0,
    "T5": 19.6, "RH_5": 50.0, "T6": 7.4,
    "RH_6": 50.0, "T7": 20.3, "RH_7": 35.0,
    "T8": 22.0, "RH_8": 42.0, "T9": 19.5,
    "RH_9": 41.6, "T_out": 7.4, "Press_mm_hg": 755.5,
    "RH_out": 79.8, "Windspeed": 4.0,
    "Visibility": 38.3, "Tdewpoint": 3.8,
}

# (room name, temperature feature, humidity feature)
rooms = [
    ("Kitchen", "T1", "RH_1"),
    ("Living room", "T2", "RH_2"),
    ("Laundry room", "T3", "RH_3"),
    ("Office", "T4", "RH_4"),
    ("Bathroom", "T5", "RH_5"),
    ("Building exterior (north)", "T6", "RH_6"),
    ("Ironing room", "T7", "RH_7"),
    ("Teenager's room", "T8", "RH_8"),
    ("Parents' room", "T9", "RH_9"),
]

CV_RMSE = 93.69      # 10-fold cross-validation RMSE (Wh)
DATASET_MEAN = 98    # approx. mean appliance use in the training data (Wh)
SCALE_MAX = 400      # right edge of the gauge (Wh)


def temp_input(label, key):
    return st.number_input(label, min_value=-30.0, max_value=50.0,
                           value=float(defaults[key]), step=0.1, format="%.1f")


def rh_input(label, key):
    return st.number_input(label, min_value=0.0, max_value=100.0,
                           value=float(defaults[key]), step=0.1, format="%.1f")


# ------------------------------------------------------------------ header
head_l, head_r = st.columns([5, 1])
with head_l:
    st.markdown(
        """
<div class="hero">
<h1>🏡 Smart Home Energy AI</h1>
<p>Estimate how much energy your appliances will use, based on the
temperature and humidity in your home and the weather outside.</p>
</div>
""",
        unsafe_allow_html=True,
    )
with head_r:
    st.button(
        "☀️ Light mode" if st.session_state.theme == "dark" else "🌙 Dark mode",
        key="theme_toggle",
        on_click=toggle_theme,
    )

left, right = st.columns([3, 2], gap="large")

# ------------------------------------------------------------------ inputs
values = defaults.copy()

with left:
    with st.form("prediction_form"):
        st.markdown("#### 🏠 Indoor conditions")
        c1, c2 = st.columns(2)
        with c1:
            values["lights"] = st.number_input(
                "Lights energy (Wh)", min_value=0, max_value=100,
                value=int(defaults["lights"]), step=10)
            values["T1"] = temp_input("Kitchen temperature (°C)", "T1")
            values["RH_1"] = rh_input("Kitchen humidity (%)", "RH_1")
        with c2:
            values["T2"] = temp_input("Living room temperature (°C)", "T2")
            values["RH_2"] = rh_input("Living room humidity (%)", "RH_2")

        st.markdown("#### 🌤️ Weather outside")
        c3, c4, c5 = st.columns(3)
        with c3:
            values["T_out"] = temp_input("Outdoor temperature (°C)", "T_out")
        with c4:
            values["RH_out"] = rh_input("Outdoor humidity (%)", "RH_out")
        with c5:
            values["Windspeed"] = st.number_input(
                "Wind speed (m/s)", min_value=0.0, max_value=30.0,
                value=float(defaults["Windspeed"]), step=0.5, format="%.1f")

        submitted = st.form_submit_button("⚡ Predict energy use")

# ------------------------------------------------------------------ result
with right:
    if not submitted:
        st.markdown(
            """
<div class="empty">
<div style="font-size:2.4rem">⚡</div>
<p class="t">No prediction yet</p>
<p class="d">Check the readings on the left, then press
<b>Predict energy use</b>.</p>
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        input_df = pd.DataFrame(
            [[values[name] for name in feature_names]], columns=feature_names
        )
        prediction = max(0.0, float(model.predict(input_df)[0]))

        if prediction < 70:
            verdict = "Below the typical level"
        elif prediction <= 130:
            verdict = "Around the typical level"
        else:
            verdict = "Above the typical level"

        fill = min(prediction / SCALE_MAX, 1) * 100
        avg = DATASET_MEAN / SCALE_MAX * 100
        low = max(0.0, prediction - CV_RMSE)
        high = prediction + CV_RMSE

        st.markdown(
            f"""
<div class="result">
<div class="label">Predicted appliance energy use</div>
<div class="value">{prediction:.1f}<span>Wh</span></div>
<div class="verdict">{verdict}</div>
<div class="track">
<div class="fill" style="width:{fill:.1f}%"></div>
<div class="avg" style="left:{avg:.1f}%"></div>
</div>
<div class="scale"><span>0</span><span>White line: dataset average (~{DATASET_MEAN} Wh)</span><span>{SCALE_MAX}+</span></div>
<div class="facts">
<b>Likely range:</b> {low:.0f} – {high:.0f} Wh<br>
<b>Model:</b> Ridge Regression<br>
<b>Typical error (10-fold CV RMSE):</b> ±{CV_RMSE} Wh
</div>
</div>
<div class="note">This is an estimate learned from historical data, not a live measurement of your home.</div>
""",
            unsafe_allow_html=True,
        )
