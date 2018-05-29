def do_transaction(symbol, contract_type, price, amount, trade_type, match_price):
        api_url = "https://www.okex.com/api/v1/future_trade.do"
        post_data={
                "api_key": api_key,
                "symbol" : "symbol"
                "contract_type" : contract_type,    #value: this_week, next_week, quarter:
                "price" : price,
                "amount" : amount,
                "type": trade_type,
                "match_price" : match_price
        }
        post_data['sign'] = buildMySign(post_data, secret_key)

        # buildMySign是生成签名的函数，交易所通常会要求提供
        res=requests.post(api_url, post_data)
        return res.json()

def buildMySign(params,secretKey)
        sign = ''
        for key in sorted(params.keys()):
                sign += key + '=' + str(params[key]) +'&'
        data = sign+'secret_key='+secretKey
        return  hashlib.md5(data.encode("utf8")).hexdigest().upper()


url_of_eos_next_week = "https://www.okex.com/api/v1/future_depth.do?symbol=eos_usdt&contract_type=next_week&size=1" #EOS次周合约市场深度API地址

req_eos_next_week = urllib2.Request(url_of_eos_next_week)
req_eos_next_week.add_header("Content-Type","application/x-www-form-urlencoded")
req_eos_next_week.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36")
res_eos_next_week= urllib2.urlopen(res_eos_next_week, timeout=2)
json_res_eos_next_week = json.loads(res_eos_next_week.read().decode("utf-8"))




url_of_eos_quarter = "https://www.okex.com/api/v1/future_depth.do?symbol=eos_usdt&contract_type=quarter&size=1" #EOS季度合约市场深度API地址

req_eos_quarter = urllib2.Request(url_of_eos_quarter)
req_eos_quarter.add_header("Content-Type","application/x-www-form-urlencoded")
req_eos_quarter.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36")
res_eos_quarter = urllib2.urlopen(res_eos_quarter, timeout=2)
json_res_eos_quarter = json.loads(res_eos_quarter.read().decode("utf-8"))