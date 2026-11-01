# Contributing to SheetSort

Thank you for your interest in contributing to **SheetSort**! This guide outlines how to set up your development environment, run tests, adhere to coding standards, and propose new features.

---

## 🛠️ Development Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/saish-vc/excel-sorter.git
   cd excel-sorter
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install pytest pyinstaller faker
   ```

4. **Launch the Application in Development Mode:**
   ```bash
   streamlit run sheetsort/app/main.py
   ```

---

## 🧪 Testing Guidelines

SheetSort enforces rigorous test coverage. Before submitting any pull request, ensure all tests pass:

```bash
# Run complete test suite
python -m pytest sheetsort/tests/ -v

# Run with test coverage report
python -m pytest sheetsort/tests/ --tb=short
```

### Adding New Tests
- Every new feature or cleaning rule must include matching unit tests in `sheetsort/tests/`.
- Ensure new test cases cover edge cases: empty cells, NaN values, non-string datatypes, and large row numbers.

---

## 🏗️ Code Organization

```
sheetsort/
├── app/
│   ├── main.py               # Streamlit multi-page UI orchestrator
│   ├── models/               # TypedDict data contracts
│   │   ├── cleaning_rule.py
│   │   ├── filter_rule.py
│   │   ├── recipe.py
│   │   ├── sort_rule.py
│   │   └── split_rule.py
│   ├── services/             # Pure functional computational logic
│   │   ├── data_cleaning.py
│   │   ├── deduplication.py
│   │   ├── export_service.py
│   │   ├── filtering.py
│   │   ├── recipe_service.py
│   │   ├── schema_detection.py
│   │   ├── sorting.py
│   │   ├── splitting.py
│   │   └── upload_service.py
│   └── utils/
│       └── config.py         # Global limits, safety thresholds, and paths
└── tests/                    # Pytest test suites (63 tests)
```

---

## 📐 Coding Conventions

- **Type Hints:** Use Python 3.10+ type annotations (`Optional`, `Union`, `List`, `Dict`, `Tuple`).
- **Data Immutability:** Services should return *copies* of DataFrames (`df.copy()`) rather than mutating inputs in place.
- **Security-First:**
  - Never parse user strings with raw regular expressions without disabling regex evaluation (`regex=False`) or escaping metacharacters.
  - Never allow raw formula strings (`=`, `+`, `-`, `@`) into unescaped Excel output.
  - Always use parameterized queries (`?`) for SQLite database interactions.

---

## 🚀 Submitting Changes

1. Fork the repository and create a feature branch (`git checkout -b feat/new-cleaning-rule`).
2. Commit changes with clear, descriptive commit messages (`git commit -m "feat(cleaning): add roll number zero-padding"`).
3. Push to your branch and open a Pull Request against `main`.
4. Explain the problem, proposed solution, and test evidence in your PR description.
