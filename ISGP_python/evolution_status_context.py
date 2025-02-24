from contextvars import ContextVar
import asyncio

# Create context variables
abort_flag: ContextVar[asyncio.Event] = ContextVar('abort_flag')
evolution_running: ContextVar[asyncio.Event] = ContextVar('evolution_running')

def set_context_vars():
    abort_flag.set(asyncio.Event())
    evolution_running.set(asyncio.Event())

def get_abort_flag() -> asyncio.Event:
    print('im getting here')
    print(abort_flag)
    return abort_flag.get()

def get_evolution_running() -> asyncio.Event:
    return evolution_running.get()