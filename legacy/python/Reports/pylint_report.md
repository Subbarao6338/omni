# Pylint Code Review Report

**Generated on:** 2025-01-29 18:31:28

### Pylint Exit Codes:
- **0**: No issues found.
- **1**: One or more issues were found.

### Pylint categories of issues:
- **C**: Convention (related to coding style)
- **W**: Warning (potential issues that may not necessarily be errors)
- **E**: Error (actual errors in the code)
### Coding Standards Adherence

The code was reviewed against the following standards:
- Maximum line length: 100 characters
- Docstrings are required (disabled check for missing docstrings)

### Pylint Rating Calculation
Pylint assigns a rating to the analyzed code on a scale from 0 to 10, where:
- **10**: Perfect code with no issues.
- **Lower scores**: Indicate the presence of various issues.

**How the Rating is Calculated:**
1. **Issue Severity**:
   - **Convention (C)**: Style-related issues (e.g., naming conventions).
   - **Warning (W)**: Potential issues that may not be errors (e.g., unused variables).
   - **Error (E)**: Actual errors that prevent code execution (e.g., syntax errors).

2. **Weighting of Issues**:
   - Each type of issue has a different impact on the score:
     - Errors typically have a higher negative impact than warnings or conventions.

3. **Calculation Process**:
   - Start with a score of **10**.
   - Deduct points for each issue found:
   - Example: Deduct **0.5** points for each Convention issue, **1** point for each Warning, and **2** points for each Error.
   - The final score is capped at a minimum of **0**.

### Summary

- **Total Files Reviewed:** 34
- **Files with Issues:** 26
- **Files without Issues:** 8

- **Total Review Time:** 8.91 seconds

### Overall Issues Count
- **Total Convention Issues:** 68
- **Total Warning Issues:** 19
- **Total Error Issues:** 7

## Detailed Results

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\main_class.py`

- **Rating:** 6.67/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 4
- **Warning Issues Count:** 0
- **Error Issues Count:** 1
- **Review Time:** 0.29 seconds

#### Output:
```
************* Module main_class
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_class.py:2:0: C0103: Class name "employee" doesn't conform to PascalCase naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_class.py:8:4: C0103: Method name "displayCount" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_class.py:10:4: C0103: Method name "displayEmployee" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_class.py:21:0: C0103: Class name "vector" doesn't conform to PascalCase naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_class.py:25:4: E0307: __str__ does not return str (invalid-str-returned)

