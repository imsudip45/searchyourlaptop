from django.shortcuts import render
from googleapiclient.discovery import build

# Create your views here.

def search_laptops(request):
    if request.method == 'POST':
        laptop_model = request.POST.get('laptop_model')
        results = google_search(laptop_model)
        return render(request, 'index.html', {'results': results})
    return render(request, 'index.html')

def google_search(search_term):
    api_key = "AIzaSyCeYMX7fK6_Vri_627eDUoGAZ8nWRzvsTY"
    cse_id = "d7b6c11d0b7ec4c27"
    
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, searchType='image', num=5).execute()
    
    results = []
    for item in res.get('items', []):
        results.append({
            'title': item['title'],
            'image_url': item['link'],
            'link': item['image']['contextLink']
        })
    
    return results
