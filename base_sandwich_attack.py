import requests, time

def sandwich_attack():
    print("Base — Sandwich Attack Detector (victim squeezed live)")
    seen = set()

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/transactions/base?limit=300")
            txs = sorted(r.json().get("transactions", []), key=lambda x: x.get("timestamp", 0))

            for i in range(1, len(txs) - 1):
                victim = txs[i]
                front = txs[i-1]
                back = txs[i+1]

                txid = victim["hash"]
                if txid in seen: continue

                if victim["pairAddress"] != front["pairAddress"] or victim["pairAddress"] != back["pairAddress"]:
                    continue

                if front["from"] == back["from"] and front["from"] != victim["from"]:
                    impact = victim.get("priceImpact", 0)
                    if impact > 5:  # significant squeeze
                        token = victim["token0"]["symbol"] if "WETH" in victim["token1"]["symbol"] else victim["token1"]["symbol"]
                        print(f"SANDWICH ATTACK LIVE\n"
                              f"{token} victim hit {impact:.1f}% impact\n"
                              f"Bot: {front['from'][:10]}...\n"
                              f"Victim tx: https://basescan.org/tx/{txid}\n"
                              f"https://dexscreener.com/base/{victim['pairAddress']}\n"
                              f"→ MEV bot just ate a retail swap\n"
                              f"{'SANDWICH'*20}")
                        seen.add(txid)

        except:
            pass
        time.sleep(1.5)

if __name__ == "__main__":
    sandwich_attack()
