import functools

from newrelic.common.async_wrapper import async_wrapper
from newrelic.api.time_trace import TimeTrace, current_trace
from newrelic.common.object_names import callable_name
from newrelic.common.object_wrapper import FunctionWrapper, wrap_object
from newrelic.core.function_node import FunctionNode


class FunctionTrace(TimeTrace):

    def __init__(self, name, group=None, label=None,
            params=None, terminal=False, rollup=None, **kwargs):
        parent = None
        if kwargs:
            if len(kwargs) > 1:
                raise TypeError("Invalid keyword arguments:", kwargs)
            parent = kwargs['parent']
        super(FunctionTrace, self).__init__(parent)

        # Deal with users who use group wrongly and add a leading
        # slash on it. This will cause an empty segment which we
        # want to avoid. In that case insert back in Function as
        # the leading segment.

        group = group or 'Function'

        if group.startswith('/'):
            group = 'Function' + group

        self.name = name
        self.group = group
        self.label = label

        self.params = params

        self.terminal = terminal
        self.rollup = terminal and rollup or None

    def __enter__(self):
        result = TimeTrace.__enter__(self)
        if not self.should_record_segment_params:
            self.params = None
        return result

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict(
                name=self.name, group=self.group, label=self.label,
                params=self.params, terminal=self.terminal,
                rollup=self.rollup))

    def terminal_node(self):
        return self.terminal

    def create_node(self):
        return FunctionNode(
                group=self.group,
                name=self.name,
                children=self.children,
                start_time=self.start_time,
                end_time=self.end_time,
                duration=self.duration,
                exclusive=self.exclusive,
                label=self.label,
                params=self.params,
                rollup=self.rollup,
                guid=self.guid,
                agent_attributes=self.agent_attributes,
                user_attributes=self.user_attributes)


def FunctionTraceWrapper(wrapped, name=None, group=None, label=None,
            params=None, terminal=False, rollup=None):

    def dynamic_wrapper(wrapped, instance, args, kwargs):
        wrapper = async_wrapper(wrapped)
        if not wrapper:
            parent = current_trace()
            if not parent:
                return wrapped(*args, **kwargs)
        else:
            parent = None

        if callable(name):
            if instance is not None:
                _name = name(instance, *args, **kwargs)
            else:
                _name = name(*args, **kwargs)

        elif name is None:
            _name = callable_name(wrapped)

        else:
            _name = name

        if callable(group):
            if instance is not None:
                _group = group(instance, *args, **kwargs)
            else:
                _group = group(*args, **kwargs)

        else:
            _group = group

        if callable(label):
            if instance is not None:
                _label = label(instance, *args, **kwargs)
            else:
                _label = label(*args, **kwargs)

        else:
            _label = label

        if callable(params):
            if instance is not None:
                _params = params(instance, *args, **kwargs)
            else:
                _params = params(*args, **kwargs)

        else:
            _params = params

        trace = FunctionTrace(_name, _group, _label, _params,
                terminal, rollup, parent=parent)

        if wrapper:
            return wrapper(wrapped, trace)(*args, **kwargs)

        with trace:
            return wrapped(*args, **kwargs)

    def literal_wrapper(wrapped, instance, args, kwargs):
        wrapper = async_wrapper(wrapped)
        if not wrapper:
            parent = current_trace()
            if not parent:
                return wrapped(*args, **kwargs)
        else:
            parent = None

        _name = name or callable_name(wrapped)

        trace = FunctionTrace(_name, group, label, params,
                terminal, rollup, parent=parent)

        if wrapper:
            return wrapper(wrapped, trace)(*args, **kwargs)

        with trace:
            return wrapped(*args, **kwargs)

    if (callable(name) or callable(group) or callable(label) or
            callable(params)):
        return FunctionWrapper(wrapped, dynamic_wrapper)

    return FunctionWrapper(wrapped, literal_wrapper)


def function_trace(name=None, group=None, label=None, params=None,
        terminal=False, rollup=None):
    return functools.partial(FunctionTraceWrapper, name=name,
            group=group, label=label, params=params, terminal=terminal,
            rollup=rollup)


def wrap_function_trace(module, object_path, name=None,
        group=None, label=None, params=None, terminal=False, rollup=None):
    return wrap_object(module, object_path, FunctionTraceWrapper,
            (name, group, label, params, terminal, rollup))
