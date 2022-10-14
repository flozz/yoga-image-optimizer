import sys
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

    def __init__(self, *args, **kwargs):
        self._state_manager = multiprocessing.Manager()
        ProcessPoolExecutor.__init__(self, *args, **kwargs)

    def shutdown(self, *args, **kwargs):
        processes = self._processes

        # Python < 3.9: We should wait else we got an OSError:
        # https://bugs.python.org/issue36281
        if sys.version_info.major >= 3 and sys.version_info.minor < 9:
            kwargs["wait"] = True

        for pid, process in processes.items():
            process.kill()
        ProcessPoolExecutor.shutdown(self, *args, **kwargs)
        self._state_manager.shutdown()

    shutdown.__doc__ = ProcessPoolExecutor.shutdown.__doc__

    def submit(self, fn, *args, **kwargs):
        is_running = self._state_manager.Value(bool, False)
        future = ProcessPoolExecutor.submit(
            self,
            functools.partial(_callable_wrapper, is_running, fn),
            *args,
            **kwargs,
        )
        # Monkey patch future.running to return the real running state
        future.running = functools.partial(_future_running_override, future, is_running)
        return future

    submit.__doc__ = ProcessPoolExecutor.submit.__doc__
