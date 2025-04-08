import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Initialize the Dash app
app = dash.Dash(__name__, title="CyclePerform Digital Twin", external_stylesheets=[
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
])

# Add custom CSS for better styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                color: #2d3436;
                background-color: #f8f9fa;
            }
            
            /* Custom styling for radio buttons */
            .custom-radio input[type="radio"] {
                cursor: pointer;
            }
            
            .custom-radio label {
                padding: 8px 12px;
                border-radius: 16px;
                margin-right: 8px;
                cursor: pointer;
                transition: background-color 0.2s;
            }
            
            .custom-radio label:hover {
                background-color: #edf2f7;
            }
            
            /* Custom styling for dropdown */
            .Select-control {
                border-radius: 6px !important;
                border-color: #e2e8f0 !important;
            }
            
            .Select-control:hover {
                border-color: #cbd5e0 !important;
            }
            
            /* Improve spacing */
            .dash-graph {
                padding-top: 8px;
            }
            
            /* Tooltip styling */
            .tooltip-inner {
                background-color: #ffffff;
                color: #2d3436;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 12px;
                font-size: 14px;
                max-width: 300px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define custom styles
colors = {
    'background': '#f8f9fa',           # Lighter background
    'panel': '#ffffff',                # White panels
    'accent1': '#ff6b6b',              # Red for menstrual phase
    'accent2': '#ffd166',              # Yellow for follicular phase
    'accent3': '#06d6a0',              # Green for ovulatory phase
    'accent4': '#118ab2',              # Blue for luteal phase
    'text': '#2d3436',                 # Dark text
    'title': '#1e3a8a',                # Navy blue for titles
    'border': '#e2e8f0',               # Light border color
    'button': '#4f46e5',               # Purple for buttons/selectors
    'hover': '#3730a3'                 # Darker purple for hover states
}

# Load and prepare data
def load_data():
    # In a real application, this would load your Excel file
    # For now, we'll create a simulated dataframe based on the analysis
    
    file_path = "C:\\Users\\marks\\Desktop\\Master's\\DBM190\\Project Dataset\\EFFECT OF MENSTRUAL CYCLE ON PHYSICAL ACTIVITY AMONG COLLEGE GOING RECREATIONAL ATHLETES (Responses).xlsx" 
    # Load the Excel file - in production code, replace with your file path
    df = pd.read_excel(file_path)

    
    # Map numeric responses to meaningful labels for better visualization
    # Based on our analysis, 1 generally indicates higher impact, 3 lower impact
    response_mapping = {1: "High Impact", 2: "Moderate Impact", 3: "Low Impact"}
    
    # Create shorthand question labels for better readability in visualizations
    question_labels = {
        "1- Do you face menstrual cycle irregularity ?": "Cycle Irregularity",
        "2- Have you been educated or informed about how the menstrual cycle may influence recreational athletic activities?": "Education on Cycle Effects",
        "3- Do you perceive the general effect of your menstrual cycle on your engagement in recreational physical activity ": "Effect on Engagement",
        "4- Do you recognise fluctuations in your energy levels throughout different phases of your menstrual cycle?": "Energy Fluctuations",
        "5- Do you have a specific pre warm up routine or rituals that you follow taking into account your menstrual cycle phases? ": "Adjusted Warm-Up",
        "6- Does your motivation for physical activities get influenced by your menstrual cycle?": "Motivation Impact",
        "7- Have you modified the intensity or duration of your recreational activities depending on the stage of your menstrual cycle?": "Modified Intensity/Duration",
        "8- Do you notice alterations in strength or endurance during particular phases of your menstrual cycle? ": "Strength/Endurance Changes",
        "9- Does your menstrual cycle impact the agility and coordination while participating in physical activity?": "Agility/Coordination Impact",
        "10- Does your menstrual cycle affect your capacity to partake in high intensity exercise? ": "High Intensity Capability",
        "11- Do you experience fluctuations in flexibility or joint health throughout your menstrual cycle? ": "Flexibility Changes",
        "12- Do you sense greater fatigue or muscle soreness during specific periods of the menstrual cycle while performing any physical activity?": "Fatigue/Soreness",
        "13- Does menstrual discomfort like cramps, bloating or changes in mood influence your training or competitive  performance?": "Discomfort Effect",
        "14- Do you perceive difference in the duration it takes for recovery after participating in recreational activities during your menstrual cycle? ": "Recovery Time Change",
        "15- Do you implement psychological strategies to sustain focus and a positive mindset during recreational athletic activities, particularly when navigating challenges associated with the menstrual cycle?": "Psychological Strategies"
    }
    
    # Add short labels for better visualization
    for col, short_label in question_labels.items():
        if col in df.columns:
            df[short_label] = df[col]
    
    # Calculate impact score (average of key questions)
    impact_questions = [
        "Effect on Engagement",
        "Motivation Impact",
        "Strength/Endurance Changes",
        "High Intensity Capability",
        "Fatigue/Soreness"
    ]
    
    # Make sure all these columns exist before calculating
    valid_impact_questions = [q for q in impact_questions if q in df.columns]
    if valid_impact_questions:
        df['Impact Score'] = df[valid_impact_questions].mean(axis=1)
    
    # Create a phase-specific impact feature (for a simulated person)
    # This would normally come from your digital twin's analysis
    cycle_phases = ['Menstrual', 'Follicular', 'Ovulatory', 'Luteal']
    
    # Create simulated phase-specific data for the current user
    # In a real app, this would be personalized based on the user's data
    current_user_data = {
        'Phase': cycle_phases,
        'Energy Level': [60, 80, 95, 70],
        'Strength': [65, 85, 90, 75],
        'Endurance': [55, 75, 90, 65],
        'Recovery': [50, 70, 85, 60],
        'Recommended Intensity': [60, 90, 95, 75]
    }
    
    user_df = pd.DataFrame(current_user_data)
    
    return df, user_df, question_labels

# Load the data
df, user_df, question_labels = load_data()

# Create reverse mapping from short labels to original questions
reverse_question_mapping = {v: k for k, v in question_labels.items()}

# Prepare the app layout
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    # Header
    html.Div(style={
        'backgroundColor': colors['panel'], 
        'padding': '20px', 
        'marginBottom': '20px', 
        'borderRadius': '10px', 
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
        'border': f'1px solid {colors["border"]}'
    }, children=[
        html.H1("CyclePerform Digital Twin", style={
            'color': colors['title'], 
            'textAlign': 'center',
            'fontFamily': 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial',
            'fontWeight': '700',
            'marginBottom': '8px'
        }),
        html.P("Optimize your running performance through menstrual cycle analysis", style={
            'textAlign': 'center',
            'fontSize': '16px',
            'color': '#718096',
            'marginBottom': '24px'
        }),
        
        # User profile snapshot
        html.Div(style={
            'display': 'flex', 
            'flexWrap': 'wrap',
            'justifyContent': 'space-between', 
            'marginTop': '20px',
            'gap': '16px'
        }, children=[
            html.Div(style={
                'flex': '1',
                'minWidth': '200px',
                'backgroundColor': '#f7fafc',
                'padding': '16px',
                'borderRadius': '8px'
            }, children=[
                html.H4("Current Status", style={
                    'fontSize': '16px',
                    'fontWeight': '600',
                    'color': colors['title'],
                    'marginBottom': '12px'
                }),
                html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
                    html.H2("Luteal Phase", style={
                        'marginRight': '10px', 
                        'color': colors['accent4'],
                        'fontSize': '24px',
                        'fontWeight': '700'
                    }),
                    html.Div("Day 22 of 28", style={
                        'fontSize': '16px',
                        'backgroundColor': '#e6f2f5',
                        'padding': '4px 8px',
                        'borderRadius': '16px',
                        'color': colors['accent4']
                    })
                ]),
                html.Div("Based on your cycle history and symptoms", style={
                    'fontSize': '14px', 
                    'color': '#718096',
                    'marginTop': '8px'
                })
            ]),
            
            html.Div(style={
                'flex': '1',
                'minWidth': '200px',
                'backgroundColor': '#f7fafc',
                'padding': '16px',
                'borderRadius': '8px'
            }, children=[
                html.H4("Today's Recommendation", style={
                    'fontSize': '16px',
                    'fontWeight': '600',
                    'color': colors['title'],
                    'marginBottom': '12px'
                }),
                html.P("Focus on moderate intensity workouts with emphasis on technique rather than pushing for new personal records.", 
                       style={
                           'fontSize': '14px',
                           'lineHeight': '1.5',
                           'color': colors['text']
                       })
            ]),
            
            html.Div(style={
                'flex': '1',
                'minWidth': '200px',
                'backgroundColor': '#f7fafc',
                'padding': '16px',
                'borderRadius': '8px',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'justifyContent': 'center'
            }, children=[
                html.H4("Current Readiness", style={
                    'fontSize': '16px',
                    'fontWeight': '600',
                    'color': colors['title'],
                    'marginBottom': '12px',
                    'textAlign': 'center'
                }),
                html.Div(style={
                    'fontSize': '48px', 
                    'fontWeight': 'bold', 
                    'color': '#f59e0b',
                    'textAlign': 'center',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'width': '100px',
                    'height': '100px',
                    'borderRadius': '50%',
                    'backgroundColor': '#fff',
                    'border': '8px solid #fef3c7',
                    'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
                }, children=["73%"]),
                html.Div("Moderate Energy Level", style={
                    'fontSize': '14px',
                    'marginTop': '8px',
                    'color': '#718096'
                })
            ])
        ])
    ]),
    
    # Main content area
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px'}, children=[
        # Left panel - Performance by Cycle Phase
        html.Div(style={
            'flex': '1', 
            'minWidth': '350px', 
            'backgroundColor': colors['panel'], 
            'padding': '24px', 
            'borderRadius': '10px', 
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'border': f'1px solid {colors["border"]}'
        }, children=[
            html.H3("Your Performance Across Cycle Phases", style={
                'marginBottom': '20px',
                'color': colors['title'],
                'fontWeight': '600',
                'fontSize': '18px'
            }),
            dcc.Graph(id='cycle-performance-radar'),
            html.Div(style={
                'marginTop': '16px',
                'backgroundColor': '#f7fafc',
                'padding': '12px',
                'borderRadius': '8px'
            }, children=[
                html.H4("Phase Selection", style={
                    'marginBottom': '8px',
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': colors['title']
                }),
                dcc.RadioItems(
                    id='phase-selection',
                    options=[{'label': phase, 'value': phase} for phase in user_df['Phase'].unique()],
                    value='Luteal',
                    inline=True,
                    style={
                        'display': 'flex',
                        'justifyContent': 'space-between'
                    },
                    className='custom-radio'
                )
            ])
        ]),
        
        # Right panel - Recommendations and training adjustments
        html.Div(style={
            'flex': '1', 
            'minWidth': '350px', 
            'backgroundColor': colors['panel'], 
            'padding': '24px', 
            'borderRadius': '10px', 
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'border': f'1px solid {colors["border"]}'
        }, children=[
            html.H3("Recommended Training Adjustments", style={
                'marginBottom': '20px',
                'color': colors['title'],
                'fontWeight': '600',
                'fontSize': '18px'
            }),
            dcc.Graph(id='training-recommendations'),
            html.Div(style={
                'marginTop': '16px',
                'backgroundColor': '#f7fafc',
                'padding': '16px',
                'borderRadius': '8px'
            }, children=[
                html.H4("Phase-Specific Advice", style={
                    'marginBottom': '12px',
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': colors['title']
                }),
                html.Div(id='phase-advice')
            ])
        ])
    ]),
    
    # Second row
    html.Div(style={
        'display': 'flex', 
        'flexWrap': 'wrap', 
        'gap': '20px', 
        'marginTop': '20px'
    }, children=[
        # Survey data visualization
        html.Div(style={
            'flex': '2', 
            'minWidth': '350px', 
            'backgroundColor': colors['panel'], 
            'padding': '24px', 
            'borderRadius': '10px', 
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'border': f'1px solid {colors["border"]}'
        }, children=[
            html.H3("Athletic Performance Impact Analysis", style={
                'marginBottom': '12px',
                'color': colors['title'],
                'fontWeight': '600',
                'fontSize': '18px'
            }),
            html.P("Based on survey of 361 recreational athletes", style={
                'fontSize': '14px', 
                'color': '#718096', 
                'marginBottom': '20px'
            }),
            dcc.Dropdown(
                id='impact-selection',
                options=[
                    {'label': label, 'value': label}
                    for label in [
                        'Energy Fluctuations', 
                        'Strength/Endurance Changes', 
                        'Fatigue/Soreness',
                        'High Intensity Capability',
                        'Recovery Time Change',
                        'Motivation Impact'
                    ]
                ],
                value='Energy Fluctuations',
                clearable=False,
                style={
                    'marginBottom': '16px',
                    'borderRadius': '6px',
                    'border': f'1px solid {colors["border"]}',
                }
            ),
            dcc.Graph(id='impact-distribution')
        ]),
        
        # Correlations and insights
        html.Div(style={
            'flex': '1', 
            'minWidth': '350px', 
            'backgroundColor': colors['panel'], 
            'padding': '24px', 
            'borderRadius': '10px', 
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'border': f'1px solid {colors["border"]}'
        }, children=[
            html.H3("Performance Insights", style={
                'marginBottom': '12px',
                'color': colors['title'],
                'fontWeight': '600',
                'fontSize': '18px'
            }),
            dcc.Graph(id='correlations-heatmap'),
            html.Div(style={
                'marginTop': '16px', 
                'padding': '16px', 
                'backgroundColor': '#f7fafc', 
                'borderRadius': '8px',
                'border': f'1px solid {colors["border"]}'
            }, children=[
                html.H4("Key Findings", style={
                    'marginBottom': '12px',
                    'fontSize': '16px',
                    'fontWeight': '500',
                    'color': colors['title']
                }),
                html.Ul([
                    html.Li("75% of athletes experience energy fluctuations across their cycle", 
                           style={'marginBottom': '6px', 'lineHeight': '1.5'}),
                    html.Li("Fatigue and recovery time are closely correlated",
                           style={'marginBottom': '6px', 'lineHeight': '1.5'}),
                    html.Li("Strength variations are most pronounced during the menstrual phase",
                           style={'marginBottom': '6px', 'lineHeight': '1.5'})
                ], style={'paddingLeft': '20px'})
            ])
        ])
    ]),
    
    # Bottom panel - Cycle phase calendar
    html.Div(style={
        'backgroundColor': colors['panel'], 
        'padding': '24px', 
        'marginTop': '20px', 
        'borderRadius': '10px', 
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
        'border': f'1px solid {colors["border"]}'
    }, children=[
        html.H3("Your Cycle-Based Training Planner", style={
            'marginBottom': '16px',
            'color': colors['title'],
            'fontWeight': '600',
            'fontSize': '18px'
        }),
        dcc.Graph(id='training-planner')
    ])
])

