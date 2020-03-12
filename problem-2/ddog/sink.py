import abc
import logging


class SinkFactory:
    def __init__(self, output):
        self.output = output

    def build_sink(self):
        if self.output == 'console':
            return ConsoleSink()
        else:
            return LocalFileSystemSink(path=self.output)


class Sink(abc.ABC):
    def write(self, triples):
        pass


def preprocess_triples(func):
    def wrapper(self, triples):
        if triples:
            sorted_triples = sorted(triples, key=lambda x: x[1], reverse=True)
            formatted_triples = ['Team triple: {} - Count: {:d}'.format('|'.join(triple), count)
                                 for triple, count in sorted_triples]
            func(self, formatted_triples)
        else:
            logging.warning('No triple fulfilled the minimum count over the requested range')
            logging.warning('No results were written to the requested output sink')

    return wrapper


class ConsoleSink(Sink):
    @preprocess_triples
    def write(self, triples):
        for triple in triples:
            print(triple)


class LocalFileSystemSink(Sink):
    def __init__(self, path):
        self.path = path

    @preprocess_triples
    def write(self, triples):
        with open(self.path, 'w') as file_obj:
            file_obj.write('\n'.join(triples))
