---
sidebar_position: 3
---

# Usage
You can use execute these commands after installing the `textbase-client` package.

### test
Before executing this command, make sure that:
1. The directory in which your `main.py` file is in, **DOES NOT** have any spaces.
2. You have a `main.py` file akin to the ones provided in the [examples](./category/examples) section.

This will start a local server and will give you a link which you can navigate to and test your bot there.
```bash
textbase-client test
```
If you wish to run this in one go, you can make use of the `--path` and `--port` flags
```bash
textbase-client test --path=<path_to_main.py>
```
**If you wish to use the `--path` flag, make sure you have your path inside quotes.**

```bash
textbase-client test --port=8080
```
**Port 8080 is the default, but it's crucial to note that it's frequently used. If you have it open for another application, this flag lets you alter the backend server's port to prevent conflicts.**

### compress
Before executing this command, make sure that
1. You have a `main.py` and `requirements.txt` file in the path that you have given to compress.
2. Your `requirements.txt` has the `textbase-client` requirement.
```bash
textbase-client compress
```
If you wish to run this in one go, you can make use of the `--path` flag
```bash
textbase-client compress --path=<path_to_the_folder_containing_main_py_and_requirements_txt>
```

### deploy
Before executing this command, make sure that
1. You have a `.zip` file which is made according to the instructions and folder structure given in the
[prerequisites](./deployment/prerequisites.md) section.
2. The path where this zip file is contained **DOES NOT** have any spaces.
3. You have an Textbase API key. This can be generated in the [dashboard](https://textbase-dashboard-nextjs.vercel.app/), guide for which is given in the [deployment](./deployment/deploy-from-cli.md#api-key-generation) section.

#### NOTE
Executing this command will ask the name for your bot as well. There is a naming convention to be followed for that: the bot name can only contain **lowercase alphanumeric characters, hyphens, and underscores**.
```bash
textbase-client deploy
```
If you wish to run this in one go, you can make use of the `--path`, `--bot-name` and `--api_key` flags
```bash
textbase-client deploy --path=<path_to_zip_folder> --bot-name=<name_of_your_bot> --api_key=<api_key>
```
**If you wish to use the `--path` flag, make sure you have your path inside quotes.**

### health
Before executing this command, make sure that
1. You have the bot ID of which you are trying to check the health of. You can get the Bot ID in the `Deployments` section of the [dashboard](https://textbase-dashboard-nextjs.vercel.app/) or by executing the [list](#list) command.
2. You have an Textbase API key. This can be generated in the [dashboard](https://textbase-dashboard-nextjs.vercel.app/), guide for which is given in the [deployment](./deployment/deploy-from-cli.md#api-key-generation) section.
```bash
textbase-client health
```
If you wish to run this in one go, you can make use of the `--bot_id` and `--api_key` flag
```bash
textbase-client health --bot_id=<bot_id> --api_key=<api_key>
```

### list
This will ask you for your API key, which can be generated in the [dashboard](https://textbase-dashboard-nextjs.vercel.app/), guide for which is given in the [deployment](./deployment/deploy-from-cli.md#api-key-generation), and on successful validation will return the list of the bots that you have deployed along with their bot ID and link.
```bash
textbase-client list
```
If you wish to run this in one go, you can make use of the `--api_key` flag
```bash
textbase-client list --api_key=<api_key>
```

### delete
Before executing this command, make sure that
1. You have the bot ID of which you are trying to check the health of. You can get the Bot ID in the `Deployments` section of the [dashboard](https://textbase-dashboard-nextjs.vercel.app/) or by executing the [list](#list) command.
2. You have an Textbase API key. This can be generated in the [dashboard](https://textbase-dashboard-nextjs.vercel.app/), guide for which is given in the [deployment](./deployment/deploy-from-cli.md#api-key-generation) section.
```bash
textbase-client delete
```
If you wish to run this in one go, you can make use of the `--bot_id` and `--api_key` flag
```bash
textbase-client delete --bot_id=<bot_id> --api_key=<api_key>
```