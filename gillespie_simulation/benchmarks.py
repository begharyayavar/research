from typing import Any,Callable
from prints import print_benchmark,print_storage
from functools import wraps
from time import perf_counter
import inspect
import sys
def benchmark(func: Callable) -> Callable:
    
    @wraps(func)
    def wrapper(*args: Any,**kwargs: Any) -> Any:
        t_start = perf_counter()
        value = func(*args,**kwargs)
        t_end = perf_counter()
        print_benchmark(func,t_end-t_start,*args,**kwargs)
        return value
    return wrapper

def benchmark_profiler(func: Callable) -> Callable:
    
    @wraps(func)
    def wrapper(*args: Any,**kwargs: Any) -> Any:
        new_args = []
        parameters = enumerate(inspect.signature(func).parameters)
        numerical_parameters = {parameter[1]:args[parameter[0]] for parameter in parameters if parameter[1].annotation == int}
        print("printing parameters")
        print((numerical_parameters))
        
        # numerical_parameters = 
        t_start = perf_counter()
        value = func(*args,**kwargs)
        t_end = perf_counter()
        print_benchmark(func,t_end-t_start,*args,**kwargs)
        return value
    return wrapper

@benchmark_profiler
def f(a: int,b: int,s: str) -> str:
    return s

f(1,2,"hi")
def storage(func: Callable) -> Callable:
    
    @wraps(func)
    def wrapper(*args: Any,**kwargs: Any) -> Any:
        parameters = inspect.signature(func).parameters
        storage_values = {  parameter[1]:sys.getsizeof(args[parameter[0]]) \
                                for parameter in enumerate(parameters)}
        value = func(*args,**kwargs)
        t_end = perf_counter()
        print_storage(func,storage_values)
        return value
    return wrapper

