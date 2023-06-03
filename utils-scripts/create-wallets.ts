import { Wallet } from "ethers";


const main = () => {
  const wallet = Wallet.createRandom();

  console.log("wallet.address", wallet.address);
  console.log("wallet.privateKey", wallet.privateKey);
}

for (let i = 0; i < 20; i++) {
  console.log(`\n\nWallet ${i}`)
  main();
}