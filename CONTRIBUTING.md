# Contributing to mcp-open-data-hk

Thank you for your interest in contributing to mcp-open-data-hk! Here are some guidelines to help you get started.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct (TBD).

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on our GitHub repository with:
1. A clear and descriptive title
2. A detailed description of the problem
3. Steps to reproduce the issue
4. Information about your environment (OS, Python version, etc.)

### Suggesting Enhancements

If you have an idea for an enhancement, please create an issue with:
1. A clear and descriptive title
2. A detailed explanation of the proposed enhancement
3. Examples of how the enhancement would be used

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass by running `pytest tests/`
6. Commit your changes with a clear and descriptive commit message
7. Push your branch to your fork
8. Create a pull request to the main repository

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install the package in development mode: `pip install -e .[dev,test]`
5. Run tests to ensure everything works: `pytest tests/`

## Code Style

This project uses:
- Black for code formatting
- Flake8 for linting

Before submitting a pull request, please ensure your code adheres to these standards by running:
```bash
black src/ tests/
flake8 src/ tests/
```

## Testing

All contributions should include appropriate tests. We use pytest for testing.

Run all tests with:
```bash
pytest tests/
```

## Questions?

If you have any questions, please create an issue or contact the maintainers.