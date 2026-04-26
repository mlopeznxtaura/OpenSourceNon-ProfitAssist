# Contributing to Modular Cognitive Engine

Thank you for considering contributing to Modular Cognitive Engine! We welcome contributions from the community.

## How to Contribute

### 1. Fork the Repository

```bash
git clone https://github.com/your-org/cognitive-engine.git
cd cognitive-engine
```

### 2. Create a Branch

```bash
git checkout -b feature/amazing-feature
```

### 3. Make Your Changes

- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 4. Run Tests

```bash
pytest tests/
```

### 5. Commit Your Changes

```bash
git commit -m "Add amazing feature"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/amazing-feature
```

Then open a pull request on GitHub.

## Code Style

We use the following tools for code quality:

- **Black** for code formatting
- **flake8** for linting
- **mypy** for type checking

Run them before submitting:

```bash
black cognitive_engine/
flake8 cognitive_engine/
mypy cognitive_engine/
```

## Testing Guidelines

- Write unit tests for all new functionality
- Aim for high test coverage
- Use descriptive test names
- Test edge cases and error conditions

## Documentation

- Update README.md if adding new features
- Add docstrings to all public functions and classes
- Include usage examples

## Questions?

Feel free to open an issue if you have questions about contributing!
