<!-- Generated: 2026-05-29 | Updated: 2026-05-29 -->

# bills-utils

## Purpose
A utility toolkit for processing exported billing data from WeChat and Alipay platforms. The project provides tools to convert PDF/CSV/Excel billing formats into structured data formats like Excel, SQL statements, and visual charts for analysis.

## Key Files
| File | Description |
|------|-------------|
| `README.md` | Project overview with features, usage instructions, and acknowledgements |
| `pyproject.toml` | Python project configuration with dependencies (matplotlib, openpyxl, pandas, pdfplumber, seaborn) |
| `LICENSE` | GPL3 license file |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `conversion/` | WeChat PDF bill to Excel conversion utilities (see `conversion/AGENTS.md`) |
| `doc/` | Documentation including disclaimer (see `doc/AGENTS.md`) |
| `sql/` | Tools to convert billing data to MySQL SQL statements (see `sql/AGENTS.md`) |


## For AI Agents

### Working In This Directory
- Python >= 3.13 is required
- Use `uv sync` to install dependencies and create virtual environment
- Files are independent - can be run directly without cross-dependencies
- Follow existing patterns for argument parsing and error handling

### Testing Requirements
- Test with actual WeChat PDF and Alipay CSV exports
- Verify encoding handling (GB18030 for Alipay, UTF-8 for WeChat)
- Check date/time format conversions and amount parsing accuracy

### Common Patterns
- Command-line interface with argparse for all utilities
- Batch processing support for directories of files
- Robust error handling with clear user feedback
- Chinese language support with proper font configuration for visualizations

## Dependencies

### External
- matplotlib>=3.10.8 - Data visualization (retained for potential future use)
- openpyxl>=3.1.5 - Excel file manipulation
- pandas>=2.3.3 - Data processing and analysis
- pdfplumber>=0.11.9 - PDF text and table extraction

<!-- MANUAL: Custom project notes can be added below -->