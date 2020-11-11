(function (global, $, undefined) {
    function main() {
        var $input = $('#textInput'),
            $results = $('#results');
        var ws = new WebSocket("ws://localhost:8080/ws");

        $input.keyup(function (ev) {
            var msg = {term: ev.target.value};
            ws.send(JSON.stringify(msg));
        });

        ws.onmessage = function (msg) {
            var data = JSON.parse(msg.data);
            var res = data[1];

            // Append the results
            $results.empty();

            $.each(res, function (index, value) {
                $('<li><a tabindex="-1" target="_blank" href="' + data[3][index] + '">' + value + '</a></li>').appendTo($results);
            });
            $results.show();
        }
    }

    main();
}(window, jQuery));
