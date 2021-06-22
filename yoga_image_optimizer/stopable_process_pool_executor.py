from concurrent.futures import ProcessPoolExecutor


class StopableProcessPoolExecutor(ProcessPoolExecutor):
    """A concurrent.futures.ProcessPoolExecutor that kills running processes on
    shutdown.
    """

    def shutdown(self, *args, **kwargs):
        processes = self._processes
        ProcessPoolExecutor.shutdown(self, *args, **kwargs)
        for pid, process in processes.items():
            process.kill()

    shutdown.__doc__ = ProcessPoolExecutor.shutdown.__doc__
