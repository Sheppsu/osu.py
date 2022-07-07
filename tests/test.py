from osu import Client
import os
import importlib
import traceback
import sys


class BaseTest:
    test_name: str

    def __init__(self, client: Client):
        self.client = client
        self.passed = True

    def test(self, func, *args, **kwargs):
        print(f"Testing {self.test_name}.{func.__name__}...")
        try:
            result = func(*args, **kwargs)
            print(f"Testing for {self.test_name}.{func.__name__} passed.")
            return result
        except:
            print(f"Testing for {self.test_name}.{func.__name__} failed.")
            self.passed = False
            traceback.print_exc()

    def run_all_tests(self):
        raise NotImplementedError()


class Test:
    def __init__(self):
        self.client = Client.from_client_credentials(
            int(os.getenv('osu_client_id')), os.getenv('osu_client_secret'),
            'http://127.0.0.1:8080'
        )

    def run_test(self, test):
        test = importlib.import_module(f'test_{test}').Test(self.client)
        print(f"Running {test.test_name} test...")
        test.run_all_tests()
        print(f"{test.test_name} test finished.")
        return test.passed

    def run_all_tests(self) -> bool:
        passed = True
        for test in os.listdir():
            if test.startswith('test_') and test.endswith('.py'):
                result = self.run_test(test[:-3])
                if passed and not result:
                    passed = False
        print("Testing finished.")
        return passed


if __name__ == '__main__':
    if len(sys.argv) == 1:
        passed = Test().run_all_tests()
    else:
        passed = Test().run_test(sys.argv[1])
    print("Testing failed." if not passed else "Testing passed!")
