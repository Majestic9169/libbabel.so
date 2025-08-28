# Hextra Starter Template

![hextra-template](https://github.com/imfing/hextra-starter-template/assets/5097752/c403b9a9-a76c-47a6-8466-513d772ef0b7)

[🌐 Demo ↗](https://imfing.github.io/hextra-starter-template/) 

> [!IMPORTANT] check out the above demo for a guide to what you can do with this website

## Local Development

Pre-requisites: [Hugo](https://gohugo.io/getting-started/installing/), [Go](https://golang.org/doc/install) and [Git](https://git-scm.com)

1. Clone the repo (make sure to add git submodules)

```shell
git clone --recursive https://github.com/imfing/hextra-starter-template.git
```

1. Start the server
```shell
hugo mod tidy
hugo server --logLevel debug --disableFastRender -p 1313
```

## Adding A CTF

there exists an archetype for each new CTF and writeup

```shell
hugo new writeups/<CTF-Name>
hugo new -k default writeups/<CTF-Name>/<challenge-name>
```

I'm also working on a script to autocreate these folders from the `challenges.json` after a CTF
