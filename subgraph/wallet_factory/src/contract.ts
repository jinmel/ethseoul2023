import { DeployedWallet as DeployedWalletEvent } from "../generated/Contract/Contract"
import { DeployedWallet } from "../generated/schema"

export function handleDeployedWallet(event: DeployedWalletEvent): void {
  let entity = new DeployedWallet(
    event.transaction.hash.concatI32(event.logIndex.toI32())
  )
  entity.owner = event.params.owner
  entity.walletAddress = event.params.walletAddress

  entity.blockNumber = event.block.number
  entity.blockTimestamp = event.block.timestamp
  entity.transactionHash = event.transaction.hash

  entity.save()
}
