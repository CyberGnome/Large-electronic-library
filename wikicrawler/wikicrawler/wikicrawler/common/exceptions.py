# -*- coding: utf-8 -*-


class CrawlException(Exception):
    FILE_ALREADY_EXISTS = 1
    FILE_DOSNT_FIT = 2

    def __init__(self, message, errors, saved_data=None):
        super(CrawlException, self).__init__(message)

        # Now for your custom code...
        self.errors = errors
        self.saved_data = saved_data
