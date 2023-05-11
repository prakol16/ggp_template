onmessage = (e) => {
    const { role, library } = e.data;
    const initialState = findinits(library);
    const moves = findlegals(initialState, library);
    shuffleArray(moves);
    postMessage({ type: "shuffled", moves });

    // The subworker sorts the moves using bogosort
    const subworker = loadWorker("subworker", ["lib"]);
    subworker.onmessage = (e) => {
        postMessage({ type: "sorted", moves: e.data.moves });
    }
    subworker.postMessage({ type: "sorted", moves: moves.map(move => JSON.stringify(move)).slice(0, 11) });
}
