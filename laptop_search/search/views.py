from django.shortcuts import render
from googleapiclient.discovery import build
import re

def home(request):
    countries = ['USA', 'UK', 'Canada', 'Australia', 'India', 'Nepal']
    return render(request, 'index.html', {'countries': countries})

def search_laptops(request):
    countries = ['USA', 'UK', 'Canada', 'Australia', 'India', 'Nepal']
    if request.method == 'POST':
        laptop_model = request.POST.get('laptop_model', '')
        country = request.POST.get('country', '')
        price_from = request.POST.get('price_from', '')
        price_upto = request.POST.get('price_upto', '')
        
        results = google_search(laptop_model, country)
        filtered_results = filter_by_price(results, price_from, price_upto)
        
        context = {
            'results': filtered_results,
            'query': laptop_model,
            'selected_country': country,
            'countries': countries,
            'price_from': price_from,
            'price_upto': price_upto,
        }
        return render(request, 'index.html', context)
    return render(request, 'index.html', {'countries': countries})

def google_search(search_term, country):
    api_key = "[use your google custom search api key here]"
    cse_id = "[insert your cse id here]"
    
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=f"{search_term} laptop price in {country}", cx=cse_id, num=10).execute()
    
    results = []
    for item in res.get('items', []):
        price = extract_price(item['snippet'])
        if price is not None:
            results.append({
                'title': item['title'],
                'link': item['link'],
                'price': price,
                'image_url': item.get('pagemap', {}).get('cse_image', [{}])[0].get('src', '')
            })
    
    return results

def extract_price(text):
    price_match = re.search(r'(\$|£|€|₹|Rs\.?)\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
    if price_match:
        return float(price_match.group(2).replace(',', ''))
    return None

def filter_by_price(results, price_from, price_upto):
    try:
        price_from = float(price_from) if price_from else 0
        price_upto = float(price_upto) if price_upto else float('inf')
    except ValueError:
        return []
    
    filtered_results = [result for result in results if price_from <= result['price'] <= price_upto]
    return sorted(filtered_results, key=lambda x: x['price'])
