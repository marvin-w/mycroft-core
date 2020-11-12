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
import shlex
from subprocess import run, SubprocessError

from mycroft.util.log import LOG
from .status import ServiceStatus


class CoreService:
    def __init__(self, unit_name):
        self.systemctl_unit_name = unit_name
        self.status = ServiceStatus()
        self.bus = None

    def start(self):
        """Start the core service using systemd."""
        self._start_systemd_service()
        self.status.set_starting()

    def _start_systemd_service(self):
        command = f"systemctl start {self.systemctl_unit_name}"
        try:
            run(shlex.split(command), check=True)
        except SubprocessError:
            LOG.exception('Failed to start the {} service')

    def stop(self):
        pass

    def check_running(self):
        pass


