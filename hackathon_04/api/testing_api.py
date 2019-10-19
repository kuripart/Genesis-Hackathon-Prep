from HTTPRequest import HTTPRequest
from suffix_keys import url_suff as suff
import kbase

if __name__ == '__main__':
    q = HTTPRequest('A', 'B')
    kbase.create_kbase('a', 's', 'a')