*** Settings ***
Documentation       Runs `_data/failing.robot` with the listener, in a dry run, and checks what it recorded.
...
...                 Every inner run uses an isolated environment that holds Robot Framework 7.5 and nothing else, and
...                 imports the listener with `--pythonpath src`. This shows that the listener works without being
...                 installed and needs nothing beyond Robot Framework.

Library             Collections
Library             OperatingSystem
Library             Process
Library             XML

Suite Setup         Create Runs Directory
Suite Teardown      Remove Directory    ${RUNS}    recursive=True


*** Variables ***
${ROOT}             ${{ pathlib.Path(r'${CURDIR}').parent.as_posix() }}
${SUITE}            ${CURDIR}/_data/failing.robot
${SOURCE}           atest/_data/failing.robot
${LISTENER}         robotframework_github_reporter.GitHubIssues
${ISSUES}           https://api.github.com/repos/octo-org/demo/issues
${LOOKUP}           ${ISSUES}?state=open&labels=robot-failure&per_page=100
${LOGIN}            Expected 200 but got 500
${LOGOUT}           Session still open\n```not closed```
${RUN URL}          https://github.com/octo-org/app/actions/runs/42
&{ACTIONS}
...                 GITHUB_ACTIONS=true
...                 GITHUB_SERVER_URL=https://github.com
...                 GITHUB_REPOSITORY=octo-org/app
...                 GITHUB_RUN_ID=42


*** Test Cases ***
Dry run records the requests
    ${run} =    Run Failing Suite    :repo=octo-org/demo
    Should Be Equal As Integers    ${run.rc}    2
    Should Not Contain    ${run.stderr}    into use failed
    Should Not Contain    ${run.stderr}    [ ERROR ]
    Should Contain X Times    ${run.stdout}    github-reporter (dry run):    3
    Should Contain X Times    ${run.stdout}    github-reporter (dry run): GET ${LOOKUP}\n    1
    Should Contain X Times    ${run.stdout}    github-reporter (dry run): POST ${ISSUES}\n    2
    ${requests} =    Recorded Requests    ${run}
    Length Should Be    ${requests}    3
    Dictionaries Should Be Equal    ${requests}[0]    ${{ {"method": "GET", "url": $LOOKUP} }}
    Issue Request Should Be    ${requests}[1]    Failing.Login Works    ${LOGIN}    7
    Issue Request Should Be    ${requests}[2]    Failing.Logout Works    ${LOGOUT}    10
    Test Statuses Should Be Unchanged    ${run}

Run URL in GitHub Actions
    ${run} =    Run Failing Suite    :repo=octo-org/demo    environment=${ACTIONS}
    Should Be Equal As Integers    ${run.rc}    2
    ${requests} =    Recorded Requests    ${run}
    Length Should Be    ${requests}    3
    Should Contain    ${requests}[1][body][body]    **Run:** ${RUN URL}
    Should Contain    ${requests}[2][body][body]    **Run:** ${RUN URL}

No run URL outside GitHub Actions
    ${run} =    Run Failing Suite    :repo=octo-org/demo
    ${requests} =    Recorded Requests    ${run}
    Should Not Contain    ${requests}[1][body][body]    **Run:**
    Should Not Contain    ${requests}[2][body][body]    **Run:**

Live run without a token falls back to a dry run
    ${run} =    Run Failing Suite    :repo=octo-org/demo:dry_run=false
    Should Be Equal As Integers    ${run.rc}    2
    Should Contain X Times    ${run.stderr}
    ...    [ WARN ] github-reporter: no GITHUB_TOKEN or GH_TOKEN; falling back to a dry run    1
    File Should Exist    ${run.output_dir}/github-requests.json
    ${requests} =    Recorded Requests    ${run}
    Length Should Be    ${requests}    3
    Test Statuses Should Be Unchanged    ${run}

Misconfiguration is only a warning under --exitonerror
    [Template]    Misconfiguration Should Only Warn
    ${EMPTY}                                repo is missing
    :repo=octo-org/demo:labels=x            ignoring unknown arguments: labels
    :repo=octo-org/demo:token=s3cret        tokens are read from GITHUB_TOKEN or GH_TOKEN only
    :repo=octo-org/demo:dry_run=maybe       dry_run must be true or false, not 'maybe'