# Callback for the radar chart
@app.callback(
    Output('cycle-performance-radar', 'figure'),
    [Input('phase-selection', 'value')]
)
def update_radar_chart(selected_phase):
    # Filter data for the selected phase
    phase_data = user_df[user_df['Phase'] == selected_phase].iloc[0]
    
    # Create radar chart
    categories = ['Energy Level', 'Strength', 'Endurance', 'Recovery', 'Recommended Intensity']
    values = [phase_data[cat] for cat in categories]
    
    # Add the first value again to close the polygon
    categories = categories + [categories[0]]
    values = values + [values[0]]
    
    # Get color for selected phase
    phase_colors = {
        'Menstrual': colors['accent1'],
        'Follicular': colors['accent2'],
        'Ovulatory': colors['accent3'],
        'Luteal': colors['accent4']
    }
    
    fig = go.Figure()
    
    # Add radar chart
    # Convert hex color to rgba for transparency
    hex_color = phase_colors[selected_phase].lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    rgba_color = f'rgba({r}, {g}, {b}, 0.5)'  # 0.5 for 50% transparency
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=rgba_color,
        line=dict(color=phase_colors[selected_phase]),
        name=selected_phase
    ))
    
    # Add reference polygon for all phases
    for phase in user_df['Phase'].unique():
        if phase != selected_phase:
            phase_data = user_df[user_df['Phase'] == phase].iloc[0]
            values = [phase_data[cat] for cat in categories[:-1]]
            values = values + [values[0]]  # Close the polygon
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                line=dict(color=phase_colors[phase], width=1, dash='dot'),
                opacity=0.3,
                showlegend=False
            ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                linecolor='lightgray',
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                linecolor='lightgray',
                gridcolor='lightgray'
            ),
            bgcolor='white'
        ),
        showlegend=True,
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=colors['border'],
            borderwidth=1
        ),
        paper_bgcolor='white',
        font=dict(
            family="system-ui, -apple-system, Segoe UI, Roboto",
            color=colors['text']
        )
    )
    
    return fig

