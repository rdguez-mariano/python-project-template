from typing import Dict, List, Union

from pytorch_lightning import LightningDataModule
from torch.utils.data import DataLoader

from {{cookiecutter.pkg_shelf}}.{{cookiecutter.pkg_name}}.data.datasets.black_or_white import (
    BlackOrWhite as BlackOrWhiteDataset,
)


class BlackOrWhite(LightningDataModule):
    def __init__(
        self,
        channels: int = 1,
        width: int = 28,
        height: int = 28,
        batch_size: int = 32,
        num_workers: int = 4,
    ):
        super().__init__()
        self.num_workers = num_workers
        self.dims = (channels, width, height)
        self.batch_size = batch_size
        self.dataset = BlackOrWhiteDataset(img_dims=self.dims)

    def train_dataloader(
        self,
    ) -> Union[Dict[str, DataLoader], List[DataLoader], DataLoader]:
        return DataLoader(
            self.dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )

    def val_dataloader(
        self,
    ) -> Union[Dict[str, DataLoader], List[DataLoader], DataLoader]:
        return DataLoader(
            self.dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )

    def test_dataloader(
        self,
    ) -> Union[Dict[str, DataLoader], List[DataLoader], DataLoader]:
        return DataLoader(
            self.dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )

    def predict_dataloader(
        self,
    ) -> Union[Dict[str, DataLoader], List[DataLoader], DataLoader]:
        return DataLoader(
            self.dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )
