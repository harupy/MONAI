# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from collections import OrderedDict

import torch
from parameterized import parameterized

from monai.networks.blocks.feature_pyramid_network import FeaturePyramidNetwork

TEST_CASES = []
TEST_CASES.append(
    [
        {"spatial_dims": 3, "in_channels_list": [32, 64], "out_channels": 6},
        ((7, 32, 16, 32, 64), (7, 64, 8, 16, 32)),
        ((7, 6, 16, 32, 64), (7, 6, 8, 16, 32)),
    ]
)
TEST_CASES.append(
    [
        {"spatial_dims": 2, "in_channels_list": [32, 64], "out_channels": 6},
        ((7, 32, 16, 32), (7, 64, 8, 16)),
        ((7, 6, 16, 32), (7, 6, 8, 16)),
    ]
)


class TestFPNBlock(unittest.TestCase):
    @parameterized.expand(TEST_CASES)
    def test_fpn_block(self, input_param, input_shape, expected_shape):
        net = FeaturePyramidNetwork(**input_param)
        data = OrderedDict()
        data["feat0"] = torch.rand(input_shape[0])
        data["feat1"] = torch.rand(input_shape[1])
        result = net(data)
        self.assertEqual(result["feat0"].shape, expected_shape[0])
        self.assertEqual(result["feat1"].shape, expected_shape[1])


if __name__ == "__main__":
    unittest.main()
