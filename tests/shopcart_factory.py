"""
Test Factory to make fake objects for testing
"""
from datetime import datetime
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Shopcart, ShopcartItem


class ShopcartFactory(factory.Factory):
    """ Creates fake shopcarts """

    class Meta:
        model = Shopcart

    id = factory.Sequence(lambda n: n)
    user_id = FuzzyChoice(choices=[1, 2, 100, 101, 200, 250, 400])
    #create time fields in db
    #create_time = datetime.isoformat(datetime.now())
    #update_time = datetime.isoformat(datetime.now())

class ShopcartItemFactory(factory.Factory):
    """ Creates fake shopcart items """

    class Meta:
        model = ShopcartItem

    id = factory.Sequence(lambda n: n)
    sid = FuzzyChoice(choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    sku = FuzzyChoice(choices=[1000, 2000, 3000, 4000, 5000, 6000, 7000])
    name = FuzzyChoice(choices=["soap", "iron", "microwave", "printer", "boots", "laptop"])
    price = FuzzyChoice(choices=[2.39, 5.99, 20.99, 45.99, 99.98, 100.00, 205.36])
    amount = FuzzyChoice(choices=[1, 2, 3, 5, 10])
    #create time fields in db
    create_time = datetime.isoformat(datetime.now())
    update_time = datetime.isoformat(datetime.now())




if __name__ == "__main__":
    for _ in range(10):
        shopcart = ShopcartFactory()
        print(shopcart.serialize())
    for _ in range(10):
        shopcart_item = ShopcartItemFactory()
        print(shopcart_item.serialize())
        