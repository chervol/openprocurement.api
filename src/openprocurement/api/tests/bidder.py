# -*- coding: utf-8 -*-
import unittest

from openprocurement.api.tests.base import BaseTenderWebTest


class TenderBidderResourceTest(BaseTenderWebTest):

    def test_create_tender_bidder_invalid(self):
        request_path = '/tenders/{}/bidders'.format(self.tender_id)
        response = self.app.post(request_path, 'data', status=415)
        self.assertEqual(response.status, '415 Unsupported Media Type')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description':
                u"Content-Type header should be one of ['application/json']", u'location': u'header', u'name': u'Content-Type'}
        ])

        response = self.app.post(
            request_path, 'data', content_type='application/json', status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'No JSON object could be decoded',
                u'location': u'body', u'name': u'data'}
        ])

        response = self.app.post_json(request_path, 'data', status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Data not available',
                u'location': u'body', u'name': u'data'}
        ])

        response = self.app.post_json(
            request_path, {'not_data': {}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Data not available',
                u'location': u'body', u'name': u'data'}
        ])

        response = self.app.post_json(request_path, {'data': {
                                      'invalid_field': 'invalid_value'}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Rogue field', u'location':
                u'body', u'name': u'invalid_field'}
        ])

        response = self.app.post_json(request_path, {
                                      'data': {'bidders': [{'id': 'invalid_value'}]}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': {u'id': [
                u'Please use a mapping for this field or identifier instance instead of unicode.']}, u'location': u'body', u'name': u'bidders'}
        ])

        response = self.app.post_json(request_path, {
                                      'data': {'bidders': [{'id': {}}]}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'id'],
                u'location': u'body', u'name': u'bidders'}
        ])

        response = self.app.post_json(request_path, {'data': {'bidders': [{
                                      'id': {'name': 'name', 'uri': 'invalid_value'}}]}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'id'],
                u'location': u'body', u'name': u'bidders'}
        ])

    def test_post_tender_not_found(self):
        response = self.app.post_json('/tenders/some_id/bidders', {
                                      'data': {'bidders': [{'id': {'name': 'Name'}}]}}, status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

    def test_create_tender_bidder(self):
        response = self.app.post_json('/tenders/{}/bidders'.format(
            self.tender_id), {'data': {'bidders': [{'id': {'name': 'Name'}}]}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bidder = response.json['data']
        self.assertEqual(bidder['bidders'][0]['id']['name'], 'Name')
        self.assertTrue('id' in bidder)
        self.assertTrue(bidder['id'] in response.headers['Location'])

    def test_patch_tender_bidder(self):
        response = self.app.post_json('/tenders/{}/bidders'.format(
            self.tender_id), {'data': {'bidders': [{'id': {'name': 'Name'}}]}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bidder = response.json['data']

        response = self.app.patch_json('/tenders/{}/bidders/{}'.format(self.tender_id, bidder['id']), {"data": {"totalValue": {"amount": 600}}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["totalValue"]["amount"], 600)

        response = self.app.get('/tenders/{}/bidders/{}'.format(self.tender_id, bidder['id']))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["totalValue"]["amount"], 600)

        response = self.app.patch_json('/tenders/{}/bidders/some_id'.format(self.tender_id), {"data": {"totalValue": {"amount": 600}}}, status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'id'}
        ])

        response = self.app.patch_json('/tenders/some_id/bidders/some_id', {"data": {"totalValue": {"amount": 600}}}, status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

    def test_get_tender_bidder(self):
        response = self.app.post_json('/tenders/{}/bidders'.format(
            self.tender_id), {'data': {'bidders': [{'id': {'name': 'Name'}}]}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bidder = response.json['data']

        response = self.app.get('/tenders/{}/bidders/{}'.format(self.tender_id, bidder['id']))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data'], bidder)

        response = self.app.get('/tenders/{}/bidders/some_id'.format(self.tender_id), status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'id'}
        ])

        response = self.app.get('/tenders/some_id/bidders/some_id', status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

    def test_delete_tender_bidder(self):
        response = self.app.post_json('/tenders/{}/bidders'.format(
            self.tender_id), {'data': {'bidders': [{'id': {'name': 'Name'}}]}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bidder = response.json['data']

        response = self.app.delete('/tenders/{}/bidders/{}'.format(self.tender_id, bidder['id']))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data'], bidder)

        revisions = self.db.get(self.tender_id).get('revisions')
        self.assertEqual(revisions[0][u'changes'][0]['op'], u'add')
        self.assertEqual(revisions[-1][u'changes'][0], {u'path': u'/bids', u'op': u'remove'})

        response = self.app.delete('/tenders/{}/bidders/some_id'.format(self.tender_id), status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'id'}
        ])

        response = self.app.delete('/tenders/some_id/bidders/some_id', status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

    def test_get_tender_bidders(self):
        response = self.app.post_json('/tenders/{}/bidders'.format(
            self.tender_id), {'data': {'bidders': [{'id': {'name': 'Name'}}]}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bidder = response.json['data']

        response = self.app.get('/tenders/{}/bidders'.format(self.tender_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data'][0], bidder)

        response = self.app.get('/tenders/some_id/bidders', status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

class TenderBidderDocumentResourceTest(BaseTenderWebTest):

    def setUp(self):
        super(TenderBidderDocumentResourceTest, self).setUp()
        # Create bid
        response = self.app.post_json('/tenders/{}/bidders'.format(
            self.tender_id), {'data': {'bidders': [{'id': {'name': 'Name'}}]}})
        bid = response.json['data']
        self.bid_id = bid['id']

    def test_post_tender_not_found(self):
        response = self.app.post('/tenders/some_id/bidders/some_id/documents', status=404, upload_files=[
                                 ('upload', 'name.doc', 'content')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

    def test_post_tender_bid_not_found(self):
        response = self.app.post('/tenders/{}/bidders/some_id/documents'.format(self.tender_id), status=404, upload_files=[('upload', 'name.doc', 'content')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'bid_id'}
        ])

    def test_create_tender_bidder_document(self):
        response = self.app.post('/tenders/{}/bidders/{}/documents'.format(
            self.tender_id, self.bid_id), upload_files=[('upload', 'name.doc', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        # self.assertTrue('name.doc' in response.headers['Location'])
        self.assertTrue('name.doc' in response.json["documents"])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TenderBidderDocumentResourceTest))
    suite.addTest(unittest.makeSuite(TenderBidderResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
