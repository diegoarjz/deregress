from unittest import mock

def mock_for_all_tests(test_case, patch):
    patcher = mock.patch(patch)
    mocked = patcher.start()
    test_case.addCleanup(patcher.stop)
    return mocked
