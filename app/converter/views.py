from django.shortcuts import render
import requests
# Create your views here.
def convert(request):
    response = requests.get('https://api.cryptorank.io/v1/currencies?api_key=3cdd17fe8384d077ca61af67b9d257a792219ee0fc35d7d4533d9e2171ec').json()
    data = response['data']
    print(data)

    curr_to_usd = {el['symbol']: round(el['values']['USD']['price'], 2) for el in data}

    if request.method == 'GET':
        context = {
            'currencies': curr_to_usd
        }
        return render(request, 'converter/index.html', context=context)

    if request.method == 'POST':
        from_amount = float(request.POST.get('from-amount'))
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        converted_amount = round((curr_to_usd[from_curr] / curr_to_usd[to_curr]) * float(from_amount), 2)

        context = {
            'currencies': curr_to_usd,
            'converted_amount': converted_amount,
            'from_amount': from_amount,
            'from_curr': from_curr,
            'to_curr': to_curr,
        }

    return render(request, 'converter/index.html', context=context)