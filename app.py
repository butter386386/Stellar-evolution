import streamlit as st
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="Stellar Evolution Explorer",
    page_icon="✨",
    layout="wide"
)

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #FF4B4B; text-align: center; }
    .subtitle { font-size: 18px; color: #A0A0A0; text-align: center; margin-bottom: 30px; }
    .card { background-color: #1E1E1E; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<p class="main-title">✨ Stellar Evolution & Life Cycle of a Star</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">An Interactive Physics & Astrophysics Visualizer based on Chapter 13</p>', unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose a Section:", [
    "1. Introduction & Birth (Nebula)",
    "2. Forces & Hydrostatic Equilibrium",
    "3. Interactive Life Cycle Paths",
    "4. Final Fates Comparison"
])

# ==========================================
# SECTION 1: BIRTH & NEBULA
# ==========================================
if app_mode == "1. Introduction & Birth (Nebula)":
    st.header("1. How Stars Are Born: From Dust to Proto-Stars")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        * **The Birthplace:** All stars are formed from massive clouds of gas and dust floating in galaxies, known as **nebulae** or **molecular clouds**[span_2](start_span)[span_2](end_span).
        * **Gravitational Collapse:** Under mutual gravitational attraction, these gas clouds contract. As they contract, their **density and temperature increase** due to the rise in the kinetic energy of particles ($\text{Kinetic Energy} \propto \text{Temperature}$)[span_3](start_span)[span_3](end_span).
        * **Proto-Star Formation:** After millions of years, these contracting regions evolve into dense cores called **proto-stars**, setting the stage for nuclear reactions[span_4](start_span)[span_4](end_span).
        """)
    with col2:
        st.info("💡 **Key Concept:** Kinetic Molecular Theory (KMT) explains that as the gas cloud compresses, particle collisions increase rapidly, causing a sharp rise in temperature and internal thermal pressure.")

    st.subheader("Visualizing Cloud Collapse")
    collapse_step = st.slider("Select Stage of Cloud Evolution:", 1, 3, 1, 
                              format="Stage %d")
    
    stages = {
        1: ("Diffuse Nebula / Molecular Cloud", "Spread out dust and gas particles with low temperature and low self-gravity."),
        2: ("Contracting Proto-Star", "Gravity pulls gas inward, increasing density, pressure, and core temperature."),
        3: ("Stable Star (Ignition)", "Core temperature reaches millions of degrees, igniting nuclear fusion and establishing balance.")
    }
    
    title, desc = stages[collapse_step]
    st.success(f"**Current Phase ({title}):** {desc}")

# ==========================================
# SECTION 2: FORCES & EQUILIBRIUM
# ==========================================
elif app_mode == "2. Forces & Hydrostatic Equilibrium":
    st.header("2. The Tug-of-War: Gravity vs. Internal Pressure")
    
    st.markdown("""
    A stable star is formed when the inward gravitational force is **exactly balanced** by the outward thermal pressure created by nuclear fusion[span_5](start_span)[span_5](end_span). This condition is described mathematically by the **hydrostatic equation**:
    """)
    
    # Displaying equation nicely using standard markdown
    st.markdown("$$\\frac{dP}{dr} = -\\frac{G M_r \\rho_r}{r^2}$$")
    st.markdown("""
    * Where **$P$** is pressure, **$r$** is distance from the center, **$G$** is the universal gravitational constant, **$M_r$** is enclosed mass, and **$\\rho_r$** is density[span_6](start_span)[span_6](end_span).
    """)

    st.subheader("Interactive Balance Simulator")
    mass_input = st.slider("Select Star Mass (Solar Masses, $M_\\odot$)", 0.1, 25.0, 1.0)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Inward Force (Gravity)", value=f"{mass_input * 1.5:.1f}x")
    with col2:
        st.metric(label="Outward Force (Pressure)", value=f"{mass_input * 1.5:.1f}x")
        
    if mass_input < 0.5:
        st.warning("⚠️ **Low Mass (Red Dwarf):** Highly efficient fuel consumption, very slow evolutionary path, eventually transitions to a low mass white dwarf[span_7](start_span)[span_7](end_span).")
    elif 0.5 <= mass_input <= 8:
        st.info("⭐ **Intermediate Mass:** Will evolve into a Red Giant, eject a Planetary Nebula, and leave behind a White Dwarf[span_8](start_span)[span_8](end_span).")
    else:
        st.error("🔥 **Massive Star:** Experiences rapid fusion, a dramatic Supernova explosion, and collapses into a Neutron Star or Black Hole[span_9](start_span)[span_9](end_span)!")

# ==========================================
# SECTION 3: LIFE CYCLE PATHS
# ==========================================
elif app_mode == "3. Interactive Life Cycle Paths":
    st.header("3. Evolutionary Paths: Average vs. Massive Stars")
    
    path_choice = st.selectbox("Select Stellar Pathway:", [
        "Average / Intermediate Mass Star (Like our Sun)",
        "Massive Star Pathway (> 10x Solar Mass)"
    ])
    
    if "Average" in path_choice:
        st.subheader("⭐ Average Star Life Cycle Pathway")
        steps = [
            "1. Stellar Nebula (Gas & Dust Cloud)[span_10](start_span)[span_10](end_span)",
            "2. Average Star (Main Sequence - Hydrogen Fusion)[span_11](start_span)[span_11](end_span)",
            "3. Red Giant (Core contracts, outer layers expand and cool)[span_12](start_span)[span_12](end_span)",
            "4. Planetary Nebula (Outer layers expelled into space)[span_13](start_span)[span_13](end_span)",
            "5. White Dwarf (Dense carbon-oxygen core left behind)[span_14](start_span)[span_14](end_span)"
        ]
        for s in steps:
            st.markdown(f"👉 {s}")
            
    else:
        st.subheader("🔥 Massive Star Life Cycle Pathway")
        steps = [
            "1. Stellar Nebula (Massive Molecular Cloud)[span_15](start_span)[span_15](end_span)[span_16](start_span)[span_16](end_span)",
            "2. Massive Star (Burns fuel very rapidly at high temperatures)[span_17](start_span)[span_17](end_span)[span_18](start_span)[span_18](end_span)",
            "3. Red Super Giant (Expands massively with heavy element fusion up to iron)[span_19](start_span)[span_19](end_span)[span_20](start_span)[span_20](end_span)",
            "4. Supernova (Dramatic explosion triggered by iron core collapse)[span_21](start_span)[span_21](end_span)[span_22](start_span)[span_22](end_span)",
            "5. Final Remnant: Neutron Star (Ultra-dense) OR Black Hole[span_23](start_span)[span_23](end_span)[span_24](start_span)[span_24](end_span)"
        ]
        for s in steps:
            st.markdown(f"💥 {s}")

# ==========================================
# SECTION 4: FINAL FATES COMPARISON
# ==========================================
elif app_mode == "4. Final Fates Comparison":
    st.header("4. Summary of Final Remnants")
    
    # Creating a comparison chart using Plotly
    fig = go.Figure(data=[
        go.Bar(
            name='Density / Intensity', 
            x=['White Dwarf', 'Neutron Star', 'Black Hole'], 
            y=[5, 9, 12],
            marker_color=['#636EFA', '#EF553B', '#000000']
        )
    ])
    fig.update_layout(
        title="Relative Density & Gravitational Pull of Final Remnants",
        xaxis_title="Remnant Type",
        yaxis_title="Scale (Logarithmic Relative Value)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    * **White Dwarf:** Supported by electron degeneracy pressure; dense core remaining after a planetary nebula[span_25](start_span)[span_25](end_span).
    * **Neutron Star:** Among the densest objects in the universe[span_26](start_span)[span_26](end_span), formed after a supernova where protons and electrons crush into neutrons.
    * **Black Hole:** Formed when core collapse is so extreme that gravity traps even light itself[span_27](start_span)[span_27](end_span)[span_28](start_span)[span_28](end_span).
    """)

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info("Designed for Physics Students & Educators to visualize Chapter 13 concepts dynamically.")
