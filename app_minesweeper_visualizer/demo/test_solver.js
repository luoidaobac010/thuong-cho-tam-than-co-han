const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const script = html.split('<script>')[1].split('</script>')[0];

const stubEl = () => new Proxy({ classList: { add() {}, remove() {}, toggle() {} }, style: {}, dataset: {}, appendChild() {}, prepend() {} }, {
  get: (t, k) => (k in t ? t[k] : ''), set: (t, k, v) => ((t[k] = v), true),
});
global.document = { getElementById: stubEl, querySelector: stubEl, createElement: stubEl };
global.window = {};
global.alert = () => {};

eval(script + `
(async () => {
  speed = 0;
  for (const key of ['test1', 'test2', 'test3', 'test4']) {
    loadPreset(key);
    const before = JSON.stringify(A);
    await togglePlay(); const first = JSON.stringify(B);
    await togglePlay(); const second = JSON.stringify(B);
    console.log(key, first === second ? 'rerun OK' : 'RERUN MISMATCH', first);
  }
  let fails = 0;
  for (let i = 0; i < 200; i++) {
    N = 1 + (i % 6); M = 1 + ((i * 7) % 6);
    generateSolvableGrid();
    await togglePlay();
    if (B.some(row => row.includes(null))) fails++;
  }
  console.log('random solvable grids: 200, false "no solution":', fails);
})();`);
