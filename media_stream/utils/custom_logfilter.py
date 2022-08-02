import logging

class IPAddressFilter(logging.Filter):

    def filter(self, record):
        if hasattr(record, 'request'):
            record.ip = record.request.getpeername()[0]
            
        return True
