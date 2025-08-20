export const handler = async () => {
  const projectId = process.env.VITE_WALLETCONNECT_PROJECT_ID;

  if (!projectId) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'WalletConnect projectId is not configured on the server.' }),
    };
  }

  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ projectId }),
  };
};
