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
from enum import Enum, auto
from dataclasses import dataclass


class Status(Enum):
    INACTIVE = auto()
    STARTING = auto()
    LOADED = auto()
    RUNNING = auto()
    STOPPING = auto()
    CRASHED = auto()


class ServiceStatus:
    def __init__(self):
        self.status = Status.INACTIVE

    def set_starting(self):
        self._change_status(
            prerequisite_status=(Status.INACTIVE, Status.CRASHED),
            new_status=Status.STARTING
        )

    def set_loaded(self):
        self._change_status(
            prerequisite_status=(Status.STARTING,),
            new_status=Status.LOADED
        )

    def set_running(self):
        self._change_status(
            prerequisite_status=(Status.LOADED,),
            new_status=Status.RUNNING
        )

    def set_stopping(self):
        self._change_status(
            prerequisite_status=(
                Status.RUNNING,
                Status.LOADED,
                Status.STARTING
            ),
            new_status=Status.STOPPING
        )

    def set_crashed(self):
        self._change_status(
            prerequisite_status=(
                Status.RUNNING,
                Status.LOADED,
                Status.STARTING,
                Status.STOPPING
            ),
            new_status=Status.CRASHED
        )

    def set_inactive(self):
        self._change_status(
            prerequisite_status=(Status.STOPPING,), new_status=Status.INACTIVE
        )

    def _change_status(self, prerequisite_status, new_status):
        if self.status in prerequisite_status:
            self.status = new_status
        else:
            raise ValueError(
                f"Cannot change to {new_status} from {self.status}. Previous "
                f"status must be one of: {', '.join(prerequisite_status)}"
            )


@dataclass
class Service:
    service_name: str
    status: ServiceStatus
