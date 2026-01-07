import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
#                    EASY UPDATE SECTION - EDIT DATA HERE
# ============================================================================

# Mass measurements - ADD NEW ROWS every 5 days
# Red for anode and Black for cathode
# Format: {"date": "DD/MM/YYYY", "cathode": grams, "anode": grams}
MASS_304 = [
    {"date": "01/12/2025", "cathode": 182, "anode": 183},  # Initial
    {"date": "09/12/2025", "cathode": 181, "anode": 183},
    {"date": "17/12/2025", "cathode": 181, "anode": 183},
    {"date": "07/01/2026", "cathode": 180.20, "anode": 183.19},
    # Add new measurements here
]

MASS_316 = [
    {"date": "01/12/2025", "cathode": 225, "anode": 224},  # Initial
    {"date": "09/12/2025", "cathode": 224, "anode": 223},
    {"date": "17/12/2025", "cathode": 225, "anode": 222},
    {"date": "07/01/2026", "cathode": 225.32, "anode": 221.64},
    # Add new measurements here
]

# Experiment runs - ADD NEW ROWS HERE
# Format: {"date": "DD/MM/YYYY", "start": "HH:MM", "end": "HH:MM", "power_start": W, "power_end": W}
RUNS_304 = [
    {"date": "01/12/2025", "start": "11:00", "end": "16:00", "power_start": 94.88, "power_end": 65.78},
    {"date": "02/12/2025", "start": "09:00", "end": "17:00", "power_start": 103.00, "power_end": 67.40},
    {"date": "03/12/2025", "start": "12:00", "end": "20:00", "power_start": 99.22, "power_end": 66.99},
    {"date": "04/12/2025", "start": "14:18", "end": "21:35", "power_start": 109.00, "power_end": 68.24},
    {"date": "08/12/2025", "start": "17:31", "end": "20:30", "power_start": 113.90, "power_end": 68.19},
    {"date": "09/12/2025", "start": "09:21", "end": "17:01", "power_start": 110.60, "power_end": 69.77},
    {"date": "10/12/2025", "start": "09:49", "end": "18:08", "power_start": 114.70, "power_end": 70.98},
    {"date": "11/12/2025", "start": "10:27", "end": "17:02", "power_start": 113.00, "power_end": 68.82},
    {"date": "12/12/2025", "start": "11:49", "end": "20:40", "power_start": 109.80, "power_end": 66.79},
]

RUNS_316 = [
    {"date": "01/12/2025", "start": "11:00", "end": "16:00", "power_start": 99.30, "power_end": 65.12},
    {"date": "02/12/2025", "start": "09:00", "end": "17:00", "power_start": 100.50, "power_end": 66.60},
    {"date": "03/12/2025", "start": "12:00", "end": "20:00", "power_start": 98.99, "power_end": 67.69},
    {"date": "04/12/2025", "start": "14:18", "end": "21:35", "power_start": 108.10, "power_end": 71.18},
    {"date": "08/12/2025", "start": "17:31", "end": "20:30", "power_start": 116.50, "power_end": 70.72},
    {"date": "09/12/2025", "start": "09:21", "end": "17:01", "power_start": 111.60, "power_end": 71.18},
    {"date": "10/12/2025", "start": "09:49", "end": "18:08", "power_start": 113.80, "power_end": 73.28},
    {"date": "11/12/2025", "start": "10:27", "end": "17:02", "power_start": 114.00, "power_end": 72.35},
    {"date": "12/12/2025", "start": "11:49", "end": "20:40", "power_start": 108.40, "power_end": 69.57},
]

# Electrode images configuration
# before_image: The image showing the electrode before the experiment
# after_image: The image showing the electrode after degradation
# steel_type: "304" or "316" - used to reference the correct total hours
ELECTRODE_IMAGES = {
    "304_cathode": {
        "before": "304_316_new.webp",
        "after": "304_black.webp",
        "label": "304 Steel - Cathode (Black)",
        "steel_type": "304"
    },
    "304_anode": {
        "before": "304_316_new.webp",
        "after": "304_red.webp",
        "label": "304 Steel - Anode (Red)",
        "steel_type": "304"
    },
    "316_cathode": {
        "before": "304_316_new.webp",
        "after": "316_black.webp",
        "label": "316 Steel - Cathode (Black)",
        "steel_type": "316"
    },
    "316_anode": {
        "before": "304_316_new.webp",
        "after": "316_red.webp",
        "label": "316 Steel - Anode (Red)",
        "steel_type": "316"
    },
}

# ============================================================================
#                         END OF EASY UPDATE SECTION
# ============================================================================

# HydroStar brand colors
PRIMARY_GREEN = "#a7d730"
SECONDARY_GREEN = "#499823"
DARK_GREY = "#30343c"
LIGHT_GREY = "#8c919a"


