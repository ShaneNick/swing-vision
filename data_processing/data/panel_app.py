import pandas as pd
import panel as pn
import hvplot.pandas
from match_data import get_match_outcomes


pn.extension('bokeh')

# Load the match outcomes data
df = get_match_outcomes()

# Ensure 'Shot_Number' and 'Outcome' are of the correct type for filtering and visualization
df['Shot_Number'] = df['Shot_Number'].astype(int)
df['Outcome'] = df['Outcome'].astype('category')

# Create a widget for selecting the shot number
shot_selector = pn.widgets.Select(name='Select Shot Number', options=[1, 3, 5])

# Function to dynamically update the plot based on the selected shot number
@pn.depends(shot_selector.param.value)
def update_plot(selected_shot):
    # Filter the DataFrame based on the selected shot number
    filtered_data = df[df['Shot_Number'] == selected_shot]

    # Aggregate the data to get counts of each outcome
    outcome_counts = filtered_data.groupby('Outcome')['Outcome'].count().reset_index(name='Counts')

    # Generate and return the bar plot for the aggregated data
    return outcome_counts.hvplot.bar(x='Outcome', y='Counts', 
                                     title=f"Outcomes for Shot Number {selected_shot}",
                                     xlabel='Outcome', ylabel='Count',
                                     width=600, height=400)

# Arrange the widget and the dynamically updated plot in a layout
layout = pn.Column(shot_selector, update_plot)

# Serve the layout as a Panel app
layout.servable()
