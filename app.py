import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# Set up page configuration
st.set_page_config(
    page_title="Stellar Evolution Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme styling matching outer space
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    div.stButton > button:first-child {
        background-color: #4A90E2; color: white; border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌟 Dynamic Stellar Evolution Simulator")
st.write("Visualizing the lifecycles of stars based on initial mass.")

# Sidebar Controls
st.sidebar.header("Simulation Settings")
star_type = st.sidebar.selectbox(
    "Select Star Pathway:",
    ["Average Star Path", "Massive Star Path"]
)

speed = st.sidebar.slider("Simulation Speed", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
delay = 0.1 / speed

# Helper function to generate cloud/particle coordinates for nebulae/supernovae
def generate_particles(num_particles, spread, center=(0, 0)):
    x = np.random.normal(center[0], spread, num_particles)
    y = np.random.normal(center[1], spread, num_particles)
    return x, y

# Define stages data for both pathways
stages_data = {
    "Average Star Path": [
        {"name": "Stellar Nebula", "type": "nebula", "size": 40, "color": "rgba(180, 100, 220, 0.4)", "desc": "A vast, cold cloud of gas and dust (nebula) begins collapsing under gravity."},
        {"name": "Average Star", "type": "star", "size": 25, "color": "yellow", "desc": "Hydrogen fusion begins. The star enters equilibrium, balancing gravity and radiation pressure."},
        {"name": "Red Giant", "type": "star", "size": 75, "color": "orangered", "desc": "Core hydrogen runs out. The core contracts and heats up, causing the outer layers to expand and cool."},
        {"name": "Planetary Nebula", "type": "nebula", "size": 90, "color": "rgba(0, 200, 200, 0.5)", "desc": "Outer layers are ejected into space, forming a glowing ring or bubble of gas."},
        {"name": "White Dwarf", "type": "star", "size": 8, "color": "lightcyan", "desc": "Only the dense, hot carbon-oxygen core remains, cooling slowly over billions of years."}
    ],
    "Massive Star Path": [
        {"name": "Stellar Nebula", "type": "nebula", "size": 45, "color": "rgba(180, 100, 220, 0.4)", "desc": "A larger, denser region of the nebula collapses rapidly under immense gravity."},
        {"name": "Massive Star", "type": "star", "size": 35, "color": "deepskyblue", "desc": "Fuses hydrogen at a furious rate. Bright, hot, and blue."},
        {"name": "Red Super Giant", "type": "star", "size": 130, "color": "red", "desc": "Massive expansion as heavier elements fuse in concentric shells up to iron."},
        {"name": "Supernova Explosion", "type": "explosion", "size": 150, "color": "white", "desc": "Core collapses violently in seconds, creating a catastrophic shockwave explosion."},
        {"name": "Neutron Star / Black Hole", "type": "remnant", "size": 5, "color": "magenta", "desc": "An ultra-dense core remnant forms. Extremely massive stars become a Black Hole."}
    ]
}

# Run Simulation Button
if st.sidebar.button("▶️ Start Simulation"):
    stages = stages_data[star_type]
    
    # Create empty placeholders for real-time dynamic updates
    status_placeholder = st.empty()
    plot_placeholder = st.empty()
    desc_placeholder = st.empty()
    
    # Total animation frames per stage transition to ensure smooth morphing
    frames_per_stage = 25
    
    for i in range(len(stages) - 1):
        current_stage = stages[i]
        next_stage = stages[i+1]
        
        # Linear interpolation between stages for smooth visuals
        for frame in range(frames_per_stage):
            t = frame / frames_per_stage
            
            # Interpolate size and color
            curr_size = current_stage["size"] + (next_stage["size"] - current_stage["size"]) * t
            
            # Setup Plotly Figure Container
            fig = go.Figure()
            
            # Visual logic depending on the stage type
            if current_stage["type"] == "nebula" or next_stage["type"] == "nebula" or next_stage["type"] == "explosion":
                # Particle distribution simulations for clouds/explosions
                num_p = 300
                spread = curr_size / 40.0
                px, py = generate_particles(num_p, spread)
                
                # Dynamic particle sizing logic during explosions
                p_size = 4 if next_stage["type"] == "explosion" else 3
                
                fig.add_trace(go.Scatter(
                    x=px, y=py, mode='markers',
                    marker=dict(size=p_size, color=next_stage["color"] if t > 0.5 else current_stage["color"], opacity=0.6),
                    showlegend=False
                ))
            
            # Standard solid core star visualization
            if current_stage["type"] == "star" or next_stage["type"] == "star" or next_stage["type"] == "remnant":
                fig.add_trace(go.Scatter(
                    x=[0], y=[0], mode='markers',
                    marker=dict(
                        size=curr_size,
                        color=next_stage["color"] if t > 0.5 else current_stage["color"],
                        line=dict(width=2, color="white") if next_stage["type"] == "remnant" else None,
                        colorscale="Electric"
                    ),
                    showlegend=False
                ))
            
            # Extra aesthetic effect for Black Hole / Neutron star remnants
            if next_stage["type"] == "remnant" and t > 0.8:
                # Add accretion disk or magnetic field rings
                theta = np.linspace(0, 2*np.pi, 100)
                fig.add_trace(go.Scatter(x=np.cos(theta)*1.5, y=np.sin(theta)*1.5, mode='lines', line=dict(color='purple', width=1, dash='dash'), showlegend=False))
                fig.add_trace(go.Scatter(x=np.cos(theta)*3, y=np.sin(theta)*0.5, mode='lines', line=dict(color='cyan', width=1), showlegend=False))

            # Maintain static axes limits to capture scale variations accurately
            fig.update_layout(
                xaxis=dict(range=[-5, 5], showgrid=False, zeroline=False, visible=False),
                yaxis=dict(range=[-5, 5], showgrid=False, zeroline=False, visible=False),
                paper_bgcolor='#0e1117',
                plot_bgcolor='#0e1117',
                margin=dict(l=0, r=0, t=0, b=0),
                width=700,
                height=500
            )
            
            # Update layouts dynamically
            status_placeholder.markdown(f"### Current Stage: **{current_stage['name']}** ➡️ **{next_stage['name']}**")
            plot_placeholder.plotly_chart(fig, use_container_width=True)
            desc_placeholder.info(current_stage["desc"])
            
            time.sleep(delay)
            
    # Final Stage Stabilization
    final_stage = stages[-1]
    fig = go.Figure()
    if final_stage["type"] == "remnant" or final_stage["type"] == "star":
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=final_stage["size"], color=final_stage["color"]), showlegend=False))
    
    fig.update_layout(
        xaxis=dict(range=[-5, 5], visible=False),
        yaxis=dict(range=[-5, 5], visible=False),
        paper_bgcolor='#0e1117', plot_bgcolor='#0e1117',
        margin=dict(l=0, r=0, t=0, b=0), width=700, height=500
    )
    status_placeholder.markdown(f"### 🎉 Evolution Complete: **{final_stage['name']}**")
    plot_placeholder.plotly_chart(fig, use_container_width=True)
    desc_placeholder.success(final_stage["desc"])

else:
    # Idle display mode state before starting simulation
    st.info("👈 Select a pathway from the sidebar menu and click 'Start Simulation' to view the interactive process.")
