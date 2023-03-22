from Database import Database
from dataclasses import dataclass, field
from math import ceil, sqrt


@dataclass
class Luxury:
    lux_name: str
    points: int
    bid_value: int = field(repr=True)
    item_price: int = field(repr=True)
    warehouse_cost: float = field(init=False)
    price_x1: float = field(init=False, repr=True)
    price_x10: float = field(init=False, repr=True)
    ppp_x1: float = field(init=False, repr=True)
    ppp_x10: float = field(init=False, repr=True)

    def __post_init__(self):
        if self.lux_name != 'Painting':
            self.warehouse_cost = Luxury.calc_warehouse_cost(self.bid_value)
            bid_price = self.item_price * self.bid_value * 1.05
        else:
            self.warehouse_cost = 0
            bid_price = self.item_price * self.bid_value

        coefficient_price = 1_000_000_000_000
        self.price_x1 = bid_price + self.warehouse_cost
        self.price_x10 = bid_price * 10 + self.warehouse_cost
        coefficient_ppp = 100_000
        self.ppp_x1 = round(self.price_x1 / self.points / coefficient_ppp)
        self.ppp_x10 = round(self.price_x10 / (self.points * 10) / coefficient_ppp)
        self.price_x1 = round(self.price_x1 / coefficient_price, 3)
        self.price_x10 = round(self.price_x10 / coefficient_price, 3)
        self.warehouse_cost = round(self.warehouse_cost / coefficient_price, 3)

    @staticmethod
    def calc_warehouse_cost(volume):
        x = ceil(sqrt(2 * volume) / 100)
        return 10000 * round(41.6666666 * x ** 3 - 62.5 * x ** 2 + 20.8333333 * x)


if __name__ == '__main__':
    db = Database()
    lst = db.select(
        table='auctions',
        select='a.lux_name, sum(bid_value), sum(points), count(a.lux_name), item_price',
        join='items',
        group_by='lux_name')
    dct = {row[0]: (round(row[1]/row[3]), round(row[2]/row[3]), row[4]) for row in lst}
    luxuries = []
    for lux_name, properties in dct.items():
        luxuries.append(Luxury(lux_name, properties[1], properties[0], properties[2]))
    for x in luxuries:
        print(x)
        db.update(
            table='luxuries',
            values=f'points = {x.points}, price_x1 = {x.price_x1}, price_x10 = {x.price_x10}, '
                   f'ppp_x1 = {x.ppp_x1}, ppp_x10 = {x.ppp_x10}, warehouse_cost = {x.warehouse_cost}',
            where=f'lux_name = "{x.lux_name}"'
        )
