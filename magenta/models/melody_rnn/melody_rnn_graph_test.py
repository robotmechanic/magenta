# Copyright 2016 Google Inc. All Rights Reserved.
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
"""Tests for melody_rnn_graph."""

# internal imports
import tensorflow as tf
import magenta

from magenta.models.melody_rnn import melody_rnn_config
from magenta.models.melody_rnn import melody_rnn_graph


class MelodyRNNGraphTest(tf.test.TestCase):

  def setUp(self):
    self.config = melody_rnn_config.MelodyRnnConfig(
        None,
        magenta.music.OneHotMelodyEncoderDecoder(0, 12, 0),
        magenta.common.HParams(
            batch_size=128,
            rnn_layer_sizes=[128, 128],
            dropout_keep_prob=0.5,
            skip_first_n_losses=0,
            clip_norm=5,
            initial_learning_rate=0.01,
            decay_steps=1000,
            decay_rate=0.85))

  def testBuildTrainGraph(self):
    g = melody_rnn_graph.build_graph(
        'train', self.config, sequence_example_file='test')
    self.assertTrue(isinstance(g, tf.Graph))

  def testBuildEvalGraph(self):
    g = melody_rnn_graph.build_graph(
        'eval', self.config, sequence_example_file='test')
    self.assertTrue(isinstance(g, tf.Graph))

  def testBuildGenerateGraph(self):
    g = melody_rnn_graph.build_graph('generate', self.config)
    self.assertTrue(isinstance(g, tf.Graph))

  def testBuildGenerateGraphWithTemp(self):
    self.config.hparams.temperature = 1.1
    g = melody_rnn_graph.build_graph('generate', self.config)
    self.assertTrue(isinstance(g, tf.Graph))

  def testBuildGraphWithAttention(self):
    self.config.hparams.attn_length = 10
    g = melody_rnn_graph.build_graph(
        'train', self.config, sequence_example_file='test')
    self.assertTrue(isinstance(g, tf.Graph))


if __name__ == '__main__':
  tf.test.main()
