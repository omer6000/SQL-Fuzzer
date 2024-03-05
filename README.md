# SQL Fuzzer Project for Security Testing Course

## Overview
This SQL Fuzzer project is an essential component of the Security Testing course, focusing on developing a grammar-based black-box fuzzer for SQLite. The project's core is to automatically generate SQL commands to uncover potential vulnerabilities and test SQLite's resilience against malicious inputs.

## Project Goals
- Develop a versatile grammar to encompass all SQLite commands.
- Create a `fuzz_one_input` function for dynamic SQL command generation, aiming to challenge SQLite's error handling and robustness.

## Technologies
- Python for scripting and fuzz logic implementation.
- Docker to manage dependencies and ensure consistency across environments.
- Use of FuzzingBook for methodologies in fuzz testing.

## Key Features
- Implementation of a custom SQL grammar based on SQLite documentation.
- Automated and diverse input generation to extensively test SQLite functionalities.

## Implementation Highlights
- Application of FuzzingBook tools to devise the grammar and fuzzing strategy.
- Efficient grammar development to enable comprehensive testing of SQLite.

## Contributions
This project showcases the practical application of fuzzing in security testing, particularly in identifying database engine vulnerabilities, thus contributing to the enhancement of software security.

