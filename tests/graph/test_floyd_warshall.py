# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest

import numpy

import retworkx


class TestFloydWarshall(unittest.TestCase):

    def test_floyd_warshall_numpy_three_edges(self):
        graph = retworkx.PyGraph()
        graph.add_nodes_from(list(range(6)))
        weights = [2, 12, 1, 5, 1]
        graph.add_edges_from([(i, i + 1, weights[i]) for i in range(5)])
        graph.add_edge(5, 0, 10)
        dist = retworkx.graph_floyd_warshall_numpy(graph, lambda x: x)
        self.assertEqual(dist[0, 3], 15)
        self.assertEqual(dist[3, 0], 15)

    def test_weighted_numpy_two_edges(self):
        graph = retworkx.PyGraph()
        graph.add_nodes_from(list(range(8)))
        graph.add_edges_from([
            (0, 1, 2),
            (1, 2, 2),
            (2, 3, 1),
            (3, 4, 1),
            (4, 5, 1),
            (5, 6, 1),
            (6, 7, 1),
            (7, 0, 1),
        ])
        dist = retworkx.graph_floyd_warshall_numpy(graph, lambda x: x)
        self.assertEqual(dist[0, 2], 4)
        self.assertEqual(dist[2, 0], 4)

    def test_weighted_numpy_negative_cycle(self):
        graph = retworkx.PyGraph()
        graph.add_nodes_from(list(range(4)))
        graph.add_edges_from([
            (0, 1, 1),
            (1, 2, -1),
            (2, 3, -1),
            (3, 0, -1),
        ])
        dist = retworkx.graph_floyd_warshall_numpy(graph, lambda x: x)
        expected = numpy.array(
            [[-6, -7, -8, -13],
             [-7, -8, -9, -14],
             [-8, -9, -10, -15],
             [-13, -14, -15, -20]], dtype=numpy.float64)
        self.assertTrue(numpy.array_equal(dist, expected))

    def test_floyd_warshall_numpy_cycle(self):
        graph = retworkx.PyGraph()
        graph.add_nodes_from(list(range(7)))
        graph.add_edges_from_no_data(
            [(0, 1), (0, 6), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])
        dist = retworkx.graph_floyd_warshall_numpy(graph, lambda x: 1)
        self.assertEqual(dist[0, 3], 3)
        self.assertEqual(dist[0, 4], 3)

    def test_numpy_no_edges(self):
        graph = retworkx.PyGraph()
        graph.add_nodes_from(list(range(4)))
        dist = retworkx.graph_floyd_warshall_numpy(graph, lambda x: x)
        expected = numpy.full((4, 4), numpy.inf)
        numpy.fill_diagonal(expected, 0)
        self.assertTrue(numpy.array_equal(dist, expected))

    def test_floyd_warshall_numpy_graph_cycle_with_removals(self):
        graph = retworkx.PyGraph()
        graph.add_nodes_from(list(range(8)))
        graph.remove_node(0)
        graph.add_edges_from_no_data(
            [(1, 2), (1, 7), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)])
        dist = retworkx.graph_floyd_warshall_numpy(graph, lambda x: 1)
        self.assertEqual(dist[0, 3], 3)
        self.assertEqual(dist[0, 4], 3)

    def test_floyd_warshall_numpy_graph_cycle_no_weight_fn(self):
        graph = retworkx.PyGraph()
        graph.add_nodes_from(list(range(8)))
        graph.remove_node(0)
        graph.add_edges_from_no_data(
            [(1, 2), (1, 7), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)])
        dist = retworkx.graph_floyd_warshall_numpy(graph)
        self.assertEqual(dist[0, 3], 3)
        self.assertEqual(dist[0, 4], 3)

    def test_floyd_warshall_numpy_graph_cycle_default_weight(self):
        graph = retworkx.PyGraph()
        graph.add_nodes_from(list(range(8)))
        graph.remove_node(0)
        graph.add_edges_from_no_data(
            [(1, 2), (1, 7), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)])
        dist = retworkx.graph_floyd_warshall_numpy(graph, default_weight=2)
        self.assertEqual(dist[0, 3], 6)
        self.assertEqual(dist[0, 4], 6)
