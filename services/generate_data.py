import requests
import numpy as np


class Features:
    API_TOKEN = 'SESUP58TEEY2NZYQ7M9KVZ98GXXUNFBAKN'
    UNIX_TIME_DENOMINATOR = 60
    SCALE = 1e+18

    def __init__(self, address):
        self.address = address
        self.__set_normal_transaction_features()
        self.__set_erc_features()
        self.feature_dict = {
            'Avg min between sent tnx': self.avg_min_between_sent_tnx,
            'Avg min between received tnx': self.avg_min_between_received_tnx,
            'Time Diff between first and last (Mins)': self.time_diff_between_first_and_last,
            'Sent tnx': self.sent_tnx,
            'Received Tnx': self.received_tnx,
            'Number of Created Contracts': self.number_of_created_contracts,
            'max value received ': self.max_value_received,
            'avg val received': self.avg_val_received,
            'avg val sent': self.avg_val_sent,
            'min value sent to contract': self.min_value_sent_to_contract,
            'total Ether sent': self.total_ether_sent,
            'total ether balance': self.total_ether_balance,
            ' ERC20 total Ether received': self.erc20_total_ether_received,
            ' ERC20 total ether sent': self.erc20_total_ether_sent,
            ' ERC20 total Ether sent contract': self.erc20_total_ether_sent_contract,
            ' ERC20 uniq sent addr': self.erc20_uniq_sent_addr,
            ' ERC20 uniq sent addr.1': self.erc20_uniq_sent_addr,
            ' ERC20 uniq rec token name': self.erc20_uniq_rec_token_name
        }

    def __set_normal_transaction_features(self):
        self.__normal_transactions_json = requests.get(
            'https://api.etherscan.io/api' +
            '?module=account' +
            '&action=txlist' +
            '&address=' + self.address +
            '&startblock=0' +
            '&endblock=99999999' +
            '&sort=asc' +
            '&apikey=' + self.API_TOKEN).json()
        self.__balance_json = requests.get(
            'https://api.etherscan.io/api' +
            '?module=account'
            '&action=balance'
            '&address=' + self.address +
            '&tag=latest' +
            '&apikey=' + self.API_TOKEN).json()
        sent_tnxs = [obj for obj in self.__normal_transactions_json["result"] if obj.get("from") == self.address]
        received_tnxs = [obj for obj in self.__normal_transactions_json["result"] if obj.get("to") == self.address]
        contract_tnxs = [obj for obj in self.__normal_transactions_json["result"] if obj.get("to") == ""]
        self.avg_min_between_sent_tnx = np.mean(np.diff([int(obj.get("timeStamp")) for obj in sent_tnxs])) / self.UNIX_TIME_DENOMINATOR
        self.avg_min_between_received_tnx = np.mean(np.diff([int(obj.get("timeStamp")) for obj in received_tnxs])) / self.UNIX_TIME_DENOMINATOR
        self.time_diff_between_first_and_last = (max(int(obj.get("timeStamp")) for obj in self.__normal_transactions_json["result"]) - min(int(obj.get("timeStamp")) for obj in self.__normal_transactions_json["result"])) / self.UNIX_TIME_DENOMINATOR
        self.sent_tnx = len(sent_tnxs)
        self.received_tnx = len(received_tnxs)
        self.number_of_created_contracts = len([obj for obj in self.__normal_transactions_json["result"] if obj.get("to") == ""])
        self.max_value_received = max([int(obj.get("value")) for obj in received_tnxs]) / self.SCALE if len(received_tnxs) != 0 else 0
        self.avg_val_received = np.average([int(obj.get("value")) for obj in received_tnxs]) / self.SCALE
        self.avg_val_sent = np.average([int(obj.get("value")) for obj in sent_tnxs]) / self.SCALE
        self.min_value_sent_to_contract = min([int(obj.get("value")) for obj in contract_tnxs]) / self.SCALE if len(contract_tnxs) != 0 else 0
        self.total_ether_sent = sum([int(obj.get("value")) for obj in sent_tnxs]) / self.SCALE
        self.total_ether_balance = int(self.__balance_json["result"]) / self.SCALE

    def __set_erc_features(self):
        self.__erc20s_json = requests.get(
            'https://api.etherscan.io/api' +
            '?module=account' +
            '&action=tokentx' +
            '&address=' + self.address +
            '&startblock=0' +
            '&endblock=27025780' +
            '&sort=asc' +
            '&apikey=' + self.API_TOKEN).json()
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

    def get_features_dict(self):
        return self.feature_dict

    def get_feature(self, feature_name):
        return self.feature_dict[feature_name]

    def get_features_value_list(self):
        return list(self.feature_dict.values())


# example
features = Features('0x00062d1dd1afb6fb02540ddad9cdebfe568e0d89')
print(features.get_features_dict())
print(features.get_feature(' ERC20 uniq rec token name'))
print(features.get_features_value_list())
