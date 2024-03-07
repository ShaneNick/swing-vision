from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OutcomeSerializer
from .data.match_data import get_match_outcomes
from bokeh.embed import server_document

def outcomes_page(request):
    # Fetch the outcomes data using function
    outcomes_data = get_match_outcomes().to_dict('records')  # Convert DataFrame to a list of dicts
    
    # Generate the script to embed the Panel app from the Bokeh server
    script = server_document('http://localhost:5006/panel_app')
    
    # Prepare the context with both the outcomes data and the Bokeh/Panel script
    context = {
        'outcomes': outcomes_data,
        'script': script  # Include the script for embedding the Bokeh/Panel app
    }
    
    # Render the 'outcomes.html' template with the combined context
    return render(request, 'data_processing/outcomes.html', context)
