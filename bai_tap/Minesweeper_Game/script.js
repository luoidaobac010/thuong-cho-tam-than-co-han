const ROWS = 16;
const COLS = 16;
const MINES_COUNT = 40;

let board = [];
let mineMatrix = [];
let countMatrix = [];
let revealedCount = 0;
let isGameOver = false;
let firstClick = true;
let flagCount = 0;
let timer = 0;
let timerInterval = null;

const boardElement = document.getElementById('game-board');
const mineCountElement = document.getElementById('mine-count');
const timerElement = document.getElementById('timer');
const messageOverlay = document.getElementById('message-overlay');
const messageText = document.getElementById('message-text');

// 4-neighborhood directions
const dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]];

function initGame() {
    board = [];
    mineMatrix = [];
    countMatrix = [];
    revealedCount = 0;
    isGameOver = false;
    firstClick = true;
    flagCount = MINES_COUNT;
    timer = 0;
    
    clearInterval(timerInterval);
    timerElement.textContent = timer;
    mineCountElement.textContent = flagCount;
    
    messageOverlay.classList.add('hidden');
    boardElement.style.gridTemplateColumns = `repeat(${COLS}, 32px)`;
    boardElement.innerHTML = '';

    for (let r = 0; r < ROWS; r++) {
        board[r] = [];
        mineMatrix[r] = Array(COLS).fill(0);
        countMatrix[r] = Array(COLS).fill(0);
        
        for (let c = 0; c < COLS; c++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.r = r;
            cell.dataset.c = c;
            
            cell.addEventListener('click', () => handleCellClick(r, c));
            cell.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                handleRightClick(r, c);
            });
            
            board[r][c] = cell;
            boardElement.appendChild(cell);
        }
    }
}

function generateMines(excludeR, excludeC) {
    let minesPlaced = 0;
    while (minesPlaced < MINES_COUNT) {
        const r = Math.floor(Math.random() * ROWS);
        const c = Math.floor(Math.random() * COLS);
        
        // Don't place mine on first click or its 4 neighbors
        const isSafeZone = (Math.abs(r - excludeR) + Math.abs(c - excludeC) <= 1);
        
        if (mineMatrix[r][c] === 0 && !isSafeZone) {
            mineMatrix[r][c] = 1;
            minesPlaced++;
        }
    }
    
    // Calculate 4-way counts
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            let count = 0;
            for (const [dr, dc] of dirs) {
                const nr = r + dr, nc = c + dc;
                if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS) {
                    count += mineMatrix[nr][nc];
                }
            }
            countMatrix[r][c] = count;
        }
    }
}

function handleCellClick(r, c) {
    if (isGameOver || board[r][c].classList.contains('flag')) return;

    if (firstClick) {
        firstClick = false;
        generateMines(r, c);
        timerInterval = setInterval(() => {
            timer++;
            timerElement.textContent = timer;
        }, 1000);
    }

    if (mineMatrix[r][c] === 1) {
        gameOver(false);
        return;
    }

    revealCell(r, c);
    checkWin();
}

function handleRightClick(r, c) {
    if (isGameOver || board[r][c].classList.contains('revealed')) return;

    const cell = board[r][c];
    if (cell.classList.contains('flag')) {
        cell.classList.remove('flag');
        cell.textContent = '';
        flagCount++;
    } else if (flagCount > 0) {
        cell.classList.add('flag');
        cell.textContent = '🚩';
        flagCount--;
    }
    mineCountElement.textContent = flagCount;
}

function revealCell(r, c) {
    if (r < 0 || r >= ROWS || c < 0 || c >= COLS || board[r][c].classList.contains('revealed') || board[r][c].classList.contains('flag')) {
        return;
    }

    const cell = board[r][c];
    cell.classList.add('revealed');
    revealedCount++;

    const count = countMatrix[r][c];
    if (count > 0) {
        cell.textContent = count;
        cell.classList.add(`num-${count}`);
    } else {
        // Flood fill for 0 using 4-way
        for (const [dr, dc] of dirs) {
            revealCell(r + dr, c + dc);
        }
    }
}

