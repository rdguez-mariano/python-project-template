import hashlib
import os
import sys

import gin
import torch
from absl import flags
from pytorch_lightning import Trainer

from {{ cookiecutter.pkg_shelf }}.{{ cookiecutter.pkg_name }}.runner import importer


def get_sha(ckpt_path: str) -> str:
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks
    sha256 = hashlib.sha256()
    with open(ckpt_path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


if __name__ == "__main__":

    flags.DEFINE_multi_string(
        "gin_file", None, "List of paths to the config files."
    )
    flags.DEFINE_multi_string(
        "gin_param", None, "Newline separated list of Gin parameter bindings."
    )
    flags.DEFINE_multi_string(
        "ckpt_path", None, "List of paths to the checkpoint files."
    )

    config_flags = flags.FLAGS
    config_flags(sys.argv)

    gin.external_configurable(Trainer)
    gin.parse_config_files_and_bindings(
        config_flags.gin_file,
        config_flags.gin_param,
        skip_unknown=True,
        finalize_config=False,
    )

    module = importer(config_flags)[0].cpu().eval()

    for ckpt_path in config_flags.ckpt_path:
        ckpt_basename = os.path.basename(ckpt_path)
        experiment_dir = os.path.dirname(os.path.abspath(ckpt_path))
        trace_path = os.path.join(
            experiment_dir, os.path.splitext(ckpt_basename)[0]
        )
        input_example_shape = tuple([1] + list(module.input_dims))

        module.load_state_dict(torch.load(ckpt_path)["state_dict"])
        print(f"Module state succesfully loaded from {ckpt_path}")

        # Save the module trace
        trace = module.to_torchscript(
            method="trace", example_inputs=torch.randn(input_example_shape)
        )
        torch.jit.save(trace, trace_path + ".pth")
