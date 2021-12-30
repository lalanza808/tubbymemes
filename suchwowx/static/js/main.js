async function notif(s, t) {
  new Noty({
    type: t,
    theme: 'relax',
    layout: 'topCenter',
    text: s,
    timeout: 4500
  }).show();
  return
}

async function confirmAvalanche(){
  let debug = true;
  let chainId;
  let rpcUrl;
  let explorerUrl;
  let name;
  if (debug) {
    name = 'Avalance Testnet';
    chainId = '0xA869';
    rpcUrl = 'https://api.avax-test.network/ext/bc/C/rpc';
    explorerUrl = 'https://testnet.snowtrace.io';
  } else {
    name = 'Avalanche Mainnet';
    chainId = '0xA86A';
    rpcUrl = 'https://api.avax.network/ext/bc/C/rpc';
    explorerUrl = 'https://snowtrace.io';
  }
  try {
    await ethereum.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: chainId }],
    });
  } catch (switchError) {
    // This error code indicates that the chain has not been added to MetaMask.
    if (switchError.code === 4902) {
      try {
        await ethereum.request({
          method: 'wallet_addEthereumChain',
          params: [{
            chainId: chainId,
            chainName: name,
            nativeCurrency: {
              name: 'Avalanche',
              symbol: 'AVAX',
              decimals: 18,
            },
            rpcUrls: [rpcUrl],
            blockExplorerUrls: [explorerUrl],
          }],
        });
      } catch (addError) {
        // handle "add" error
      }
    }
    // handle other "switch" errors
  }
}
