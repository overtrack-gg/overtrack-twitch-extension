const twitch = window.Twitch.ext;

twitch.onContext(function(context) {
    if (context.theme === 'dark'){
        // dark mode - use white text
        document.body.style.color = '#dad8de';
    } else {
        // light mode - use dark text
        document.body.style.color = '#19171c';
    }
});

twitch.onAuthorized(function(auth) {
	fetch('https://api2.overtrack.gg/overwatch_twitch_extension/check_twitch_user', {
	// fetch('http://localhost:5001/overwatch_twitch_extension/check_twitch_user', {
		method: 'POST',
		headers: {
			'content-type': 'application/json',
			'x-extension-jwt': auth.token
    	},
		body: JSON.stringify({})
	}).then(res => {
		let loading = document.getElementsByClassName('loading')[0];
		let found = document.getElementsByClassName('account-found')[0];
		let not_found = document.getElementsByClassName('account-not-found')[0];
		let last_game = document.getElementsByClassName('last-game')[0];
		loading.style.display = 'none';
		if (res.status == 200){
			found.style.display = 'block';
			not_found.style.display = 'none';
			res.json().then(data => {
				if (data.overwatch_last_game){
					last_game.src = 'https://overtrack.gg/overwatch/games/' + data.overwatch_last_game + '/card.png';
				}
			});
		} else {
			found.style.display = 'none';
			not_found.style.display = 'block';
		}
	});
});

// twitch.configuration.onChanged(function(){});
