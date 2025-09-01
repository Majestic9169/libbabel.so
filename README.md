# Hextra Starter Template

[🌐 Theme Docs ↗](https://imfing.github.io/hextra-starter-template/) 

> [!IMPORTANT] check out the above demo for a guide to what you can do with this website

## Local Development

Pre-requisites: [Hugo](https://gohugo.io/getting-started/installing/), [Go](https://golang.org/doc/install) and [Git](https://git-scm.com)

1. Clone the repo (make sure to add git submodules)

```shell
git clone --recursive https://github.com/Majestic9169/libbabel.so.git
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

also with every new CTF add the necessary data to `./data/ctf_ids.yaml`, it will be auto added to the main table on pushing

data looks like 

```yaml
scriptCTF-2025:
  ctftime_id: 2792
  position: 20
  team_name: "libbabel.so"
  comments: "ezpz, selection ctf for libbabel"
```

I'm also working on a script to autocreate these folders from the `challenges.json` after a CTF
