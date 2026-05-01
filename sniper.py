#!/usr/bin/env python3
"""BSC Sniper Bot — Free arbitrage scanner"""
import urllib.request, json

RPC = "https://1rpc.io/bnb"
ROUTERS = {
    "PancakeSwap": "0x10ED43C718714eb63d5aA57B78B54704E256024E",
    "Biswap": "0x3a6d8cA21D1CF76F653A67577FA0D27453350dD8",
}

def rpc(method, params=[]):
    d = json.dumps({"jsonrpc":"2.0","method":method,"params":params,"id":1}).encode()
    r = urllib.request.Request(RPC, data=d, headers={'Content-Type':'application/json'})
    return json.loads(urllib.request.urlopen(r, timeout=10).read())

def get_price(router, token):
    sig = "0xd06ca61f"
    amt = format(10**18, '064x')
    off = format(0x40, '064x')
    n = format(2, '064x')
    wbnb = "0"*24 + "bb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
    tok = "0"*24 + token[2:].lower()
    data = sig + amt + off + n + wbnb + tok
    result = rpc("eth_call", [{"to": router, "data": data}, "latest"])
    if result.get('result') and result['result'] != '0x':
        chunks = [int(result['result'][i:i+64], 16) for i in range(0, len(result['result']), 64)]
        return chunks[-1] / 10**18 if len(chunks) >= 2 else 0
    return 0

print("\n🔍 BSC DEX Arbitrage Scanner")
print("=" * 50)
usdt = "0x55d398326f99059fF775485246999027B3197955"
for name, router in ROUTERS.items():
    price = get_price(router, usdt)
    print(f"  {name}: 1 BNB = ${price:.2f}")
print(f"\n💝 Tip: 0xa59161F6De5021E4dc533ABd256d730A622D2999")
