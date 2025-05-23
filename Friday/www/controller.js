$(document).ready(function () {
    eel.expose(DisplayMessage);

    function DisplayMessage(message) {
        $(".Siri-message").text(message);

        // Stop previous animations
        $(".Siri-message").textillate('stop');

        // Restart animation for each new message
        $(".Siri-message").textillate({
            loop: false, // No infinite loop
            sync: true,
            in: { effect: "fadeInUp", sync: true },
            out: { effect: "fadeOutUp", sync: true, delay: 5000 } // Show text for 5s before fading out
        });
    }
});