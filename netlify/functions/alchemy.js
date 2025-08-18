import { Alchemy, Network } from 'alchemy-sdk';

export const handler = async (event) => {
  // Get the wallet address from the query string parameters
  const { address } = event.queryStringParameters;

  if (!address) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Wallet address is required' }),
    };
  }

  // Ensure the API key is available from the build environment variables
  const apiKey = process.env.VITE_ALCHEMY_API_KEY;
  if (!apiKey) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Alchemy API key is not configured on the server.' }),
    };
  }

  const settings = {
    apiKey: apiKey,
    network: Network.ETH_MAINNET,
  };

  const alchemy = new Alchemy(settings);

  try {
    // Fetch NFTs using the Alchemy SDK
    const nfts = await alchemy.nft.getNftsForOwner(address);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(nfts),
    };
  } catch (error) {
    console.error('Error fetching NFTs from Alchemy:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to fetch NFT data.' }),
    };
  }
};