*** Keywords ***
Create Runs Directory
    ${runs} =    Evaluate    tempfile.mkdtemp(prefix="github-reporter-atest-")    modules=tempfile
    VAR    ${RUNS}    ${runs}    scope=SUITE

Run Failing Suite
    [Documentation]    Runs the failing suite in an isolated environment, with `arguments` appended to the
    ...    listener's name and `environment` added to a clean GitHub environment. Returns the process result
    ...    with an `output_dir` attribute.
    ...
    ...    The keyword takes no free named arguments, so that `arguments` such as `:repo=octo-org/demo` are not
    ...    mistaken for named ones.
    [Arguments]    ${arguments}    @{options}    ${environment}=${{ {} }}
    ${output_dir} =    Evaluate    tempfile.mkdtemp(dir=$RUNS)    modules=tempfile
    ${env} =    Get Environment Variables
    Set To Dictionary    ${env}    GITHUB_TOKEN=    GH_TOKEN=    GITHUB_ACTIONS=    &{environment}
    ${run} =    Run Process
    ...    uv    run    --isolated    --no-project    --with    robotframework\=\=7.5
    ...    python    -m    robot
    ...    --pythonpath    ${ROOT}/src
    ...    --listener    ${LISTENER}${arguments}
    ...    --outputdir    ${output_dir}
    ...    @{options}
    ...    ${SUITE}
    ...    cwd=${ROOT}    env=${env}    timeout=5 min
    Log    ${run.stdout}
    Log    ${run.stderr}
    Evaluate    setattr($run, "output_dir", $output_dir)
    RETURN    ${run}

Recorded Requests
    [Arguments]    ${run}
    ${text} =    Get File    ${run.output_dir}/github-requests.json    encoding=UTF-8
    ${requests} =    Evaluate    json.loads($text)    modules=json
    RETURN    ${requests}

Issue Request Should Be
    [Arguments]    ${request}    ${full name}    ${message}    ${line}
    Should Be Equal    ${request}[method]    POST
    Should Be Equal    ${request}[url]    ${ISSUES}
    Should Be Equal    ${request}[body][title]    Failing test: ${full name}
    Should Be Equal    ${request}[body][labels]    ${{ ["robot-failure"] }}
    Should Contain    ${request}[body][body]    \n${message}\n
    Should Contain    ${request}[body][body]    **Source:** `${SOURCE}:${line}`

Test Statuses Should Be Unchanged
    [Arguments]    ${run}
    ${output} =    Parse XML    ${run.output_dir}/output.xml
    FOR    ${name}    ${status}    ${message}    IN
    ...    Login Works    FAIL    ${LOGIN}
    ...    Logout Works    FAIL    ${LOGOUT}
    ...    Passes    PASS    ${EMPTY}
    ...    Is Skipped    SKIP    Not today
        ${element} =    Get Element    ${output}    .//test[@name='${name}']/status
        Should Be Equal    ${element.get('status')}    ${status}
        Should Be Equal    ${{ $element.text or '' }}    ${message}
    END

Misconfiguration Should Only Warn
    [Arguments]    ${arguments}    ${warning}
    ${run} =    Run Failing Suite    ${arguments}    --exitonerror
    Should Be Equal As Integers    ${run.rc}    2
    Should Not Contain    ${run.stderr}    into use failed
    Should Not Contain    ${run.stderr}    [ ERROR ]
    Should Contain    ${run.stderr}    [ WARN ] github-reporter: ${warning}
    Test Statuses Should Be Unchanged    ${run}
    Should Not Contain    ${run.stdout}    s3cret
    Should Not Contain    ${run.stderr}    s3cret
    @{files} =    List Files In Directory    ${run.output_dir}    absolute=True
    Should Not Be Empty    ${files}
    FOR    ${file}    IN    @{files}
        ${text} =    Get File    ${file}    encoding=UTF-8
        Should Not Contain    ${text}    s3cret    msg=${file} contains the token
    END
