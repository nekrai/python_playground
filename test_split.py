import random
import unittest
import split_tests


def create_test_element(x, set_time): return {'name': 'test' + str(x), 'time': str(set_time())}


class TestInitTestList(unittest.TestCase):
    # def init_test_list(number_jobs)

    def test_init_test_list_one_job(self):
        # arrange
        t = split_tests.init_job_tests(0)
        expected = [t, t]
        # act
        res = split_tests.init_test_list(1)
        # assert
        self.assertEqual(expected, res)

    def test_init_test_list_five_jobs(self):
        # arrange
        t = split_tests.init_job_tests(0)
        expected = [t, t, t, t, t, t]
        # act
        res = split_tests.init_test_list(5)
        # assert
        self.assertEqual(expected, res)


class TestGetTotalTime(unittest.TestCase):
    # def get_total_time(test_list)

    def test_get_total_time_empty(self):
        # act
        res = split_tests.get_total_time([])
        # assert
        self.assertEqual(0.0, res)

    def test_get_total_time_single(self):
        # arrange
        test_list = [create_test_element(1, lambda : 5.0)]
        # act
        res = split_tests.get_total_time(test_list)
        # assert
        self.assertEqual(5.0, res)

    def test_get_total_time_multiple(self):
        # arrange
        test_list = [create_test_element(x, lambda : x) for x in range(5)]
        # act
        res = split_tests.get_total_time(test_list)
        # assert
        self.assertEqual(10.0, res)


class TestGetMinimalPosition(unittest.TestCase):
    # def get_minimal_position(test_list, number_jobs)

    def test_get_minimal_position_empty(self):
        # arrange
        # act
        # assert
        self.assertTrue(False)

    def test_get_minimal_position_single(self):
        # arrange
        # act
        # assert
        self.assertTrue(False)

    def test_get_minimal_position_many_beginning(self):
        # arrange
        # act
        # assert
        self.assertTrue(False)

    def test_get_minimal_position_many_middle(self):
        # arrange
        # act
        # assert
        self.assertTrue(False)

    def test_get_minimal_position_many_end(self):
        # arrange
        # act
        # assert
        self.assertTrue(False)


class TestFixTestList(unittest.TestCase):
    # def fix_test_list(test_list, number_jobs)

    def test_fix_test_list_empty(self):
        # arrange
        t = split_tests.init_job_tests(0)
        init_list = [t, t]
        final_list = [t, t]
        # act
        split_tests.fix_test_list(final_list, 1)
        # assert
        self.assertEqual(init_list, final_list)

    def test_fix_test_list_single_without_overload(self):
        # arrange
        testing_list = [(1, ['test1']), (0, [])]
        expected_list = [(1, ['test1']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 1)
        # assert
        self.assertEqual(expected_list, testing_list)

    def test_fix_test_list_multiple_without_overload(self):
        # arrange
        testing_list = [(1, ['test1']), (2, ['test2']), (3, ['test3']), (0, [])]
        expected_list = [(1, ['test1']), (2, ['test2']), (3, ['test3']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 3)
        # assert
        self.assertEqual(expected_list, testing_list)

    def test_fix_test_list_single_with_overload(self):
        # arrange
        testing_list = [(1, ['test1']), (2, ['test2'])]
        expected_list = [(3, ['test1', 'test2']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 1)
        # assert
        self.assertEqual(expected_list, testing_list)

    def test_fix_test_list_multiple_with_overload_first_slot(self):
        # arrange
        testing_list = [(1, ['test1']), (2, ['test2']), (3, ['test3']), (4, ['test4'])]
        expected_list = [(5, ['test1', 'test4']), (2, ['test2']), (3, ['test3']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 3)
        # assert
        self.assertEqual(expected_list, testing_list)

    def test_fix_test_list_multiple_with_overload_second_slot(self):
        # arrange
        testing_list = [(2, ['test2']), (1, ['test1']), (3, ['test3']), (4, ['test4'])]
        expected_list = [(2, ['test2']), (5, ['test1', 'test4']), (3, ['test3']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 3)
        # assert
        self.assertEqual(expected_list, testing_list)

    def test_fix_test_list_multiple_with_overload_third_slot(self):
        # arrange
        testing_list = [(2, ['test2']), (3, ['test3']), (1, ['test1']), (4, ['test4'])]
        expected_list = [(2, ['test2']), (3, ['test3']), (5, ['test1', 'test4']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 3)
        # assert
        self.assertEqual(expected_list, testing_list)


class TestSplitTests(unittest.TestCase):
    # def split_tests(test_list, number_jobs)

    def test_split_tests_empty(self):
        # arrange
        # act
        # assert
        self.assertTrue(False)

    def test_split_tests_one_test_single_job(self):
        # arrange
        # act
        # assert
        self.assertTrue(False)

    def test_split_tests_one_test_multiple_jobs(self):
        # arrange
        # act
        # assert
        self.assertTrue(False)

    def test_split_tests_many_tests_multiple_jobs(self):
        # arrange
        # act
        # assert
        self.assertTrue(False)

    def test_split_tests_preserve_test_list(self):
        # arrange
        # act
        # assert
        self.assertTrue(False)

    def test_split_tests_preserve_total_test_time(self):
        # arrange
        # act
        # assert
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()



