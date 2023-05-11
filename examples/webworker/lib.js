/**
 * This file contains some library functions that you might use in several other files
 */

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function isSorted(array) {
    for (let i = 0; i < array.length - 1; ++i) {
        if (array[i] > array[i + 1]) return false;
    }
    return true;
}