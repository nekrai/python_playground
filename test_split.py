import unittest
import split_tests
import random


def create_test_element(x, set_time): return {'name': 'test' + str(x), 'time': str(set_time())}


class TestInitTestList(unittest.TestCase):

    def test_less_than_one_job(self):
        # act
        obtained = split_tests.init_test_list(0)
        # assert
        self.assertEqual([], obtained)

    def test_one_job(self):
        # arrange
        t = split_tests.init_job_tests(0)
        expected = [t, t]
        # act
        obtained = split_tests.init_test_list(1)
        # assert
        self.assertEqual(expected, obtained)

    def test_five_jobs(self):
        # arrange
        t = split_tests.init_job_tests(0)
        expected = [t, t, t, t, t, t]
        # act
        obtained = split_tests.init_test_list(5)
        # assert
        self.assertEqual(expected, obtained)


class TestGetTotalTime(unittest.TestCase):
    # def get_total_time(test_list)

    def test_empty_list(self):
        # act
        obtained = split_tests.get_total_time([])
        # assert
        self.assertEqual(0.0, obtained)

    def test_single_element(self):
        # arrange
        test_list = [create_test_element(1, lambda: 5.0)]
        # act
        obtained = split_tests.get_total_time(test_list)
        # assert
        self.assertEqual(5.0, obtained)

    def test_multiple_elements(self):
        # arrange
        test_list = [create_test_element(x, lambda: x) for x in range(5)]
        # act
        obtained = split_tests.get_total_time(test_list)
        # assert
        self.assertEqual(10.0, obtained)


class TestGetMinimalPosition(unittest.TestCase):
    # def get_minimal_position(test_list, number_jobs)

    def test_number_is_greater_than_1(self):
        # act
        obtained = split_tests.get_minimal_position([(1, []), (1, [])], 0)
        # assert
        self.assertEqual(-3, obtained)

    def test_empty_list(self):
        # act
        obtained = split_tests.get_minimal_position([], 1)
        # assert
        self.assertEqual(-1, obtained)

    def test_single_element(self):
        # arrange
        testing_list = [(0, [])]
        # act
        obtained = split_tests.get_minimal_position(testing_list, 1)
        # assert
        self.assertEqual(-2, obtained)

    def test_minimal_in_beginning(self):
        # arrange
        testing_list = [(1, []), (2, []), (3, []), (4, []), (0, [])]
        # act
        obtained = split_tests.get_minimal_position(testing_list, 4)
        # assert
        self.assertEqual(0, obtained)

    def test_minimal_in_middle(self):
        # arrange
        testing_list = [(2, []), (1, []), (3, []), (4, []), (0, [])]
        # act
        obtained = split_tests.get_minimal_position(testing_list, 4)
        # assert
        self.assertEqual(1, obtained)

    def test_minimal_in_end(self):
        # arrange
        testing_list = [(3, []), (2, []), (1, []), (4, []), (0, [])]
        # act
        obtained = split_tests.get_minimal_position(testing_list, 4)
        # assert
        self.assertEqual(2, obtained)


