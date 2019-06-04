import pypyrus_logbook as logbook


log = logbook.getlogger(file=True)
smth = 'Something'
n = 100

def test_init():
    log = logbook.getlogger()
    pass

def test_config():
    log.configure(filename='{root.logger.name}.{root.logger.start_date:%Y%m%d}')
    pass

def test_head():
    log.head()
    pass

def test_info():
    log.info(smth)
    pass

def test_error():
    try:
        1/0
    except:
        log.error()
    pass

def test_empty_error():
    log.error()
    pass

def test_ooops():
    try:
        1/0
    except:
        log.error('Ooops')
    pass

rec_init = timeit.timeit(test_init, number=n)/n
res_config = timeit.timeit(test_config, number=n)/n
res_head = timeit.timeit(test_head, number=n)/n
res_info = timeit.timeit(test_info, number=n)/n
res_error = timeit.timeit(test_error, number=n)/n
res_empty_error = timeit.timeit(test_empty_error, number=n)/n
res_ooops = timeit.timeit(test_ooops, number=n)/n

print('Result of init:', res_config)
print('Result of config:', res_config)
print('Result of head:', res_head)
print('Result of info:', res_info)
print('Result of error:', res_error)
print('Result of empty error:', res_empty_error)
print('Result of ooops:', res_ooops)
