## Introduction 
The high complexity of tests and the amount of information that can be logged makes the final report very confusing and unreadable for colleagues who aren't testers with Robot Framework knowledge but need to know the rough test flow and result. To provide a better overview of the test content, the library can filter the content by message content, keyword names or even keyword paths.

## Configuration assignment

The report is configured using YAML files. The YAML files must be saved within the /tests folder. The name of the file to be used must be stored as a "report:" tag on the test case - either as a test tag for all test cases in the file or as a tag for a specific test case. There is also the option of a base configuration for all test cases using tag "report:basic_config" with file "basic_config.yaml" withing the /test directory. Examples:
```shell
*** Settings ***

Test tags    report:basic_config
```
==> All test cases receive the custom report with the configuration basic_config.yaml

Alternatively/additionally you can define the report at every test, e.g. 

```shell
*** Test Cases ***

My Robot Test With Custom Log

    [Tags]    report:custom

My Robot Test With Custom Log 2

    [Tags]    report:custom_log2
```

## Configuration content

The YAML-configuration supports the following options:
 - keywords
 - messages
 - ignored_messages
 - keyword_name_as_info
 - keyword_as_structure

**Option "keywords"**

Filtering based on the keyword names or paths.

The keyword configuration can be used to store the name of a keyword, part of the call path of a keyword or the complete call path of a keyword. Different keywords can be defined in additional lines, e.g.:
```shell
keywords:
 - Second Level Keyword. Third Level Keyword    → All logged contents of the keyword *Second Level Keyword. Third Level Keyword* are included, regardless of how often this call was made in the test case.
```

**Option "messages"**

Filtering based on message content.

The message configuration collects logs that contain a specific text or correspond to a specific regular expression. It means, the message is valid as soon as defined text is found in the message or the regular expression has any foundings. For the definition of the RegEx pattern, we recommend an online test, e.g. on regex.com. Characters such as $ must be escaped with a backslash (\). You can specify text, pattern of status.
Examples: 
```shell
message = "Starting test case with a custom log."
messages:
 - text: custom                → Log is relevant because message contains the word "custom" 
 - pattern: Starting .* log    → Log is relevant because regex.findall("Starting .* log", "message", regex.IGNORECASE) returns at least one hit
 - status: FAIL | PASS | SKIP  → Log is relevant if the message level is equal to predefined status
```

**Option "ignored_messages"**

Removal of unwanted content that was taken along by previous configuration, e.g.:

message 1 = "Starting test case with a custom log."
message 2 0 "Finished test case with a custom log."

yaml configuration: 
```shell
messages:
 - text: custom
ignored_messages:
 - text: finished    → The 2nd message "Finished test case with a custom log." is ignored even though it was found using the pattern "custom".
 - pattern: fin.*    → The 2nd message "Finished test case with a custom log." is ignored even though it was found using the pattern "custom".
```

**Option "keyword_name_as_info"**

To make the test procedure easier to read, it can be helpful to list the names of certain keywords, including the documentation, as information. These are automatically highlighted in colour. The configuration is as follows:
```shell
keyword_name_as_info:
 - Third Level Keyword
```

**Option "keyword_as_structure"**

Another option for improving the readability of the report is to specify the keyword structure. This means that it is possible to include keywords as such in the modified report and place them at the top level of the report - directly below the test case. The structure specification requires that content is found via "messages" or "keywords" that are found in these keywords.
```shell
keyword_as_structure:
 - Second Level Keyword
```

In the tests/robot directory you can find some examples.

## Usage
You can create a custom log calling the class ReportModifier with the parameters *basis_output_xml*, *result_dir* and *report_name*, e.g.:
```shell
ReportModifier(basis_output_xml, result_dir, report_name).write_report()
```

or using the listener "ReportModifierListener" which is a Listener V3. In this case, the source xml file is the current created xml file, result dir the current result dir and report name the configured tag name.