class TestFixTestList(unittest.TestCase):
    # def fix_test_list(test_list, number_jobs)

    def test_empty_list(self):
        # arrange
        init_list = []
        final_list = []
        # act
        split_tests.fix_test_list(final_list, 1)
        # assert
        self.assertEqual(init_list, final_list)

    def test_exception_short_list(self):
        # arrange
        t = split_tests.init_job_tests(0)
        testing_list = [t]
        num_jobs = 1
        # assert
        with self.assertRaises(Exception) as context:
            split_tests.fix_test_list(testing_list, num_jobs)

        self.assertTrue('Invalid arguments' in context.exception)

    def test_exception_too_many_jobs(self):
        # arrange
        t = split_tests.init_job_tests(0)
        testing_list = [t, t]
        num_jobs = 5
        # assert
        with self.assertRaises(Exception) as context:
            split_tests.fix_test_list(testing_list, num_jobs)

        self.assertTrue('Invalid arguments' in context.exception)

    def test_single_without_overload(self):
        # arrange
        testing_list = [(1, ['test1']), (0, [])]
        expected_list = [(1, ['test1']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 1)
        # assert
        self.assertEqual(expected_list, testing_list)

    def test_single_with_overload(self):
        # arrange
        testing_list = [(1, ['test1']), (2, ['test2'])]
        expected_list = [(3, ['test1', 'test2']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 1)
        # assert
        self.assertEqual(expected_list, testing_list)

    def test_multiple_without_overload(self):
        # arrange
        testing_list = [(1, ['test1']), (2, ['test2']), (3, ['test3']), (0, [])]
        expected_list = [(1, ['test1']), (2, ['test2']), (3, ['test3']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 3)
        # assert
        self.assertEqual(expected_list, testing_list)

    def test_multiple_with_overload_first_slot(self):
        # arrange
        testing_list = [(1, ['test1']), (2, ['test2']), (3, ['test3']), (4, ['test4'])]
        expected_list = [(5, ['test1', 'test4']), (2, ['test2']), (3, ['test3']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 3)
        # assert
        self.assertEqual(expected_list, testing_list)

    def test_multiple_with_overload_second_slot(self):
        # arrange
        testing_list = [(2, ['test2']), (1, ['test1']), (3, ['test3']), (4, ['test4'])]
        expected_list = [(2, ['test2']), (5, ['test1', 'test4']), (3, ['test3']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 3)
        # assert
        self.assertEqual(expected_list, testing_list)

    def test_multiple_with_overload_third_slot(self):
        # arrange
        testing_list = [(2, ['test2']), (3, ['test3']), (1, ['test1']), (4, ['test4'])]
        expected_list = [(2, ['test2']), (3, ['test3']), (5, ['test1', 'test4']), (0, [])]
        # act
        split_tests.fix_test_list(testing_list, 3)
        # assert
        self.assertEqual(expected_list, testing_list)

    def test_single_test_goes_for_first_job(self):
        # arrange
        t = split_tests.init_job_tests(0)
        testing_list = [t, t, (1, ['test1']), t]
        expected_list = [(1, ['test1']), t, t, t]
        # act
        split_tests.fix_test_list(testing_list, 3)
        # assert
        self.assertEqual(expected_list, testing_list)


class TestSplitTests(unittest.TestCase):
    # def split_tests(test_list, number_jobs)

    def test_empty_list(self):
        # act
        obtained = split_tests.split_tests([], 1)
        # assert
        self.assertEqual([], obtained)

    def test_one_test_single_job(self):
        # arrange
        test_list = [create_test_element(1, lambda: 5.0)]
        # act
        obtained = split_tests.split_tests(test_list, 1)
        # assert
        self.assertEqual([(5, ['test1']), (0, [])], obtained)

    def test_one_test_multiple_jobs(self):
        # arrange
        test_list = [create_test_element(1, lambda: 5.0)]
        # act
        obtained = split_tests.split_tests(test_list, 2)
        # assert
        self.assertEqual([(5, ['test1']), (0, []), (0, [])], obtained)

    def test_many_tests_multiple_jobs(self):
        # arrange
        test_list = [create_test_element(x, lambda: x) for x in range(5)]
        expected = [(3.0, ['test0', 'test1', 'test2']), (3.0, ['test3']), (4.0, ['test4']), (0, [])]
        # act
        obtained = split_tests.split_tests(test_list, 3)
        # assert
        self.assertEqual(expected, obtained)

    def test_split_guarantees_balance(self):
        import numpy
        max_run_time = 50

        test_list = [
            create_test_element(x, lambda: random.randint(1, max_run_time))
            for x in xrange(1000)
        ]

        # act
        obtained = split_tests.split_tests(test_list, 3)[:-1]
        standard_deviation = numpy.std([job[0] for job in obtained])

        # assert
        self.assertLessEqual(standard_deviation, max_run_time)

    def test_split_guarantees_order(self):
        # arrange
        test_list = [
            create_test_element(1, lambda: 2),
            create_test_element(2, lambda: 4),
            create_test_element(3, lambda: 1),
            create_test_element(4, lambda: 3),
            create_test_element(5, lambda: 1),
            create_test_element(6, lambda: 5),
            create_test_element(7, lambda: 2),
            create_test_element(8, lambda: 4),
            create_test_element(9, lambda: 1),
            create_test_element(10, lambda: 3),
            create_test_element(11, lambda: 2),
            create_test_element(12, lambda: 5),
            create_test_element(13, lambda: 1),
            create_test_element(14, lambda: 3),
            create_test_element(15, lambda: 5),
            create_test_element(16, lambda: 5),
            create_test_element(17, lambda: 2),
            create_test_element(18, lambda: 4),
            create_test_element(19, lambda: 1),
            create_test_element(20, lambda: 2)
        ]

        expected = [
            (18.0, ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7']),
            (16.0, ['test8', 'test9', 'test10', 'test11', 'test12', 'test13']),
            (22.0, ['test14', 'test15', 'test16', 'test17', 'test18', 'test19', 'test20']),
            (0, [])
        ]

        # act

        obtained = split_tests.split_tests(test_list, 3)

        # assert
        self.assertEqual(expected, obtained)

    def test_preserves_test_list(self):
        # arrange
        test_list = [create_test_element(x, lambda: random.uniform(1, 10)) for x in range(100)]
        tests_names_expected = [test.values()[0] for test in test_list].sort()
        # act
        obtained = split_tests.split_tests(test_list, 5)
        tests_names_obtained = [test_name for test in obtained for test_name in test[1]].sort()
        # assert
        self.assertEqual(tests_names_expected, tests_names_obtained)

    def test_preserves_total_test_time(self):
        # arrange
        test_list = [create_test_element(x, lambda: random.uniform(1, 10)) for x in range(100)]
        total_time_expected = int(sum([float(test.values()[1]) for test in test_list])*1000)/1000.0
        # act
        obtained = split_tests.split_tests(test_list, 5)
        total_time_obtained = int(sum([float(test[0]) for test in obtained])*1000)/1000.0
        # assert
        self.assertEqual(total_time_expected, total_time_obtained)


if __name__ == '__main__':
    unittest.main()
