def wallettostring(wallet):
    ws = "{0:#0{1}x}".format(int(wallet,16),1)
    if len(ws) < 42:
        addzeros = 42 - len(ws)
        ws = ws.replace("0x","0x" + "0" * addzeros)
    return ws
