import plotly.graph_objects as go
import numpy as np

class SatelliteModel:
    """
    Generates a high-fidelity 3D mesh of the spacecraft.
    """
    @staticmethod
    def get_spacecraft_fig():
        fig = go.Figure()

        # --- 1. SATELLITE BUS (Gold Foil) ---
        # 1x1x2 Unit Cube
        x_bus = [-1, -1, 1, 1, -1, -1, 1, 1]
        y_bus = [-1, 1, 1, -1, -1, 1, 1, -1]
        z_bus = [-1, -1, -1, -1, 1, 1, 1, 1]
        
        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]

        fig.add_trace(go.Mesh3d(
            x=x_bus, y=y_bus, z=z_bus,
            i=i, j=j, k=k,
            color='#FFD700', 
            opacity=1.0,
            name='Bus (MLI)',
            lighting=dict(ambient=0.5, diffuse=0.8, specular=0.5),
            flatshading=True
        ))

        # --- 2. SOLAR PANELS (Blue) ---
        fig.add_trace(go.Mesh3d(x=[-1, -1, -1, -1], y=[-6, -1.2, -1.2, -6], z=[0.8, 0.8, -0.8, -0.8], color='#0044ff', name='Solar Array Port'))
        fig.add_trace(go.Mesh3d(x=[1, 1, 1, 1], y=[6, 1.2, 1.2, 6], z=[0.8, 0.8, -0.8, -0.8], color='#0044ff', name='Solar Array Stbd'))
        
        # --- 3. COMMS (Dish) ---
        theta = np.linspace(0, 2*np.pi, 20)
        x_dish, y_dish = 0.8 * np.cos(theta), 0.8 * np.sin(theta)
        z_dish = np.ones(20) * 1.5
        
        fig.add_trace(go.Scatter3d(x=x_dish, y=y_dish, z=z_dish, mode='lines', line=dict(color='silver', width=5), name='HGA Antenna'))
        fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[1, 2], mode='lines', line=dict(color='white', width=4), name='Feed Horn'))

        fig.update_layout(
            scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, b=0, t=0),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig