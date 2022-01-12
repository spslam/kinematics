import numpy as np
from kinematics import Joint
from load_robot_from_file import load_robot
import plotly.graph_objects as go
import plotly.express as px

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)


robot = load_robot()
joint_ct = len(robot)

div_config = []
inputs = []

for i in range(joint_ct):
    div_config.append(html.P(f"Joint {i} Theta:"))
    div_config.append(dcc.Slider(id=f'range-slider{i}',
                                    min=0, max=360, step=1,
                                    # marks={0: '0', 2.5: '2.5'},
                                    value=np.rad2deg(robot[i].theta),
                                    tooltip={'always_visible': True},
                                    updatemode='drag'))
    div_config.append(dcc.Input(id=f'd{i}', value=round(robot[i].d, 2)))

    # make a list of inputs for the slider callback decorator
    inputs.append(Input(f'range-slider{i}', 'value'))


app.layout = html.Div([html.Div(dcc.Graph(id="scatter-plot"), style={'width': '69%', 'display': 'inline-block'}),
                       html.Div(div_config, style={'width': '29%', 'display': 'inline-block'})])


@app.callback(Output("scatter-plot", "figure"), inputs)
def update_robot(*sliders):
    chain_x = []
    chain_y = []
    chain_z = []

    # size of the dashed indicator at each joint axis
    indicator_pt1 = [0, 0, .25]
    indicator_pt2 = [0, 0, -.25]

    # list to collect the pairs of joint axis indicator points
    j_pts = []

    for i, s in enumerate(sliders):
        robot[i].theta = np.deg2rad(s)

    t = None
    for n in robot:
        if t is None:
            t = n.matrix()
        else:
            t = t @ n.matrix()

        chain_x.append(t[0, 3])
        chain_y.append(t[1, 3])
        chain_z.append(t[2, 3])

        # rotate the vector to indicate the rotational axis of the joint
        # select the R sub-matrix, multiply by std length axis vectors and add translation to joint
        j_pts1 = t[0:3, 0:3] @ np.array(indicator_pt1) + t[0:3, 3].T
        j_pts2 = t[0:3, 0:3] @ np.array(indicator_pt2) + t[0:3, 3].T
        j_pts.append(np.array([j_pts1, j_pts2]))

    print(t)

    # uirevision preserves user input state of the plot (i.e. doesn't re-frame on data update)
    # cube aspectmode keeps equal scale axes
    layout = go.Layout(scene={'aspectmode': 'cube'}, uirevision='dataset')

    # fig = px.line_3d(x=x, y=y, z=z, markers=True, range_x=[0, 1], range_y=[0,1], range_z=[0,1])
    fig = go.Figure(data=go.Scatter3d(x=chain_x, y=chain_y, z=chain_z,
                                      showlegend=False, line={'width': 10}), layout=layout)

    for j_pt in j_pts:
        fig.add_trace(go.Scatter3d(x=j_pt[:, 0], y=j_pt[:, 1], z=j_pt[:, 2],
                                   showlegend=False, mode='lines', line={'dash': 'dash'}))

    fig.update_scenes(aspectmode='cube')

    return fig


app.run_server(debug=True)

