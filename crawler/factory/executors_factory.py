from concurrent import futures

executor = futures.ThreadPoolExecutor(20)


def get_thread_executor():
    return executor
