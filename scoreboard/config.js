window.Twitch.ext.onContext(function(context) {
    if (context.theme === 'dark'){
        // dark mode - use white text
        document.body.style.color = "#dad8de";
    } else {
        // light mode - use dark text
        document.body.style.color = "#19171c";
    }
});
