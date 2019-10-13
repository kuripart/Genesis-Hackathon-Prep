from kbase import *
import unittest

'''
As a first pass, all of these test whether a successful response is being
obtained by invoking the HTTP requests made from the API functions.

Further tests may be added after full access to the Genesys API
'''

class TestKbase(unittest.TestCase):

    def test_create_kbase(self):
        server_name = 'https://httpbin.org/post'
        url_suff = {"create_kbase": ''}
        payload_info = {"name": None,
                        "description": None,
                        "coreLanguage": "en-US"}
        kbase_responses = {}
        response = create_kbase(server_name, url_suff, payload_info, kbase_responses)
        self.assertEqual(response['status_code'], 200)

    def test_update_kbase(self):
        server_name = 'https://httpbin.org/put'
        url_suff = {"update_kbase": ''}
        response = update_kbase(server_name, url_suff, '')
        self.assertEqual(response['status_code'], 200)

    def test_delete_kbase(self):
        server_name = 'https://httpbin.org/delete'
        url_suff = {"delete_kbase": ''}
        response = delete_kbase(server_name, url_suff, '')
        self.assertEqual(response['status_code'], 200)


if __name__ == '__main__':
    unittest.main()
