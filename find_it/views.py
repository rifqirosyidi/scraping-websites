import requests
import os
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


def search(request):
    if request.method == 'GET':
        search_keyword = request.GET['find']

        # --- THIS IS FOR LATEST SEARCH MENU CHECK
        check = ProductSearch.objects.filter(keyword__iexact=search_keyword)
        if check:
            check.delete()

        entry = ProductSearch.objects.create(keyword=search_keyword)
        entry.save()

        # # Ready The Driver
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        #
        # driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver'), options=chrome_options)

        # print(driver.page_source.encode('utf-8'))  # The Process of getting the data

        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
        headers = {'User-Agent': user_agent}

        olx_url = 'https://www.olx.co.id/'
        # laz_url = 'https://www.lazada.co.id/'

        if search_keyword:
            final_olx_url = olx_url + f'items/q-{search_keyword}'
            # final_laz_url = laz_url + f'catalog/?q={search_keyword}'

            page_olx = requests.get(final_olx_url, headers=headers)
            # driver.get(final_laz_url)

            tree_olx = html.fromstring(page_olx.content)

            # container = driver.find_elements_by_xpath('div[@class="c16H9d"]/a')
            #
            # print(container)
            # driver.quit()

            title = tree_olx.xpath('//span[@class="_2tW1I"]/text()')
            price = tree_olx.xpath('//span[@class="_89yzn"]/text()')
            image = tree_olx.xpath('//figure[@class="_2grx4"]//img//@src')

            my_list = zip(title, price, image)
            context = {
                'products': my_list
            }

            return render(request, 'find_it/search.html', context)

    return render(request, 'find_it/search.html')
