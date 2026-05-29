<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-05-29 | Updated: 2026-05-29 -->

# conversion

## Purpose
WeChat PDF bill to Excel conversion utilities. Converts exported WeChat billing PDFs into structured Excel files with proper date/amount formatting.

## Key Files
| File | Description |
|------|-------------|
| `wx_conversion.py` | Main CLI tool for converting WeChat PDF bills to Excel format |
| `README.md` | Usage instructions and output format documentation |

## Subdirectories
None

## For AI Agents

### Working In This Directory
- Uses `pdfplumber` for PDF table extraction
- Output Excel files use openpyxl with "账单" sheet name
- Date columns (index 1) are converted to datetime with `yyyy-mm-dd hh:mm:ss` format
- Amount columns (index 5) are converted to float with 2 decimal places
- Supports both single file and batch directory processing

### Testing Requirements
- Test with actual WeChat exported PDF bills
- Verify table extraction handles multi-line cell content (newline replacement)
- Check date parsing handles ISO format strings- Validate amount parsing handles string-to-float conversion

### Common Patterns
- argparse CLI with positional input and optional output_dir arguments
- Error handling returns None on failure, prints Chinese error messages
- Batch processing continues on individual file failures
- Output filename format: `{original}_converted_{timestamp}.xlsx`

## Dependencies

### Internal
- None (standalone utility)

### External
- pdfplumber>=0.11.9 - PDF table extraction
- openpyxl>=3.1.5 - Excel file generation

<!-- MANUAL: Custom notes can be added below -->