import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

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

    all_metrics = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    selected_metrics = st.sidebar.multiselect(
        "Metrik Polutan",
        all_metrics,
        default=["PM2.5"],
    )
    if not selected_metrics:
        selected_metrics = ["PM2.5"]

    date_range = st.sidebar.date_input(
        "Rentang Tanggal", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )
    try:
        start_date, end_date = date_range
        if end_date is None:
            raise ValueError("End date is missing")
    except Exception:
        if isinstance(date_range, (tuple, list)) and len(date_range) > 0:
            start_date = date_range[0]
        else:
            start_date = date_range if hasattr(date_range, "year") else min_date
        end_date = max_date

    filtered = df[
        (df["station"].isin(selected_stations))
        & (df["datetime"].dt.date >= start_date)
        & (df["datetime"].dt.date <= end_date)
    ].copy()
    filtered_metric = filtered.copy()

    tabs = st.tabs(
        [
            "Ringkasan",
            "Pola Bulanan (Semua Stasiun)",
            "Pola Bulanan per Stasiun",
            "Perbandingan Antar Stasiun",
            "Heatmap Metrik Terpilih",
            "Analisis Lanjutan",
        ]
    )

    with tabs[0]:
        st.subheader("Ringkasan")
        if len(selected_metrics) == 1:
            metric = selected_metrics[0]
            col1, col2, col3 = st.columns(3)
            col1.metric("Rata-rata", f"{filtered_metric[metric].mean():.2f}")
            col2.metric("Maksimum", f"{filtered_metric[metric].max():.2f}")
            col3.metric("Jumlah Jam", f"{filtered_metric[metric].dropna().shape[0]:,}")
        else:
            summary_df = (
                filtered_metric[selected_metrics]
                .agg(["mean", "max", "count"])
                .transpose()
                .rename(columns={"mean": "Rata-rata", "max": "Maksimum", "count": "Jumlah Jam"})
            )
            st.dataframe(summary_df.style.format({"Rata-rata": "{:.2f}", "Maksimum": "{:.2f}"}))

    with tabs[1]:
        st.subheader("Pola Bulanan (Semua Stasiun)")
        monthly_all = (
            filtered_metric.groupby("month")[selected_metrics]
            .mean()
            .reset_index()
            .melt(id_vars="month", var_name="metric", value_name="value")
            .dropna(subset=["value"])
        )

        fig0, ax0 = plt.subplots(figsize=(8, 4))
        sns.lineplot(
            data=monthly_all,
            x="month",
            y="value",
            hue="metric",
            marker="o",
            ax=ax0,
        )
        ax0.set_title("Pola Bulanan Rata-rata (Gabungan Stasiun)")
        ax0.set_xlabel("Bulan")
        ax0.set_ylabel("Nilai")
        ax0.set_xticks(range(1, 13))
        ax0.legend(title="Metrik", bbox_to_anchor=(1.02, 1), loc="upper left")
        st.pyplot(fig0)

    with tabs[2]:
        st.subheader("Pola Bulanan per Stasiun")
        monthly = (
            filtered_metric
            .groupby(["station", "year", "month"])[selected_metrics]
            .mean()
            .reset_index()
        )
        monthly["date"] = pd.to_datetime(
            monthly[["year", "month"]].assign(day=1)
        )
        monthly = monthly.melt(
            id_vars=["station", "year", "month", "date"],
            var_name="metric",
            value_name="value",
        ).dropna(subset=["value"])

        fig1, ax1 = plt.subplots(figsize=(10, 4))
        if len(selected_metrics) == 1:
            sns.lineplot(data=monthly, x="date", y="value", hue="station", ax=ax1)
        else:
            sns.lineplot(data=monthly, x="date", y="value", hue="metric", style="station", ax=ax1)
        ax1.set_title("Rata-rata Bulanan per Stasiun")
        ax1.set_xlabel("Bulan")
        ax1.set_ylabel("Nilai")
        ax1.legend(title="Legenda", bbox_to_anchor=(1.02, 1), loc="upper left")
        st.pyplot(fig1)

    with tabs[3]:
        st.subheader("Perbandingan Antar Stasiun")
        avg_by_station = (
            filtered_metric.groupby("station")[selected_metrics]
            .mean()
            .reset_index()
        )
        avg_long = avg_by_station.melt(
            id_vars="station",
            var_name="metric",
            value_name="value",
        ).dropna(subset=["value"])
        avg_long = avg_long.sort_values("value", ascending=False)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        if len(selected_metrics) == 1:
            sns.barplot(data=avg_long, x="station", y="value", ax=ax2, color="#2a9d8f")
        else:
            sns.barplot(data=avg_long, x="station", y="value", hue="metric", ax=ax2)
            ax2.legend(title="Metrik", bbox_to_anchor=(1.02, 1), loc="upper left")
        ax2.set_title("Rata-rata per Stasiun")
        ax2.set_xlabel("Stasiun")
        ax2.set_ylabel("Nilai")
        ax2.tick_params(axis="x", rotation=45)
        st.pyplot(fig2)

    with tabs[4]:
        st.subheader("Heatmap Metrik Terpilih per Stasiun")
        mean_metrics = (
            filtered.dropna(subset=selected_metrics)
            .groupby("station")[selected_metrics]
            .mean()
        )
        fig4 = px.imshow(
            mean_metrics,
            color_continuous_scale="YlGnBu",
            labels={"x": "Metrik", "y": "Stasiun", "color": "Rata-rata"},
            aspect="auto",
        )
        fig4.update_layout(title="Rata-rata Metrik Terpilih per Stasiun")
        st.plotly_chart(fig4, use_container_width=True)

    with tabs[5]:
        st.subheader("Analisis Lanjutan")
        st.caption(
            "PM2.5 memiliki analisis khusus berupa distribusi kategori per musim. "
            "Metrik lain ditampilkan sebagai boxplot per stasiun."
        )
        if "PM2.5" in selected_metrics:
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

        box_data = (
            filtered_metric.melt(
                id_vars=["station"],
                value_vars=selected_metrics,
                var_name="metric",
                value_name="value",
            ).dropna(subset=["value"])
        )
        if not box_data.empty:
            fig3, ax3 = plt.subplots(figsize=(8, 4))
            if len(selected_metrics) == 1:
                sns.boxplot(data=box_data, x="station", y="value", ax=ax3)
                ax3.set_title(f"Distribusi {selected_metrics[0]} per Stasiun")
            else:
                sns.boxplot(data=box_data, x="station", y="value", hue="metric", ax=ax3)
                ax3.set_title("Distribusi Metrik Terpilih per Stasiun")
                ax3.legend(title="Metrik", bbox_to_anchor=(1.02, 1), loc="upper left")
            ax3.set_xlabel("Stasiun")
            ax3.set_ylabel("Nilai")
            ax3.tick_params(axis="x", rotation=45)
            st.pyplot(fig3)


if __name__ == "__main__":
    sns.set_theme(style="whitegrid")
    main()
