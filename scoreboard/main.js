// made using http://vanilla-js.com/

/* BEGIN: !twitch */
function getJSON(url, callback) {
	var xhr = new XMLHttpRequest();
	xhr.open('GET', url, true);
	xhr.responseType = 'json';
	xhr.onload = function() {
		let status = xhr.status;
		if (status === 200) {
			callback(xhr.response);
		} else {
			console.error(status, xhr.response);
		}
	};
	xhr.send();
};

var lastMessage = null;
var lastDelayedMessage = null;
var start = new Date().getTime() / 1000;
var lastUpdate = null;
/* END: !twitch */

function onMessage(data){
    /* BEGIN: !twitch */
    lastUpdate = new Date().getTime();
	if (latestContext){
		let now = new Date().getTime() / 1000;
		let currentFrameTimestamp = now - latestContext.hlsLatencyBroadcaster;
		let offset = data.timestamp - currentFrameTimestamp;

        // log event received timings
        if (lastMessage){
            let shownTime = false;
            for (let i=0; i < 12; i++){
                let team = data.teams.blue;
                let lastTeam = lastMessage.teams.blue;
                if (i >= 6){
                    team = data.teams.red;
                    lastTeam = lastMessage.teams.red;
                }
                let player = team[i % 6];
                let lastPlayer = lastTeam[i % 6];
                if (player.kills != lastPlayer.kills){
                    if (!shownTime){
                        console.log(
                            'now=' + (now - start) +
                            ', frame=' + currentFrameTimestamp +
                            ', event=' + (data.timestamp - start) +
                            ', latency=' + latestContext.hlsLatencyBroadcaster +
                            ', offset=' + offset
                        );
                        shownTime = true;
                    }
                    console.log('Got ' + player.name + ' kills ' + lastPlayer.kills + ' -> ' + player.kills);
                }
            }
        }
        lastMessage = data;
    }
    /* END: !twitch */

    let scoreboard = document.getElementsByClassName('scoreboard')[0];
    if (data.teams){
        scoreboard.style.display = 'block';
        let players = document.getElementsByClassName('player');
        for (let i=0; i<12; i++){
            let team = data.teams.blue;
            if (i >= 6){
                team = data.teams.red;
            }
            let player = team[i % 6];
            let element = players[i];

            let name = element.getElementsByClassName('name')[0];
            let hero = element.getElementsByClassName('hero')[0];
            let kills = element.getElementsByClassName('kills')[0];
            let deaths = element.getElementsByClassName('deaths')[0];
            let resurrects = element.getElementsByClassName('resurrects')[0];

            name.innerText = player.name;
            hero.className = 'hero hero-' + player.current_hero;
            kills.innerText = player.kills;
            deaths.innerText = player.deaths;
            resurrects.innerText = player.resurrects;
            if (player.current_hero === 'mercy'){
                resurrects.style.display = 'block';
                element.classList.add('show-resurrects');
            } else {
                resurrects.style.display = 'none';
                element.classList.remove('show-resurrects');
            }
        }
    } else {
        scoreboard.style.display = 'none';
    }

    let postgame = document.getElementsByClassName('lastgame')[0];
    if (data.postgame){
        postgame.style.display = 'flex';
        postgame.className = 'lastgame lastgame-' + data.postgame.role
            + ' lastgame-' + data.postgame.result;

        let thumbnail = postgame.getElementsByClassName('thumbnail')[0];
        thumbnail.style.backgroundImage = `url(./images/map_thumbnails/${data.postgame.map.replace(' ', '-')}.jpg)`;
        let hero_icon_image = thumbnail.getElementsByClassName('hero-icon-image')[0];
        hero_icon_image.src = `./images/heroes/${data.postgame.hero}.png`;

        let game_result = postgame.getElementsByClassName('game-result')[0];
        let game_time = postgame.getElementsByClassName('game-time')[0];
        let sr_change = postgame.getElementsByClassName('sr-change')[0];
        let duration = postgame.getElementsByClassName('duration')[0];
        game_result.innerText = data.postgame.result.toUpperCase();
        game_time.innerText = new Date(data.postgame.timestamp * 1000)
            .toLocaleString('default', {hour: 'numeric', minute: '2-digit'});
        sr_change.innerText = data.postgame.description;
        duration.innerText = data.postgame.duration;

        let stretched_link = postgame.getElementsByClassName('stretched-link')[0];
        let link = postgame.getElementsByClassName('link')[0];
        stretched_link.href = data.postgame.link;
        link.href = data.postgame.link;

        let stats_block = postgame.getElementsByClassName('stats')[0];
        let rows = stats_block.getElementsByClassName('row');
        let headers = stats_block.getElementsByClassName('header');
        let stats = stats_block.getElementsByClassName('stat');

        for (var i = 0; i < 6; i++) {
            if (i >= data.postgame.stats.length) {
                rows[i].style.display = 'none';
                continue;
            }

            headers[i].innerText = data.postgame.stats[i].key;
            let stat = data.postgame.stats[i].value;
            stats[i].innerText = stat === null ? '?' : stat;
        }
    } else {
        postgame.style.display = 'none';
    }
}

var latestContext = null;
window.onload = function() {
    /* BEGIN: !twitch */
	if (window.Twitch){
		window.Twitch.ext.onError(function(error){
			console.error(error);
		});
		/* END: !twitch */

		window.Twitch.ext.onAuthorized(function(auth) {
			window.setInterval(function(){
			    if (!lastUpdate || (new Date().getTime()) - lastUpdate > 120 * 1000){
			        // no update for the last 2min - EBS is offline
			        document.getElementsByClassName('scoreboard')[0].style.display = 'none';
			    }
			}, 15 * 1000);
		});

		window.Twitch.ext.listen('broadcast', function(target, contentType, message){
			onMessage(JSON.parse(message));
		});

		window.Twitch.ext.onContext(function(context) {
			latestContext = context;
		});

	/* BEGIN: !twitch */
	} else {
	    getJSON('/scoreboard.json', function(data){
            onMessage(data);
        });
		window.setInterval(function(){
			getJSON('/scoreboard.json', function(data){
				onMessage(data);
			});
		}, 5000);
	}
	/* END: !twitch */
};
