import datetime

# ct stores current time
ct = str(datetime.datetime.now())


def log_error(error):
    with open('./error_log.txt', 'r+', encoding='UTF-8') as file:
        file.writelines(ct)
        file.writelines("\n")
        file.writelines(getattr(error, 'message', repr(error)))
        file.writelines('\n---------------------------------------------------------\n')