------------------------------------------------------------------
Your code has been rated at 6.67/10 (previous run: 6.67/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_class.py:2:0: C0103: Class name "employee" doesn't conform to PascalCase naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_class.py:8:4: C0103: Method name "displayCount" doesn't conform to snake_case naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_class.py:10:4: C0103: Method name "displayEmployee" doesn't conform to snake_case naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_class.py:21:0: C0103: Class name "vector" doesn't conform to PascalCase naming style (invalid-name)

#### Error Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_class.py:25:4: E0307: __str__ does not return str (invalid-str-returned)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\main_files.py`

- **Rating:** 8.50/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 2
- **Warning Issues Count:** 1
- **Error Issues Count:** 0
- **Review Time:** 0.16 seconds

#### Output:
```
************* Module main_files
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_files.py:21:0: C0103: Constant name "s" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_files.py:27:0: C0413: Import "import calendar" should be placed at the top of the module (wrong-import-position)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_files.py:2:0: W0611: Unused import sys (unused-import)

------------------------------------------------------------------
Your code has been rated at 8.50/10 (previous run: 8.50/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_files.py:21:0: C0103: Constant name "s" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_files.py:27:0: C0413: Import "import calendar" should be placed at the top of the module (wrong-import-position)

#### Warning Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_files.py:2:0: W0611: Unused import sys (unused-import)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\main_functions.py`

- **Rating:** 7.86/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 3
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.08 seconds

#### Output:
```
************* Module main_functions
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_functions.py:18:0: C0304: Final newline missing (missing-final-newline)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_functions.py:13:0: C0103: Function name "KtoF" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_functions.py:13:9: C0103: Argument name "T" doesn't conform to snake_case naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 7.86/10 (previous run: 7.86/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_functions.py:18:0: C0304: Final newline missing (missing-final-newline)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_functions.py:13:0: C0103: Function name "KtoF" doesn't conform to snake_case naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_functions.py:13:9: C0103: Argument name "T" doesn't conform to snake_case naming style (invalid-name)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\main_lists.py`

- **Rating:** 8.75/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 0
- **Warning Issues Count:** 1
- **Error Issues Count:** 0
- **Review Time:** 0.08 seconds

#### Output:
```
************* Module main_lists
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_lists.py:10:0: W0105: String statement has no effect (pointless-string-statement)

------------------------------------------------------------------
Your code has been rated at 8.75/10 (previous run: 8.75/10, +0.00)


```

#### Warning Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_lists.py:10:0: W0105: String statement has no effect (pointless-string-statement)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\main_main.py`

- **Rating:** 10.00/10
- **Status:** No issues found.
- **Exit Code:** 0
- **Convention Issues Count:** 0
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.07 seconds

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\main_new1.py`

- **Rating:** 0.00/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 1
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.07 seconds

#### Output:
```
************* Module main_new1
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_new1.py:1:0: C0304: Final newline missing (missing-final-newline)

------------------------------------------------------------------
Your code has been rated at 0.00/10 (previous run: 0.00/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_new1.py:1:0: C0304: Final newline missing (missing-final-newline)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py`

- **Rating:** 9.35/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 6
- **Warning Issues Count:** 5
- **Error Issues Count:** 0
- **Review Time:** 0.16 seconds

#### Output:
```
************* Module main_patterns
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:190:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:207:0: W0311: Bad indentation. Found 1 spaces, expected 4 (bad-indentation)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:210:0: W0311: Bad indentation. Found 2 spaces, expected 8 (bad-indentation)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:212:0: W0311: Bad indentation. Found 1 spaces, expected 4 (bad-indentation)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:215:0: W0311: Bad indentation. Found 2 spaces, expected 8 (bad-indentation)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:218:0: W0311: Bad indentation. Found 1 spaces, expected 4 (bad-indentation)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:154:0: C0103: Constant name "c" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:182:0: C0103: Constant name "x" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:189:0: C0103: Constant name "r" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:190:0: R1730: Consider using 'k = min(k, n - k)' instead of unnecessary if block (consider-using-min-builtin)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:202:0: C0413: Import "from math import factorial" should be placed at the top of the module (wrong-import-position)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:205:0: C0103: Constant name "n" doesn't conform to UPPER_CASE naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 9.35/10 (previous run: 9.35/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:190:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:154:0: C0103: Constant name "c" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:182:0: C0103: Constant name "x" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:189:0: C0103: Constant name "r" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:202:0: C0413: Import "from math import factorial" should be placed at the top of the module (wrong-import-position)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:205:0: C0103: Constant name "n" doesn't conform to UPPER_CASE naming style (invalid-name)

#### Warning Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:207:0: W0311: Bad indentation. Found 1 spaces, expected 4 (bad-indentation)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:210:0: W0311: Bad indentation. Found 2 spaces, expected 8 (bad-indentation)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:212:0: W0311: Bad indentation. Found 1 spaces, expected 4 (bad-indentation)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:215:0: W0311: Bad indentation. Found 2 spaces, expected 8 (bad-indentation)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_patterns.py:218:0: W0311: Bad indentation. Found 1 spaces, expected 4 (bad-indentation)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\main_progrms.py`

- **Rating:** 6.25/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 3
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.07 seconds

#### Output:
```
************* Module main_progrms
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_progrms.py:60:0: C0304: Final newline missing (missing-final-newline)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_progrms.py:55:0: C0103: Constant name "b" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_progrms.py:58:4: C0103: Constant name "b" doesn't conform to UPPER_CASE naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 6.25/10 (previous run: 6.25/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_progrms.py:60:0: C0304: Final newline missing (missing-final-newline)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_progrms.py:55:0: C0103: Constant name "b" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_progrms.py:58:4: C0103: Constant name "b" doesn't conform to UPPER_CASE naming style (invalid-name)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\main_re.py`

- **Rating:** 7.50/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 2
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.31 seconds

#### Output:
```
************* Module main_re
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_re.py:10:0: C0305: Trailing newlines (trailing-newlines)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_re.py:2:0: C0103: Constant name "line" doesn't conform to UPPER_CASE naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 7.50/10 (previous run: 7.50/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_re.py:10:0: C0305: Trailing newlines (trailing-newlines)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_re.py:2:0: C0103: Constant name "line" doesn't conform to UPPER_CASE naming style (invalid-name)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\main_series.py`

- **Rating:** 7.06/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 5
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.07 seconds

#### Output:
```
************* Module main_series
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_series.py:42:0: C0305: Trailing newlines (trailing-newlines)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_series.py:28:4: C0103: Constant name "s" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_series.py:29:4: C0103: Constant name "c" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_series.py:32:8: C0103: Constant name "c" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_series.py:34:4: C0103: Constant name "s" doesn't conform to UPPER_CASE naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 7.06/10 (previous run: 7.06/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_series.py:42:0: C0305: Trailing newlines (trailing-newlines)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_series.py:28:4: C0103: Constant name "s" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_series.py:29:4: C0103: Constant name "c" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_series.py:32:8: C0103: Constant name "c" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_series.py:34:4: C0103: Constant name "s" doesn't conform to UPPER_CASE naming style (invalid-name)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py`

- **Rating:** 7.00/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 8
- **Warning Issues Count:** 1
- **Error Issues Count:** 0
- **Review Time:** 0.08 seconds

#### Output:
```
************* Module main_strings
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:18:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:33:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:2:0: C0103: Constant name "s1" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:15:0: C0103: Constant name "s3" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:16:0: C0103: Constant name "co" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:30:0: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:31:4: C0103: Constant name "c1" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:32:4: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:36:0: W0105: String statement has no effect (pointless-string-statement)

------------------------------------------------------------------
Your code has been rated at 7.00/10 (previous run: 7.00/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:18:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:33:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:2:0: C0103: Constant name "s1" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:15:0: C0103: Constant name "s3" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:16:0: C0103: Constant name "co" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:30:0: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:31:4: C0103: Constant name "c1" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:32:4: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)

#### Warning Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\main_strings.py:36:0: W0105: String statement has no effect (pointless-string-statement)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_class.py`

- **Rating:** 6.67/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 4
- **Warning Issues Count:** 0
- **Error Issues Count:** 1
- **Review Time:** 0.09 seconds

#### Output:
```
************* Module python_class
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_class.py:2:0: C0103: Class name "employee" doesn't conform to PascalCase naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_class.py:8:4: C0103: Method name "displayCount" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_class.py:10:4: C0103: Method name "displayEmployee" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_class.py:21:0: C0103: Class name "vector" doesn't conform to PascalCase naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_class.py:25:4: E0307: __str__ does not return str (invalid-str-returned)

------------------------------------------------------------------
Your code has been rated at 6.67/10 (previous run: 6.67/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_class.py:2:0: C0103: Class name "employee" doesn't conform to PascalCase naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_class.py:8:4: C0103: Method name "displayCount" doesn't conform to snake_case naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_class.py:10:4: C0103: Method name "displayEmployee" doesn't conform to snake_case naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_class.py:21:0: C0103: Class name "vector" doesn't conform to PascalCase naming style (invalid-name)

#### Error Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_class.py:25:4: E0307: __str__ does not return str (invalid-str-returned)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df1.py`

- **Rating:** 10.00/10
- **Status:** No issues found.
- **Exit Code:** 0
- **Convention Issues Count:** 0
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 3.79 seconds

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df2.py`

- **Rating:** 9.00/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 1
- **Warning Issues Count:** 1
- **Error Issues Count:** 0
- **Review Time:** 0.40 seconds

#### Output:
```
************* Module python_df2
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df2.py:44:0: C0304: Final newline missing (missing-final-newline)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df2.py:41:0: W0105: String statement has no effect (pointless-string-statement)

------------------------------------------------------------------
Your code has been rated at 9.00/10 (previous run: 9.00/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df2.py:44:0: C0304: Final newline missing (missing-final-newline)

#### Warning Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df2.py:41:0: W0105: String statement has no effect (pointless-string-statement)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df3.py`

- **Rating:** 9.66/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 1
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.39 seconds

#### Output:
```
************* Module python_df3
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df3.py:39:0: C0304: Final newline missing (missing-final-newline)

------------------------------------------------------------------
Your code has been rated at 9.66/10 (previous run: 9.66/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df3.py:39:0: C0304: Final newline missing (missing-final-newline)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df4.py`

- **Rating:** 10.00/10
- **Status:** No issues found.
- **Exit Code:** 0
- **Convention Issues Count:** 0
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.13 seconds

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df5.py`

- **Rating:** 9.00/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 1
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.08 seconds

#### Output:
```
************* Module python_df5
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df5.py:10:0: C0304: Final newline missing (missing-final-newline)

------------------------------------------------------------------
Your code has been rated at 9.00/10 (previous run: 9.00/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df5.py:10:0: C0304: Final newline missing (missing-final-newline)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df6.py`

- **Rating:** 8.57/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 1
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.14 seconds

#### Output:
```
************* Module python_df6
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df6.py:11:0: C0304: Final newline missing (missing-final-newline)

------------------------------------------------------------------
Your code has been rated at 8.57/10 (previous run: 8.57/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df6.py:11:0: C0304: Final newline missing (missing-final-newline)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df7.py`

- **Rating:** 9.29/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 1
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.17 seconds

#### Output:
```
************* Module python_df7
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df7.py:17:0: C0304: Final newline missing (missing-final-newline)

------------------------------------------------------------------
Your code has been rated at 9.29/10 (previous run: 9.29/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df7.py:17:0: C0304: Final newline missing (missing-final-newline)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df8.py`

- **Rating:** 5.00/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 2
- **Warning Issues Count:** 1
- **Error Issues Count:** 0
- **Review Time:** 0.32 seconds

#### Output:
```
************* Module python_df8
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df8.py:3:0: C0301: Line too long (150/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df8.py:7:0: C0304: Final newline missing (missing-final-newline)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df8.py:2:0: W0611: Unused numpy imported as np (unused-import)

------------------------------------------------------------------
Your code has been rated at 5.00/10 (previous run: 5.00/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df8.py:3:0: C0301: Line too long (150/100) (line-too-long)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df8.py:7:0: C0304: Final newline missing (missing-final-newline)

#### Warning Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_df8.py:2:0: W0611: Unused numpy imported as np (unused-import)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py`

- **Rating:** 6.25/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 6
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.08 seconds

#### Output:
```
************* Module python_files (2)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:55:0: C0325: Unnecessary parens after 'while' keyword (superfluous-parens)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:1:0: C0103: Module name "python_files (2)" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:53:0: C0103: Constant name "h" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:54:0: C0103: Constant name "c" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:62:0: C0103: Constant name "o" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:65:4: C0103: Constant name "o" doesn't conform to UPPER_CASE naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 6.25/10 (previous run: 6.25/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:55:0: C0325: Unnecessary parens after 'while' keyword (superfluous-parens)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:1:0: C0103: Module name "python_files (2)" doesn't conform to snake_case naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:53:0: C0103: Constant name "h" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:54:0: C0103: Constant name "c" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:62:0: C0103: Constant name "o" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files (2).py:65:4: C0103: Constant name "o" doesn't conform to UPPER_CASE naming style (invalid-name)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files.py`

- **Rating:** 8.50/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 2
- **Warning Issues Count:** 1
- **Error Issues Count:** 0
- **Review Time:** 0.08 seconds

#### Output:
```
************* Module python_files
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files.py:21:0: C0103: Constant name "s" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files.py:27:0: C0413: Import "import calendar" should be placed at the top of the module (wrong-import-position)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files.py:2:0: W0611: Unused import sys (unused-import)

------------------------------------------------------------------
Your code has been rated at 8.50/10 (previous run: 8.50/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files.py:21:0: C0103: Constant name "s" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files.py:27:0: C0413: Import "import calendar" should be placed at the top of the module (wrong-import-position)

#### Warning Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_files.py:2:0: W0611: Unused import sys (unused-import)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_functions.py`

- **Rating:** 7.86/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 3
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.08 seconds

#### Output:
```
************* Module python_functions
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_functions.py:18:0: C0304: Final newline missing (missing-final-newline)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_functions.py:13:0: C0103: Function name "KtoF" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_functions.py:13:9: C0103: Argument name "T" doesn't conform to snake_case naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 7.86/10 (previous run: 7.86/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_functions.py:18:0: C0304: Final newline missing (missing-final-newline)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_functions.py:13:0: C0103: Function name "KtoF" doesn't conform to snake_case naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_functions.py:13:9: C0103: Argument name "T" doesn't conform to snake_case naming style (invalid-name)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_lists.py`

- **Rating:** 10.00/10
- **Status:** No issues found.
- **Exit Code:** 0
- **Convention Issues Count:** 0
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.07 seconds

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_main.py`

- **Rating:** 10.00/10
- **Status:** No issues found.
- **Exit Code:** 0
- **Convention Issues Count:** 0
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.07 seconds

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_matrix.py`

- **Rating:** 9.58/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 1
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.38 seconds

#### Output:
```
************* Module python_matrix
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_matrix.py:46:0: C0304: Final newline missing (missing-final-newline)

------------------------------------------------------------------
Your code has been rated at 9.58/10 (previous run: 9.58/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_matrix.py:46:0: C0304: Final newline missing (missing-final-newline)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_np.py`

- **Rating:** 9.57/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 0
- **Warning Issues Count:** 1
- **Error Issues Count:** 0
- **Review Time:** 0.12 seconds

#### Output:
```
************* Module python_np
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_np.py:3:0: W0105: String statement has no effect (pointless-string-statement)

------------------------------------------------------------------
Your code has been rated at 9.57/10 (previous run: 9.57/10, +0.00)


```

#### Warning Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_np.py:3:0: W0105: String statement has no effect (pointless-string-statement)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_panda.py`

- **Rating:** 0.00/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 0
- **Warning Issues Count:** 4
- **Error Issues Count:** 0
- **Review Time:** 0.16 seconds

#### Output:
```
************* Module python_panda
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_panda.py:3:21: W1401: Anomalous backslash in string: '\.'. String constant might be missing an r prefix. (anomalous-backslash-in-string)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_panda.py:3:27: W1401: Anomalous backslash in string: '\S'. String constant might be missing an r prefix. (anomalous-backslash-in-string)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_panda.py:3:33: W1401: Anomalous backslash in string: '\A'. String constant might be missing an r prefix. (anomalous-backslash-in-string)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_panda.py:3:42: W1401: Anomalous backslash in string: '\G'. String constant might be missing an r prefix. (anomalous-backslash-in-string)

------------------------------------------------------------------
Your code has been rated at 0.00/10 (previous run: 0.00/10, +0.00)


```

#### Warning Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_panda.py:3:21: W1401: Anomalous backslash in string: '\.'. String constant might be missing an r prefix. (anomalous-backslash-in-string)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_panda.py:3:27: W1401: Anomalous backslash in string: '\S'. String constant might be missing an r prefix. (anomalous-backslash-in-string)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_panda.py:3:33: W1401: Anomalous backslash in string: '\A'. String constant might be missing an r prefix. (anomalous-backslash-in-string)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_panda.py:3:42: W1401: Anomalous backslash in string: '\G'. String constant might be missing an r prefix. (anomalous-backslash-in-string)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_patterns.py`

- **Rating:** None/10
- **Status:** No issues found.
- **Exit Code:** 0
- **Convention Issues Count:** 0
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.07 seconds

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_progrms.py`

- **Rating:** None/10
- **Status:** No issues found.
- **Exit Code:** 0
- **Convention Issues Count:** 0
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.06 seconds

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py`

- **Rating:** 0.00/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 4
- **Warning Issues Count:** 2
- **Error Issues Count:** 5
- **Review Time:** 0.60 seconds

#### Output:
```
************* Module python_scipy1
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:21:0: C0304: Final newline missing (missing-final-newline)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:7:2: E1101: Module 'scipy.special' has no 'exp10' member (no-member)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:9:2: E1101: Module 'scipy.special' has no 'exp2' member; maybe 'exp'? (no-member)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:11:2: E1101: Module 'scipy.special' has no 'sindg' member (no-member)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:13:2: E1101: Module 'scipy.special' has no 'cosdg' member (no-member)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:15:17: W0108: Lambda may not be necessary (unnecessary-lambda)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:15:26: E1101: Module 'scipy.special' has no 'exp10' member (no-member)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:17:2: C3001: Lambda expression assigned to a variable. Define a function using the "def" keyword instead. (unnecessary-lambda-assignment)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:18:2: C3001: Lambda expression assigned to a variable. Define a function using the "def" keyword instead. (unnecessary-lambda-assignment)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:19:2: C3001: Lambda expression assigned to a variable. Define a function using the "def" keyword instead. (unnecessary-lambda-assignment)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:2:0: W0611: Unused cluster imported from scipy (unused-import)

------------------------------------------------------------------
Your code has been rated at 0.00/10 (previous run: 0.00/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:21:0: C0304: Final newline missing (missing-final-newline)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:17:2: C3001: Lambda expression assigned to a variable. Define a function using the "def" keyword instead. (unnecessary-lambda-assignment)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:18:2: C3001: Lambda expression assigned to a variable. Define a function using the "def" keyword instead. (unnecessary-lambda-assignment)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:19:2: C3001: Lambda expression assigned to a variable. Define a function using the "def" keyword instead. (unnecessary-lambda-assignment)

#### Warning Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:15:17: W0108: Lambda may not be necessary (unnecessary-lambda)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:2:0: W0611: Unused cluster imported from scipy (unused-import)

#### Error Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:7:2: E1101: Module 'scipy.special' has no 'exp10' member (no-member)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:9:2: E1101: Module 'scipy.special' has no 'exp2' member; maybe 'exp'? (no-member)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:11:2: E1101: Module 'scipy.special' has no 'sindg' member (no-member)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:13:2: E1101: Module 'scipy.special' has no 'cosdg' member (no-member)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_scipy1.py:15:26: E1101: Module 'scipy.special' has no 'exp10' member (no-member)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_series.py`

- **Rating:** 7.27/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 3
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.07 seconds

#### Output:
```
************* Module python_series
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_series.py:78:0: C0325: Unnecessary parens after 'while' keyword (superfluous-parens)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_series.py:82:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_series.py:76:4: C0103: Constant name "c" doesn't conform to UPPER_CASE naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 7.27/10 (previous run: 7.27/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_series.py:78:0: C0325: Unnecessary parens after 'while' keyword (superfluous-parens)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_series.py:82:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_series.py:76:4: C0103: Constant name "c" doesn't conform to UPPER_CASE naming style (invalid-name)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_str.py`

- **Rating:** 5.45/10
- **Status:** Issues found.
- **Exit Code:** 1
- **Convention Issues Count:** 4
- **Warning Issues Count:** 1
- **Error Issues Count:** 0
- **Review Time:** 0.07 seconds

#### Output:
```
************* Module python_str
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_str.py:98:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_str.py:2:0: C0103: Constant name "s" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_str.py:93:0: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_str.py:97:0: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
C:\Users\2631239\Downloads\New folder\local_repo\Python\python_str.py:100:0: W0105: String statement has no effect (pointless-string-statement)

------------------------------------------------------------------
Your code has been rated at 5.45/10 (previous run: 5.45/10, +0.00)


```

#### Convention Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_str.py:98:0: C0325: Unnecessary parens after 'if' keyword (superfluous-parens)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_str.py:2:0: C0103: Constant name "s" doesn't conform to UPPER_CASE naming style (invalid-name)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_str.py:93:0: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_str.py:97:0: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)

#### Warning Issues:
- C:\Users\2631239\Downloads\New folder\local_repo\Python\python_str.py:100:0: W0105: String statement has no effect (pointless-string-statement)

### File: `C:\Users\2631239\Downloads\New folder\local_repo\Python\python_strings.py`

- **Rating:** None/10
- **Status:** No issues found.
- **Exit Code:** 0
- **Convention Issues Count:** 0
- **Warning Issues Count:** 0
- **Error Issues Count:** 0
- **Review Time:** 0.06 seconds

