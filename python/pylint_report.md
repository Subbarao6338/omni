# Pylint Code Review Report

**Generated on:** 2025-01-30 11:28:54

## Summary

- **Total Files Reviewed:** 15
- **Files with Issues:** 15
- **Files without Issues:** 0

## Detailed Results

### File: `C:\Users\2631239\Downloads\New folder\Main\github4.py`

- **Rating:** 8.52/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module github4
C:\Users\2631239\Downloads\New folder\Main\github4.py:60:0: C0301: Line too long (117/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\github4.py:129:0: C0301: Line too long (103/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\github4.py:132:0: C0301: Line too long (101/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\github4.py:141:0: C0301: Line too long (118/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\github4.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\github4.py:46:11: W0718: Catching too general exception Exception (broad-exception-caught)
C:\Users\2631239\Downloads\New folder\Main\github4.py:43:19: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
C:\Users\2631239\Downloads\New folder\Main\github4.py:53:15: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
C:\Users\2631239\Downloads\New folder\Main\github4.py:61:15: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
C:\Users\2631239\Downloads\New folder\Main\github4.py:65:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
C:\Users\2631239\Downloads\New folder\Main\github4.py:103:20: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
C:\Users\2631239\Downloads\New folder\Main\github4.py:146:9: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\github4.py:162:4: W0603: Using the global statement (global-statement)
C:\Users\2631239\Downloads\New folder\Main\github4.py:173:26: W1309: Using an f-string that does not have any interpolated variables (f-string-without-interpolation)
C:\Users\2631239\Downloads\New folder\Main\github4.py:184:4: W0601: Global variable 'BASE_URL' undefined at the module level (global-variable-undefined)
C:\Users\2631239\Downloads\New folder\Main\github4.py:3:0: C0411: standard import "csv" should be placed before third party import "requests" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\github4.py:5:0: C0411: standard import "time" should be placed before third party imports "requests", "dotenv" (wrong-import-order)

------------------------------------------------------------------
Your code has been rated at 8.52/10 (previous run: 8.52/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py`

- **Rating:** 8.63/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module listdicts_logs
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:63:0: C0301: Line too long (103/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:79:0: C0301: Line too long (101/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:4:0: C0115: Missing class docstring (missing-class-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:4:0: R0902: Too many instance attributes (9/7) (too-many-instance-attributes)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:16:17: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:19:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:21:13: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:24:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:27:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:30:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:33:16: W0612: Unused variable 'i' (unused-variable)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:42:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:45:16: W0612: Unused variable 'i' (unused-variable)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:55:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:71:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:87:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:102:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:114:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:116:17: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\listdicts_logs.py:170:7: W0718: Catching too general exception Exception (broad-exception-caught)

------------------------------------------------------------------
Your code has been rated at 8.63/10 (previous run: 8.63/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\new.py`

- **Rating:** 8.21/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module new
C:\Users\2631239\Downloads\New folder\Main\new.py:54:0: C0301: Line too long (130/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\new.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\new.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\new.py:11:15: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
C:\Users\2631239\Downloads\New folder\Main\new.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\new.py:21:15: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
C:\Users\2631239\Downloads\New folder\Main\new.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\new.py:33:15: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
C:\Users\2631239\Downloads\New folder\Main\new.py:41:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\new.py:77:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\new.py:80:15: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
C:\Users\2631239\Downloads\New folder\Main\new.py:89:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\new.py:95:9: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\new.py:102:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\new.py:3:0: C0411: standard import "csv" should be placed before third party import "requests" (wrong-import-order)

------------------------------------------------------------------
Your code has been rated at 8.21/10 (previous run: 8.21/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\otp_new.py`

- **Rating:** 8.40/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module otp_new
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:74:0: C0301: Line too long (106/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:75:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:79:0: C0301: Line too long (126/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:82:0: C0301: Line too long (148/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:11:12: W0621: Redefining name 'otp' from outer scope (line 128) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:36:9: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:45:4: W0621: Redefining name 'blacklist' from outer scope (line 110) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:73:27: W0621: Redefining name 'whitelist' from outer scope (line 110) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:73:43: W0621: Redefining name 'blacklist' from outer scope (line 110) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:84:4: W0621: Redefining name 'otp' from outer scope (line 128) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\otp_new.py:131:11: W0718: Catching too general exception Exception (broad-exception-caught)

------------------------------------------------------------------
Your code has been rated at 8.40/10 (previous run: 8.40/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\P1_keywords.py`

- **Rating:** 7.58/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module P1_keywords
C:\Users\2631239\Downloads\New folder\Main\P1_keywords.py:30:0: C0301: Line too long (106/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\P1_keywords.py:41:0: C0301: Line too long (107/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\P1_keywords.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\P1_keywords.py:1:0: C0103: Module name "P1_keywords" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\Main\P1_keywords.py:17:11: W0718: Catching too general exception Exception (broad-exception-caught)
C:\Users\2631239\Downloads\New folder\Main\P1_keywords.py:11:13: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\P1_keywords.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\P1_keywords.py:44:21: W0621: Redefining name 'keyword_score' from outer scope (line 23) (redefined-outer-name)

------------------------------------------------------------------
Your code has been rated at 7.58/10 (previous run: 7.58/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py`

- **Rating:** 8.91/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module P2_otp_pwd
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:15:0: C0301: Line too long (103/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:115:0: C0301: Line too long (106/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:116:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:120:0: C0301: Line too long (126/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:123:0: C0301: Line too long (148/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:200:0: C0301: Line too long (104/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:201:0: C0301: Line too long (104/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:203:0: C0301: Line too long (108/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:206:0: C0301: Line too long (120/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:1:0: C0103: Module name "P2_otp_pwd" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:79:9: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:158:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:187:19: W0718: Catching too general exception Exception (broad-exception-caught)
C:\Users\2631239\Downloads\New folder\Main\P2_otp_pwd.py:209:19: W0718: Catching too general exception Exception (broad-exception-caught)

------------------------------------------------------------------
Your code has been rated at 8.91/10 (previous run: 8.91/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py`

- **Rating:** 9.48/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module P3_multiple
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:1:0: C0103: Module name "P3_multiple" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:4:0: C0115: Missing class docstring (missing-class-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:4:0: R0902: Too many instance attributes (12/7) (too-many-instance-attributes)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:24:17: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:34:13: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:206:17: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:235:16: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:242:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:242:28: W0621: Redefining name 'choice' from outer scope (line 300) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:273:16: R1722: Consider using 'sys.exit' instead (consider-using-sys-exit)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:242:4: R0912: Too many branches (17/12) (too-many-branches)
C:\Users\2631239\Downloads\New folder\Main\P3_multiple.py:303:11: W0718: Catching too general exception Exception (broad-exception-caught)

------------------------------------------------------------------
Your code has been rated at 9.48/10 (previous run: 9.48/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\P3_single.py`

- **Rating:** 8.57/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module P3_single
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:1:0: C0103: Module name "P3_single" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:1:0: C0115: Missing class docstring (missing-class-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:6:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:9:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:12:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:15:16: W0612: Unused variable 'i' (unused-variable)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:22:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:25:16: W0612: Unused variable 'i' (unused-variable)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:33:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:46:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:59:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:68:4: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\P3_single.py:112:7: W0718: Catching too general exception Exception (broad-exception-caught)

------------------------------------------------------------------
Your code has been rated at 8.57/10 (previous run: 8.57/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\p4_scd2.py`

- **Rating:** 8.18/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module p4_scd2
C:\Users\2631239\Downloads\New folder\Main\p4_scd2.py:74:0: C0301: Line too long (103/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\p4_scd2.py:98:0: C0301: Line too long (106/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\p4_scd2.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\p4_scd2.py:9:0: C0103: Constant name "sql_create" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\Main\p4_scd2.py:21:0: C0103: Constant name "sql_history" doesn't conform to UPPER_CASE naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\Main\p4_scd2.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\p4_scd2.py:57:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\p4_scd2.py:117:7: W0718: Catching too general exception Exception (broad-exception-caught)

------------------------------------------------------------------
Your code has been rated at 8.18/10 (previous run: 8.18/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\r1.py`

- **Rating:** 8.63/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module r1
C:\Users\2631239\Downloads\New folder\Main\r1.py:30:0: C0301: Line too long (101/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\r1.py:50:0: C0301: Line too long (109/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\r1.py:88:0: C0301: Line too long (117/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\r1.py:89:0: C0301: Line too long (113/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\r1.py:102:0: C0301: Line too long (265/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\r1.py:132:0: C0301: Line too long (119/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\r1.py:190:0: C0301: Line too long (124/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\r1.py:193:0: C0301: Line too long (122/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\r1.py:219:0: C0301: Line too long (133/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\r1.py:225:0: C0305: Trailing newlines (trailing-newlines)
C:\Users\2631239\Downloads\New folder\Main\r1.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\r1.py:43:11: W0718: Catching too general exception Exception (broad-exception-caught)
C:\Users\2631239\Downloads\New folder\Main\r1.py:18:8: W0612: Unused variable 'rcfile_path' (unused-variable)
C:\Users\2631239\Downloads\New folder\Main\r1.py:21:8: W0612: Unused variable 'run' (unused-variable)
C:\Users\2631239\Downloads\New folder\Main\r1.py:75:9: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\r1.py:71:0: R0915: Too many statements (78/50) (too-many-statements)
C:\Users\2631239\Downloads\New folder\Main\r1.py:4:0: C0411: standard import "io.StringIO" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\r1.py:5:0: C0411: standard import "pathlib.Path" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\r1.py:6:0: C0411: standard import "datetime.datetime" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\r1.py:7:0: C0411: standard import "time" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\r1.py:8:0: C0411: standard import "os" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)

------------------------------------------------------------------
Your code has been rated at 8.63/10 (previous run: 8.63/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\review.py`

- **Rating:** 8.72/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module review
C:\Users\2631239\Downloads\New folder\Main\review.py:38:0: C0301: Line too long (146/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review.py:47:0: C0301: Line too long (180/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review.py:85:0: C0301: Line too long (119/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review.py:133:0: C0301: Line too long (152/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\review.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\review.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\review.py:48:11: W0718: Catching too general exception Exception (broad-exception-caught)
C:\Users\2631239\Downloads\New folder\Main\review.py:52:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\review.py:53:9: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\review.py:116:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\review.py:4:0: C0411: standard import "io.StringIO" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\review.py:5:0: C0411: standard import "pathlib.Path" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\review.py:6:0: C0411: standard import "datetime.datetime" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)

------------------------------------------------------------------
Your code has been rated at 8.72/10 (previous run: 8.72/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\review_new.py`

- **Rating:** 8.41/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module review_new
C:\Users\2631239\Downloads\New folder\Main\review_new.py:46:0: C0301: Line too long (146/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:56:0: C0301: Line too long (192/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:91:0: C0301: Line too long (111/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:92:0: C0301: Line too long (110/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:96:0: C0301: Line too long (109/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:101:0: C0301: Line too long (149/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:125:0: C0301: Line too long (119/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:174:0: C0301: Line too long (164/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:195:0: C0301: Line too long (116/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:37:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:57:11: W0718: Catching too general exception Exception (broad-exception-caught)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:44:8: W0612: Unused variable 'run' (unused-variable)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:61:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:66:9: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:61:0: R0915: Too many statements (71/50) (too-many-statements)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:156:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:156:0: R0914: Too many local variables (16/15) (too-many-locals)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:4:0: C0411: standard import "io.StringIO" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:5:0: C0411: standard import "pathlib.Path" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:6:0: C0411: standard import "datetime.datetime" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\review_new.py:7:0: C0411: standard import "time" should be placed before third party imports "pylint.lint", "pylint.reporters.text.TextReporter" (wrong-import-order)

------------------------------------------------------------------
Your code has been rated at 8.41/10 (previous run: 8.41/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\review_pylint.py`

- **Rating:** 8.43/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module review_pylint
C:\Users\2631239\Downloads\New folder\Main\review_pylint.py:14:0: C0301: Line too long (107/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_pylint.py:32:0: C0301: Line too long (116/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_pylint.py:70:0: C0301: Line too long (124/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_pylint.py:71:0: C0301: Line too long (126/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_pylint.py:90:0: C0301: Line too long (101/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_pylint.py:94:0: C0301: Line too long (116/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\review_pylint.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\review_pylint.py:21:8: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
C:\Users\2631239\Downloads\New folder\Main\review_pylint.py:28:8: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
C:\Users\2631239\Downloads\New folder\Main\review_pylint.py:65:9: W1514: Using open without explicitly specifying an encoding (unspecified-encoding)
C:\Users\2631239\Downloads\New folder\Main\review_pylint.py:93:18: R1728: Consider using a generator instead 'sum(len(files) for (_, _, files) in os.walk(folder_to_review) if files and any((f.endswith('.py') for f in files)))' (consider-using-generator)

------------------------------------------------------------------
Your code has been rated at 8.43/10 (previous run: 8.43/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\Strong_otp.py`

- **Rating:** 7.95/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module Strong_otp
C:\Users\2631239\Downloads\New folder\Main\Strong_otp.py:36:0: C0301: Line too long (102/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\Strong_otp.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\Strong_otp.py:1:0: C0103: Module name "Strong_otp" doesn't conform to snake_case naming style (invalid-name)
C:\Users\2631239\Downloads\New folder\Main\Strong_otp.py:10:12: W0621: Redefining name 'otp' from outer scope (line 72) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\Strong_otp.py:19:27: W0621: Redefining name 'whitelist' from outer scope (line 68) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\Strong_otp.py:19:43: W0621: Redefining name 'blacklist' from outer scope (line 69) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\Strong_otp.py:38:4: W0621: Redefining name 'otp' from outer scope (line 72) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\Strong_otp.py:23:4: R1720: Unnecessary "elif" after "raise", remove the leading "el" from "elif" (no-else-raise)
C:\Users\2631239\Downloads\New folder\Main\Strong_otp.py:79:7: W0718: Catching too general exception Exception (broad-exception-caught)

------------------------------------------------------------------
Your code has been rated at 7.95/10 (previous run: 7.95/10, +0.00)


```

### File: `C:\Users\2631239\Downloads\New folder\Main\weather.py`

- **Rating:** 5.96/10
- **Exit Code:** 1

**Status:** Issues found.

#### Output:
```
************* Module weather
C:\Users\2631239\Downloads\New folder\Main\weather.py:13:0: C0301: Line too long (136/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\weather.py:52:0: C0301: Line too long (104/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\weather.py:53:0: C0301: Line too long (128/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\weather.py:58:0: C0301: Line too long (141/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\weather.py:64:0: C0301: Line too long (148/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\weather.py:67:0: C0301: Line too long (104/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\weather.py:70:0: C0301: Line too long (145/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\weather.py:89:0: C0301: Line too long (127/100) (line-too-long)
C:\Users\2631239\Downloads\New folder\Main\weather.py:1:0: C0114: Missing module docstring (missing-module-docstring)
C:\Users\2631239\Downloads\New folder\Main\weather.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\weather.py:22:16: W0621: Redefining name 'location' from outer scope (line 116) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\weather.py:38:19: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
C:\Users\2631239\Downloads\New folder\Main\weather.py:70:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\weather.py:70:0: R0913: Too many arguments (8/5) (too-many-arguments)
C:\Users\2631239\Downloads\New folder\Main\weather.py:70:0: R0917: Too many positional arguments (8/5) (too-many-positional-arguments)
C:\Users\2631239\Downloads\New folder\Main\weather.py:70:89: W0621: Redefining name 'location' from outer scope (line 116) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\weather.py:95:0: C0116: Missing function or method docstring (missing-function-docstring)
C:\Users\2631239\Downloads\New folder\Main\weather.py:95:26: W0621: Redefining name 'location' from outer scope (line 116) (redefined-outer-name)
C:\Users\2631239\Downloads\New folder\Main\weather.py:2:0: C0411: standard import "json" should be placed before third party import "requests" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\weather.py:3:0: C0411: standard import "logging" should be placed before third party import "requests" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\weather.py:5:0: C0411: standard import "os" should be placed before third party imports "requests", "dotenv" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\weather.py:6:0: C0411: standard import "time" should be placed before third party imports "requests", "dotenv" (wrong-import-order)
C:\Users\2631239\Downloads\New folder\Main\weather.py:7:0: C0411: standard import "re" should be placed before third party imports "requests", "dotenv" (wrong-import-order)

------------------------------------------------------------------
Your code has been rated at 5.96/10 (previous run: 5.96/10, +0.00)


```

