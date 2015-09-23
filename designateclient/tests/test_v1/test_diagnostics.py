# Copyright 2015 NEC Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
from mock import patch

from designateclient.tests import test_v1
from designateclient.v1 import diagnostics


class TestDiagnostics(test_v1.APIV1TestCase, test_v1.CrudMixin):

    @patch.object(diagnostics.DiagnosticsController, "ping")
    def test_ping(self, ping):
        args = mock.MagicMock()
        args.service = "foo"
        args.host = "host1"
        self.client.diagnostics.ping(args.host, args.service)
        self.client.diagnostics.ping.assert_called_with("host1", "foo")
