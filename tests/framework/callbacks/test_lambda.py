from unittest.mock import MagicMock, ANY, Mock


import torch
import torch.nn as nn

from poutyne import Model, LambdaCallback, Callback
from tests.framework.tools import some_data_tensor_generator
from tests.framework.model.base import ModelFittingTestCase

class LambdaTest(ModelFittingTestCase):
    # pylint: disable=too-many-public-methods

    def setUp(self):
        super().setUp()
        torch.manual_seed(42)
        self.pytorch_network = nn.Linear(1, 1)
        self.loss_function = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.pytorch_network.parameters(), lr=1e-3)
        self.model = Model(self.pytorch_network,
                           self.optimizer,
                           self.loss_function)

    def test_lambda_train_calls(self):
        mock_callback = Mock(spec=Callback())
        lambda_callback = LambdaCallback(on_epoch_begin=mock_callback.on_epoch_begin,
                 on_epoch_end=mock_callback.on_epoch_end,
                 on_train_batch_begin=mock_callback.on_train_batch_begin,
                 on_train_batch_end=mock_callback.on_train_batch_end,
                 on_valid_batch_begin=mock_callback.on_valid_batch_begin,
                 on_valid_batch_end=mock_callback.on_valid_batch_end,
                 on_test_batch_begin=mock_callback.on_test_batch_begin,
                 on_test_batch_end=mock_callback.on_test_batch_end,
                 on_train_begin=mock_callback.on_train_begin,
                 on_train_end=mock_callback.on_train_end,
                 on_valid_begin=mock_callback.on_valid_begin,
                 on_valid_end=mock_callback.on_valid_end,
                 on_test_begin=mock_callback.on_test_begin,
                 on_test_end=mock_callback.on_test_end,
                 on_backward_end=mock_callback.on_backward_end)

        train_generator = some_data_tensor_generator(LambdaTest.batch_size)
        valid_generator = some_data_tensor_generator(LambdaTest.batch_size)
        logs = self.model.fit_generator(train_generator,
                                        valid_generator,
                                        epochs=LambdaTest.epochs,
                                        steps_per_epoch=LambdaTest.steps_per_epoch,
                                        validation_steps=LambdaTest.steps_per_epoch,
                                        callbacks=[lambda_callback])
        params = {
            'epochs': LambdaTest.epochs,
            'steps': LambdaTest.steps_per_epoch,
            'valid_steps': LambdaTest.steps_per_epoch
        }
        expected_calls = self._get_callback_expected_on_calls_when_training(params, logs,
                                                                            valid_steps=LambdaTest.steps_per_epoch)
        actual_calls = mock_callback.method_calls
        self.assertEqual(len(expected_calls), len(actual_calls))
        self.assertEqual(expected_calls, actual_calls)
