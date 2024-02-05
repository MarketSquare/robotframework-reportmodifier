## Introduction 
The high complexity of tests and the amount of information that can be logged makes the final report very confusing and unreadable for colleagues who aren't testers with Robot Framework knowledge but need to know the rough test flow and result. To provide a better overview of the test content, the library can filter the content by message content, keyword names or even keyword paths.

## Configuration assignment

The report is configured using YAML files. The YAML files must be saved within the /tests folder. The name of the file to be used must be stored as a "report" tag on the test case - either as a test tag for all test cases in the file or as a tag for a specific test case, e.g:
```shell
*** Settings ***

Test tags    report:custom_log
```
==> All test cases receive the custom report with the configuration custom_log.yaml

Alternatively you can define the report at every test, e.g. 

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
 - Play Backup.Log Screen → All logged contents of the keyword Play Backup.Log Screen are included, regardless of how often this call was made in the test case.
 - name: Should Be Equal As ASCII → The set setting means that only different outputs of the keyword "Should Be Equal As ASCII" are displayed in the report. Attention: Please pay attention to the spelling, the name of the keyword must follow "name:" in this case
```

**Option "messages"**

Filtering based on message content.

The message configuration collects logs that contain a specific text or correspond to a specific regular expression. It means, the message is valid as soos as defined text is found in the message or the regular expression has any foundings. For the definition of the RegEx pattern, we recommend an online test, e.g. on regex.com. Characters such as $ must be escaped with a backslash (\).
Examples: 
```shell
message = "Starting test case with a custom log."
messages:
 - text: custom    → Log is relevant because message contains the word "custom" 
 - pattern: Starting .* log    → Log is relevant because regex.findall("Starting .* log", "message", regex.IGNORECASE) returns at least one hit
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
 - Execute batch processing
```

**Option "keyword_as_structure"**

Another option for improving the readability of the report is to specify the keyword structure. This means that it is possible to include keywords as such in the modified report and place them at the top level of the report - directly below the test case. The structure specification requires that content is found via "messages" or "keywords" that are found in these keywords.
```shell
keyword_as_structure:
 - Execute batch processing
```
## Build and Test
TODO: Describe and show how to build your code and run the tests. 
