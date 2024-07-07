from pb_api import PrivatBankAPI


class CurrencyExchange:
    def __init__(self):
        self.api = PrivatBankAPI()

    async def get_exchange_rates(self, start_date, end_date, currencies):
        return await self.api.get_exchange_rates(start_date, end_date, currencies)
