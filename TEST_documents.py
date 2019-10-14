from documents import *
import unittest

'''
As a first pass, all of these test whether a successful response is being
obtained by invoking the HTTP requests made from the API functions.

Further tests may be added after full access to the Genesys API
'''


class TestCategories(unittest.TestCase):

    def test_upload_doc(self):
        server_name = 'https://httpbin.org/post'
        url_suff = {"upload_doc": ''}
        doc_payload = {"question": "",
                       "answer": "",
                       "alternatives": ""}
        response_code = upload_doc(server_name, url_suff, '', '', doc_payload, {})
        self.assertEqual(response_code, 200)

    def test_mod_docs(self):
        server_name = 'https://httpbin.org/patch'
        url_suff = {"mod_docs": ''}
        doc_payloads = [{"question": "", "answer": "", "alternatives": ""},
                        {"question": "", "answer": "", "alternatives": ""},
                        {"question": "", "answer": "", "alternatives": ""}]
        responses = mod_docs(server_name, url_suff, '', '', doc_payloads, {})
        self.assertEqual(len(responses), len(doc_payloads))

    def test_update_doc(self):
        server_name = 'https://httpbin.org/put'
        url_suff = {"update_doc": ''}
        doc_payload = {"question": "",
                       "answer": "",
                       "alternatives": ""}
        response_code = update_doc(server_name, url_suff, '', '', doc_payload, '', {})
        self.assertTrue(response_code, 200)

    def test_view_doc(self):
        server_name = 'https://httpbin.org/get'
        url_suff = {"view_doc": ''}
        response_list = view_doc(server_name, url_suff, '', '', '')
        self.assertTrue(len(response_list), 1)

    def test_view_docs(self):
        server_name = 'https://httpbin.org/get'
        url_suff = {"view_docs": ''}
        response_list = view_docs(server_name, url_suff, '', '')
        self.assertTrue(len(response_list) > 0)

    def test_delete_doc(self):
        server_name = 'https://httpbin.org/delete'
        url_suff = {"delete_doc": ''}
        response_code = delete_doc(server_name, url_suff, '', '', '')
        self.assertEqual(response_code, 200)


if __name__ == '__main__':
    unittest.main()
