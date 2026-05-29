<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-05-29 | Updated: 2026-05-29 -->

# sql

## Purpose
Tools to convert WeChat Excel and Alipay CSV billing data into MySQL INSERT statements. Includes SQL table creation scripts and Python converters for both platforms.

## Key Files
| File | Description |
|------|-------------|
| `wx_bills_to_sql.py` | Converts WeChat Excel bills to MySQL INSERT statements (CLI: --source-dir, --output, --table-name) |
| `alipay_bills_to_sql.py` | Converts Alipay CSV bills to MySQL INSERT statements (CLI: --source-dir, --output, --table-name) |
| `csv_encoding.py` | Shared encoding detection utility (GB18030 → UTF-8 fallback) for Alipay CSV files |
| `wx_bills_create_table.sql` | MySQL CREATE TABLE script for WeChat bills schema |
| `alipay_bills_create_table.sql` | MySQL CREATE TABLE script for Alipay bills schema |
| `README.md` | CLI usage examples for both converters |

## Subdirectories
None

## For AI Agents

### Working In This Directory
- All configuration via CLI arguments: `--source-dir`, `--output`, `--table-name`
- WeChat converter auto-detects header row by searching for "交易单号"
- Alipay converter uses `csv_encoding.py` for encoding detection (GB18030 → UTF-8 fallback)
- Both use pandas for data processing and manual SQL string construction
- SQL values are escaped via module-level `clean_sql_value()` function

### Testing Requirements
- Test with actual exported bill files (WeChat .xlsx, Alipay .csv)
- Verify encoding handling (GB18030 for Alipay, UTF-8/GB18030 fallback for WeChat)
- Check amount parsing handles currency symbols (¥) and comma separators
- Validate generated SQL is valid MySQL syntax

### Common Patterns
- argparse CLI with required --source-dir, --output, --table-name arguments
- Batch processing via glob pattern matching
- Module-level clean_sql_value() handles NaN, whitespace, and quote escaping
- Shared csv_encoding.py for Alipay CSV encoding detection
- Output is single .sql file with multiple INSERT statements

## Dependencies

### Internal
- `csv_encoding.py` - Shared encoding detection used by alipay_bills_to_sql.py

### External
- pandas>=2.3.3 - Data processing and CSV/Excel reading
- openpyxl>=3.1.5 - Excel file reading (via pandas engine)

<!-- MANUAL: Custom notes can be added below -->