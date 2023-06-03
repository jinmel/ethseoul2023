import httpx
import numpy as np


class EtherScan:
    API_TOKEN = 'SESUP58TEEY2NZYQ7M9KVZ98GXXUNFBAKN'
    UNIX_TIME_DENOMINATOR = 60
    SCALE = 1e+18

    def __init__(self, address, base_url='https://api.etherscan.io/api'):
        self.address = address
        self.base_url = base_url

    async def _set_normal_transaction_features(self):
        async with httpx.AsyncClient() as client:
            result  = await client.get(
                self.base_url +
                '?module=account' +
                '&action=txlist' +
                '&address=' + self.address +
                '&startblock=0' +
                '&endblock=99999999' +
                '&sort=asc' +
                '&apikey=' + self.API_TOKEN)
            self.__normal_transactions_json = result.json()
            result = await client.get(
                self.base_url +
                '?module=account'
                '&action=balance'
                '&address=' + self.address +
                '&tag=latest' +
                '&apikey=' + self.API_TOKEN)
            self.__balance_json = result.json()
        sent_tnxs = [obj for obj in self.__normal_transactions_json["result"] if obj.get("from") == self.address]
        received_tnxs = [obj for obj in self.__normal_transactions_json["result"] if obj.get("to") == self.address]
        self.sent_tnx = len(sent_tnxs)
        self.received_tnx = len(received_tnxs)
        contract_tnxs = [obj for obj in self.__normal_transactions_json["result"] if obj.get("to") == ""]
        self.avg_min_between_sent_tnx = np.mean(np.diff([int(obj.get("timeStamp")) for obj in sent_tnxs])) / self.UNIX_TIME_DENOMINATOR if self.sent_tnx != 0 else 0
        self.avg_min_between_received_tnx = np.mean(np.diff([int(obj.get("timeStamp")) for obj in received_tnxs])) / self.UNIX_TIME_DENOMINATOR if self.sent_tnx != 0 else 0
        self.time_diff_between_first_and_last = (max(int(obj.get("timeStamp")) for obj in self.__normal_transactions_json["result"]) - min(int(obj.get("timeStamp")) for obj in self.__normal_transactions_json["result"])) / self.UNIX_TIME_DENOMINATOR
        self.number_of_created_contracts = len([obj for obj in self.__normal_transactions_json["result"] if obj.get("to") == ""])
        self.max_value_received = max([int(obj.get("value")) for obj in received_tnxs]) / self.SCALE if len(received_tnxs) != 0 else 0
        self.avg_val_received = np.average([int(obj.get("value")) for obj in received_tnxs]) / self.SCALE if self.received_tnx != 0 else 0
        self.avg_val_sent = np.average([int(obj.get("value")) for obj in sent_tnxs]) / self.SCALE if self.sent_tnx != 0 else 0
        self.min_value_sent_to_contract = min([int(obj.get("value")) for obj in contract_tnxs]) / self.SCALE if len(contract_tnxs) != 0 else 0
        self.total_ether_sent = sum([int(obj.get("value")) for obj in sent_tnxs]) / self.SCALE
        self.total_ether_balance = int(self.__balance_json["result"]) / self.SCALE

    async def _set_erc_features(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                self.base_url +
                '?module=account' +
                '&action=tokentx' +
                '&address=' + self.address +
                '&startblock=0' +
                '&endblock=27025780' +
                '&sort=asc' +
                '&apikey=' + self.API_TOKEN)

        self.__erc20s_json = r.json()

        unique_sent_addr = set()
        unique_token_name = set()

        for obj in self.__erc20s_json["result"]:
            unique_sent_addr.add(obj.get("to"))
        for obj in self.__erc20s_json["result"]:
            unique_token_name.add(obj.get("tokenName"))
        self.erc20_total_ether_received = sum([int(obj.get("value")) for obj in self.__erc20s_json["result"] if obj.get("to") == self.address]) / self.SCALE
        self.erc20_total_ether_sent = sum([int(obj.get("value")) for obj in self.__erc20s_json["result"] if obj.get("from") == self.address]) / self.SCALE
        self.erc20_total_ether_sent_contract = sum([int(obj.get("value")) for obj in self.__erc20s_json["result"] if obj.get("contractAddress") != ""]) / self.SCALE
        self.erc20_uniq_sent_addr = len(unique_sent_addr)
        self.erc20_uniq_rec_token_name = len(unique_token_name)

    async def get_features_list(self):
        await self._set_normal_transaction_features()
        await self._set_erc_features()
        return [
            self.avg_min_between_sent_tnx,
            self.avg_min_between_received_tnx,
            self.time_diff_between_first_and_last,
            self.sent_tnx,
            self.received_tnx,
            self.number_of_created_contracts,
            self.max_value_received,
            self.avg_val_received,
            self.avg_val_sent,
            self.total_ether_sent,
            self.total_ether_balance,
            self.erc20_total_ether_received,
            self.erc20_total_ether_sent,
            self.erc20_total_ether_sent_contract,
            self.erc20_uniq_sent_addr,
            self.erc20_uniq_rec_token_name
        ]
