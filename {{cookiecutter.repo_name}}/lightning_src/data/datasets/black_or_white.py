import random
from typing import Tuple

import torch
from torch.utils.data import Dataset


class BlackOrWhite(Dataset):
    def __init__(
        self, img_dims: Tuple[int, ...] = (1, 28, 28), n_samples: int = 1000
    ) -> None:
        super().__init__()
        self.n_samples = n_samples
        self.img_dims = img_dims

    def __len__(self) -> int:
        return self.n_samples

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int]:
        if random.randint(0, 1) == 0:
            img = torch.zeros(self.img_dims)
            class_idx = 0
        else:
            img = torch.ones(self.img_dims)
            class_idx = 1
        return img, class_idx
