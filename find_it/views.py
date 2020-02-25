import requests
import os
import difflib
from itertools import chain
from django.shortcuts import render, redirect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import html
from .models import MarketplaceSource, ProductSearch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('mysite/mysite')))


# Create your views here.
def home(request):
    our_partners = MarketplaceSource.objects.all()
    latest_search = ProductSearch.objects.all().order_by('-id')[:7]
    context = {
        'our_partners': our_partners,
        'latest_search': latest_search
    }
    return render(request, 'find_it/index.html', context)


# def search(request):
#     if request.method == 'GET':
#         search_keyword = request.GET['find']
#
#         # --- THIS IS FOR LATEST SEARCH MENU CHECK
#         check = ProductSearch.objects.filter(keyword__iexact=search_keyword)
#         if check:
#             check.delete()
#
#         entry = ProductSearch.objects.create(keyword=search_keyword)
#         entry.save()
#
#         # # Ready The Driver
#         # chrome_options = Options()
#         # chrome_options.add_argument("--headless")
#         #
#         # driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver'), options=chrome_options)
#
#         # print(driver.page_source.encode('utf-8'))  # The Process of getting the data
#
#         user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
#         headers = {'User-Agent': user_agent}
#
#         olx_url = 'https://www.olx.co.id/'
#         # laz_url = 'https://www.lazada.co.id/'
#         uqi_url = 'https://www.uqishop.com/'
#
#         if search_keyword:
#             final_olx_url = olx_url + f'items/q-{search_keyword}'
#             final_uqi_url = uqi_url + f'?s={search_keyword}&post_type=product'
#             # final_laz_url = laz_url + f'catalog/?q={search_keyword}'
#
#             olx_list = handle_olx(final_olx_url, headers)
#             uq_list = handle_uqshop(final_uqi_url, headers)
#
#             list_not_sorted = list(chain(olx_list, uq_list))
#
#             # Sort By Default - Relevance
#             my_list = sorted(list_not_sorted,
#                              key=lambda z: difflib.SequenceMatcher(None, z[0], search_keyword).ratio(),
#                              reverse=True)
#
#             # driver.get(final_laz_url)
#
#
#             # container = driver.find_elements_by_xpath('div[@class="c16H9d"]/a')
#             #
#             # print(container)
#             # driver.quit()
#
#             context = {
#                 'products': my_list,
#                 'searched': search_keyword
#             }
#
#             return render(request, 'find_it/search.html', context)
#     else:
#         return render(request, 'find_it/search.html')

def search(request):
    return render(request, 'find_it/search.html')

def handle_uqshop(target_url, header_url):
    page = requests.get(target_url, headers=header_url)
    tree = html.fromstring(page.content)

    title = tree.xpath('//h2[@class="woocommerce-loop-product__title"]/text()')
    price = tree.xpath('//span[@class="price"]/ins/span/text()')
    image = tree.xpath('//div[@class="product-image-box"]/a/img/@src')
    location = []
    date = []
    source = []

    for i in range(len(title)):
        location.append("Malang, Jawa Timur")
        date.append('')
        source.append('uqshop')

    return zip(title, price, image, location, date, source)


def handle_olx(target_url, header_url):
    page = requests.get(target_url, headers=header_url)
    tree = html.fromstring(page.content)

    title = tree.xpath('//span[@class="_2tW1I"]/text()')
    price = tree.xpath('//span[@class="_89yzn"]/text()')
    image = tree.xpath('//figure[@class="_2grx4"]//img//@src')
    location = tree.xpath('//div[@class="_1KOFM"]/span[@class="tjgMj"]/text()')
    date = tree.xpath('//div[@class="_1KOFM"]/span[@class="zLvFQ"]/span/text()')
    source = []

    for i in range(len(title)):
        source.append('olx')

    return zip(title, price, image, location, date, source)
