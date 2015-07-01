# Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# Author: Endre Karlson <endre.karlson@hp.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from designateclient import client
from designateclient.v2 import utils as v2_utils


class ZoneController(client.Controller):
    def create(self, name, type_=None, email=None, description=None, ttl=None,
               masters=None):
        type_ = type_ or "PRIMARY"

        data = {
            "name": name,
            "type": type_
        }

        if type_ == "PRIMARY":
            data["email"] = email

            if ttl is not None:
                data["ttl"] = ttl

        elif type_ == "SECONDARY":
            data["masters"] = masters

        if description is not None:
            data["description"] = description

        return self._post('/zones', data=data)

    def list(self, criterion=None, marker=None, limit=None):
        url = self.build_url('/zones', criterion, marker, limit)

        return self._get(url, response_key="zones")

    def get(self, zone):
        zone = v2_utils.resolve_by_name(self.list, zone)

        return self._get('/zones/%s' % zone)

    def update(self, zone, values):
        zone = v2_utils.resolve_by_name(self.list, zone)

        url = self.build_url('/zones/%s' % zone)

        return self._patch(url, data=values)

    def delete(self, zone):
        zone = v2_utils.resolve_by_name(self.list, zone)

        url = self.build_url('/zones/%s' % zone)

        return self._delete(url)

    def abandon(self, zone):
        zone = v2_utils.resolve_by_name(self.list, zone)

        url = '/zones/%s/tasks/abandon' % zone

        self.client.session.post(url)

    def axfr(self, zone):
        zone = v2_utils.resolve_by_name(self.list, zone)

        url = '/zones/%s/tasks/axfr' % zone

        self.client.session.post(url)


class ZoneTransfersController(client.Controller):
    def create_request(self, zone, target_project_id, description=None):
        zone = v2_utils.resolve_by_name(self.client.zones.list, zone)

        data = {
            "target_project_id": target_project_id
        }

        if description is not None:
            data["description"] = description

        url = '/zones/%s/tasks/transfer_requests' % zone

        return self._post(url, data=data)

    def get_request(self, transfer_id):
        url = '/zones/tasks/transfer_requests/%s' % transfer_id
        return self._get(url)

    def list_requests(self):
        url = '/zones/tasks/transfer_requests'
        return self._get(url, response_key="transfer_requests")

    def update_request(self, transfer_id, values):
        url = '/zones/tasks/transfer_requests/%s' % transfer_id
        return self._patch(url, data=values)

    def delete_request(self, transfer_id):
        url = '/zones/tasks/transfer_requests/%s' % transfer_id
        self._delete(url)

    def accept_request(self, transfer_id, key):
        url = '/zones/tasks/transfer_accepts'

        data = {
            "key": key,
            "zone_transfer_request_id": transfer_id
        }
        return self._post(url, data=data)

    def get_accept(self, accept_id):
        url = '/zones/tasks/transfer_accepts/%s' % accept_id
        return self._get(url)
