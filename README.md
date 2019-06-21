OverTrack Twitch Scoreboard
---

[![All Contributors](https://img.shields.io/badge/all_contributors-0-orange.svg?style=flat-square)](#contributors)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Discord chat](https://img.shields.io/badge/chat-on_discord-008080.svg?style=flat-square)](https://discord.gg/JywstAB)

Install the extension here
https://www.twitch.tv/ext/eug7fim8pj2b6w2od8ht1vk3aga3ad

![twitch_ui.png](https://raw.githubusercontent.com/overtrack-gg/overtrack-twitch-extension/readme-images/twitch_ui.png)

## Contributors
This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification and is 
brought to you by these [awesome contributors](./CONTRIBUTORS.md).

# Developing

Much of the development discussion for this extension takes place on the [OverTrack discord](https://discord.gg/JywstAB) in the #development channel.
Come say hi!
Issues are also welcome for ideas, suggestions, and bug reports.

## Testing your changes
There are 2 main options for testing your changes as you develop.

First you can run the extension frame separate from Twitch entirely. 
This is the most minimal approach and avoids having to have a stream running to develop the extension.
For this method, you must provide mock data for each player.

Alternatively you can host the extension locally and create a locally hosted Twitch extension.
This allows you to test how the extension integrates with a stream.

When you are happy with your changes, create a Pull Request and hopefully your changes will make it into the next 
live version of this extension deployed to Twitch. Keep in mind the extension needs to be submitted for review by
Twitch, so it may take some time between your PR being accepted and the changes making it to live.

## Running Locally

Run `scoreboard_local_server.py` and browse to http://localhost:8000
![local_ui.png](https://raw.githubusercontent.com/overtrack-gg/overtrack-twitch-extension/readme-images/local_ui.png)

Use the Player Selector UI to change properties of the players and watch the scoreboard update.
![player_selector.png](https://raw.githubusercontent.com/overtrack-gg/overtrack-twitch-extension/readme-images/player_selector.png)


## Running as a Local Twitch Extension

```
Info coming soon
```

## Running on Twitch

You should not need this - deployment is managed by the repository maintainers.

# Support us

If you like OverTrack, consider becoming a [subscriber](https://overtrack.gg/subscribe). 
