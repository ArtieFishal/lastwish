const API_URL = 'https://api.coingecko.com/api/v3/simple/price';

/**
 * Fetches the USD price for a list of cryptocurrencies.
 * @param {string[]} coinIds - An array of CoinGecko coin IDs (e.g., ['bitcoin', 'ethereum']).
 * @returns {Promise<object>} A promise that resolves to an object mapping coin IDs to their USD price.
 */
export async function getPrices(coinIds) {
  if (!coinIds || coinIds.length === 0) {
    return {};
  }

  const ids = coinIds.join(',');
  const url = `${API_URL}?ids=${ids}&vs_currencies=usd`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`CoinGecko API request failed with status ${response.status}`);
    }
    const data = await response.json();

    // The API returns an object like { "bitcoin": { "usd": 60000 } }.
    // We want to simplify it to { "bitcoin": 60000 }.
    const prices = {};
    for (const id in data) {
      if (data[id] && data[id].usd) {
        prices[id] = data[id].usd;
      }
    }
    return prices;
  } catch (error) {
    console.error('Error fetching prices from CoinGecko:', error);
    return {};
  }
}
