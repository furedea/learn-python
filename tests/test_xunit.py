from src import xunit


class TestTestCase:
    def setup_method(self) -> None:
        self.result = xunit.TestResult()

    def test_template_method(self) -> None:
        test = xunit.WasRun("test_method")
        test.run(self.result)
        assert test.log == "setup test_method teardown "

    def test_result(self) -> None:
        test = xunit.WasRun("test_method")
        test.run(self.result)
        assert self.result.summary() == "1 run, 0 failed"

    def test_failed_result_formatting(self) -> None:
        self.result.test_started()
        self.result.test_failed()
        assert self.result.summary() == "1 run, 1 failed"

    def test_failed_result(self) -> None:
        test = xunit.WasRun("test_broken_method")
        test.run(self.result)
        assert self.result.summary() == "1 run, 1 failed"

    def test_suite(self) -> None:
        suite = xunit.TestSuite()
        suite.add(xunit.WasRun("test_method"))
        suite.add(xunit.WasRun("test_broken_method"))
        suite.run(self.result)
        assert self.result.summary() == "2 run, 1 failed"

    def test_failed_teardown(self) -> None:
        test = xunit.WasRun("test_broken_method")
        test.run(self.result)
        assert test.log == "setup teardown "

    # TODO: setup_methodのエラーをキャッチして出力する


if __name__ == "__main__":
    test = xunit.WasRun("test_method")
    print(test.log)
    result = xunit.TestResult()
    test.run(result)
    print(test.log)
