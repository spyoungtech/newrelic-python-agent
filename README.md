This is an **unofficial** export of the
[New Relic Python agent](https://docs.newrelic.com/docs/agents/python-agent)
source, extracted from the [package on PyPI](https://pypi.python.org/pypi/newrelic).

Ideally New Relic would provide their own repository (even if it didn't accept pull
requests), especially given that the source is freely available on PyPI. However they
[do not wish to do so](https://discuss.newrelic.com/t/hosting-the-python-agent-on-github/27878)
at the current time.

This repo is used for:
* generating diffs between each agent version, when deciding risk of upgrading (I'll
add tags for each release)
* debugging issues seen when using the agent and clarifying behaviour in cases where
the docs are unclear (without having to download and extract the archive from PyPI
for the umpteenth time)
* providing a way to link to specific lines in the source when reporting issues to New Relic

It must not be used for:
* installation of the agent (use the package from PyPI or the New Relic servers instead)
* opening pull requests (I have no connection with New Relic)
* anything that violates the agent's [LICENSE agreement](newrelic/newrelic/LICENSE)

If you have problems with the agent, report issues directly to New Relic by either
[opening a ticket](https://support.newrelic.com/tickets/new) or posting to the
[discussion forum](https://discuss.newrelic.com/c/python-agent).
