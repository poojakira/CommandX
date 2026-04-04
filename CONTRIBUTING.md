# Contributing to CommandX

First off, thank you for considering contributing to CommandX! It’s people like you that make CommandX such a great tool for orbital mechanics simulation and MLOps learning.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:
- Be respectful and inclusive.
- Use professional language.
- Focus on constructive feedback.

## How Can I Contribute?

### Reporting Bugs
- Use the GitHub Issue Tracker.
- Describe the bug clearly with steps to reproduce.
- Include your OS and Python version.

### Suggesting Enhancements
- Open a GitHub Issue with the tag `enhancement`.
- Explain why the feature would be useful.

### Pull Requests
1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes (`pytest tests/`).
4. Make sure your code lints (`flake8 .`).
5. Issue the PR!

## Project Structure

- `gnc/` - Guidance, Navigation, and Control modules.
- `ml/` - Streaming ML and anomaly detection.
- `docs/` - Documentation and assets.
- `tests/` - Unit and integration tests.

## Development Setup

```bash
git clone https://github.com/poojakira/CommandX.git
cd CommandX
pip install -r requirements.txt
pytest tests/
```

Thank you for your contributions!
