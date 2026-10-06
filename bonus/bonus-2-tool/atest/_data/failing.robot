*** Settings ***
Documentation       Run by `github_issues.robot` with the listener. The folder's `_` prefix keeps
...                 `robot atest` from running it on its own.


*** Test Cases ***
Login Works
    Fail    Expected 200 but got 500

Logout Works
    Fail    Session still open\n```not closed```

Passes
    No Operation

Is Skipped
    Skip    Not today
