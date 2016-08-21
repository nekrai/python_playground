def init_job_tests(_): return 0, []


def init_test_list(number_jobs): return map(init_job_tests, range(number_jobs + 1))


def get_total_time(test_list):
    return sum([float(single_test['time']) for single_test in test_list])


def get_minimal_position(test_list, number_jobs):
    return test_list.index(min(test_list[:number_jobs]))


def fix_test_list(test_list, number_jobs):
    last_pos_time, last_pos_list = test_list[number_jobs]
    if last_pos_time != 0:
        min_pos = get_minimal_position(test_list, number_jobs)

        min_pos_time, min_pos_list = test_list[min_pos]
        min_pos_list.extend(last_pos_list)

        test_list[min_pos] = min_pos_time + last_pos_time, min_pos_list
        test_list[number_jobs] = 0, []


def split_tests(test_list, number_jobs):
    final_test_list = init_test_list(number_jobs)
    total_time = get_total_time(test_list)
    average_time_per_job = total_time / number_jobs

    current_job_time = 0
    current_job = 0

    for single_test in test_list:
        test_name = single_test['name']
        test_time = float(single_test['time'])
        current_job_time += test_time
        if current_job_time <= average_time_per_job:
            current_test_list = final_test_list[current_job][1]
        else:
            current_job += 1
            current_job_time = test_time
            current_test_list = []
        current_test_list.append(test_name)
        final_test_list[current_job] = current_job_time, current_test_list

    fix_test_list(final_test_list, number_jobs)

    return final_test_list

