# AI-Powered Local Computer Automation — Phase 1 Prototype

Terminal proof-of-concept: ML intent classification + task planning + MCP-style local tool registry + safety controls.

## Run
Windows: `python main.py` or double-click `run_demo.bat`

## Demo commands
- create a folder named ML Project
- list files
- find pdf files
- search for report
- open calculator
- open notepad
- delete sample_report.pdf

All file operations are restricted to the project's `sandbox/` folder. Application launch is allowlisted. Deletion requires confirmation.

Note: this is an educational MCP-style prototype, not a full wire-compatible MCP implementation.
