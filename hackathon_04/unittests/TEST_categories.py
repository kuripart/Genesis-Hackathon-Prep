from hackathon_04.api.documents import *
import unittest

'''
As a first pass, all of these test whether a successful response is being
obtained by invoking the HTTP requests made from the API functions.

Further tests may be added after full access to the Genesys API
'''


class TestCategories(unittest.TestCase):

    def test_create_ctg(self):
        server_name = 'https://httpbin.org/post'
        url_suff = {"create_ctg": ''}
        payload_info_ctg = {"name": None,
                            "description": None}
        response_code = create_ctg(server_name, url_suff, payload_info_ctg, '', '')
        self.assertEqual(response_code, 200)

    def test_update_ctg(self):
        server_name = 'https://httpbin.org/put'
        url_suff = {"update_ctg": ''}
        response_code = update_ctg(server_name, url_suff, '', '', '')
        self.assertEqual(response_code, 200)

    def test_delete_ctg(self):
        server_name = 'https://httpbin.org/delete'
        url_suff = {"delete_ctg": ''}
        response_code = delete_ctg(server_name, url_suff, '', '', '')
        self.assertEqual(response_code, 200)

    def test_view_ctg(self):
        server_name = 'https://httpbin.org/get'
        url_suff = {"view_ctg": ''}
        response_list = view_ctg(server_name, url_suff, '', '')
        self.assertTrue(len(response_list) > 0)


if __name__ == '__main__':
    unittest.main()
