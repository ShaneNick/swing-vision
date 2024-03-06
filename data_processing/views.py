from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OutcomeSerializer
from .data.match_data import get_match_outcomes  



def outcomes_page(request):
    # Fetch the outcomes data using function
    outcomes_data = get_match_outcomes().to_dict('records')  # Convert DataFrame to a list of dicts
    
    # Prepare the context with the outcomes data
    context = {'outcomes': outcomes_data}
    
    # Render the 'outcomes.html' template with the outcomes data
    return render(request, 'data_processing/outcomes.html', context)