def calculate_hours(start_time: str, end_time: str) -> float:
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")
    diff = (end - start).total_seconds() / 3600
    return round(diff, 2)


def calculate_energy(hours: float, power_start: float, power_end: float) -> float:
    return round(0.5 * hours * (power_start + power_end), 2)


def process_runs(runs: list) -> pd.DataFrame:
    data = []
    for run in runs:
        hours = calculate_hours(run["start"], run["end"])
        energy = calculate_energy(hours, run["power_start"], run["power_end"])
        data.append({
            "Date": run["date"],
            "Time": f"{run['start']} - {run['end']}",
            "Hours": hours,
            "Power Start (W)": run["power_start"],
            "Power End (W)": run["power_end"],
            "Energy (Wh)": energy,
        })
    return pd.DataFrame(data)


def get_mass_loss(mass_list: list) -> dict:
    initial = mass_list[0]
    current = mass_list[-1]
    return {
        "initial_cathode": initial["cathode"],
        "initial_anode": initial["anode"],
        "current_cathode": current["cathode"],
        "current_anode": current["anode"],
        "loss_cathode": round(initial["cathode"] - current["cathode"], 2),
        "loss_anode": round(initial["anode"] - current["anode"], 2),
        "loss_total": round((initial["cathode"] - current["cathode"]) + (initial["anode"] - current["anode"]), 2),
        "current_date": current["date"]
    }


def display_mass_metric(label: str, loss: float, initial: float, current: float):
    """Display mass loss metric with appropriate delta indicator."""
    # Calculate actual mass change (negative = mass was lost, positive = mass was gained)
    mass_change = round(current - initial, 2)
    
    if mass_change == 0:
        # No change
        st.metric(label, f"{loss:.2f} g", delta="No change", delta_color="off")
    else:
        # Show the mass change with correct arrow and color:
        # - Negative change (mass lost/degradation): red down arrow
        # - Positive change (mass gained): green up arrow
        # delta_color="normal" makes: down arrow = red, up arrow = green
        st.metric(label, f"{loss:.2f} g", delta=f"{mass_change:+.2f}g (was {initial}g)", delta_color="normal")


