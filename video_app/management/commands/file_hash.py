import hashlib
from django.core.management.base import BaseCommand

# read only 1024 bytes at a time
BLOCK_SIZE  = 1024

class Command(BaseCommand):
    """
    Takes file-path as input and updates the file-name based on file-content
    by hashing it.

    e.g abc.txt -> abc-hashed124.txt
    """

    help = 'Take file path as input and rename the file with its content hash'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-f', '--file', type=str, help='')
        
        
    def handle(self, *args, **options):
        file_path = options['file']

        # make a hash object
        h = hashlib.sha1()

        # open file for reading in binary mode
        with open(file_path,'rb') as file:

            # loop till the end of the file
            chunk = 0
            while chunk != b'':
                chunk = file.read(BLOCK_SIZE)
                h.update(chunk)

        # return the hex representation of digest
        file_hash =  h.hexdigest()