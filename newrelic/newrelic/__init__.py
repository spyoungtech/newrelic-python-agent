version = '5.2.2'

try:
    from newrelic.build import build_number
except ImportError:
    build_number = 0

version_info = list(map(int, version.split('.'))) + [build_number]
version = '.'.join(map(str, version_info))
