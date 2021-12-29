from binance.client import Client
from config import api_key, api_secret, mail_to
from mail import send

client = Client(api_key, api_secret)
account = client.get_account()

assets = {}
prices = client.get_all_tickers()
usdtovnd = float(client.get_avg_price(symbol="USDTBVND")["price"])

total_usdt = 0

for balance in account["balances"]:
    if float(balance["free"]) > 0 or float(balance["locked"]) > 0:
        for price in prices:
            if price["symbol"].startswith(balance["asset"]) and price[
                "symbol"
            ].endswith("USDT"):
                latest_price = float(price["price"])

        usdprice = (float(balance["free"]) + float(balance["locked"])) * latest_price
        vndprice = usdprice * usdtovnd
        total_usdt += usdprice
        assets[balance["asset"]] = {
            "name": balance["asset"],
            "free": balance["free"],
            "locked": balance["locked"],
            "usdprice": "$" + f"{round(usdprice, 2):,}",
            "vndprice": f"{round(vndprice):,}" + "đ",
        }
        print(
            balance["asset"],
            balance["free"],
            balance["locked"],
            "=>",
            assets[balance["asset"]]["usdprice"],
            "=>",
            assets[balance["asset"]]["vndprice"],
        )

print("Total:", "$" + f"{round(total_usdt, 2):,}")
print("Total:", f"{round(total_usdt * usdtovnd):,}" + "đ")

send(
    mail_to,
    "Wallet Tracker",
    f"""
<html>
<body>
<p>
<h5>Total: (USD) <b>${round(total_usdt, 2):,}</b> - (VND) <b>{round(total_usdt * usdtovnd):,}</b>đ.</h5>
</p>
<h3>Summary of all current balances:</h3>
<p>
<table border="1">
<tr>
<th>Coin</th>
<th>Free</th>
<th>Locked</th>
<th>USD</th>
<th>VND</th>
</tr>
"""
    + "\n".join(
        [
            f"""
<tr>
<td>{name}</td>
<td>{asset["free"]}</td>
<td>{asset["locked"]}</td>
<td><b>{asset["usdprice"]}</b></td>
<td><b>{asset["vndprice"]}</b></td>
</tr>
"""
            for name, asset in assets.items()
        ]
    )
    + """
</table>
</p>
</body>
</html>
""",
)
