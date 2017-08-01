# -*- coding: utf-8 -*-

import lxml
import lxml.etree
import requests


class PermanentSMSError(Exception):
    """
    Permanent SMS Error
    """


class TransientSMSError(Exception):
    """
    Transient SMS Error
    """


class AlpaSMSClient(object):

    perm_error = ('403', '408', '414')
    """
    403 - Invalid API key
    408 - Insufficient credits
    414 - Bloqued account
    """

    def __init__(self, key):
        self.key = key
        self.url = 'http://painel.smsalfa.com.br/%s'

    def send(self, tel, message, type_send=9):
        """
        Send sms with Alpa SMS Api.
        :param tel: int: national format phone number
        :param message: str: unicode base text
        :return: str: message sent id
        """
        url = self.url % 'send'
        params = {
            'number': tel,
            'msg': message,
            'type': type_send,
            'key': self.key
        }
        resp = requests.post(url, params)
        xml = lxml.etree.fromstring(resp.content)
        try:
            sent_id = xml.find('retorno').attrib['id']
        except KeyError:
            code = xml.find('retorno').attrib.get('codigo')
            if code in self.perm_error:
                raise PermanentSMSError('Response error code: %s' % code)
            else:
                raise TransientSMSError('Response error code: %s' % code)
        return sent_id

    def status(self, sms_id):
        """
        Return sms status by ID.
        :param sms_id: int: SMS Sent ID
        :return: str: Status sent
        """
        url = self.url % 'get'
        params = {
            'id': sms_id,
            'key': self.key,
            'action': 'status'
        }
        resp = requests.post(url, params)
        xml = lxml.etree.fromstring(resp.content)
        return xml.find('retorno').text