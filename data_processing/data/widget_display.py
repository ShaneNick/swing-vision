# import pandas as pd
# import panel as pn
# import hvplot.pandas
# from match_data import get_match_outcomes  

# # Load your match outcomes data
# df = get_match_outcomes()

# # If keeping MultiSelect for multiple selections
# shot_numbers = [1, 3, 5]  # Directly specify since we know the filtered shots
# w_shot_number = pn.widgets.Select(name='Shot Number', value=1, options=shot_numbers)

# # Adjusted function with @pn.depends for dynamic update based on widget's selection
# @pn.depends(w_shot_number.param.value)
# def filter_shots(selected_shot):
#     filtered_data = df[df['Shot_Number'].isin([selected_shot])]  # Adjust based on Single or MultiSelect
#     return filtered_data.groupby('Outcome').size().hvplot.bar(
#         title=f"Outcomes for Shot Number {selected_shot}",
#         xlabel='Outcome',
#         ylabel='Count',
#         width=600,
#         height=400
#     )

# # Arrange widget and dynamically updated plot into a layout
# layout = pn.Column(w_shot_number, filter_shots)

# # Serve the layout as a Panel app
# layout.servable()

