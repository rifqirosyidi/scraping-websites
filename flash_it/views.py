from django.shortcuts import render
from .functions import handle_elevenia_flashsale, handle_uqshop_flashsale


# Create your views here.
def flashsale(request):

    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
    headers = {'User-Agent': user_agent}

    ele_url = 'https://www.elevenia.co.id/daily-deals'
    uqi_url = 'https://www.uqishop.com/'

    # Zip Object
    ele_list = handle_elevenia_flashsale(ele_url, headers)
    uqi_list = handle_uqshop_flashsale(uqi_url, headers)

    # Convert To List
    ele_flash = list(ele_list)
    uqi_flash = list(uqi_list)

    context = {
        'ele_flash': ele_flash,
        'uqi_flash': uqi_flash
    }
    return render(request, 'flash_it/flashsale.html', context)
