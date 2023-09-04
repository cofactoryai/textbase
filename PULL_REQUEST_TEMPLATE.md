## Scope
`[Add context about what this feature is about and explain why of the feature and your technical decisions.]`
Added a new ui for the application, you can use different ui for the same application the default ui can be used by running the command poetry run python textbase/textbase_cli.py test

you can use the streamlit run examples\streamlit\streamlit_vicky-chatbot.py command to run the ui built with stream lit 


- [ ] `[Sub task]`

there were not enough modification made other then stroing the api key in a sperate file called secrets.toml  the file will not be stroed in the repo when you clone the repo please create a .streamlit folder in the main path and add a secrets.toml file in there add your api key here
# .streamlit/secrets.toml
OPENAI_API_KEY = "YOUR_API_KEY"

### Screenshots
---


## Code improvements
- `[Did you add some generic like utility, component, or anything else useful outside of this PR]`


### Developer checklist
- [✅] I’ve manually tested that code works locally on desktop and mobile browsers.
- [✅] I’ve reviewed my code.
- [✅] I’ve removed all my personal credentials (API keys etc.) from the code.