//==============================================================================
// The code below defines a basic legal player.
// We also send the initial state to a WebWorker to do some further processing
//==============================================================================

var role = 'robot';
var startclock = 10;
var playclock = 10;

var library = [];
var roles = [];
var state = [];
var move = 'nil';
var worker;

//==============================================================================

function ping() {
    return 'ready'
}

function start(r, rs, sc, pc) {
    role = r;
    library = definemorerules([], rs.slice(1));
    roles = findroles(library);
    state = findinits(library);
    startclock = numberize(sc);
    playclock = numberize(pc);
    console.log("The roles are", shuffleArray(roles));
    worker = loadWorker("worker",
        ["http://ggp.stanford.edu/epilog/javascript/epilog.js",
                    "http://ggp.stanford.edu/gamemaster/reasoning/general.js",
                    "loadworker", "lib"], ["lib", "subworker"]);
    worker.postMessage({ role, library });
    worker.onmessage = (e) => {
        console.log("Received message from the worker!", e.data);
    }
    return 'ready'
}

function play(move) {
    if (move !== nil) {
        state = simulate(move, state, library)
    };
    if (findcontrol(state, library) !== role) {
        return false
    }
    return findlegalx(state, library)
}

function stop(move) {
    return false
}

function abort() {
    return false
}

//==============================================================================
// End of player code
//==============================================================================

