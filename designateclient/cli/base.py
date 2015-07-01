# Copyright 2012 Managed I.T.
#
# Author: Kiall Mac Innes <kiall@managedit.ie>
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
import abc

from cliff.command import Command as CliffCommand
from cliff.lister import Lister
from cliff.show import ShowOne
from keystoneclient import exceptions as ks_exceptions
import six

from designateclient import exceptions
from designateclient import utils
from designateclient.v1 import Client


@six.add_metaclass(abc.ABCMeta)
class Command(CliffCommand):
    def run(self, parsed_args):
        self.client = Client(
            region_name=self.app.options.os_region_name,
            service_type=self.app.options.os_service_type,
            session=self.app.session,
            all_tenants=self.app.options.all_tenants,
            edit_managed=self.app.options.edit_managed)

        try:
            return super(Command, self).run(parsed_args)
        except exceptions.RemoteError as e:
            columns = ['Code', 'Type']
            values = [e.code, e.type]

            if e.message:
                columns.append('Message')
                values.append(e.message)

            if e.errors:
                columns.append('Errors')
                values.append(e.errors)

            self.error_output(parsed_args, columns, values)
        except ks_exceptions.EndpointNotFound:
            self.app.log.error("No endpoint was found. Missing credentials?")

            return 1

    def error_output(self, parsed_args, column_names, data):
        self.formatter.emit_one(column_names,
                                data,
                                self.app.stdout,
                                parsed_args)
        self.app.log.error('The requested action did not complete '
                           'successfully')

    @abc.abstractmethod
    def execute(self, parsed_args):
        """
        Execute something, this is since we overload self.take_action()
        in order to format the data

        This method __NEEDS__ to be overloaded!

        :param parsed_args: The parsed args that are given by take_action()
        """

    def post_execute(self, data):
        """
        Format the results locally if needed, by default we just return data

        :param data: Whatever is returned by self.execute()
        """
        return data

    def take_action(self, parsed_args):
        results = self.execute(parsed_args)
        return self.post_execute(results)

    def find_resourceid_by_name_or_id(self, resource_plural, name_or_id):
        resource_client = getattr(self.client, resource_plural)
        return utils.find_resourceid_by_name_or_id(resource_client, name_or_id)


class ListCommand(Command, Lister):
    columns = None

    def post_execute(self, results):
        if len(results) > 0:
            columns = self.columns or utils.get_columns(results)
            data = [utils.get_item_properties(i, columns) for i in results]
            return columns, data
        else:
            return [], ()


class GetCommand(Command, ShowOne):
    def post_execute(self, results):
        return results.keys(), results.values()


class CreateCommand(Command, ShowOne):
    def post_execute(self, results):
        return results.keys(), results.values()


class UpdateCommand(Command, ShowOne):
    def post_execute(self, results):
        return results.keys(), results.values()


class DeleteCommand(Command, ShowOne):
    def post_execute(self, results):
        return [], []
