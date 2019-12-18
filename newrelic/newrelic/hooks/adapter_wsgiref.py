import newrelic.api.wsgi_application
import newrelic.api.in_function

def instrument_wsgiref_simple_server(module):

    def wrap_wsgi_application_entry_point(server, application,
                                          *args, **kwargs):
        application = newrelic.api.wsgi_application.WSGIApplicationWrapper(
                application)
        args = [server, application] + list(args)
        return (args, kwargs)

    newrelic.api.in_function.wrap_in_function(module,
            'WSGIServer.set_app', wrap_wsgi_application_entry_point)
