import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Stellar Evolution Visualizer",
    page_icon="🌌",
    layout="wide"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    body {
        color: #fff;
        background-color: #111;
    }
    .stApp {
        background-color: #111;
    }
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #636EFA;
        text-align: center;
        margin-bottom: 30px;
    }
    .subtitle {
        font-size: 20px;
        color: #A0A0A0;
        text-align: center;
        margin-bottom: 20px;
    }
    .status-panel {
        background-color: rgba(30, 30, 30, 0.8);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<p class="main-title">🌌 Stellar Evolution: Visual Simulation</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Interactive visualization of molecular cloud collapse and force balance</p>', unsafe_allow_html=True)

# --- Simulation Parameters & Sidebar ---
st.sidebar.header("🔧 Simulation Controls")

# Parameter Sliders
n_gas = st.sidebar.slider("Number of Gas Particles (N)", 500, 2000, 1000, 100)
n_dust = st.sidebar.slider("Number of Dust Particles (N)", 100, 500, 200, 50)
collapse_speed = st.sidebar.slider("Collapse Speed (Relative)", 0.1, 2.0, 1.0, 0.1)
duration_sim = st.sidebar.slider("Simulation Seconds", 20, 100, 50, 10)

start_sim = st.sidebar.button("▶️ Start Simulation")

# --- Initialize Simulation Data ---
num_steps = 100
t = np.linspace(0, 1, num_steps)

# Helper function to generate cloud coordinates
def generate_cloud(num_p, base_radius=1.0, dispersion=0.2):
    radii = base_radius + np.random.normal(0, dispersion, num_p)
    phi = np.random.uniform(0, 2 * np.pi, num_p)
    theta = np.arccos(np.random.uniform(-1, 1, num_p))
    
    x = radii * np.sin(theta) * np.cos(phi)
    y = radii * np.sin(theta) * np.sin(phi)
    z = radii * np.cos(theta)
    return x, y, z

# Initial Cloud Data (Gas and Dust)
x_gas_0, y_gas_0, z_gas_0 = generate_cloud(n_gas, base_radius=1.0, dispersion=0.3)
x_dust_0, y_dust_0, z_dust_0 = generate_cloud(n_dust, base_radius=1.0, dispersion=0.1)

# Function to calculate collapse based on time 't' and speed
def get_positions(t_val, x_0, y_0, z_0, speed):
    collapse_factor = np.exp(-t_val * 4 * speed) # Exponential decay
    x = x_0 * collapse_factor
    y = y_0 * collapse_factor
    z = z_0 * collapse_factor
    return x, y, z

# --- Plotly Visualization (Figure Factory) ---
def create_simulation_plot(step, status):
    # Get current positions
    x_g, y_g, z_g = get_positions(t[step], x_gas_0, y_gas_0, z_gas_0, collapse_speed)
    x_d, y_d, z_d = get_positions(t[step], x_dust_0, y_dust_0, z_dust_0, collapse_speed)
    
    # Trace for Gas (Filaments/Streams)
    gas_trace = go.Scatter3d(
        x=x_g, y=y_g, z=z_g,
        mode='markers',
        name='Gas (H, He)',
        marker=dict(
            size=2.5,
            color=t[step],  # Color by simulation time
            colorscale='Turbo', # Vibrant filament colors
            opacity=0.4
        )
    )

    # Trace for Dust (Solid Particles)
    dust_trace = go.Scatter3d(
        x=x_d, y=y_d, z=z_d,
        mode='markers',
        name='Dust Particles',
        marker=dict(
            size=4,
            color='#b5651d', # Brown color
            opacity=0.7,
            symbol='diamond'
        )
    )

    # Core/Proto-star (Central point)
    core_trace = go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        name='Proto-Star Core',
        marker=dict(
            size=15,
            color='#FFD700', # Gold core
            opacity=1.0,
            symbol='circle'
        )
    )

    fig = go.Figure(data=[gas_trace, dust_trace, core_trace])

    # Layout Configuration
    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=4, range=[-1.2, 1.2], showbackground=False),
            yaxis=dict(nticks=4, range=[-1.2, 1.2], showbackground=False),
            zaxis=dict(nticks=4, range=[-1.2, 1.2], showbackground=False),
            camera_eye=dict(x=1.5, y=1.5, z=1.5),
            aspectmode='cube'
        ),
        title=f"MOLECULAR CLOUD COLLAPSE INITIATED<br><span style='font-size:14px; color:#A0A0A0'>{status}</span>",
        template="plotly_dark",
        margin=dict(r=0, l=0, b=0, t=60),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    return fig

