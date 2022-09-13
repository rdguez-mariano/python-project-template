from typing import Tuple

import torch
import torch.nn.functional as F
from pytorch_lightning import LightningModule
from torch import nn
from torchmetrics.functional import accuracy


class Dummy(LightningModule):
    DROPOUT_PROB = 0.1

    def __init__(
        self,
        channels: int = 1,
        width: int = 28,
        height: int = 28,
        num_classes: int = 10,
        hidden_size: int = 64,
        learning_rate: float = 2e-4,
    ):

        super().__init__()

        # We take in input dimensions as parameters and
        # use those to dynamically build model.
        self.channels = channels
        self.width = width
        self.height = height
        self.num_classes = num_classes
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate

        self.model = nn.Sequential(
            nn.Flatten(),
            nn.Linear(channels * width * height, hidden_size),
            nn.ReLU(),
            nn.Dropout(self.DROPOUT_PROB),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(self.DROPOUT_PROB),
            nn.Linear(hidden_size, num_classes),
        )

    @property
    def input_dims(self) -> Tuple[int, int, int]:
        return (self.channels, self.width, self.height)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.model(x)
        return F.log_softmax(x, dim=1)

    def training_step(
        self, batch: torch.Tensor, batch_idx: int
    ) -> torch.Tensor:
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        return loss

    def validation_step(self, batch: torch.Tensor, batch_idx: int) -> None:
        x, y = batch
        logits = self(x)
        loss = F.nll_loss(logits, y)
        preds = torch.argmax(logits, dim=1)
        acc = accuracy(preds, y)
        metrics = {"val_loss": loss, "val_acc": acc}
        self.log_dict(metrics, prog_bar=True)

    def test_step(self, batch: torch.Tensor, batch_idx: int) -> None:
        x, y = batch
        logits = self(x)
        preds = torch.argmax(logits, dim=1)
        acc = accuracy(preds, y)
        metrics = {"test_acc": acc}
        self.log_dict(metrics, prog_bar=True)

    def predict_step(self, batch: torch.Tensor) -> torch.Tensor:
        x, _ = batch
        logits = self(x)
        preds = torch.argmax(logits, dim=1)
        return preds

    def configure_optimizers(self) -> torch.optim.Optimizer:
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        return optimizer
