"""Chain & Token Registry for Smart Money Pulse Monitor"""
CHAIN_CONFIG = {
    "base": {"id": 8453, "name": "Base", "symbol": "ETH", "rpc": "https://mainnet.base.org", "explorer": "https://basescan.org"},
    "ethereum": {"id": 1, "name": "Ethereum", "symbol": "ETH", "rpc": "https://eth.llamarpc.com", "explorer": "https://etherscan.io"},
    "solana": {"id": "solana", "name": "Solana", "symbol": "SOL", "rpc": "https://api.mainnet-beta.solana.com", "explorer": "https://solscan.io"},
    "arbitrum": {"id": 42161, "name": "Arbitrum One", "symbol": "ETH", "rpc": "https://arb1.arbitrum.io/rpc", "explorer": "https://arbiscan.io"},
    "optimism": {"id": 10, "name": "Optimism", "symbol": "ETH", "rpc": "https://mainnet.optimism.io", "explorer": "https://optimistic.etherscan.io"},
}
TOKEN_REGISTRY = {
    "base": {
        "ETH": {"address": None, "decimals": 18}, "WETH": {"address": "0x4200000000000000000000000000000000000006", "decimals": 18},
        "USDC": {"address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "decimals": 6},
        "USDT": {"address": "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2", "decimals": 6},
        "DEGEN": {"address": "0x4ed4e86286bed2e48d49ad66e40341f8ab08e4d5", "decimals": 18},
        "AERO": {"address": "0x940181a94A35A4569E452Cc9642A4A42C29C4E24", "decimals": 18},
        "BRETT": {"address": "0x532f27121965B3463105bB1b2cA5D1D4Dfa9F2b2", "decimals": 18},
        "VIRTUAL": {"address": "0x0F1A8a36832d8f7BA17F2aE84dE69C6E9a9Bc6e1", "decimals": 18},
        "PENGU": {"address": "0xC6b18F7aD06006C0935E2D8c5D2a27B14e6d8E3b", "decimals": 18},
        "cbBTC": {"address": "0xcbB7C0000aB88B4738f6f8E2fB8aE1bB5eDd5A0", "decimals": 8},
        "AIXBT": {"address": "0x2DaC88F8C5E8C28f2aA92DDB4D1b86E52f9cbDD5", "decimals": 18},
        "AI16Z": {"address": "0x04F70aF3E5dEC4C52b81A82B2AA04bC34F8a26B7", "decimals": 18},
    },
    "ethereum": {
        "ETH": {"address": None, "decimals": 18}, "WETH": {"address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "decimals": 18},
        "USDC": {"address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "decimals": 6},
        "USDT": {"address": "0xdAC17F958D2ee523a2206206994597C13D831ec7", "decimals": 6},
        "WBTC": {"address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599", "decimals": 8},
        "stETH": {"address": "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84", "decimals": 18},
        "LDO": {"address": "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32", "decimals": 18},
        "UNI": {"address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", "decimals": 18},
        "LINK": {"address": "0x514910771AF9Ca656af840dff83E8264EcF986CA", "decimals": 18},
        "AAVE": {"address": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9", "decimals": 18},
        "ARB": {"address": "0xB50721BCf8d664c30412Cfbc6cf7a15145234ad1", "decimals": 18},
        "OP": {"address": "0x4200000000000000000000000000000000000042", "decimals": 18},
        "HYPE": {"address": "0xFa6aA21B9CFE5F2d8d2dE34B38d8f81942dB6b1", "decimals": 18},
    },
    "solana": {
        "SOL": {"address": None, "decimals": 9},
        "USDC": {"address": "EPjFWdd5AufqSSqeM2qN1xzybapC8MY4WN7K7yX7J5N", "decimals": 6},
        "USDT": {"address": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB", "decimals": 6},
        "WIF": {"address": "EKpQGSJt2NP7C6qmD5aD8RrxrM4Lhp8BQB9Je3J6L3s", "decimals": 9},
        "BONK": {"address": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263", "decimals": 5},
        "POPCAT": {"address": "RTixqKJDi2mG5vG5WEzT2twZ7bKHwfH4ZhVEvBfqXhL", "decimals": 9},
        "MEW": {"address": "MEW1gQWJ3nEXg2qgERiKu7FAFj79PHvQVREQUzScPP5", "decimals": 5},
        "BOME": {"address": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963vexs", "decimals": 6},
        "WEN": {"address": "WENwVDj6M4DnJbqiBA4uCb9E2qSxrAsPMP7T3QXLXo", "decimals": 5},
        "JTO": {"address": "jtojtomepa8beP8AuQc6eXtcbfriSsCmf1FWAPEPGQ", "decimals": 9},
        "JUP": {"address": "JUPyiwrYJFNFUP2PAliUdR2VwG2YHwALpWM5YcXhdn", "decimals": 6},
    },
    "arbitrum": {
        "ETH": {"address": None, "decimals": 18},
        "USDC": {"address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831", "decimals": 6},
        "ARB": {"address": "0x912CE59144191C1204E64559FE8253a0e49E6548", "decimals": 18},
    },
    "optimism": {
        "ETH": {"address": None, "decimals": 18},
        "USDC": {"address": "0x0b2C639c533813f1aB0a5cB90dbE2B76d4f6Bb2", "decimals": 6},
        "OP": {"address": "0x4200000000000000000000000000000000000042", "decimals": 18},
    },
}
def get_supported_chains(): return list(CHAIN_CONFIG.keys())
def resolve_token(symbol, chain=None):
    for c, tokens in TOKEN_REGISTRY.items():
        if chain and c != chain.lower(): continue
        if symbol.upper() in tokens: return {"chain": c, "token": symbol.upper(), **tokens[symbol.upper()]}
    return None
