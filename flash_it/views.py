from django.shortcuts import render
from .functions import handle_elevenia_flashsale


# Create your views here.
def flashsale(request):

    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
    headers = {'User-Agent': user_agent}

    ele_url = 'https://www.elevenia.co.id/daily-deals'

    # Zip Object
    ele_list = handle_elevenia_flashsale(ele_url, headers)

    # Convert To List
    flash_list = list(ele_list)

    context = {
        'flash_sale': flash_list
    }
    return render(request, 'flash_it/flashsale.html', context)
