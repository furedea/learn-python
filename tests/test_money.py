from src import money


class TestMoney:
    # TODO: Moneyの丸め処理
    # TODO: hashableかどうか　ハッシュテーブルのキーとして使えるようにする
    # TODO: nullとの等価性比較
    # TODO: 他のオブジェクトとの等価性比較

    def test_multiplication(self) -> None:
        five_dollars: money.Money = money.Money.dollar(5)
        assert five_dollars.times(2) == money.Money.dollar(10)
        assert five_dollars.times(3) == money.Money.dollar(15)

    def test_equality(self) -> None:
        assert money.Money.dollar(5) == money.Money.dollar(5)
        assert money.Money.dollar(5) != money.Money.dollar(6)
        assert money.Money.dollar(5) != money.Money.franc(5)

    def test_currency(self) -> None:
        assert money.Money.dollar(1).currency() == "USD"
        assert money.Money.franc(1).currency() == "CHF"

    def test_simple_addition(self) -> None:
        five_dollars = money.Money.dollar(5)
        sum_expr = five_dollars.plus(five_dollars)
        bank = money.Bank()
        reduced = bank.reduce(sum_expr, "USD")
        assert reduced == money.Money.dollar(10)

    def test_plus_returns_sum(self) -> None:
        five = money.Money.dollar(5)
        sum_expr = five.plus(five)
        assert sum_expr.augend == five
        assert sum_expr.addend == five

    def test_reduce_sum(self) -> None:
        sum_expr = money.Sum(money.Money.dollar(3), money.Money.dollar(4))
        bank = money.Bank()
        seven_dollars = bank.reduce(sum_expr, "USD")
        assert seven_dollars == money.Money.dollar(7)

    def test_reduce_money(self) -> None:
        bank = money.Bank()
        reduced = bank.reduce(money.Money.dollar(1), "USD")
        assert reduced == money.Money.dollar(1)

    def test_reduce_money_different_currency(self) -> None:
        bank = money.Bank()
        bank.add_rate("CHF", "USD", 2)
        result = bank.reduce(money.Money.franc(2), "USD")
        assert result == money.Money.dollar(1)

    def test_identity_rate(self) -> None:
        assert money.Bank().rate("USD", "USD") == 1

    def test_mixed_addition(self) -> None:
        five_dollars = money.Money.dollar(5)
        ten_francs = money.Money.franc(10)
        bank = money.Bank()
        bank.add_rate("CHF", "USD", 2)
        ten_dollars = bank.reduce(five_dollars.plus(ten_francs), "USD")
        assert ten_dollars == money.Money.dollar(10)

    def test_sum_plus_money(self) -> None:
        five_dollars = money.Money.dollar(5)
        ten_francs = money.Money.franc(10)
        bank = money.Bank()
        bank.add_rate("CHF", "USD", 2)
        sum_expr = money.Sum(five_dollars, ten_francs).plus(five_dollars)
        reduced = bank.reduce(sum_expr, "USD")
        assert reduced == money.Money.dollar(15)

    def test_sum_times(self) -> None:
        five_dollars = money.Money.dollar(5)
        ten_francs = money.Money.franc(10)
        bank = money.Bank()
        bank.add_rate("CHF", "USD", 2)
        sum_expr = money.Sum(five_dollars, ten_francs).times(2)
        reduced = bank.reduce(sum_expr, "USD")
        assert reduced == money.Money.dollar(20)
