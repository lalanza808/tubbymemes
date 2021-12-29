window.addEventListener('DOMContentLoaded', () => {
  onboardMetaMask();
})

async function onboardMetaMask(){
  const onboarding = new MetaMaskOnboarding();
  const onboardButton = document.getElementById('metamaskConnect');
  let accounts;
  let nonce = 0;

  const connectButton = async () => {
    if (!MetaMaskOnboarding.isMetaMaskInstalled()) {
      onboardButton.innerText = 'Click here to install MetaMask!';
      onboardButton.onclick = () => {
        onboardButton.classList.add('is-loading');
        onboardButton.disabled = true;
        onboarding.startOnboarding();
      };
    } else if (accounts && accounts.length > 0) {
      onboardButton.classList.remove('is-loading');
      onboardButton.disabled = false;
      onboarding.stopOnboarding();
    } else {
      onboardButton.onclick = async () => {
        onboardButton.classList.add('is-loading');
        onboardButton.disabled = true;
        let userExists;
        await confirmAvalanche();
        const allAccounts = await window.ethereum.request({
          method: 'eth_requestAccounts',
        });
        await fetch('/api/v1/user_exists?public_address=' + allAccounts[0])
          .then((resp) => resp.json())
          .then(function(data) {
              if (!data['success']) {
                console.log('error checking user_exists!')
                return
              }
              console.log(data);
              nonce = data['nonce'];
          })

        const msg = 'Authentication request from SuchWowX app! Verifying message with nonce ' + nonce
        const signedData = await window.ethereum.request({
          method: 'personal_sign',
          params: [msg, allAccounts[0]]
        });
        console.log(`Signing data with msg "${msg}", address "${allAccounts[0]}", signed data: ${signedData}`)

        await fetch('/api/v1/authenticate/metamask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
          body: JSON.stringify({
            'signed_data': signedData,
            'public_address': allAccounts[0],
            'nonce': nonce,
            'message': msg,
          })
        })
          .then((resp) => resp.json())
          .then(function(data) {
              console.log(data);
              if (data['success']) {
                window.location.href = '/';
              }
          })
        }
    }
  };

  connectButton();
  if (MetaMaskOnboarding.isMetaMaskInstalled()) {
    window.ethereum.on('accountsChanged', (newAccounts) => {
      window.location.href = '/disconnect';
    });
  }
};
