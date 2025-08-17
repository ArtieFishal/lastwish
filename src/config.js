window.LASTWISH_CONFIG = {
  payToAddress: "0x016ae25Ac494B123C40EDb2418d9b1FC2d62279b",
  payAmountEth: 0.0001,
  ensDiscountPercent: 20,
  n8nWebhookUrl: "", // optional webhook
  moralisApiKey: "YOUR_MORALIS_API_KEY_HERE",
  walletConnectProjectId: "YOUR_WALLETCONNECT_PROJECT_ID_HERE",

  chains: {
    1: {
      name: "Ethereum",
      moralis_name: "eth",
      symbol: "ETH",
      explorer: "https://etherscan.io",
    },
    137: {
      name: "Polygon",
      moralis_name: "polygon",
      symbol: "MATIC",
      explorer: "https://polygonscan.com",
    },
    56: {
      name: "BNB Smart Chain",
      moralis_name: "bsc",
      symbol: "BNB",
      explorer: "https://bscscan.com",
    },
    42161: {
      name: "Arbitrum",
      moralis_name: "arbitrum",
      symbol: "ETH",
      explorer: "https://arbiscan.io",
    }
  }
};
