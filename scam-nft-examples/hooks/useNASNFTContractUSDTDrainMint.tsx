import { useAccount, useContractWrite, usePrepareContractWrite } from "wagmi";
import NASNFTContractUSDTDrainABI from "../abis/NASNFTContractUSDTDrain.sol/NASNFTContractUSDTDrain.json";
import { NASNFTContractUSDTDrain_ADDRESS } from "./constants";

/**
 * Hook to get NASNFTContractUSDTDrainABI using wagmi
 */
export const useNASNFTContractUSDTDrainMint = () => {
  return useContractWrite({
    abi: NASNFTContractUSDTDrainABI.abi,
    address: NASNFTContractUSDTDrain_ADDRESS,
    functionName: "mint",
  });
};
