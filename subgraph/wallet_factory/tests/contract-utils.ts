import { newMockEvent } from "matchstick-as"
import { ethereum, Address } from "@graphprotocol/graph-ts"
import { DeployedWallet } from "../generated/Contract/Contract"

export function createDeployedWalletEvent(
  owner: Address,
  walletAddress: Address
): DeployedWallet {
  let deployedWalletEvent = changetype<DeployedWallet>(newMockEvent())

  deployedWalletEvent.parameters = new Array()

  deployedWalletEvent.parameters.push(
    new ethereum.EventParam("owner", ethereum.Value.fromAddress(owner))
  )
  deployedWalletEvent.parameters.push(
    new ethereum.EventParam(
      "walletAddress",
      ethereum.Value.fromAddress(walletAddress)
    )
  )

  return deployedWalletEvent
}
