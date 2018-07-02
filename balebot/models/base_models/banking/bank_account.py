import json as json_handler

from balebot.models.constants.errors import Error


class BankAccount:
    def __init__(self, account_number, branch_code, open_date, rate, available_balance,
                 last_money_transfer_date, first_name, last_name):

        self._account_number = str(account_number)
        self._branch_code = int(branch_code)
        self._open_date = str(open_date)
        self._rate = int(rate)
        self._available_balance = str(available_balance)
        self._last_money_transfer_date = str(last_money_transfer_date)
        self._first_name = str(first_name)
        self._last_name = str(last_name)

    def get_json_object(self):
        data = {
            "accountNumber": self._account_number,
            "branchCode": self._branch_code,
            "openDate": self._open_date,
            "rate": self._rate,
            "availableBalance": self._available_balance,
            "lastMoneyTransferDate": self._last_money_transfer_date,
            "firstName": self._first_name,
            "lastName": self._last_name,

        }
        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())

    @classmethod
    def load_from_json(cls, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)

        account_number = json_dict.get('accountNumber', None)
        branch_code = json_dict.get('branchCode', None)
        open_date = json_dict.get('openDate', None)
        rate = json_dict.get('rate', None)
        available_balance = json_dict.get('availableBalance', None)
        last_money_transfer_date = json_dict.get('lastMoneyTransferDate', None)
        first_name = json_dict.get('firstName', None)
        last_name = json_dict.get('lastName', None)

        if (not account_number) or (branch_code is None) or (not open_date) or (rate is None) \
                or (available_balance is None) or (not last_money_transfer_date) \
                or (not first_name) or (not last_name):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(account_number=account_number, branch_code=branch_code, open_date=open_date,
                   rate=rate, available_balance=available_balance,
                   last_money_transfer_date=last_money_transfer_date,
                   first_name=first_name, last_name=last_name)
