from collections import namedtuple

ErrorNode = namedtuple('ErrorNode',
        ['timestamp', 'type', 'message', 'span_id', 'stack_trace', 'custom_params',
        'file_name', 'line_number', 'source'])
