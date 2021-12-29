async function getSignedData(publicAddress, jsonData) {
  const signedData = await window.ethereum.request({
    method: 'eth_signTypedData_v3',
    params: [publicAddress, JSON.stringify(jsonData)]
  });
  console.log(signedData);
  return signedData
}

async function confirmAvalanche(){
  try {
    await ethereum.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: '0xA86A' }],
    });
  } catch (switchError) {
    // This error code indicates that the chain has not been added to MetaMask.
    if (switchError.code === 4902) {
      try {
        await ethereum.request({
          method: 'wallet_addEthereumChain',
          params: [{
            chainId: '0xA86A',
            chainName: 'Avalanche',
            nativeCurrency: {
              name: 'Avalanche',
              symbol: 'AVAX',
              decimals: 18,
            },
            rpcUrls: ['https://api.avax.network/ext/bc/C/rpc'],
            blockExplorerUrls: ['https://snowtrace.io'],
          }],
        });
      } catch (addError) {
        // handle "add" error
      }
    }
    // handle other "switch" errors
  }
}