# Page config
st.set_page_config(
    page_title="HydroStar Electrode Degradation Experiment",
    page_icon="logo.png",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Hind:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Hind', sans-serif;
    }
    
    .main-header {
        background-color: #30343c;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .main-title {
        color: #a7d730;
        font-size: 2.2em;
        font-weight: 700;
        margin: 0 0 8px 0;
    }
    
    .subtitle {
        color: white;
        font-size: 1.1em;
        margin: 0;
    }
    
    .steel-header {
        color: #499823;
        font-size: 1.5em;
        font-weight: 600;
        border-bottom: 2px solid #a7d730;
        padding-bottom: 5px;
    }
    
    .electrode-label {
        color: #499823;
        font-size: 1.2em;
        font-weight: 600;
        margin-bottom: 10px;
        padding: 8px 0;
        border-bottom: 1px solid #a7d730;
    }
    
    .image-caption {
        color: #8c919a;
        font-size: 0.9em;
        text-align: center;
        font-style: italic;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header with logo
col_logo, col_title = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo.png", width=180)
    except:
        pass

with col_title:
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">Electrode Degradation Experiment</h1>
        <p class="subtitle">304 vs 316 stainless steel</p>
    </div>
    """, unsafe_allow_html=True)

# Process data
df_304 = process_runs(RUNS_304)
df_316 = process_runs(RUNS_316)

total_hours_304 = df_304["Hours"].sum()
total_hours_316 = df_316["Hours"].sum()
total_energy_304 = df_304["Energy (Wh)"].sum()
total_energy_316 = df_316["Energy (Wh)"].sum()

# Mass loss calculations
mass_304 = get_mass_loss(MASS_304)
mass_316 = get_mass_loss(MASS_316)

# Experiment Overview
st.markdown("---")
st.markdown("## Experiment overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total runs", len(RUNS_304))
with col2:
    st.metric("Total hours (304)", f"{total_hours_304:.1f} hrs")
with col3:
    st.metric("Total hours (316)", f"{total_hours_316:.1f} hrs")
with col4:
    st.metric("Experiment start", RUNS_304[0]["date"] if RUNS_304 else "N/A")

# Results for each steel type
st.markdown("---")

tab1, tab2 = st.tabs(["304 Stainless Steel", "316 Stainless Steel"])

with tab1:
    st.markdown('<p class="steel-header">304 Stainless Steel Results</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        display_mass_metric(
            "Cathode mass loss",
            mass_304['loss_cathode'],
            mass_304['initial_cathode'],
            mass_304['current_cathode']
        )
    with col2:
        display_mass_metric(
            "Anode mass loss",
            mass_304['loss_anode'],
            mass_304['initial_anode'],
            mass_304['current_anode']
        )
    with col3:
        st.metric("Total mass loss", f"{mass_304['loss_total']:.2f} g")
    with col4:
        st.metric("Total energy", f"{total_energy_304:.1f} Wh")
    
    st.markdown("#### Mass measurement history")
    df_mass_304 = pd.DataFrame(MASS_304)
    df_mass_304.columns = ["Date", "Cathode (g)", "Anode (g)"]
    st.dataframe(df_mass_304, use_container_width=True, hide_index=True)
    
    st.markdown("#### Run log")
    st.dataframe(df_304, use_container_width=True, hide_index=True)

with tab2:
    st.markdown('<p class="steel-header">316 Stainless Steel Results</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        display_mass_metric(
            "Cathode mass loss",
            mass_316['loss_cathode'],
            mass_316['initial_cathode'],
            mass_316['current_cathode']
        )
    with col2:
        display_mass_metric(
            "Anode mass loss",
            mass_316['loss_anode'],
            mass_316['initial_anode'],
            mass_316['current_anode']
        )
    with col3:
        st.metric("Total mass loss", f"{mass_316['loss_total']:.2f} g")
    with col4:
        st.metric("Total energy", f"{total_energy_316:.1f} Wh")
    
    st.markdown("#### Mass measurement history")
    df_mass_316 = pd.DataFrame(MASS_316)
    df_mass_316.columns = ["Date", "Cathode (g)", "Anode (g)"]
    st.dataframe(df_mass_316, use_container_width=True, hide_index=True)
    
    st.markdown("#### Run log")
    st.dataframe(df_316, use_container_width=True, hide_index=True)

# Comparison summary
st.markdown("---")
st.markdown("## Comparison summary")

comparison_data = {
    "Metric": ["Total hours", "Total energy (Wh)", "Cathode mass loss (g)", "Anode mass loss (g)", "Total mass loss (g)"],
    "304 Steel": [
        f"{total_hours_304:.1f}",
        f"{total_energy_304:.1f}",
        f"{mass_304['loss_cathode']:.2f}",
        f"{mass_304['loss_anode']:.2f}",
        f"{mass_304['loss_total']:.2f}"
    ],
    "316 Steel": [
        f"{total_hours_316:.1f}",
        f"{total_energy_316:.1f}",
        f"{mass_316['loss_cathode']:.2f}",
        f"{mass_316['loss_anode']:.2f}",
        f"{mass_316['loss_total']:.2f}"
    ]
}
st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)

# ============================================================================
#                    ELECTRODE DEGRADATION IMAGES SECTION
# ============================================================================
st.markdown("---")
st.markdown("## Electrode degradation images")
st.markdown("Microscope images showing visual degradation of electrodes before and after the experiment.")

# Store total hours in a dictionary for easy lookup
total_hours = {
    "304": total_hours_304,
    "316": total_hours_316
}

# Display before/after images for each electrode
for electrode_key, electrode_info in ELECTRODE_IMAGES.items():
    st.markdown(f'<p class="electrode-label">{electrode_info["label"]}</p>', unsafe_allow_html=True)
    
    col_before, col_after = st.columns(2)
    
    # Get the total hours for this electrode's steel type
    steel_type = electrode_info["steel_type"]
    hours_for_this_electrode = total_hours[steel_type]
    
    with col_before:
        try:
            st.image(electrode_info["before"], use_container_width=True)
            st.markdown('<p class="image-caption">Before experiment (new condition)</p>', unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not load before image: {electrode_info['before']}")
    
    with col_after:
        try:
            st.image(electrode_info["after"], use_container_width=True)
            st.markdown(f'<p class="image-caption">After {hours_for_this_electrode:.1f} hours of operation</p>', unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not load after image: {electrode_info['after']}")
    
    st.markdown("")  # Add spacing between rows

# ============================================================================
#                         END OF IMAGES SECTION
# ============================================================================

# Visualizations at the bottom
st.markdown("---")
st.markdown("## Visualizations")

col_chart1, col_chart2 = st.columns(2)

# Chart 1: Cumulative Energy Over Time
with col_chart1:
    df_304["Cumulative Energy (Wh)"] = df_304["Energy (Wh)"].cumsum()
    df_316["Cumulative Energy (Wh)"] = df_316["Energy (Wh)"].cumsum()
    
    fig_energy = go.Figure()
    fig_energy.add_trace(go.Scatter(
        x=df_304["Date"],
        y=df_304["Cumulative Energy (Wh)"],
        mode="lines+markers",
        name="304 Steel",
        line=dict(color=PRIMARY_GREEN, width=3),
        marker=dict(size=8)
    ))
    fig_energy.add_trace(go.Scatter(
        x=df_316["Date"],
        y=df_316["Cumulative Energy (Wh)"],
        mode="lines+markers",
        name="316 Steel",
        line=dict(color=SECONDARY_GREEN, width=3),
        marker=dict(size=8)
    ))
    fig_energy.update_layout(
        title="Cumulative energy over time",
        xaxis_title="Date",
        yaxis_title="Cumulative Energy (Wh)",
        plot_bgcolor="white",
        font=dict(family="Hind"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_energy, use_container_width=True)

# Chart 2: Mass Loss Comparison
with col_chart2:
    fig_mass = go.Figure()
    fig_mass.add_trace(go.Bar(
        x=["Cathode", "Anode", "Total"],
        y=[mass_304["loss_cathode"], mass_304["loss_anode"], mass_304["loss_total"]],
        name="304 Steel",
        marker_color=PRIMARY_GREEN
    ))
    fig_mass.add_trace(go.Bar(
        x=["Cathode", "Anode", "Total"],
        y=[mass_316["loss_cathode"], mass_316["loss_anode"], mass_316["loss_total"]],
        name="316 Steel",
        marker_color=SECONDARY_GREEN
    ))
    fig_mass.update_layout(
        title="Mass loss comparison (grams)",
        xaxis_title="Electrode",
        yaxis_title="Mass Loss (g)",
        barmode="group",
        plot_bgcolor="white",
        font=dict(family="Hind"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_mass, use_container_width=True)

# Chart 3: Power Readings Over Time
fig_power = go.Figure()
fig_power.add_trace(go.Scatter(
    x=df_304["Date"],
    y=df_304["Power Start (W)"],
    mode="lines+markers",
    name="304 Power Start",
    line=dict(color=PRIMARY_GREEN, width=2),
))
fig_power.add_trace(go.Scatter(
    x=df_304["Date"],
    y=df_304["Power End (W)"],
    mode="lines+markers",
    name="304 Power End",
    line=dict(color=PRIMARY_GREEN, width=2, dash="dash"),
))
fig_power.add_trace(go.Scatter(
    x=df_316["Date"],
    y=df_316["Power Start (W)"],
    mode="lines+markers",
    name="316 Power Start",
    line=dict(color=SECONDARY_GREEN, width=2),
))
fig_power.add_trace(go.Scatter(
    x=df_316["Date"],
    y=df_316["Power End (W)"],
    mode="lines+markers",
    name="316 Power End",
    line=dict(color=SECONDARY_GREEN, width=2, dash="dash"),
))
fig_power.update_layout(
    title="Power readings over time",
    xaxis_title="Date",
    yaxis_title="Power (W)",
    plot_bgcolor="white",
    font=dict(family="Hind"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig_power, use_container_width=True)

# Chart 4: Mass Over Time (if more than one measurement)
if len(MASS_304) > 1:
    fig_mass_time = go.Figure()
    
    dates_304 = [m["date"] for m in MASS_304]
    cathode_304 = [m["cathode"] for m in MASS_304]
    anode_304 = [m["anode"] for m in MASS_304]
    
    dates_316 = [m["date"] for m in MASS_316]
    cathode_316 = [m["cathode"] for m in MASS_316]
    anode_316 = [m["anode"] for m in MASS_316]
    
    fig_mass_time.add_trace(go.Scatter(
        x=dates_304, y=cathode_304,
        mode="lines+markers",
        name="304 Cathode",
        line=dict(color=PRIMARY_GREEN, width=2),
    ))
    fig_mass_time.add_trace(go.Scatter(
        x=dates_304, y=anode_304,
        mode="lines+markers",
        name="304 Anode",
        line=dict(color=PRIMARY_GREEN, width=2, dash="dash"),
    ))
    fig_mass_time.add_trace(go.Scatter(
        x=dates_316, y=cathode_316,
        mode="lines+markers",
        name="316 Cathode",
        line=dict(color=SECONDARY_GREEN, width=2),
    ))
    fig_mass_time.add_trace(go.Scatter(
        x=dates_316, y=anode_316,
        mode="lines+markers",
        name="316 Anode",
        line=dict(color=SECONDARY_GREEN, width=2, dash="dash"),
    ))
    fig_mass_time.update_layout(
        title="Electrode mass over time",
        xaxis_title="Date",
        yaxis_title="Mass (g)",
        plot_bgcolor="white",
        font=dict(family="Hind"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_mass_time, use_container_width=True)

# Footer
st.markdown("---")
st.markdown('<p style="color: #8c919a; text-align: center;">HydroStar Europe Ltd. | Constant: 14A current, 10V cap | Energy = 1/2 x hr x (P1 + P2)</p>', unsafe_allow_html=True)
