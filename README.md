# LLM-Horst

LLM-Horst is a tailored AI assistant environment built on Open WebUI and Ollama, designed to deliver practical, real-world applications of large language models.

# State of the repository

This repository is currently just a docusaurus page set up for automatic deployment to github pages.
I will later add the actual files needed to run LLM Horst as advertised.

# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

### Installation

```
$ yarn
```

### Local Development

```
$ yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

Using SSH:

```
$ USE_SSH=true yarn deploy
```

Not using SSH:

```
$ GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
