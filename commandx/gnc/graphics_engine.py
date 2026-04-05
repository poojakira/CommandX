import plotly.graph_objects as go
import numpy as np

class TacticalDisplay:
    """
    Renders 3D Orbital Trajectories and Sensor Cones.
    """
    @staticmethod
    def create_3d_plot(history_data):
        # Unpack History
        x = [s[0] for s in history_data]
        y = [s[1] for s in history_data]
        z = [s[2] for s in history_data]
        
        fig = go.Figure()

        # 1. The Flight Path
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color=list(range(len(x))), colorscale='Plasma', width=6),
            name='Trajectory'
        ))

        # 2. The Target (Docking Port)
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(size=12, color='#00ff00', symbol='diamond'),
            name='Target Port'
        ))

        # 3. Start Point
        fig.add_trace(go.Scatter3d(
            x=[x[0]], y=[y[0]], z=[z[0]],
            mode='markers',
            marker=dict(size=8, color='#ff0000'),
            name='Injection'
        ))

        # 4. Approach Cone (Visual Guide)
        cone_length = 200
        cone_radius = cone_length * np.tan(np.radians(15))
        
        fig.add_trace(go.Scatter3d(
            x=[0, -cone_length, -cone_length, -cone_length, -cone_length, 0],
            y=[0, cone_radius, -cone_radius, 0, 0, 0],
            z=[0, 0, 0, cone_radius, -cone_radius, 0],
            mode='lines',
            line=dict(color='rgba(0, 255, 0, 0.2)', width=2),
            name='Safety Corridor'
        ))

        # Layout styling
        fig.update_layout(
            scene=dict(
                xaxis_title='V-Bar (m)',
                yaxis_title='H-Bar (m)',
                zaxis_title='R-Bar (m)',
                xaxis=dict(backgroundcolor="rgb(20, 20, 20)", gridcolor="gray", showbackground=True),
                yaxis=dict(backgroundcolor="rgb(20, 20, 20)", gridcolor="gray", showbackground=True),
                zaxis=dict(backgroundcolor="rgb(20, 20, 20)", gridcolor="gray", showbackground=True),
            ),
            title="3D PROXIMITY OPERATIONS (PROX-OPS)",
            margin=dict(l=0, r=0, b=0, t=40),
            paper_bgcolor="#0e1117", 
            font=dict(color="white")
        )
        return fig