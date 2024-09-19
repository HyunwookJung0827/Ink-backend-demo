# /tattoo_matcher/views.py

import logging
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .services import fetch_tattoo_artists, match_user_with_artist
    
logger = logging.getLogger(__name__)

@require_GET
def test_nocodb(request):
    artists = fetch_tattoo_artists()
    return JsonResponse(artists, safe=False)

@require_GET
def handle_typebot_request(request):
    try:
        # Extract user preferences from the request
        user_preferences = {
            'min_budget': request.GET.get('min_budget'),
            'max_budget': request.GET.get('max_budget')
        }
        logger.info(f"Received user preferences: {user_preferences}")

        # Fetch tattoo artists from NocoDB
        artists = fetch_tattoo_artists()
        logger.info(f"Fetched artists: {artists}")

        # Match user with artist
        matched_artist = match_user_with_artist(user_preferences, artists)
        if matched_artist:
            return JsonResponse({'artist': matched_artist[0], 'score': matched_artist[1]})
        else:
            return JsonResponse({'error': 'No matching artist found'}, status=404)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)