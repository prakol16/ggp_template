function bogoSort(arr) {
    while (!isSorted(arr)) shuffleArray(arr);
}

onmessage = (e) => {
    let { moves } = e.data;
    bogoSort(moves);
    postMessage({ moves });
}