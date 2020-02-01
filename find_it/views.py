from django.shortcuts import render, redirect
from lxml import html
import requests


# Create your views here.
def home(request):
    return render(request, 'find_it/index.html')


def search(request):
    if request.method == 'GET':
        search_keyword = request.GET.get('find')
        olx_url = 'https://www.olx.co.id/'

        if search_keyword:
            final_olx_url = olx_url + f'items/q-{eval(search_keyword)}'

            page_olx = requests.get(final_olx_url)
            tree_olx = html.fromstring(page_olx.content)

            searched_olx = tree_olx.xpath('//span[@class="_89yzn"]/text()')

            print('OLX ------------------------: ', searched_olx)

            return redirect('/')

    return render(request, 'find_it/search.html')
