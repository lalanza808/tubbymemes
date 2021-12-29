async function getSignedData(publicAddress, jsonData) {
  const signedData = await window.ethereum.request({
    method: 'eth_signTypedData_v3',
    params: [publicAddress, JSON.stringify(jsonData)]
  });
  console.log(signedData);
  return signedData
}
