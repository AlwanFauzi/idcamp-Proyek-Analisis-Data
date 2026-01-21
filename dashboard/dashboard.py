import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Beijing Air Quality Dashboard", layout="wide")

@st.cache_data

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df


def month_to_season(month: int) -> str:
    if month in [12, 1, 2]:
        return "DJF"
    if month in [3, 4, 5]:
        return "MAM"
    if month in [6, 7, 8]:
        return "JJA"
    return "SON"


def main() -> None:
    st.title("Beijing Air Quality Dashboard")
    st.write(
        "Dashboard interaktif untuk melihat pola kualitas udara di 12 stasiun Beijing "
        "(2013-2017). Gunakan filter di sisi kiri untuk mengeksplorasi data."
    )

    df = load_data("dashboard/main_data.csv")

    min_date = df["datetime"].min().date()
    max_date = df["datetime"].max().date()

    st.sidebar.header("Filter")
    stations = sorted(df["station"].unique())
    selected_stations = st.sidebar.multiselect(
        "Stasiun", stations, default=stations
    )

    metric = st.sidebar.selectbox(
        "Metrix Polutan",
        ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"],
        index=0,
    )

    date_range = st.sidebar.date_input(
        "Rentang Tanggal", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )
    if isinstance(date_range, tuple):
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    filtered = df[
        (df["station"].isin(selected_stations))
        & (df["datetime"].dt.date >= start_date)
        & (df["datetime"].dt.date <= end_date)
    ].copy()

    filtered_metric = filtered.dropna(subset=[metric])

    st.subheader("Ringkasan")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rata-rata", f"{filtered_metric[metric].mean():.2f}")
    col2.metric("Maksimum", f"{filtered_metric[metric].max():.2f}")
    col3.metric("Jumlah Jam", f"{len(filtered_metric):,}")

    st.subheader("Pola Bulanan")
    monthly = (
        filtered_metric
        .groupby(["station", "year", "month"])[metric]
        .mean()
        .reset_index()
    )
    monthly["date"] = pd.to_datetime(
        monthly[["year", "month"]].assign(day=1)
    )

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=monthly, x="date", y=metric, hue="station", ax=ax1)
    ax1.set_title(f"Rata-rata Bulanan {metric} per Stasiun")
    ax1.set_xlabel("Bulan")
    ax1.set_ylabel(metric)
    ax1.legend(title="Stasiun", bbox_to_anchor=(1.02, 1), loc="upper left")
    st.pyplot(fig1)

    st.subheader("Perbandingan Antar Stasiun")
    avg_by_station = (
        filtered_metric.groupby("station")[metric]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(data=avg_by_station, x="station", y=metric, ax=ax2, color="#2a9d8f")
    ax2.set_title(f"Rata-rata {metric} per Stasiun")
    ax2.set_xlabel("Stasiun")
    ax2.set_ylabel(metric)
    ax2.tick_params(axis="x", rotation=45)
    st.pyplot(fig2)

    st.subheader("Analisis Lanjutan")
    if metric == "PM2.5":
        bins = [0, 35, 75, 115, 150, 250, 500]
        labels = ["Good", "Moderate", "Unhealthy(SG)", "Unhealthy", "Very Unhealthy", "Hazardous"]
        filtered_metric["pm25_level"] = pd.cut(
            filtered_metric["PM2.5"], bins=bins, labels=labels, right=False
        )
        filtered_metric["season"] = filtered_metric["month"].map(month_to_season)

        season_dist = (
            filtered_metric.dropna(subset=["pm25_level"])
            .groupby(["season", "pm25_level"])
            .size()
            .groupby(level=0)
            .apply(lambda x: x / x.sum())
            .unstack()
        )

        fig3, ax3 = plt.subplots(figsize=(8, 4))
        season_dist.plot(kind="bar", stacked=True, ax=ax3, colormap="viridis")
        ax3.set_title("Proporsi Kategori PM2.5 per Musim")
        ax3.set_xlabel("Musim")
        ax3.set_ylabel("Proporsi")
        ax3.legend(title="Kategori", bbox_to_anchor=(1.02, 1), loc="upper left")
        st.pyplot(fig3)
    else:
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=filtered_metric, x="station", y=metric, ax=ax3)
        ax3.set_title(f"Distribusi {metric} per Stasiun")
        ax3.set_xlabel("Stasiun")
        ax3.set_ylabel(metric)
        ax3.tick_params(axis="x", rotation=45)
        st.pyplot(fig3)


if __name__ == "__main__":
    sns.set_theme(style="whitegrid")
    main()
