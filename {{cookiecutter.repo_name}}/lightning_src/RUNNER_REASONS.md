# Reasons for the runner

## Lightning Trainer

PL uses `Trainer` for passing all args for either training, tune, test or predict. This makes most classic calls equal.

```python
# file 1
trainer = Trainer(**kwargs1)
trainer.tune(model, dataloader)


# file 2
trainer = Trainer(**kwargs2)
trainer.fit(model, dataloader)


# file 3
trainer = Trainer(**kwargs3)
trainer.tune(model, dataloader)
trainer.fit(model, dataloader)
trainer.predict(model, dataloader)


# file 4
trainer = Trainer(**kwargs3)
trainer.test(model, dataloader)
```

**Our runner proposes to unify all these calls in one file**. Now, instead of calling different files you just do:

```python
# equivalent to call file 1
runner.py --gin_file config.gin --run tune

# equivalent to call file 2
runner.py --gin_file config.gin --run fit

# equivalent to call file 3
runner.py --gin_file config.gin --run tune --run fit --run predict

# equivalent to call file 4
runner.py --gin_file config.gin --run test
```

## Multiple independent research modules and datamodules ?

In this case, maybe you would no care about importing all modules and datamodules for they to be usable at some point. But what if they are a lot ? It is not reasonable to import them all if you're only going to use very few each time.

* Possible solution: you import only what you need.

```python
if args.module == "module1":
    from module1 import module1 as mymodule
    from datamodule1 import datamodule1 as mydatamodule
```

* More elegant solution: **Use importlib**

```python
import importlib
modulelib = importlib.import_module(module_filename)
cls = modulelib.__dict__[module_class_name]
```

## Too many args is a headache ?

When both modules and datamodules start having too much args is dificult to follow. So, what if you can have them all in one clean file. We adopt [gin-config](https://github.com/google/gin-config) files for this matter.
