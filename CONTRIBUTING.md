# Contributing to Textbase

Being part of the core `Textbase` team is accessible to anyone who is motivated and wants to be part of that journey!

Please see below how to contribute to the project, also refer to the contributing documentation.

## How can you help us?

* Report a bug
* Improve documentation
* Discuss the code implementation
* Submit a bug fix
* Propose new features
* Test Textbase

## Code contributions

1. Fork the repository to your personal GitHub account. 
    We call this forked repo as `<YOUR_USERNAME>/textbase` repo.

2. Now, clone `<YOUR_USERNAME>/textbase` and add `cofactoryai/textbase` as the upstream:
    ```bash
    git clone https://github.com/<YOUR_USERNAME>/textbase.git
    cd textbase
    git remote add upstream https://github.com/cofactoryai/textbase.git
    git fetch upstream
    ```

3. Create a new branch with the name of your feature (eg. `docs`):
    ```bash
    git pull upstream main
    git checkout -b <FEATURE_NAME>
    ```

4. Close the terminal and complete the task. You may commit your progress as many times as you like during the process:
    ```bash
    git add .
    git commit -m "<YOUR_MESSAGE>"
    ```

5. Commit your progress if you haven't already and push it to `<YOUR_USERNAME>:<FEATURE_NAME>` likewise:
    ```bash
    git push origin <FEATURE_NAME>
    ```

6. Open your browser and go to `<YOUR_USERNAME>/textbase` repo on GitHub.

7. Create a PR
**from `<YOUR_USERNAME>:<FEATURE_NAME>` to `cofactoryai:main`** (Very important step)

8. Wait for the maintainer to review your code.
If you need to make some changes, commit and push to `<YOUR_USERNAME>:<FEATURE_NAME>`.

9. Delete `<YOUR_USERNAME>:<FEATURE_NAME>` branch **after** the PR is merged or is out of scope.
    ```bash
    git checkout dev
    git push -d origin <FEATURE_NAME>
    git branch -d <FEATURE_NAME>
    ```

10. Repeat from step 3 for a new PR.

And you're done!

> NOTE: Be sure to merge the latest from "upstream" before making a pull request! Also, make the PR to the staging branch.

## Feature and Bug reports
We use GitHub issues to track bugs and features. Report them by opening a [new issue](https://github.com/cofactoryai/textbase/issues/)

If you are new to `textbase` and opensource in general we have collected some `good-first-issues` for you to get started. Have a look at it [here](https://github.com/cofactoryai/textbase/labels/good%20first%20issue)

## Code review process

The Pull Request reviews are done on a regular basis. Please, make sure you respond to our feedback/questions.



Join our mission of `building and deploying AI chatbots` with a single command!
