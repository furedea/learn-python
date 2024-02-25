from typing import Protocol, Self, override, runtime_checkable


@runtime_checkable
class Expression(Protocol):
    def times(self, multiplier: int) -> "Expression":
        ...

    def plus(self, addend: "Expression") -> "Expression":
        ...

    def reduce(self, bank: "Bank", to: str) -> "Money":
        ...


class Sum:
    def __init__(self, augend: Expression, addend: Expression) -> None:
        self.augend = augend
        self.addend = addend

    def times(self, multiplier: int) -> "Expression":
        return Sum(self.augend.times(multiplier), self.addend.times(multiplier))

    def plus(self, addend: Expression) -> "Expression":
        return Sum(self, addend)

    def reduce(self, bank: "Bank", to: str) -> "Money":
        amount = self.augend.reduce(bank, to).amount + self.addend.reduce(bank, to).amount
        return Money(amount, to)


class Money:
    def __init__(self, amount: int, currency: str) -> None:
        self.amount = amount
        self.__currency = currency

    @override
    def __eq__(self, other: Self) -> bool:
        return self.amount == other.amount and self.__currency == other.__currency

    @classmethod
    def dollar(cls, amount: int) -> Self:
        return cls(amount, "USD")

    @classmethod
    def franc(cls, amount: int) -> Self:
        return cls(amount, "CHF")

    def currency(self) -> str:
        return self.__currency

    def times(self, multiplier: int) -> Expression:
        return Money(self.amount * multiplier, self.__currency)

    def plus(self, addend: Expression) -> Expression:
        return Sum(self, addend)

    def reduce(self, bank: "Bank", to: str) -> Self:
        rate = bank.rate(self.__currency, to)
        return Money(int(self.amount / rate), to)


class Bank:
    def __init__(self) -> None:
        self.__rates: dict["Pair", int] = {}

    def reduce(self, source: Expression, to: str) -> Money:
        return source.reduce(self, to)

    def add_rate(self, from_: str, to: str, rate: int) -> None:
        self.__rates[Pair(from_, to)] = rate

    def rate(self, from_: str, to: str) -> int:
        if from_ == to:
            return 1
        return self.__rates[Pair(from_, to)]


class Pair:
    def __init__(self, from_: str, to: str) -> None:
        self.from_ = from_
        self.to = to

    @override
    def __eq__(self, other: Self) -> bool:
        return self.from_ == other.from_ and self.to == other.to

    @override
    def __hash__(self) -> int:
        return 0
