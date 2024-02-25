from typing import override


class TestResult:
    def __init__(self) -> None:
        self.run_count = 0
        self.error_count = 0

    def test_started(self) -> None:
        self.run_count += 1

    def test_failed(self) -> None:
        self.error_count += 1

    def summary(self) -> str:
        return f"{self.run_count} run, {self.error_count} failed"


class TestCase:
    def __init__(self, method_name: str) -> None:
        self.method_name = method_name

    def setup_method(self) -> None:
        pass

    def teardown_method(self) -> None:
        pass

    def run(self, result: TestResult) -> None:
        result.test_started()

        self.setup_method()
        method = getattr(self, self.method_name)
        try:
            method()
        except Exception:
            result.test_failed()
        self.teardown_method()


class WasRun(TestCase):
    @override
    def setup_method(self) -> None:
        self.log = "setup "

    def test_method(self) -> None:
        self.log += "test_method "

    def test_broken_method(self) -> None:
        raise Exception("broken")

    @override
    def teardown_method(self) -> None:
        self.log += "teardown "


class TestSuite:
    def __init__(self) -> None:
        self.tests: list[TestCase] = []

    def add(self, test: TestCase) -> None:
        self.tests.append(test)

    def run(self, result: TestResult) -> None:
        for test in self.tests:
            test.run(result)