function gameOver(win) {
    isGameOver = true;
    clearInterval(timerInterval);
    
    messageText.textContent = win ? "You Win!" : "Game Over!";
    messageText.className = win ? "win-text" : "lose-text";
    messageOverlay.classList.remove('hidden');

    // Reveal all mines
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            if (mineMatrix[r][c] === 1) {
                board[r][c].classList.add('mine', 'revealed');
                board[r][c].textContent = '💣';
            }
        }
    }
}

function checkWin() {
    if (revealedCount === ROWS * COLS - MINES_COUNT) {
        gameOver(true);
    }
}

// === AUTO-SOLVER ===
function autoSolve() {
    if (firstClick || isGameOver) return;
    
    // DP Backtracking Solver logic (Translated from C++)
    let B = Array.from({length: ROWS}, () => Array(COLS).fill(0));
    let solutionFound = false;

    function checkAndFill() {
        for (let r = 1; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                let val = countMatrix[r-1][c];
                if (r >= 2) val -= B[r-2][c];
                if (c > 0) val -= B[r-1][c-1];
                if (c < COLS-1) val -= B[r-1][c+1];
                if (val < 0 || val > 1) return false;
                B[r][c] = val;
            }
        }
        for (let c = 0; c < COLS; c++) {
            let sum = 0;
            if (ROWS >= 2) sum += B[ROWS-2][c];
            if (c > 0) sum += B[ROWS-1][c-1];
            if (c < COLS-1) sum += B[ROWS-1][c+1];
            if (sum !== countMatrix[ROWS-1][c]) return false;
        }
        return true;
    }

    function backtrack(c) {
        if (solutionFound) return;
        if (c === COLS) {
            if (checkAndFill()) solutionFound = true;
            return;
        }

        let lo = 0, hi = 1;
        if (c >= 1) {
            let base = countMatrix[0][c-1] - (c >= 2 ? B[0][c-2] : 0);
            if (ROWS === 1) {
                if (base < 0 || base > 1) return;
                lo = hi = base;
            } else {
                lo = Math.max(0, base - 1);
                hi = Math.min(1, base);
                if (lo > hi) return;
            }
        }

        for (let val = lo; val <= hi; val++) {
            B[0][c] = val;
            let ok = true;

            let maxR = Math.min(c, ROWS-1);
            for (let r = 1; r <= maxR && ok; r++) {
                let col = c - r;
                let rv = countMatrix[r-1][col];
                if (r >= 2) rv -= B[r-2][col];
                if (col > 0) rv -= B[r-1][col-1];
                rv -= B[r-1][col+1];
                if (rv < 0 || rv > 1) ok = false;
                else B[r][col] = rv;
            }

            if (!ok) continue;
            backtrack(c + 1);
            if (solutionFound) return;
        }
    }

    // Since we know the true mine matrix, we only want the solver to run to visually show its power!
    // But to make it more like a real game, the solver should only use information that is REVEALED.
    // However, our C++ solver expects the ENTIRE A matrix (countMatrix) to be known from the start.
    // So for the sake of this "Hack" button, we just cheat and use the full countMatrix to solve it instantly.
    
    let t0 = performance.now();
    backtrack(0);
    let t1 = performance.now();
    console.log(`Auto-solver finished in ${t1 - t0}ms`);

    if (solutionFound) {
        // Apply solution visually
        for (let r = 0; r < ROWS; r++) {
            for (let c = 0; c < COLS; c++) {
                if (!board[r][c].classList.contains('revealed')) {
                    if (B[r][c] === 1) {
                        if (!board[r][c].classList.contains('flag')) {
                            handleRightClick(r, c); // Flag it
                        }
                    } else {
                        revealCell(r, c);
                    }
                }
            }
        }
        checkWin();
    }
}

document.getElementById('btn-restart').addEventListener('click', initGame);
document.getElementById('btn-solve').addEventListener('click', autoSolve);
document.getElementById('btn-play-again').addEventListener('click', initGame);

// Start game
initGame();
