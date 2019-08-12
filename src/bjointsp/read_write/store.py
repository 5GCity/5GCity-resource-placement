# Copyright (C) 2019 - Virtual Open Systems SAS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#   author          =   Teodora Sechkova
#   author_email    =   teodora@virtualopensystems.com

import logging

# Stores the placement result until a GET request is received
placement_db = []


def get_placement_db():
    if not placement_db:
        return None
    else:
        return placement_db


def store_placement_result(result):
    placement_db.append(result)
    logging.info("\nID {} added to the DB".format(result['id']))


def get_placement_result(placement_id):
    ret = None
    for result in placement_db:
        if str(result['id']) == placement_id:
            ret = result
            placement_db.remove(result)
        else:
            print("UUID not found")
            logging.info("\nResult ID {} not found".format(placement_id))

    return ret