# Callback for the training recommendations
@app.callback(
    Output('training-recommendations', 'figure'),
    [Input('phase-selection', 'value')]
)
def update_training_recommendations(selected_phase):
    # Create a dictionary of recommended workouts by phase
    phase_workouts = {
        'Menstrual': [
            {'type': 'Light Jog', 'intensity': 50, 'duration': 25},
            {'type': 'Recovery Walk', 'intensity': 30, 'duration': 40},
            {'type': 'Gentle Yoga', 'intensity': 45, 'duration': 30}
        ],
        'Follicular': [
            {'type': 'Hill Sprints', 'intensity': 75, 'duration': 30},
            {'type': 'Tempo Run', 'intensity': 70, 'duration': 40},
            {'type': 'Long Run', 'intensity': 65, 'duration': 60}
        ],
        'Ovulatory': [
            {'type': 'HIIT Session', 'intensity': 90, 'duration': 35},
            {'type': 'Race Pace Run', 'intensity': 85, 'duration': 45},
            {'type': 'Speed Intervals', 'intensity': 95, 'duration': 30}
        ],
        'Luteal': [
            {'type': 'Steady State', 'intensity': 65, 'duration': 45},
            {'type': 'Fartlek Training', 'intensity': 70, 'duration': 35},
            {'type': 'Cross Training', 'intensity': 60, 'duration': 40}
        ]
    }
    
    # Filter workouts for the selected phase
    workouts = phase_workouts[selected_phase]
    
    # Get color for selected phase
    phase_colors = {
        'Menstrual': colors['accent1'],
        'Follicular': colors['accent2'],
        'Ovulatory': colors['accent3'],
        'Luteal': colors['accent4']
    }
    
    # Create figure with two subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "bar"}]])
    
    # Add intensity bars
    fig.add_trace(
        go.Bar(
            x=[w['type'] for w in workouts],
            y=[w['intensity'] for w in workouts],
            name='Intensity (%)',
            marker_color=phase_colors[selected_phase],
            opacity=0.8
        ),
        row=1, col=1
    )
    
    # Add duration bars
    fig.add_trace(
        go.Bar(
            x=[w['type'] for w in workouts],
            y=[w['duration'] for w in workouts],
            name='Duration (min)',
            marker_color=phase_colors[selected_phase],
            opacity=0.5
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        title_text="Recommended Workouts",
        title_font=dict(size=16, color=colors['title'], family="system-ui, -apple-system, Segoe UI, Roboto"),
        height=350,
        margin=dict(l=40, r=40, t=60, b=80),
        paper_bgcolor='white',
        plot_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=colors['border'],
            borderwidth=1
        ),
        font=dict(
            family="system-ui, -apple-system, Segoe UI, Roboto",
            color=colors['text']
        )
    )
    
    # Update y-axes
    fig.update_yaxes(title_text="Intensity (%)", range=[0, 100], row=1, col=1)
    fig.update_yaxes(title_text="Duration (min)", range=[0, 90], row=1, col=2)
    
    # Update x-axes
    fig.update_xaxes(title_text="Workout Type", row=1, col=1)
    fig.update_xaxes(title_text="Workout Type", row=1, col=2)
    
    return fig

