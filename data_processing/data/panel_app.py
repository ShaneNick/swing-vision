import matplotlib.pyplot as plt
import pandas as pd
import panel as pn
import hvplot.pandas
import io
import numpy as np

# Corrected import paths based on the provided folder structure
from ..data_access.data_access import get_shots_df, get_points_df, setup_client

# Assuming that player_filtering.py and sequence_analysis.py are in the data/ directory
from .player_filtering import get_match_outcomes
from .sequence_analysis import enrich_shots_with_point_outcomes


# Load the match outcomes data
df = get_match_outcomes()

# Ensure 'Point' and 'Game' are of integer type for filtering
df['Point'] = df['Point'].astype(int)
df['Game'] = df['Game'].astype(int)

# Widgets for selecting a game, point, and shot type
games = ['All'] + sorted(df['Game'].unique().tolist())
game_selector = pn.widgets.Select(name='Select Game', options=games)

points = ['All'] + sorted(df['Point'].unique().tolist())
point_selector = pn.widgets.Select(name='Select Point', options=points)

shot_types = ['All'] + sorted(df['Shot'].unique().tolist())
shot_type_selector = pn.widgets.MultiSelect(name='Select Shot Type(s)', options=shot_types, size=10)

# Toggle button for enabling/disabling multiple selection
multi_select_toggle = pn.widgets.Toggle(name='Allow Multiple Selection', value=False)

# Define dynamic updates
@pn.depends(point_selector.param.value)
def update_plot_point(selected_point):
    if selected_point == "All":
        filtered_data = df
    else:
        filtered_data = df[df['Point'] == int(selected_point)]
    result_counts = filtered_data.groupby('Result').size().reset_index(name='Counts')
    return result_counts.hvplot.bar(x='Result', y='Counts', title=f"Outcomes for Point {selected_point}", xlabel='Outcome', ylabel='Count', width=600, height=400, color=['blue', 'orange'])


def create_pie_chart(data, title='Shot Type Distribution'):
    fig, ax = plt.subplots()
    data.plot(kind='pie', ax=ax, ylabel='', autopct='%1.1f%%')
    ax.set_title(title)
    
    # Save the plot to a BytesIO object and use it to create a Panel pane
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)  # Close the figure to free memory
    return pn.pane.PNG(buf, width=400, height=400)


@pn.depends(game_selector.param.value, shot_type_selector.param.value, multi_select_toggle.param.value)
def update_plot_game_shot_type(selected_game, selected_shot_types, allow_multi_select):
    if selected_game != 'All':
        filtered_data = df[df['Game'] == int(selected_game)]
    else:
        filtered_data = df

    if selected_shot_types:
        if allow_multi_select:
            filtered_rows = []
            for shot_type in selected_shot_types:
                if shot_type != 'All':
                    filtered_rows.append(filtered_data[filtered_data['Shot'] == shot_type])
            filtered_data = pd.concat(filtered_rows, ignore_index=True)
        else:
            selected_shot_type = selected_shot_types[0]
            if selected_shot_type != 'All':
                filtered_data = filtered_data[filtered_data['Shot'] == selected_shot_type]
    else:
        filtered_data = filtered_data[filtered_data['Shot'].isin(df['Shot'].unique())]

    if filtered_data.empty:
        return pn.pane.Markdown("No data available for the selected filters.")

    # Calculate win/loss totals
    win_count = filtered_data[filtered_data['Result'] == 'Won'].shape[0]
    loss_count = filtered_data[filtered_data['Result'] == 'Lost'].shape[0]

     # Calculate win percentage
    total_games = win_count + loss_count
    if total_games > 0:
        win_percentage = (win_count / total_games) * 100
    else:
        win_percentage = 0  # Avoid division by zero

    # Create totals card with win percentage
    totals_card = pn.Column(
        pn.pane.Markdown(f"**Wins:** {win_count}"),
        pn.pane.Markdown(f"**Losses:** {loss_count}"),
        pn.pane.Markdown(f"**Win Percentage:** {win_percentage:.2f}%")
    )

   # Generate pie chart for shot type frequency
    shot_type_counts = filtered_data['Shot'].value_counts()
    pie_chart_pane = create_pie_chart(shot_type_counts, 'Shot Type Distribution')

    # Adjust layout to incorporate the pie chart
    return pn.Row(filtered_data.hvplot.table(columns=['Player', 'Shot', 'Shot Type', 'Point', 'Game', 'Result'], width=600), totals_card, pie_chart_pane)

win_count_label = pn.pane.Markdown("Wins:", width=400)  

layout = pn.Column(
    pn.pane.Markdown("# Match Outcome Analysis"),
    pn.pane.Markdown("## Select Game and Shot Type"),
    game_selector,
    shot_type_selector,
    multi_select_toggle,
    win_count_label,  # Now reference the pre-defined win_count_label
    update_plot_game_shot_type,
    pn.pane.Markdown("## Select Point for Outcome Analysis"),
    point_selector,
    update_plot_point
)

# Serve the layout as a Panel app
layout.servable()


# Function to analyze and visualize serve outcome distribution
def serve_outcome_distribution():
    shots_df = get_shots_df()
    points_df = get_points_df()
    
    # Filter serves from the DataFrame
    serve_df = df[df['Shot'] == 1]

    # Categorize serve outcomes into 'Ace', 'Double Fault', 'Service Winner', and 'Other'
    conditions = [
        serve_df['Shot Description'].str.contains('Ace', case=False),
        serve_df['Shot Description'].str.contains('Double Fault', case=False),
        serve_df['Shot Description'].str.contains('Service Winner', case=False)
    ]
    choices = ['Ace', 'Double Fault', 'Service Winner']
    serve_df['Serve Outcome'] = np.select(conditions, choices, default='Other')

    # Count occurrences of each serve outcome
    outcome_counts = serve_df['Serve Outcome'].value_counts().reset_index()
    outcome_counts.columns = ['Serve Outcome', 'Count']

    # Create a bar plot for serve outcome distribution using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(outcome_counts['Serve Outcome'], outcome_counts['Count'], color='skyblue')
    plt.xlabel('Serve Outcome')
    plt.ylabel('Count')
    plt.title('Distribution of Serve Outcomes')
    plt.tight_layout()

    # Convert the Matplotlib plot to a Panel object for embedding in the Panel app
    serve_outcome_plot = pn.pane.Matplotlib(plt.gcf(), tight=True)
    plt.close()  # Close the plot to free memory
    return serve_outcome_plot

# Define Panel layout including the serve outcome distribution plot
serve_outcome_plot = serve_outcome_distribution()
layout = pn.Column(pn.pane.Markdown("# Serve Outcome Distribution Analysis"), serve_outcome_plot)

# Make the layout servable as a Panel app
layout.servable()