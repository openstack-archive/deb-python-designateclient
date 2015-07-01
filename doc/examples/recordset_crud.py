import logging

from designateclient.v2 import client
from designateclient import exceptions
from designateclient import shell

from keystoneclient.auth.identity import generic
from keystoneclient import session as keystone_session


logging.basicConfig(level='DEBUG')

auth = generic.Password(
    auth_url=shell.env('OS_AUTH_URL'),
    username=shell.env('OS_USERNAME'),
    password=shell.env('OS_PASSWORD'),
    tenant_name=shell.env('OS_TENANT_NAME'))

session = keystone_session.Session(auth=auth)

client = client.Client(session=session)


try:
    zone = dict([(z['name'], z) for z in client.zones.list()])['i.io.']
    client.zones.delete(zone['id'])
except exceptions.NotFound:
    pass

zone = client.zones.create(name='i.io.', email='i@i.io')

# Clean all recordsets first in this zone (for sanity sake)
for rrset in client.recordsets.list(zone['id']):
    if rrset['type'] in ('NS', 'SOA'):
        continue
    client.recordsets.delete(zone['id'], rrset['id'])

# Make some A records
www = client.recordsets.create(
    zone['id'],
    'www.%s' % zone['name'],
    'A',
    ['10.0.0.1'])

values = {
    'records': ['10.0.1.1', '10.0.0.2']
}

client.recordsets.update(zone['id'], www['id'], values)

cname = client.recordsets.create(
    zone['id'],
    'my-site.%s' % zone['name'],
    'CNAME',
    [www['name']])

# Now let's do some Mailserver examples

# First create the A record
mail1 = client.recordsets.create(
    zone['id'], 'mail1.' + zone['name'], 'A', ["10.0.0.11"])

mail2 = client.recordsets.create(
    zone['id'], 'mail2.' + zone['name'], 'A', ["10.0.0.12"])

# Create the MX records - it will be 1 recordset with multiple records pointing
# to the A records we created above
mx_rrset = client.recordsets.create(
    zone['id'], zone['name'], 'MX',
    ['0 ' + mail1['name'], '5 ' + mail2['name']])

print(zone['id'])