# Callback for the phase advice
@app.callback(
    Output('phase-advice', 'children'),
    [Input('phase-selection', 'value')]
)
def update_phase_advice(selected_phase):
    # Update phase advice
    phase_advice = {
        'Menstrual': [
            "Focus on gentle recovery workouts",
            "Pay extra attention to iron-rich foods",
            "Prioritize sleep and hydration",
            "Consider shorter but more frequent sessions"
        ],
        'Follicular': [
            "Great time to work on building strength",
            "Your body can handle more intensity now",
            "Good phase for trying new workout routines",
            "Focus on skill development and technique"
        ],
        'Ovulatory': [
            "Peak performance window - ideal for tests or races",
            "Body is primed for high-intensity workouts",
            "Recovery tends to be efficient in this phase",
            "Good time to push for personal records"
        ],
        'Luteal': [
            "Focus on maintaining rather than building",
            "Pay attention to cooling down properly",
            "You may need more carbohydrates for energy",
            "Adjust expectations as fatigue may increase"
        ]
    }
    
    advice = phase_advice[selected_phase]
    
    return html.Ul([
        html.Li(item, style={
            'marginBottom': '8px',
            'lineHeight': '1.5',
            'fontSize': '14px'
        }) for item in advice
    ], style={'paddingLeft': '20px'})

