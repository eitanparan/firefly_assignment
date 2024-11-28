import logging


class Logger:
    """
    A class for modifying native python logger with formatting, colors
    """

    def __init__(self, logger_name='Logger', log_level='DEBUG', verbose=True, color_logs=True):
        """

        :param logger_name: the name of the instansiated logger
        :param log_level:
        :param verbose: currently not in use. should indicate weather DEBUG log level messages will be printed or not
        :param color_logs: if True, then logs will be colored by log level, if not, logs will not be colored.
                           this is for avoiding seeing the special characters printed in the jenkins and allure reports
                           such as [0m (for reset) ect...
        """
        log_name_max_length = 25
        spaces = int(log_name_max_length - len(logger_name))
        formatter = (f'%(asctime)s   [%(levelname)-12s]   %(name)-5s {int(spaces) * " "} '
                     f'%(message)s [%(filename)s:%(lineno)d]')
        self.custom_formatter = CustomFormatter(formatter)
        self.add_success_level()
        self.add_notification_level()

        self.verbose = verbose
        self.log_level = log_level
        self.verbose = True
        self.color_logs = color_logs
        self.logger_name = logger_name
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(getattr(logging, self.log_level))

        self.ch = logging.StreamHandler()
        self.ch.setLevel(getattr(logging, self.log_level))

        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.ch)
        self.ch.setFormatter(self.custom_formatter)
        self.logger.propagate = False

    def add_success_level(self):
        """

        """
        try:
            level_name = 'SUCCESS'
            level_value = 21
            logging.addLevelName(level_value, level_name)

            def success(self, msg, *args, **kwargs):
                if self.isEnabledFor(level_value):
                    self.log(level_value, msg, *args, **kwargs)

            self.success = success
            setattr(logging, level_name, level_value)
            setattr(logging.getLoggerClass(), level_name.lower(), success)
            self.custom_formatter.formats[logging.SUCCESS] = (self.custom_formatter.LIGHT_GREEN +
                                                              self.custom_formatter.fmt + self.custom_formatter.reset)
        except Exception as err:
            raise Exception(f"failed adding log level {level_name}: {err}")

    def add_notification_level(self):
        """
        """
        try:
            level_name = 'NOTIFICATION'
            level_value = 22
            logging.addLevelName(level_value, level_name)

            def notification(self, msg, *args, **kwargs):
                if self.isEnabledFor(level_value):
                    self.log(level_value, msg, *args, **kwargs)

            self.notification = notification
            setattr(logging, level_name, level_value)
            setattr(logging.getLoggerClass(), level_name.lower(), notification)
            self.custom_formatter.formats[logging.NOTIFICATION] = (self.custom_formatter.PURPLE +
                                                                   self.custom_formatter.fmt +
                                                                   self.custom_formatter.reset)
        except Exception as err:
            raise Exception(f"failed adding log level {level_name}: {err}")

        # Log level order:
        # NOTSET = 0.
        # DEBUG = 10.
        # INFO = 20.
        # WARN = 30.
        # ERROR = 40.
        # CRITICAL = 50


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    green = "\033[0;32m"

    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

    def __init__(self, fmt, color_logs=True):
        super().__init__()
        self.color_logs = color_logs
        self.fmt = fmt
        if self.color_logs:
            self.formats = {
                logging.DEBUG: self.grey + self.fmt + self.reset,
                logging.INFO: self.blue + self.fmt + self.reset,
                logging.WARNING: self.yellow + self.fmt + self.reset,
                logging.ERROR: self.LIGHT_RED + self.fmt + self.reset,
                logging.CRITICAL: self.bold_red + self.fmt + self.reset

                # logging.NOTSET: self.PURPLE + self.fmt + self.reset
            }
        else:
            self.formats = {
                logging.DEBUG: self.fmt,
                logging.INFO: self.fmt,
                logging.WARNING: self.fmt,
                logging.ERROR: self.fmt,
                logging.CRITICAL: self.fmt

                # logging.NOTSET: self.PURPLE + self.fmt + self.reset
            }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)