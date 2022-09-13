import importlib
import sys
from typing import Optional, Tuple, Union

import gin
from absl import flags
from pytorch_lightning import LightningDataModule, LightningModule, Trainer

ALLOW_CALLS_TO = ["fit", "tune", "test", "predict"]


def find_module_using_name(
    module_name: str,
    module_type: str = "module",
    module_relpath: Optional[str] = None,
) -> Union[LightningModule, LightningDataModule]:
    """Import the module "module/[module_name]_module.py".

    In the file, the class called [module_name]() will
    be instantiated. It has to be a subclass of LightningModule,
    and it is case-insensitive.
    """
    module_name = module_name.lower()
    if module_type == "module":
        module_class = LightningModule
        if module_relpath is None:
            module_relpath = f"modules.{module_name}"
    elif module_type == "datamodule":
        module_class = LightningDataModule
        if module_relpath is None:
            module_relpath = f"data.datamodules.{module_name}"
    else:
        raise Exception(f"Error: type {module_type} not implemented.")

    modulelib = importlib.import_module(module_relpath)
    module = None
    target_module_name = module_name.replace("_", "")
    for name, cls in modulelib.__dict__.items():
        if name.lower() == target_module_name.lower() and issubclass(
            cls, module_class
        ):
            module = cls

    if module is None:
        raise Exception(
            f"Error: Inside {module_relpath}.py, a class deriving from \
{module_class.__name__} should exist. Also, the class name should match \
{target_module_name} in lowercase."
        )

    return gin.external_configurable(module, module_type)


@gin.configurable(denylist=["config_flags"])
def importer(
    config_flags: flags.FlagValues,
    module_name: str = gin.REQUIRED,
    datamodule_name: Optional[str] = None,
    module_relpath: Optional[str] = None,
    datamodule_relpath: Optional[str] = None,
) -> Union[
    Tuple[LightningModule], Tuple[LightningModule, LightningDataModule]
]:

    module_class = find_module_using_name(
        module_name, "module", module_relpath=module_relpath
    )
    if datamodule_name is not None:
        datamodule_class = find_module_using_name(
            datamodule_name, "datamodule", module_relpath=datamodule_relpath
        )

    gin.parse_config_files_and_bindings(
        config_flags.gin_file, config_flags.gin_param
    )

    module = module_class()
    print(f"The LightningModule <{type(module).__name__}> was instanciated.")

    if datamodule_name is None:
        # The module knows also has the data for train, test, etc.
        return (module,)
    else:
        # The module is agnostic to data for train, test, etc.
        datamodule = datamodule_class()
        print(
            f"The LightningDataModule <{type(datamodule).__name__}> \
was instanciated."
        )
        return module, datamodule


if __name__ == "__main__":
    flags.DEFINE_multi_string(
        "gin_file", None, "List of paths to the config files."
    )
    flags.DEFINE_multi_string(
        "gin_param", None, "Newline separated list of Gin parameter bindings."
    )
    flags.DEFINE_multi_string(
        "run",
        "fit",
        f"Pytorch Lightning Trainer's function to run \
(e.g. {ALLOW_CALLS_TO}",
    )

    config_flags = flags.FLAGS
    config_flags(sys.argv)

    configurable_trainer_class = gin.external_configurable(Trainer)

    gin.parse_config_files_and_bindings(
        config_flags.gin_file,
        config_flags.gin_param,
        skip_unknown=True,
        finalize_config=False,
    )

    trainer = configurable_trainer_class()
    run_args = importer(config_flags)

    for run in config_flags.run:
        if run not in ALLOW_CALLS_TO:
            msg = f"Error: {Trainer.__name__}.{run} is not allowed.\n"
            msg += f"Try one of: {ALLOW_CALLS_TO}\n"
            raise Exception(msg)
        fn = getattr(trainer, run)
        fn(*run_args)