# Callback for impact distribution
@app.callback(
    Output('impact-distribution', 'figure'),
    [Input('impact-selection', 'value')]
)
def update_impact_distribution(selected_impact):
    # Get the original question from our mapping
    if selected_impact in reverse_question_mapping:
        original_question = reverse_question_mapping[selected_impact]
        
        # Count values
        value_counts = df[original_question].value_counts().sort_index()
        
        # Map numeric values to labels for better understanding
        labels = {1: "High Impact", 2: "Moderate Impact", 3: "Low Impact"}
        
        # Create colors list based on impact level
        colors_list = ['#ff6b6b', '#feca57', '#1dd1a1']
        
        # Create the bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=[labels[i] for i in value_counts.index],
            y=value_counts.values,
            marker_color=colors_list,
            text=value_counts.values,
            textposition='auto'
        ))
        
        # Update layout
        fig.update_layout(
            title=f"Distribution of {selected_impact}",
            title_font=dict(size=16, color=colors['title'], family="system-ui, -apple-system, Segoe UI, Roboto"),
            xaxis_title="Impact Level",
            yaxis_title="Number of Athletes",
            height=350,
            margin=dict(l=40, r=40, t=80, b=40),
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(
                family="system-ui, -apple-system, Segoe UI, Roboto",
                color=colors['text']
            ),
            xaxis=dict(
                gridcolor='rgba(0,0,0,0.05)',
                showgrid=True
            ),
            yaxis=dict(
                gridcolor='rgba(0,0,0,0.05)',
                showgrid=True
            )
        )
        
        return fig
    
    # Fallback if mapping not found
    return go.Figure()

