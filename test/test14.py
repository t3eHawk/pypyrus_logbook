import logging
import pypyrus_logbook as logbook
import timeit


log = logbook.getlogger(file=True, filename='logbook')

smth = 'Something'
n = 100

def test_logbook():
    log.info(smth)
    pass

res_logbook = timeit.timeit(test_logbook, number=n)/n
print('Result logbook:', res_logbook)


logging.basicConfig(
    filename="logs/logging.log", level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

def test_logging():
    logging.info(smth)
    pass

res_logging = timeit.timeit(test_logging, number=n)/n
print('Result logging:', res_logging)
