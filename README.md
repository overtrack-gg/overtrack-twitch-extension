OverTrack Twitch Scoreboard
---

[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Discord chat](https://img.shields.io/badge/chat-on_discord-008080.svg?style=flat-square)](https://discord.gg/JywstAB)

Install the extension here
https://www.twitch.tv/ext/eug7fim8pj2b6w2od8ht1vk3aga3ad

![twitch_ui.png](https://raw.githubusercontent.com/overtrack-gg/overtrack-twitch-extension/readme-images/twitch_ui.png)

## Contributors
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<table><tr><td align="center"><a href="https://github.com/synap5e"><img src="https://avatars0.githubusercontent.com/u/2515062?v=4" width="100px;" alt="Simon Pinfold"/><br /><sub><b>Simon Pinfold</b></sub></a><br /><a href="https://github.com/overtrack-gg/overtrack-twitch-extension/commits?author=synap5e" title="Code">💻</a> <a href="#design-synap5e" title="Design">🎨</a></td><td align="center"><a href="https://github.com/jess-sio"><img src="https://avatars3.githubusercontent.com/u/3945148?v=4" width="100px;" alt="Jessica Mortimer"/><br /><sub><b>Jessica Mortimer</b></sub></a><br /><a href="https://github.com/overtrack-gg/overtrack-twitch-extension/commits?author=jess-sio" title="Code">💻</a></td></tr></table>

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification and is 
brought to you by these [awesome contributors](./CONTRIBUTORS.md).

# Developing

Much of the development discussion for this extension takes place on the [OverTrack discord](https://discord.gg/JywstAB) in the #development channel.
Come say hi!
Issues are also welcome for ideas, suggestions, and bug reports.

## Testing your changes
There are 3 options for testing your changes as you develop.

First you can run the extension frame separate from Twitch entirely. 
This is the most minimal approach and avoids having to have a stream running to develop the extension.
For this method, you must provide mock data for each player.

Alternatively you can host the extension locally and create a locally hosted Twitch extension.
This allows you to test how the extension integrates with a stream.

Finally, you can host the extension as a test extension on Twitch servers, to ensure that everything is working as intended.

When you are happy with your changes, create a Pull Request and hopefully your changes will make it into the next 
live version of this extension deployed to Twitch. Keep in mind the extension needs to be submitted for review by
Twitch, so it may take some time between your PR being accepted and the changes making it to live.

Note that parts of the extension use a basic preprocessor to allow running both locally, twitch locally hosted, and twitch hosted.
For fully local testing, sections of the script surrounded by
`/* BEGIN: twitch */` and `/* END: twitch */` are excluded. These sections replace the pubsub data with periodic fetching from the local server.
For hosted testing, twitch requires that no logging is included, so `/* BEGIN: !twitch */` and `/* END: !twitch */` can be used to surround 
logging and debug sections of the scripts. The build script will remove these sections when creating the assets zip to upload to twtich.

## Running Locally

Run `scoreboard_local_server.py` and browse to http://localhost:8000
![local_ui.png](https://raw.githubusercontent.com/overtrack-gg/overtrack-twitch-extension/readme-images/local_ui.png)

Use the Player Selector UI to change properties of the players and watch the scoreboard update.
![player_selector.png](https://raw.githubusercontent.com/overtrack-gg/overtrack-twitch-extension/readme-images/player_selector.png)


## Running as a Local Twitch Extension

To test the extension on Twitch, you must create an extension through the [Twitch Developer Console](https://dev.twitch.tv/console).
Select the type of extension to be **Video - Component**, and optionally fill out the other fields. 
Complete the creation of your extension, and you should now have an extension in the **Local Test** phase.

Install the extension on your own channel using the **View on Twitch and Install* button in the Developer Console.
You will also need to set the extension as a component and position it under your installed extensions.

![activate_extension_position.png](https://raw.githubusercontent.com/overtrack-gg/overtrack-twitch-extension/readme-images/activate_extension_position.png)

Find your extension's **Client ID** (top right in the extension's Developer Console), 
and a **Client ID Secret** under **Extension Authorization Settings** > **Extension Client Configuration**.
The **Client ID Secret** should be a base64 encoded string.
Once you have these, you can run the local server script:

`./local_twitch_extension.py <client_id> <extension_secret> <your_channel_name>` 

Follow the script's instructions for ensuring that the SSL certificate is accepted by your browser.

Start your stream, and you should see the extension icon at the bottom centre of your stream.

You may need to click on it and accept the test extension warning.
Note that this may have to be accepted *each time* you reload the stream.

![accept_developer_extension.png](https://raw.githubusercontent.com/overtrack-gg/overtrack-twitch-extension/readme-images/accept_developer_extension.png)


Finally your extension should display on your stream, and can be updated with the GUI. To modify the extension, simply edit the extension files
e.g. `main.js` and reload the page.
![twitch_localhost_extension.png](https://raw.githubusercontent.com/overtrack-gg/overtrack-twitch-extension/readme-images/twitch_localhost_extension.png)

## Running as a Hosted Test Extension

The `./build.py` script can be used to generate a zip file of the assets you must upload. 

## Deploying on Twitch

Unless you are creating a maintained fork of this extension, you should not need to do this.
Deployment of this extension is managed by the repository maintainers - please PR your changes, and hopefully they can make it into the next release of this extension.

# Support us

If you like OverTrack, consider becoming a [subscriber](https://overtrack.gg/subscribe). 
