---
sidebar_position: 2
---

# Deploy from CLI

## API key generation

Before deploying your bot from the CLI, you need to generate an API key in the dashboard. To do that, you need to:

1. Navigate to the Textbase [dashboard](https://textbase-dashboard-nextjs.vercel.app/).
2. Sign in using your google account.
3. Generate an API key by clicking on `Generate` in the bottom left section.

## Deployment

After this, you can execute the `textbase_cli deploy` command to deploy your bot from a terminal.

After executing it, it will ask for:
1. Path to the zip folder
2. Bot name (**IMPORTANT:** can only contain lowercase alphanumeric characters, hyphens, and underscores)
3. Textbase API key

If you want to run this command in one shot, you can make use of flags:

```bash
textbase_cli deploy --path=<path_to_zip_folder> --bot-name=<name_of_your_bot> --api_key=<api_key>
```

If this command executes successfully, it will return a table with `Status`, `Bot ID` and `URL` and you can click on that URL to view your bot!
