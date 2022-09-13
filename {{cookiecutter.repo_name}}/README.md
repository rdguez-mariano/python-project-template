# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Installation

{% if cookiecutter.enable_github_action_ci == 'y' %}
This package is available from the pypi repository. Now, you can simply run:

```bash
pip install {{ cookiecutter.pkg_name }}
```

{% endif %}

## Usage


{% if cookiecutter.enable_lightning_repo == 'y' %}
## AI Lightning template repo

- Focus on research. Avoid common technicalities to get mixed with actual training strategies.
- Top packages out there. We adopt pytorch lightning, gin configurations, and code-writing best practices.
- Well organized and easy to get the whole picture quickly.

Some choices in our [runner.py](runner.py) are explained in [RUNNER_REASONS.md](RUNNER_REASONS.md)


{% endif %}
## Contributing

If you would like to contribute, please read our [contributing](CONTRIBUTING.md) section.
