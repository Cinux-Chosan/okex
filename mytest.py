from urllib import request
import requests
import hashlib
import json

# 一、 交易指令函数

# 定义交易函数 do_transaction(symbol, contract_type, price, amount, trade_type, match_price)，参数解释如下：
# 1. symbol:  币种，例如eos_usd, btc_usd, ltc_usd
# 2. contract_type:  合约类型，例如next_weex（次周）、quarter（季度）、this_weex（当周）
# 3. price:  价格
# 4. amount:  合约张数。okex上，1张BTC合约等于100美元、其它币种1张合约等于10美元。
# 5. trade_type:  交易类型，1表示开多，2表示开空，3表示平多，4表示平空
# 6. match_price:  表示是否直接采用对手价。0:不采用 1:采用。 当match_price为1时, price参数无效

# 代码：

api_key = 'e091bc61-9a1f-4fdf-a2b2-40cca7bb7300'
secret_key = '92417525CCBF1735B6F609F1B26ABBDD'

def do_transaction(symbol, contract_type, price, amount, trade_type, match_price):
    api_url = "https://www.okex.com/api/v1/future_trade.do"
    post_data = {
        "api_key": api_key,
        "symbol": "symbol",
        # value: this_week, next_week, quarter:
        "contract_type": contract_type,
        "price": price,
        "amount": amount,
        "type": trade_type,
        "match_price": match_price
    }
    post_data['sign'] = buildMySign(post_data, secret_key)

    # buildMySign是生成签名的函数，交易所通常会要求提供
    res = requests.post(api_url, post_data)
    return res.json()


def buildMySign(params, secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) + '&'
    data = sign+'secret_key='+secretKey
    return hashlib.md5(data.encode("utf8")).hexdigest().upper()

# buildMySign是Okex要求的生成签名的函数。要实现自动交易，你需要在okex网站获取你的API key和secret，使用API key和secret生成签名

# 二、获取市场行情

# 获取市场行情（深度）的代码如下：
# 代码：

# 使用 urllib2获取 EOS次周合约市场深度

url_of_eos_next_week = "https://www.okex.com/api/v1/future_depth.do?symbol=eos_usdt&contract_type=next_week&size=1"  # EOS次周合约市场深度API地址

req_eos_next_week = request.Request(url_of_eos_next_week)
req_eos_next_week.add_header("Content-Type", "application/x-www-form-urlencoded")
req_eos_next_week.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36")
res_eos_next_week = request.urlopen(req_eos_next_week, timeout = 4.0)
json_res_eos_next_week = json.loads(res_eos_next_week.read().decode("utf-8"))

print(json_res_eos_next_week)

# json_res_eos_next_week即为EOS次周合约价格信息

# 使用 urllib2获取 EOS季度合约市场深度
url_of_eos_quarter = "https://www.okex.com/api/v1/future_depth.do?symbol=eos_usdt&contract_type=quarter&size=1"  # EOS季度合约市场深度API地址

req_eos_quarter = request.Request(url_of_eos_quarter)
req_eos_quarter.add_header("Content-Type", "application/x-www-form-urlencoded")
req_eos_quarter.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36")
res_eos_quarter = request.urlopen(req_eos_quarter, timeout=4.0)
json_res_eos_quarter = json.loads(res_eos_quarter.read().decode("utf-8"))  # json_res_eos_quarter 即为EOS季度合约价格信息

print(json_res_eos_quarter)

# 三、比较两个合约的价差，发出交易指令

# 这里我们假设价差大于1美元时，双向开仓；当价差小于0.5美元时，双向平仓。

# 代码：

# 当季度合约卖出（做空）价格，减去次周合约买入（做多）价格，得到的价差大于 1美元时，即做空季度，做多次周。

if json_res_eos_quarter['bids'][0][0] - json_res_eos_next_week['asks'][0][0] > 1:

    # 做多eos次周
    do_transaction(
        symbol='eos_usd',
        contract_type="next_week",
        price=str(json_res_eos_next_week['asks'][0][0]),
        amount='1',
        trade_type='1',
        match_price='0')

    # 做空eos季度
    do_transaction(
        symbol='eos_usd',
        contract_type="quarter",
        price=str(json_res_eos_quarter['bids'][0][0]),
        amount='1',
        trade_type='2',
        match_price='0')

# 当季度合约买入（平空）价格，减去次周合约卖出（平多）价格，得到的价差小于0.5美元时，即双向平仓。
# if json_res_eos_quarter['asks'][0][0] - json_res_eos_next_week['bids'][0][0] < 0.5:

#     # eos次周平多
#     do_Future_Tx(symbol='eos_usd', contract_type="next_week", price=str(
#         json_res_eos_next_week['bids'][0][0]), amount='1', trade_type='3', match_price='0')

#     # eos季度平空
#     do_Future_Tx(symbol='eos_usd', contract_type="quarter", price=str(
#         json_res_eos_quarter['asks'][0][0]), amount='1', trade_type='4', match_price='0')

# 上面代码中，我们直接指定了开仓价差为1美元、平仓价差为0.5美元。实际应用中，可采用均值法确定具体数值，采用网格法开仓，也可根据市场行情人工修改。
# 当价差很小或者为价差负时，我们可以反向开仓，即做空本周、做多季度，当价差扩大时，我们即平仓获利。
# 最后，跨期套利不是完全无风险套利，大家一定要注意仓位的控制，以防爆仓。