# --- Main Application Logic ---
plot_area = st.empty()  # Container for the chart

# Side panels for status/metrics
st.sidebar.markdown("---")
with st.sidebar.container():
    st.markdown("### 📊 Live Simulation Metrics")
    metric_gas = st.empty()
    metric_dust = st.empty()
    metric_balance = st.empty()

# --- RUN SIMULATION LOOP ---
if start_sim:
    for i in range(num_steps):
        # Determine status and metrics
        t_current = t[i]
        sim_time_sec = (i / num_steps) * duration_sim
        
        # Calculate simulation time string
        sim_years_scaled = int(sim_time_sec * 500)
        time_status = f"SIMULATION TIME: {sim_years_scaled:,} YEARS"

        # Dynamically change status text based on collapse
        if t_current < 0.3:
            stage_status = "STABLE CLOUD DISSIPATION"
        elif t_current < 0.7:
            stage_status = "RAPID ACCRETION PHASE"
        else:
            stage_status = "PROTO-STAR CORE FORMATION"
        
        final_status = f"{stage_status} | {time_status}"

        # Get simulation figure
        fig = create_simulation_plot(i, final_status)
        plot_area.plotly_chart(fig, use_container_width=True)

        # Update metrics panel
        gas_remaining = n_gas - (i * (n_gas // num_steps))
        dust_collected = (i * (n_dust // num_steps))
        
        # Simulated Force Balance
        gravity_val = 5 + (t_current * collapse_speed * 10)
        pressure_val = 2 + (t_current * 5)
        
        balance_text = f"G ({gravity_val:.1f}) > P ({pressure_val:.1f})"
        
        with st.sidebar.container():
            metric_gas.metric(label="Gas Remaining (H, He)", value=f"{gas_remaining}", delta=f"-{n_gas // num_steps}")
            metric_dust.metric(label="Dust Collected", value=f"{dust_collected}", delta=f"+{n_dust // num_steps}")
            metric_balance.metric(label="Simulated Force Balance (G vs P)", value=balance_text)

        # Control animation speed
        time.sleep(duration_sim / num_steps)
    
    st.success("Simulation Complete: Proto-Star Core stabilized.")

else:
    # Initial state
    st.info("👈 Set parameters and press 'Start Simulation' in the sidebar to visualize.")
    fig = create_simulation_plot(0, "SIMULATION IDLE | 0 YEARS")
    plot_area.plotly_chart(fig, use_container_width=True)
    
    # Initialize initial metrics
    with st.sidebar.container():
        metric_gas.metric(label="Gas Remaining (H, He)", value=f"{n_gas}")
        metric_dust.metric(label="Dust Collected", value=f"0")
        metric_balance.metric(label="Simulated Force Balance (G vs P)", value="Idle")

# --- Footer Info ---
st.markdown("---")
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Understanding the Visualization
        1.  **Gas (Turbo Filament):** Represents the primary raw materials (Hydrogen, Helium). Brighter points indicate higher temperatures. They form large, swirling structures (filaments).
        2.  **Dust Particles (Brown Diamonds):** Solid elements and molecules that serve as accretion points, helping build up the core.
        3.  **Proto-Star Core (Gold Sphere):** The central collection point where density and temperature are rapidly increasing.
        4.  **Collapse Flow:** As time progresses (or 't' value on sliders increases), particles are visibly drawn toward the center, forming streams (accretion flows).
        """)
    with col2:
        st.markdown("""
        ### Simulation Mechanics
        * **N**: The total number of points representing gas or dust.
        * **Collapse Speed**: A multiplier affecting how rapidly particles are pulled inward (exponential decay model).
        * **Force Balance**: Gravity (inward pull) must overcome Pressure (outward push) for collapse to sustain. The metric panel shows this simulated dynamic.
        """)
