import os
from flask import Flask, jsonify, make_response, send_from_directory, request

app = Flask(__name__)

# --- DATENBANK ---
PLAYERS = {
    "da2ef042b12c4da4960517a17bb89ae3": {
        "name": "Dotggicealts469",
        "rankings": {
            "vanilla": {"tier": 2, "pos": 1, "display": "LT2 §cVanilla"},
            "sword":   {"tier": 3, "pos": 1, "display": "HT3 §9Sword"},
            "uhc":     {"tier": 4, "pos": 1, "display": "LT4 §6UHC"},
            "smp":     {"tier": 4, "pos": 1, "display": "HT4 §aSMP"},
            "axe":     {"tier": 4, "pos": 1, "display": "LT4 §bAxe"},
            "mace":    {"tier": 3, "pos": 1, "display": "LT3 §5Mace"},
            "nethop":  {"tier": 4, "pos": 1, "display": "HT4 §4Nethop"},
            "diapot":  {"tier": 3, "pos": 1, "display": "HT3 §dDia Pot"}
        }
    },
    "b50d117436fa4390bb78d9204a200806": {
        "name": "VoidWalker120",
        "rankings": {
            "vanilla": {"tier": 5, "pos": 1, "display": "LT5 §cVanilla"},
            "sword":   {"tier": 4, "pos": 1, "display": "HT4 §9Sword"},
            "diapot":  {"tier": 4, "pos": 1, "display": "LT4 §dDia Pot"}
        }
    },
    "6c1e73ba5dc24b82b7c6bb4571df2ced": {
        "name": "NeuHinzugefügt",
        "rankings": {
            "vanilla": {"tier": 4, "pos": 1, "display": "HT4 §cVanilla"},
            "sword":   {"tier": 3, "pos": 1, "display": "HT3 §9Sword"},
            "uhc":     {"tier": 2, "pos": 1, "display": "LT2 §6UHC"},
            "smp":     {"tier": 3, "pos": 1, "display": "HT3 §aSMP"},
            "axe":     {"tier": 3, "pos": 1, "display": "HT3 §bAxe"},
            "mace":    {"tier": 3, "pos": 1, "display": "HT3 §5Mace"},
            "nethop":  {"tier": 2, "pos": 1, "display": "LT2 §4Nethop"},
            "diapot":  {"tier": 3, "pos": 1, "display": "HT3 §dDia Pot"}
        }
    },
    # --- BEARBEITET: SWEXITY ---
    "a0b6f7bb458c48e9b649ce15f635bea4": {
        "name": "Swexity",
        "rankings": {
            "vanilla": {"tier": 1, "pos": 1, "display": "LT1 §cVanilla"},
            "sword":   {"tier": 3, "pos": 1, "display": "HT3 §9Sword"},
            "uhc":     {"tier": 3, "pos": 1, "display": "LT3 §6UHC"},
            "smp":     {"tier": 3, "pos": 1, "display": "LT3 §aSMP"},
            "axe":     {"tier": 3, "pos": 1, "display": "HT3 §bAxe"},
            "mace":    {"tier": 3, "pos": 1, "display": "HT3 §5Mace"},
            "nethop":  {"tier": 2, "pos": 1, "display": "LT2 §4Nethop"},
            "diapot":  {"tier": 3, "pos": 1, "display": "LT3 §dDia Pot"}
        }
    },
    "2186f5c492e04dbea036d07298d240f9": {
        "name": "doctoturtle",
        "rankings": {
            "vanilla": {"tier": 3, "pos": 1, "display": "LT3 §cVanilla"},
            "uhc":     {"tier": 4, "pos": 1, "display": "LT4 §6UHC"},
            "axe":     {"tier": 3, "pos": 1, "display": "HT3 §bAxe"},
            "mace":    {"tier": 3, "pos": 1, "display": "HT3 §5Mace"},
            "nethop":  {"tier": 3, "pos": 1, "display": "LT3 §4Nethop"},
            "diapot":  {"tier": 3, "pos": 1, "display": "HT3 §dDia Pot"}
        }
    },
    "fad8bd19ca5a46bab1b6638aab290b0b": {
        "name": "Abutotem",
        "rankings": {
            "vanilla": {"tier": 2, "pos": 1, "display": "LT2 §cVanilla"},
            "sword":   {"tier": 3, "pos": 1, "display": "HT3 §9Sword"},
            "uhc":     {"tier": 5, "pos": 1, "display": "LT5 §6UHC"},
            "smp":     {"tier": 5, "pos": 1, "display": "HT5 §aSMP"},
            "axe":     {"tier": 4, "pos": 1, "display": "LT4 §bAxe"},
            "mace":    {"tier": 5, "pos": 1, "display": "LT5 §5Mace"},
            "nethop":  {"tier": 4, "pos": 1, "display": "LT4 §4Nethop"},
            "diapot":  {"tier": 5, "pos": 1, "display": "HT5 §dDia Pot"}
        }
    },
    "1b3cea7b99084dad8a25912eedd0222e": {
        "name": "zScriver",
        "rankings": {
            "vanilla": {"tier": 5, "pos": 1, "display": "§7No Tier"},
            "axe":     {"tier": 4, "pos": 1, "display": "HT4 §bAxe"},
            "nethop":  {"tier": 3, "pos": 1, "display": "LT3 §4Nethop"}
        }
    },
    "c0eec6cffe104c8784e601691f970ee1": {
        "name": "Melyxs",
        "rankings": {
            "vanilla": {"tier": 2, "pos": 1, "display": "HT2 §cVanilla"}
        }
    },
    "3b04c5e7d33b4cb5b74491579a6e57ee": {
        "name": "3fjm",
        "rankings": {
            "vanilla": {"tier": 3, "pos": 1, "display": "LT3 §cVanilla"},
            "axe":     {"tier": 5, "pos": 1, "display": "LT5 §bAxe"},
            "mace":    {"tier": 4, "pos": 1, "display": "HT4 §5Mace"},
            "smp":     {"tier": 4, "pos": 1, "display": "LT4 §aSMP"},
            "sword":   {"tier": 4, "pos": 1, "display": "HT4 §9Sword"}
        }
    },
    "a573c68ac7ab451c8650cb73f3da0145": {
        "name": "buddy_thebud",
        "rankings": {
            "vanilla": {"tier": 5, "pos": 1, "display": "§7No Tier"},
            "sword":   {"tier": 4, "pos": 1, "display": "HT4 §9Sword"}
        }
    }
}

