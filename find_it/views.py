import os
import difflib
import csv
from itertools import chain

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .models import MarketplaceSource, ProductSearch
from .functions import handle_uqshop, handle_olx, handle_elevenia, handle_sorabel
from operator import itemgetter


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

    sources = MarketplaceSource.objects.all()
    page = request.GET.get('page', 1)

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
        uqi_url = 'https://www.uqishop.com/'
        ele_url = 'https://www.elevenia.co.id/'
        sor_url = 'https://www.sorabel.com/'

        if search_keyword:
            final_olx_url = olx_url + f'items/q-{search_keyword}'
            final_uqi_url = uqi_url + f'?s={search_keyword}&post_type=product'
            final_elevenia_url = ele_url + f'search?q={search_keyword}'
            final_sor_url = sor_url + f'products/search?query={search_keyword}'
            # final_laz_url = laz_url + f'catalog/?q={search_keyword}'

            olx_list = handle_olx(final_olx_url, headers)
            uq_list = handle_uqshop(final_uqi_url, headers)
            ele_list = handle_elevenia(final_elevenia_url, headers)
            sor_list = handle_sorabel(final_sor_url, headers)

            list_not_sorted = list(chain(olx_list, uq_list, ele_list, sor_list))

            convert_to_list = [list(ele) for ele in list_not_sorted]

            cleaned_list = []
            for l in convert_to_list:
                l[1] = l[1].replace("Rp ", "").replace(".", "")
                l[1] = int(l[1])
                cleaned_list.append(l)

            with open("output.csv", "w") as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Price", "Image", "Location", "Source"])
                writer.writerows(cleaned_list)

            # Sort By Default - Relevance
            my_list = sorted(cleaned_list,
                             key=lambda z: difflib.SequenceMatcher(None, z[0], search_keyword).ratio())

            # Sort By High Price
            sort_by = request.GET.get('sort', 'relevant')
            if request.GET.get("sort") or None:
                sort_by = request.GET.get('sort')

                if sort_by == 'price-low':
                    my_list = sorted(cleaned_list, key=itemgetter(1))
                elif sort_by == 'price-high':
                    my_list = sorted(cleaned_list, key=itemgetter(1), reverse=True)

            # Render The Content with pagination, 12/page
            paginator = Paginator(my_list, 12)
            try:
                my_list = paginator.page(page)
            except PageNotAnInteger:
                my_list = paginator.page(1)
            except EmptyPage:
                my_list = paginator.page(paginator.num_pages)

            # driver.get(final_laz_url)



            # container = driver.find_elements_by_xpath('div[@class="c16H9d"]/a')
            #
            # print(container)
            # driver.quit()

            context = {
                'products': my_list,
                'sources': sources,
                'searched': search_keyword,
                'sort_by': sort_by,
            }

            return render(request, 'find_it/search.html', context)
    else:
        return render(request, 'find_it/search.html')


def about(request):
    return render(request, 'find_it/about.html')