# Callback for correlations heatmap
@app.callback(
    Output('correlations-heatmap', 'figure'),
    [Input('dummy-input', 'children')]  # Dummy input to trigger on load
)
def update_correlations_heatmap(dummy):
    # Select key performance metrics
    performance_metrics = [
        'Energy Fluctuations', 
        'Strength/Endurance Changes', 
        'Fatigue/Soreness',
        'High Intensity Capability',
        'Recovery Time Change',
        'Motivation Impact'
    ]
    
    # Create a dummy correlation matrix (in a real app, calculate this from actual data)
    # These correlations are simulated based on our limited analysis
    correlation_matrix = np.array([
        [1.00, 0.58, 0.47, 0.52, 0.35, 0.30],  # Energy Fluctuations
        [0.58, 1.00, 0.43, 0.65, 0.38, 0.25],  # Strength/Endurance
        [0.47, 0.43, 1.00, 0.39, 0.68, 0.42],  # Fatigue/Soreness
        [0.52, 0.65, 0.39, 1.00, 0.41, 0.33],  # High Intensity
        [0.35, 0.38, 0.68, 0.41, 1.00, 0.29],  # Recovery Time
        [0.30, 0.25, 0.42, 0.33, 0.29, 1.00]   # Motivation
    ])
    
    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=performance_metrics,
        y=performance_metrics,
        colorscale='Viridis',
        zmin=-1, zmax=1,
        text=correlation_matrix,
        texttemplate='%{text:.2f}',
        colorbar=dict(title='Correlation')
    ))
    
    # Update layout
    fig.update_layout(
        title="Correlation Between Performance Metrics",
        title_font=dict(size=16, color=colors['title'], family="system-ui, -apple-system, Segoe UI, Roboto"),
        height=350,
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            tickfont=dict(size=10)
        ),
        paper_bgcolor='white',
        font=dict(
            family="system-ui, -apple-system, Segoe UI, Roboto",
            color=colors['text']
        )
    )
    
    return fig