def response(data):
    r = make_response(jsonify(data))
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/v2/profile/<uuid>/rankings')
def get_rankings(uuid):
    u = uuid.replace("-", "").lower()
    player_data = PLAYERS.get(u, {"rankings": {"vanilla": {"tier": 5, "pos": 1, "display": "§7No Tier"}}})
    return response(player_data["rankings"])

@app.route('/api/v2/tierlists')
@app.route('/tierlists')
def list_tiers():
    host = request.host_url.rstrip('/')
    return response({
        "vanilla": {"title": "§cVanilla", "kit_url": f"{host}/static/vanilla.png"},
        "sword": {"title": "§9Sword", "kit_url": f"{host}/static/sword.png"},
        "uhc": {"title": "§6UHC", "kit_url": f"{host}/static/uhc.png"},
        "smp": {"title": "§aSMP", "kit_url": f"{host}/static/smp.png"},
        "axe": {"title": "§bAxe", "kit_url": f"{host}/static/axe.png"},
        "mace": {"title": "§5Mace", "kit_url": f"{host}/static/mace.png"},
        "nethop": {"title": "§4Nethop", "kit_url": f"{host}/static/nethop.png"},
        "diapot": {"title": "§dDia Pot", "kit_url": f"{host}/static/diapot.png"}
    })

@app.route('/api/v2/tierlist/<gamemode>')
def get_tierlist(gamemode):
    gamemode = gamemode.lower()
    players_in_tier = []
    
    for uuid, data in PLAYERS.items():
        if gamemode in data["rankings"]:
            players_in_tier.append({
                "uuid": uuid,
                "name": data["name"],
                "ranking": data["rankings"][gamemode]
            })
    
    # Sort by tier (ascending) and then position
    players_in_tier.sort(key=lambda x: (x["ranking"]["tier"], x["ranking"]["pos"]))
    
    return response(players_in_tier)

@app.route('/api/v2/search')
def search_player():
    query = request.args.get('q', '').lower()
    if not query:
        return response([])
    
    results = []
    for uuid, data in PLAYERS.items():
        if query in data["name"].lower():
            results.append({
                "uuid": uuid,
                "name": data["name"],
                "rankings": data["rankings"]
            })
            
    return response(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)