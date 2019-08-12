# Modifications Copyright (C) 2019 - Virtual Open Systems SAS
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

import random
import logging
from datetime import datetime
import os
import bjointsp.read_write.reader as reader
import bjointsp.read_write.writer as writer
from bjointsp.heuristic import control
import bjointsp.objective as objective


# set objective for MIP and heuristic
obj = objective.RESOURCES


# solve with heuristic; interface to place-emu: triggers placement
def place(network_file, template_file, source_file, fixed_file=None, prev_embedding_file=None, cpu=None, mem=None,
          dr=None):
    seed = random.randint(0, 9999)
    seed_subfolder = False
    random.seed(seed)
    result = {}

    # set up logging into file Data/logs/heuristic/scenario_timestamp_seed.log
    # logging.disable(logging.CRITICAL)     # disable logging
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("logs/heuristic/obj{}".format(obj), exist_ok=True)
    logging.basicConfig(
        filename="logs/heuristic/obj{}/{}_{}_{}.log".format(obj, os.path.basename('test')[:-4], timestamp, seed),
        level=logging.DEBUG, format="%(asctime)s(%(levelname)s):\t%(message)s", datefmt="%H:%M:%S")

    nodes, links = reader.read_network(network_file, cpu, mem, dr)
    template, source_components = reader.read_template(template_file, return_src_components=True)
    templates = [template]
    # print(template)
    # exit()
    sources = reader.read_sources(source_file, source_components)
    components = {j for t in templates for j in t.components}
    fixed = []
    if fixed_file is not None:
        fixed = reader.read_fixed_instances(fixed_file, components)
    prev_embedding = {}
    if prev_embedding_file is not None:
        prev_embedding = reader.read_prev_embedding(prev_embedding_file, templates)

    # input_files = [network_file, template_file, source_file, fixed_file, prev_embedding_file]
    input_files = ['parameters/networks/test.graphml', 'parameters/5gcity/fw1chain.json', None, None, None]
    # TODO: support >1 template

    print("Using seed {}".format(seed))

    logging.info("Starting initial embedding at {}".format(timestamp))
    print("Initial embedding\n")
    # TODO: make less verbose or only as verbose when asked for (eg, with -v argument)
    init_time, runtime, obj_value, changed, overlays = control.solve(nodes, links, templates, prev_embedding, sources,
                                                                     fixed, obj)
    writer.write_heuristic_result(runtime, obj_value, changed, overlays.values(), input_files, obj, nodes, links, seed,
                                  seed_subfolder)

    result = writer.format_output(result, changed, overlays.values(), nodes, links)
    return result