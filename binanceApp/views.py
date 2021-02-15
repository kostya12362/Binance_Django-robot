from django.shortcuts import render
from binance.client import Client
from django.http import JsonResponse
from django.template.loader import render_to_string
from binance.websockets import BinanceSocketManager
from binanceApp.forms import OrderCreateForm
from binanceApp.models import Order
from binance.enums import *


api_key = ''
secret_key = ''

client = Client(api_key, secret_key)

btc_price = {'error': False}
df1 = list()
sum_MA = 0
MA = 0


def to_fixed(num_obj, digits=0):
    return f"{num_obj:.{digits}f}"


def btc_trade_history(msg):
    global df1, sum_MA, MA
    if msg['k']['x']:
        df1.append(float(msg['k']['c']))
        print(df1)
        if len(df1) >= 8:
            sum_MA = sum(df1[len(df1)-2:len(df1)])
    if len(df1) >= 8:
        MA = float(to_fixed(sum_MA + float(msg['k']['c'])/9, digits=2))
        delta = float(to_fixed(MA - float(to_fixed(float(msg['k']['c']))), digits=2))
        if delta > 0:
            print(delta, '---')
            if Order.objects.filter(range_price=delta, status=False):
                print(delta, '---')
                buy_order = client.create_test_order(
                    symbol='BTCUSDT',
                    side=SIDE_BUY,
                    type=ORDER_TYPE_MARKET,
                    quantity=float(Order.objects.filter(range_price=delta, status=False).values()[0]['btc_count']))
                order = Order.objects.filter(range_price=delta, status=False).first()
                order.status = True
                order.order_id = buy_order['orderId']
                order.save()
            else:
                pass
        elif delta < 0:
            print(delta, '+++')
            if Order.objects.filter(range_price=delta, status=False):
                sell_order = client.create_test_order(
                    symbol='BTCUSDT',
                    side=SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=float(Order.objects.filter(range_price=delta, status=False).values()[0]['btc_count'])
                    )
                order = Order.objects.filter(range_price=delta, status=False).first()
                order.status = True
                order.order_id = sell_order['orderId']
                order.save()
            else:
                pass
        if MA == float(msg['k']['c']):
            print("CLOSE")
            for obj in Order.objects.all():
                client.cancel_order(
                    symbol='BNBBTC',
                    orderId=obj.order_id
                    )

    else:
        pass


def order_list(request):
    orders_obj = Order.objects.all()
    content = {'orders': orders_obj, 'ma_obj': MA}
    return render(request, 'binance/list_binance.html', content)


def save_book_form(request, form, template_name):
    data = dict()
    print(MA)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            orders = Order.objects.all()
            data['html_order_list'] = render_to_string('binance/partial_order_list.html',
                                                       {'orders': orders})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    data['MA'] = MA
    return JsonResponse(data)


def ma(request):
    data = dict()
    data['MA'] = MA
    return JsonResponse(data, safe=False)


def order_create(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
    else:
        form = OrderCreateForm()
    return save_book_form(request, form, 'binance/partial_order_create.html')


client.get_avg_price(symbol='BNBBTC')
bsm = BinanceSocketManager(client)
conn_key = bsm.start_kline_socket('BTCUSDT', btc_trade_history, interval=Client.KLINE_INTERVAL_15MINUTE)
print(bsm.start())
