# Copyright 2020 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from threading import Event

from mycroft.configuration import Configuration
from mycroft.messagebus.client import MessageBusClient
from mycroft.util import create_daemon, create_echo_function
from mycroft.util.log import LOG
from .service import CoreService


def _define_services():
    return dict(
        message_bus=CoreService('mycroft-message-bus.service'),
        skills=CoreService('mycroft-skills.service'),
        audio_input=CoreService('mycroft-audio-input.service'),
        audio_output=CoreService('mycroft-audio-output.service'),
        enclosure=CoreService('mycroft-enclosure.service'),
    )


def _start_services(services):
    for service_name, service in services.items():
        if service_name != 'message_bus':
            service.start()


def _start_message_bus_client():
    """Start the bus client daemon."""
    bus = MessageBusClient()
    Configuration.set_config_update_handlers(bus)
    bus.on('message', create_echo_function('SUPERVISOR'))
    # Set the bus connected event when connection is established
    create_daemon(bus.run_forever)

    return bus


def _wait_for_message_bus_connection(bus):
    bus_connected = Event()
    bus.once('open', bus_connected.set)
    # Wait for connection
    bus_connected.wait()
    LOG.info('Connected to messagebus')


# example json object passed to server:
#   {service_name: skill, message: status, value: running}
def handle_message(reader, writer):
    data = await reader.readuntil(separator='|')
    message = data.decode()


def main():
    services = _define_services()
    services['message_bus'].start()
    bus = _start_message_bus_client()
    _wait_for_message_bus_connection(bus)
    for service in services.values():
        service.bus = bus
    _start_services(services)


if __name__ == '__main__':
    main()
