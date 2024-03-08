from django.shortcuts import render
from .data.player_filtering import get_match_outcomes  
from bokeh.embed import server_document

def outcomes_page(request):
    # Fetch the outcomes data using function
    outcomes_df = get_match_outcomes()  
    
    # Convert DataFrame to a list of dicts and enumerate it for numbering
    outcomes_data = []
    for index, row in outcomes_df.iterrows():
        outcome_dict = row.to_dict()
        outcome_dict['Number'] = index + 1  # Adding numbering starting from 1
        outcomes_data.append(outcome_dict)
    
    # Generate the script to embed the Panel app from the Bokeh server
    script = server_document('http://localhost:5006/panel_app')
    
    # Prepare the context with both the outcomes data and the Bokeh/Panel script
    context = {
        'outcomes': outcomes_data,
        'script': script
    }
    
    # Render the 'outcomes.html' template with the combined context
    return render(request, 'data_processing/outcomes.html', context)
