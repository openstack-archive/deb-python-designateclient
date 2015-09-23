# Copyright 2014 Hewlett-Packard Development Company, L.P.
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

import logging

from cliff import command
from cliff import lister
from cliff import show
import six

from designateclient import utils

LOG = logging.getLogger(__name__)


def _format_floatingip(fip):
    # Remove unneeded fields for display output formatting
    fip.pop('links', None)


class ListFloatingIPCommand(lister.Lister):
    """List floatingip ptr records"""

    columns = ['id', 'ptrdname', 'description', 'ttl']

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        cols = self.columns
        data = client.floatingips.list()
        return cols, (utils.get_item_properties(s, cols) for s in data)


class ShowFloatingIPCommand(show.ShowOne):
    """Show floatingip ptr record details"""

    def get_parser(self, prog_name):
        parser = super(ShowFloatingIPCommand, self).get_parser(prog_name)

        parser.add_argument('floatingip_id', help="Floating IP ID")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns
        data = client.floatingips.get(parsed_args.floatingip_id)
        _format_floatingip(data)
        return zip(*sorted(six.iteritems(data)))


class SetFloatingIPCommand(show.ShowOne):
    """Set floatingip ptr record"""

    def get_parser(self, prog_name):
        parser = super(SetFloatingIPCommand, self).get_parser(prog_name)

        parser.add_argument('floatingip_id', help="Floating IP ID")
        parser.add_argument('ptrdname', help="PTRD Name")

        description_group = parser.add_mutually_exclusive_group()
        description_group.add_argument('--description', help="Description")
        description_group.add_argument('--no-description', action='store_true')

        ttl_group = parser.add_mutually_exclusive_group()
        ttl_group.add_argument('--ttl', type=int, help="TTL")
        ttl_group.add_argument('--no-ttl', action='store_true')

        return parser

    def take_action(self, parsed_args):
        data = {}

        if parsed_args.no_description:
            data['description'] = None
        elif parsed_args.description:
            data['description'] = parsed_args.description

        if parsed_args.no_ttl:
            data['ttl'] = None
        elif parsed_args.ttl:
            data['ttl'] = parsed_args.ttl

        client = self.app.client_manager.dns

        fip = client.floatingips.set(
            parsed_args.floatingip_id,
            parsed_args.ptrdname,
            parsed_args.description,
            parsed_args.ttl)

        _format_floatingip(fip)
        return zip(*sorted(six.iteritems(fip)))


class UnsetFloatingIPCommand(command.Command):
    """Unset floatingip ptr record"""

    def get_parser(self, prog_name):
        parser = super(UnsetFloatingIPCommand, self).get_parser(prog_name)

        parser.add_argument('floatingip_id', help="Floating IP ID")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns
        client.floatingips.unset(parsed_args.floatingip_id)
        LOG.info('FloatingIP PTR %s was unset' % parsed_args.floatingip_id)
