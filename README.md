# CyclePerform Digital Twin Dashboard

This dashboard is a visualization prototype for a digital twin that helps runners optimize their training based on their menstrual cycle data. It showcases the main features of the digital twin concept without requiring full implementation.

## Design Prototype

View our full interface design prototype on Figma:
[CyclePerform Prototype](https://www.figma.com/proto/QHdwiavdZKRaH5nu095P6Z/Design?page-id=0%3A1&node-id=361-173&viewport=-6684%2C-6640%2C0.49&t=w7YMPLBfipHLib5q-1&scaling=scale-down&content-scaling=fixed&starting-point-node-id=361%3A173)

## Features

The dashboard includes:

1. **Current Status Panel**: Shows the current cycle phase, day in cycle, and overall readiness score
2. **Performance Radar Chart**: Visualizes performance metrics across different cycle phases
3. **Training Recommendations**: Provides workout suggestions tailored to the current cycle phase
4. **Phase-Specific Advice**: Offers nutrition, recovery, and training tips based on the cycle phase
5. **Performance Impact Analysis**: Shows survey data from female athletes on how menstrual cycles affect performance
6. **Correlation Heatmap**: Illustrates relationships between different performance metrics
7. **28-Day Training Planner**: A visual calendar showing recommended workouts across a cycle

## Data Sources

The dashboard uses two primary data sources:

1. **Survey Data**: Responses from the Excel file "EFFECT OF MENSTRUAL CYCLE ON PHYSICAL ACTIVITY AMONG COLLEGE GOING RECREATIONAL ATHLETES Responses.xlsx"
2. **Simulated User Data**: Represents personalized performance metrics across cycle phases

In a fully implemented digital twin, the user data would come from:
- Personal tracking of menstrual cycle
- Performance metrics from wearable devices
- Training logs and perceived exertion
- Recovery metrics

## Research Data

Our dashboard incorporates data from the study "Effect of Menstrual Cycle on Physical Activity Among College Going Recreational Athletes" (available at: https://data.mendeley.com/datasets/33bcv2jfbx/1, Toor, Dilrose; saha, joydip (2024), Mendeley Data, V1, doi: 10.17632/33bcv2jfbx.1).

## Design Roles

CyclePerform implements two key design roles as part of its digital twin architecture:

1. **The Coach**: Provides personalized training recommendations, adapts to the user's physiological state, and delivers actionable insights for daily training decisions.

2. **The Forecaster**: Tracks cycle phases and bodily changes, visualizes physiological readiness, and predicts future performance patterns to enable long-term planning.

Each visualization in the dashboard is aligned with one or both of these roles:
- Radar Chart: Coach role (performance profile across metrics)
- Bar Charts: Coach role (specific workout recommendations)
- Body Readiness Indicator: Coach role (current physiological state)
- 28-day Calendar: Forecaster role (future planning)
- Impact Distribution Chart: Both roles (contextual understanding)
- Correlation Heatmap: Forecaster role (understanding performance relationships)


## How to Run the Dashboard

### Standard Python Installation

1. Install the required packages:
```bash
pip install dash pandas numpy plotly openpyxl
```

2. Place the Excel file in the same directory as the Python script.

3. Run the script:
```bash
python cycle_analysis.py
```

4. Open your web browser and navigate to:
```
http://127.0.0.1:8050/
```

### Docker Installation

1. Build the Docker image:
```bash
docker build -t cycle-analysis .
```

2. Run the container:
```bash
docker run -p 8050:8050 -v "./EFFECT OF MENSTRUAL CYCLE ON PHYSICAL ACTIVITY AMONG COLLEGE GOING RECREATIONAL ATHLETES Responses.xlsx:/app/EFFECT OF MENSTRUAL CYCLE ON PHYSICAL ACTIVITY AMONG COLLEGE GOING RECREATIONAL ATHLETES Responses.xlsx" cycle-analysis
```

3. Access the dashboard at:
```
http://localhost:8050
```

Alternatively, use Docker Compose:
```bash
docker-compose up
```

## Implementation Notes

### Customization

The dashboard is designed to be easily customizable. Key areas to modify include:

- **Color Scheme**: Edit the `colors` dictionary at the top of the file
- **Phases Duration**: Currently set to standard lengths (Menstrual: 5 days, Follicular: 9 days, etc.)
- **Training Recommendations**: Can be customized in the `phase_workouts` dictionary in the `update_training_recommendations` function
- **Performance Metrics**: Modify the radar chart categories in `update_radar_chart`

### For Production Use

To turn this prototype into a production-ready application:

1. **User Authentication**: Add login functionality to personalize the experience
2. **Data Storage**: Implement a proper database to store user cycle and performance data
3. **API Integration**: Connect with wearables and fitness apps via APIs
4. **Machine Learning Model**: Train a model on the user's data to improve predictions over time
5. **Mobile Responsiveness**: Optimize the layout for mobile devices

## Key Visualizations

### Radar Chart
Shows performance metrics across cycle phases, helping athletes identify strengths and weaknesses during each phase.

### Training Calendar
Displays a 28-day view with color-coded phases and recommended workouts, allowing athletes to plan their training cycles effectively.

### Impact Analysis
Compares individual responses to the broader survey data, showing how common certain experiences are among female athletes.

## Dashboard Architecture

The dashboard uses Dash callbacks to create an interactive experience:

- **Layout**: Defined in the `app.layout` section
- **Callbacks**: Connect user interactions to data updates
- **Data Processing**: Handled in the `load_data()` function

## Future Enhancements

Potential features for future iterations:

1. **Predictive Analytics**: Forecast performance windows based on historical data
2. **Symptom Tracking**: Allow users to log symptoms and correlate with performance
3. **Nutrition Recommendations**: Tailored dietary suggestions for each phase
4. **Recovery Monitoring**: Integration with sleep and HRV data
5. **Team Integration**: Features for coaches working with female athletes

## Planned Evaluation Strategy

We've planned the following evaluation methods to assess the effectiveness of the CyclePerform digital twin:

1. **User Acceptance Testing**: With 8-12 competitive female runners to evaluate interface usability and recommendation relevance
2. **Expert Review Sessions**: With sports physiologists and running coaches to validate our training recommendations model
3. **A/B Testing**: To compare different visualization approaches for physiological data representation

These methods will help us measure key metrics including usability (via System Usability Scale), user satisfaction, and trust in the digital twin's recommendations across different cycle phases.

## About Digital Twins

This dashboard demonstrates the concept of a digital twin for athletic performance, creating a virtual representation of an athlete that:

1. **Monitors**: Tracks physiological changes throughout the menstrual cycle
2. **Predicts**: Forecasts optimal performance windows
3. **Optimizes**: Provides personalized training recommendations
4. **Learns**: Improves its predictions with more data over time

---

This prototype shows how a digital twin can help female athletes work with their physiology rather than against it, potentially improving performance, reducing injury risk, and enhancing overall wellbeing.
