from django.shortcuts import render, redirect
import requests
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import time
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import SignupForm
from main.forms import SignupForm, search_box
import plotly.graph_objs as go
from alpha_vantage.timeseries import TimeSeries

@login_required(login_url='usr/login')
def index(request):
    if request.method == 'POST':
        search_form = search_box(request.POST)
        if search_form.is_valid():
            symbol = search_form.cleaned_data['symbol_forms']
            return redirect('search', symbol=symbol)
    else:
        search_form = search_box()

    # List of stock symbols to display
    symbols = ['AAPL', 'TSLA', 'GOOG', 'IBM']
    api_key = 'A4XHTZWKU4Z14AUJ'
    stock_prices = {}
    for symbol in symbols:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()
        stock_price = data.get('Global Quote', {}).get('05. price')
        stock_prices[symbol] = stock_price
    context = {'stock_prices': stock_prices}
    return render(request, "main/home.html", context)

#search demo
@login_required(login_url='usr/login')
def search(request, symbol=None):
    api_key = "A4XHTZWKU4Z14AUJ"
    stock_data = None
    
    if symbol:
        # Build the API request URL
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}'
        
        # Get data from the Alpha Vantage API and handle rate limits
        for i in range(12):  # 12 requests will take 1 minute
            response = requests.get(url)
            data = response.json().get('Time Series (Daily)')
            if data:  # If we got data, stop retrying
                break
            time.sleep(5)  # Wait 5 seconds before trying again
        
        # Extract the date and closing price from the data
        dates = []
        prices = []
        for date, price_data in data.items():
            dates.append(date)
            prices.append(float(price_data['4. close']))
        
        # Create the chart data
        chart_data = {
            'labels': dates,
            'datasets': [{
                'label': symbol,
                'data': prices,
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }]
        }
        
        # Pass the stock data and chart data to the template
        stock_data = {
            'symbol': symbol,
            'price': data[dates[0]]['4. close'],
            'chart_data': chart_data
        }
    
    context = {'stock_data': stock_data}
    return render(request, 'main/search.html', context)
#search demo end

def SignupPage(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'main\singup.html', {'form': form})

def LoginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def candlestick_chart(request):
    # Set your Alpha Vantage API key
    api_key = 'your_api_key_here'

    # Retrieve the historical stock data for a specific symbol
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta_data = ts.get_daily(symbol='AAPL', outputsize='compact')

    # Generate a candlestick chart using Plotly
    chart = go.Figure(data=[go.Candlestick(x=data.index,
                                            open=data['1. open'],
                                            high=data['2. high'],
                                            low=data['3. low'],
                                            close=data['4. close'])])

    # Render the chart in your template
    return render(request, 'demos/search.html', {'chart': chart})