# Callback for training planner
@app.callback(
    Output('training-planner', 'figure'),
    [Input('dummy-input-2', 'children')]  # Dummy input to trigger on load
)
def update_training_planner(dummy):
    # Create calendar data for next 28 days (one cycle)
    # In a real app, this would be calculated based on the user's cycle tracking
    days = list(range(1, 29))
    
    # Assign phases - this is simplified; would be personalized in real app
    phases = ['Menstrual'] * 5 + ['Follicular'] * 9 + ['Ovulatory'] * 3 + ['Luteal'] * 11
    
    # Assign recommended workout types
    workout_types = []
    for phase in phases:
        if phase == 'Menstrual':
            workout_types.append(np.random.choice(['Light Jog', 'Recovery Walk', 'Gentle Yoga']))
        elif phase == 'Follicular':
            workout_types.append(np.random.choice(['Hill Sprints', 'Tempo Run', 'Long Run']))
        elif phase == 'Ovulatory':
            workout_types.append(np.random.choice(['HIIT Session', 'Race Pace Run', 'Speed Intervals']))
        else:  # Luteal
            workout_types.append(np.random.choice(['Steady State', 'Fartlek Training', 'Cross Training']))
    
    # Assign intensity levels (0-100)
    intensity_levels = []
    for phase in phases:
        if phase == 'Menstrual':
            intensity_levels.append(np.random.randint(30, 60))
        elif phase == 'Follicular':
            intensity_levels.append(np.random.randint(60, 80))
        elif phase == 'Ovulatory':
            intensity_levels.append(np.random.randint(80, 100))
        else:  # Luteal
            intensity_levels.append(np.random.randint(50, 75))
    
    # Create a DataFrame for the calendar
    calendar_df = pd.DataFrame({
        'Day': days,
        'Phase': phases,
        'Workout': workout_types,
        'Intensity': intensity_levels
    })
    
    # Define colors for each phase
    phase_colors = {
        'Menstrual': colors['accent1'],
        'Follicular': colors['accent2'],
        'Ovulatory': colors['accent3'],
        'Luteal': colors['accent4']
    }
    
    # Create color-coded calendar
    fig = go.Figure()
    
    # Add color bands for phases
    current_phase = None
    phase_start = 0
    
    for i, phase in enumerate(phases):
        if phase != current_phase:
            if current_phase is not None:
                # Add a colored rectangle for the previous phase
                # Convert hex color to rgba for transparency
                hex_color = phase_colors[current_phase].lstrip('#')
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                rgba_color = f'rgba({r}, {g}, {b}, 0.3)'  # 0.3 for 30% transparency
                
                fig.add_shape(
                    type="rect",
                    x0=phase_start - 0.5,
                    x1=i - 0.5,
                    y0=-0.5,
                    y1=1.5,
                    fillcolor=rgba_color,
                    line=dict(width=0),
                    layer="below"
                )
            current_phase = phase
            phase_start = i
    
    # Add the last phase
    # Convert hex color to rgba for transparency for the last phase
    hex_color = phase_colors[current_phase].lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    rgba_color = f'rgba({r}, {g}, {b}, 0.3)'  # 0.3 for 30% transparency
    
    fig.add_shape(
        type="rect",
        x0=phase_start - 0.5,
        x1=len(phases) - 0.5,
        y0=-0.5,
        y1=1.5,
        fillcolor=rgba_color,
        line=dict(width=0),
        layer="below"
    )
    
    # Add intensity markers
    fig.add_trace(go.Scatter(
        x=calendar_df['Day'],
        y=[1] * len(calendar_df),  # All at the same y-level
        mode='markers',
        marker=dict(
            size=calendar_df['Intensity'] / 2,  # Size based on intensity
            color=[phase_colors[phase] for phase in calendar_df['Phase']],
            line=dict(width=1, color='white')
        ),
        text=calendar_df.apply(lambda row: f"Day {row['Day']}<br>Phase: {row['Phase']}<br>Workout: {row['Workout']}<br>Intensity: {row['Intensity']}%", axis=1),
        hoverinfo='text'
    ))
    
    # Add phase labels
    phase_starts = {}
    for i, phase in enumerate(phases):
        if phase not in phase_starts:
            phase_starts[phase] = i + 1  # Day number (1-indexed)
    
    # Add annotations for phase starts
    for phase, day in phase_starts.items():
        fig.add_annotation(
            x=day,
            y=1.3,
            text=phase,
            showarrow=False,
            font=dict(
                color=phase_colors[phase],
                size=12
            )
        )
    
    # Update layout
    fig.update_layout(
        title="28-Day Training Calendar Based on Cycle Phases",
        xaxis=dict(
            title="Day of Cycle",
            tickmode='linear',
            tick0=1,
            dtick=1,
            range=[0, 29]
        ),
        yaxis=dict(
            showticklabels=False,
            range=[0, 2]
        ),
        height=200,
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )
    
    return fig

# Add a dummy div for triggering callbacks
app.layout.children.append(html.Div(id='dummy-input', style={'display': 'none'}))
app.layout.children.append(html.Div(id='dummy-input-2', style={'display': 'none'}))

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)