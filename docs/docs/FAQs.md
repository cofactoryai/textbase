---
sidebar_position: 5
---

### Why is my bot deploy failing even though I have follwed the correct folder structure?
Make sure that you have an `on_message` function inside your `main.py` file and you also have the `bot()` decorator.

If you are a MacOS user, make sure that you use the website which we have provided in the [prerequisites](./deployment/prerequisites.md#important-note-for-macos-users) section to zip your files.

### Why am I getting a weird axios error when I am trying to deploy my bot using the CLI?
We currently have a two bot limit per user. If you have exceeded that, then you will get this error in the CLI.