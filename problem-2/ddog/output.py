"""
This modules gathers all the classes and functions dedicated to the outputting of the computed triples.
"""
import abc
import logging

import ddog.constants as csts

HEADER = 'Team triple         Count\n-------------------------'


class SinkFactory:
    """This factory class builds and returns the appropriate `Sink` object based on its `output` attribute.

    Attributes:
        output (str): Describes the destination for the computed results. Parsed from the command line argument
        `csts.CONSOLE_SINK_NAME`. Either `csts.CONSOLE_SINK_NAME` or a path on the local file system.
    """
    def __init__(self, output):
        """ Initializes the `SinkFactory` object.

        Args:
            output (str): Cf. class docstring.
        """
        self.output = output

    def build_sink(self):
        """ Builds and returns the appropriate `Sink` object based on the `output` instance attribute.

        Returns:
             Sink: The `Sink` object that encapsulates the specific writing logic associated with the chosen
             destination.
        """
        if self.output == csts.CONSOLE_SINK_NAME:
            return ConsoleSink()
        else:
            return LocalFileSystemSink(path=self.output)


class Sink(abc.ABC):
    """ Abstract base class that defines the interface contract each `Sink` class must implement.
    """
    def write(self, triples):
        """ Abstract method the implementation of which must contain the logic needed to write a list of triples to a
        given destination.

        Args:
            triples (list[(frozenset, int)]): List of (baseball team triple, player count) tuples.
        """
        pass


def preprocess_triples(func):
    """ Decorator function. Decorates `Sink.write` methods. Gather all the logic dedicated to the formatting of baseball
    team triples.

    Args:
        func (function): Function/method to be decorated. Must have a `self` and a `triples` argument.

    Returns:
        function: The decorated `func` function.
    """
    def wrapper(self, triples):
        if triples:
            sorted_triples = sorted(triples, key=lambda x: x[1], reverse=True)
            formatted_triples = ['{triple:}, {count:d}'.format(triple='|'.join(sorted(triple)), count=count)
                                 for triple, count in sorted_triples]
            func(self, formatted_triples)
        else:
            logging.warning('No triple fulfilled the minimum count over the requested range')
            logging.warning('No results were written to the requested output sink')

    return wrapper


class ConsoleSink(Sink):
    """ Concrete implementation of `Sink` that allows to write baseball triples to the standard output.
    """
    @preprocess_triples
    def write(self, triples):
        """ Concrete implementation of `Sink.write` that allows to write baseball triples to the standard output.

        Args:
            triples (list[str]): List of formatted (baseball team triple, player count) tuples.
        """
        print(HEADER)
        for triple in triples:
            print(triple)


class LocalFileSystemSink(Sink):
    """ Concrete implementation of `Sink` that allows to write baseball triples into a text file on the local file
    system.

    Attributes:
          path (str): Path of the target text file. The directory structure must exist.
    """
    def __init__(self, path):
        """ Initializes the `LocalFileSystemSink` object.

        Args:
            path (str): Cf. class docstring.
        """
        self.path = path

    @preprocess_triples
    def write(self, triples):
        """ Concrete implementation of `Sink.write` that allows to write baseball triples into a text file on the local
        file system.

        Args:
            triples (list[str]): List of formatted (baseball team triple, player count) tuples.
        """
        with open(self.path, 'w') as file_obj:
            logging.info('Writing results to {path:}'.format(path=self.path))
            file_obj.write('\n'.join([HEADER] + triples))
