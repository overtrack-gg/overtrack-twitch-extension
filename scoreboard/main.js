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
var epoch = new Date().getTime() / 1000;
/* END: !twitch */
var lastUpdate = null;

function onMessage(data){
    lastUpdate = new Date().getTime();

    let offset = 0;
	if (latestContext){
		let now = new Date().getTime() / 1000;
		let currentFrameTimestamp = now - latestContext.hlsLatencyBroadcaster;
		offset = data.timestamp - currentFrameTimestamp;

        /* BEGIN: !twitch */
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
                        console.log('now=' + (now - epoch) + ', ts=' + (data.timestamp - epoch) + ', latency=' + latestContext.hlsLatencyBroadcaster + ', offset=' + offset);
                        shownTime = true;
                    }
                    console.log('Got ' + player.name + ' kills ' + lastPlayer.kills + ' -> ' + player.kills);
                }
            }
        }
        lastMessage = data;
        /* END: !twitch */
    }

	window.setTimeout(function(){
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
				let dead = element.getElementsByClassName('dead')[0];

				name.innerText = player.name;
				hero.className = 'hero hero-' + player.current_hero;
				kills.innerText = player.kills;
				deaths.innerText = player.deaths;
				resurrects.innerText = player.resurrects;
				if (player.current_hero === 'mercy'){
					resurrects.style.display = 'block';
				} else {
					resurrects.style.display = 'none';
				}
			}
		} else {
			scoreboard.style.display = 'none';
		}
	}, offset * 1000);
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
			    if (!lastUpdate || (new Date().getTime()) - lastUpdate > 60 * 1000){
			        // no update for the last 60s - EBS is offline
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
