---
sidebar_position: 6
---

### Why is my bot deploy failing even though I have followed the correct folder structure?
Make sure that you have an `on_message` function inside your `main.py` file and you also have the `bot()` decorator.

If you are a MacOS user, make sure that you use the website which we have provided in the [prerequisites](./deployment/prerequisites.md#important-note-for-macos-users) section to zip your files.

### Why am I getting a weird axios error when I am trying to deploy my bot using the CLI?
We currently have a two bot limit per user. If you have exceeded that, then you will get this error in the CLI.

### Why am I getting an Error: Got unexpected extra argument?
This is because your path has a space in between somewhere and it's considering whatever's there after the space as an entirely extra argument. Check your path and make sure that there are no spaces in between.