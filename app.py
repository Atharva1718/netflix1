from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Netflix Data Analysis",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="collapsed",
)

RED = "#E50914"
BLACK = "#090909"
WHITE = "#F5F5F1"
MUTED = "#A7A7A7"
PALETTE = [RED, "#B20710", "#F5F5F1", "#777777", "#6B0008", "#D94B52", "#CCCCCC", "#8E1B22"]

st.markdown(
    f"""
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: {BLACK};
        color: {WHITE};
      }}
      [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(180deg, #171111 0, {BLACK} 300px);
      }}
      [data-testid="stHeader"] {{ background: transparent; }}
      [data-testid="stToolbar"] {{ right: 1rem; }}
      .block-container {{ max-width: 1360px; padding-top: 2.2rem; }}
      h1, h2, h3, p, label {{ color: {WHITE} !important; }}
      .brand {{
        color: {RED}; font-size: 14px; font-weight: 800;
        letter-spacing: 2px; border-left: 4px solid {RED};
        padding-left: 10px; margin-bottom: 15px;
      }}
      .subhead {{ color: {MUTED} !important; margin-top: -10px; }}
      [data-testid="stFileUploader"] {{
        border: 1px solid #343434; border-radius: 6px;
        background: rgba(255,255,255,.025); padding: 12px;
      }}
      [data-testid="stFileUploaderDropzone"] {{
        background: #111; border: 1px dashed #555;
      }}
      [data-testid="stFileUploaderDropzone"] * {{ color: {WHITE} !important; }}
      [data-testid="stAlert"] {{ background: #171717; }}
      hr {{ border-color: #333; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def find_local_csv() -> Path | None:
    candidates = (
        Path(__file__).resolve().parent / "netflix.csv",
        Path.cwd() / "netflix.csv",
        Path.home() / "netflix.csv",
    )
    for candidate in dict.fromkeys(candidates):
        if candidate.is_file():
            return candidate
    return None


def load_data(uploaded_file: object) -> tuple[pd.DataFrame | None, str]:
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file), "Uploaded CSV"

    local_csv = find_local_csv()
    if local_csv is not None:
        return pd.read_csv(local_csv), local_csv.name
    return None, ""


def chart_style(axis: plt.Axes, title: str) -> None:
    axis.set_title(title, loc="left", color=WHITE, fontsize=15, fontweight="bold", pad=18)
    axis.set_facecolor(BLACK)
    axis.tick_params(colors=MUTED, labelsize=10)
    for spine in axis.spines.values():
        spine.set_visible(False)
    axis.grid(axis="y", color="#333333", linewidth=0.7)
    axis.set_axisbelow(True)


def make_bar_chart(values: pd.Series, title: str, y_label: str) -> plt.Figure:
    figure, axis = plt.subplots(figsize=(7, 4.1), facecolor=BLACK)
    chart_style(axis, title)
    bars = axis.bar(values.index.astype(str), values.values, color=RED, width=0.58)
    axis.set_ylabel(y_label, color=MUTED, labelpad=10)
    axis.grid(axis="x", visible=False)
    axis.margins(y=0.18)
    for bar, value in zip(bars, values.values):
        axis.annotate(
            f"{value:,.0f}",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            color=WHITE,
            fontsize=9,
        )
    figure.tight_layout()
    return figure


def make_pie_chart(values: pd.Series, title: str) -> plt.Figure:
    figure, axis = plt.subplots(figsize=(7, 4.1), facecolor=BLACK)
    axis.set_facecolor(BLACK)
    axis.set_title(title, loc="left", color=WHITE, fontsize=15, fontweight="bold", pad=18)
    wedges, _, percentage_labels = axis.pie(
        values.values,
        colors=PALETTE[: len(values)],
        startangle=90,
        counterclock=False,
        autopct=lambda percent: f"{percent:.0f}%" if percent >= 5 else "",
        pctdistance=0.7,
        radius=0.88,
        wedgeprops={"edgecolor": BLACK, "linewidth": 2},
        textprops={"color": WHITE, "fontsize": 9},
    )
    for label in percentage_labels:
        label.set_fontweight("bold")
    legend_labels = [f"{name}  ·  {value:,.0f}" for name, value in values.items()]
    legend = axis.legend(
        wedges,
        legend_labels,
        loc="center left",
        bbox_to_anchor=(0.92, 0.5),
        frameon=False,
        labelcolor=WHITE,
        fontsize=9,
        handlelength=0.9,
        borderaxespad=0,
    )
    for text in legend.get_texts():
        text.set_color(WHITE)
    axis.set_aspect("equal")
    figure.tight_layout()
    return figure


st.markdown('<div class="brand">NETFLIX  /  DATA ANALYSIS</div>', unsafe_allow_html=True)
st.title("Audience & revenue")
st.markdown(
    '<p class="subhead">Explore the four views defined in the original analysis.</p>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("Use a Netflix dataset", type=["csv"])
data, data_source = load_data(uploaded_file)

if data is None:
    st.info("Add `netflix.csv` beside this app or in your home folder, or upload it here.")
    st.stop()

required_columns = {"Region", "Monthly_Revenue", "Subscription_Plan", "Rating", "Category"}
missing_columns = sorted(required_columns.difference(data.columns))
if missing_columns:
    st.error(f"This CSV is missing required columns: {', '.join(missing_columns)}")
    st.stop()

st.caption(f"{len(data):,} records  ·  {data_source}")
data["Monthly_Revenue"] = pd.to_numeric(data["Monthly_Revenue"], errors="coerce")
data["Rating"] = pd.to_numeric(data["Rating"], errors="coerce")

left, right = st.columns(2, gap="large")
with left:
    revenue_by_region = data.groupby("Region")["Monthly_Revenue"].sum().sort_values(ascending=False)
    st.pyplot(make_bar_chart(revenue_by_region, "Region-wise revenue", "Monthly revenue"), clear_figure=True)
with right:
    rating_by_plan = data.groupby("Subscription_Plan")["Rating"].sum().sort_values(ascending=False)
    st.pyplot(make_pie_chart(rating_by_plan, "Subscription plan-wise rating"), clear_figure=True)

left, right = st.columns(2, gap="large")
with left:
    rating_counts = data["Rating"].value_counts().sort_index()
    st.pyplot(make_bar_chart(rating_counts, "Rating distribution", "Number of ratings"), clear_figure=True)
with right:
    revenue_by_category = data.groupby("Category")["Monthly_Revenue"].sum().sort_values(ascending=False)
    st.pyplot(make_pie_chart(revenue_by_category, "Category-wise revenue"), clear_figure=True)
