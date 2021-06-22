import functools
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures._base import RUNNING


def _callable_wrapper(is_running, fn, *args, **kwargs):
    is_running.value = True
    fn(*args, **kwargs)
    is_running.value = False


def _future_running_override(future, is_running):
    return future._state == RUNNING and is_running.value


class StoppableProcessPoolExecutor(ProcessPoolExecutor):
    """A concurrent.futures.ProcessPoolExecutor that kills running processes on
    shutdown.

    This also fix the wrong running state of futures. See
    https://bugs.python.org/issue37276
    """

    def shutdown(self, *args, **kwargs):
        processes = self._processes
        ProcessPoolExecutor.shutdown(self, *args, **kwargs)
        for pid, process in processes.items():
            process.kill()

    shutdown.__doc__ = ProcessPoolExecutor.shutdown.__doc__

    def submit(self, fn, *args, **kwargs):
        is_running = multiprocessing.Manager().Value(bool, False)
        future = ProcessPoolExecutor.submit(
            self,
            functools.partial(_callable_wrapper, is_running, fn),
            *args,
            **kwargs,
        )
        # Monkey patch future.running to return the real running state
        future.running = functools.partial(
            _future_running_override, future, is_running
        )
        return future

    submit.__doc__ = ProcessPoolExecutor.submit.__doc__
