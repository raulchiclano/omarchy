// Local data only: no clipboard access or network needed.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = path.join(__dirname, '../payload/plugins/lavanda.emojis');
const search = require(path.join(base, 'EmojiSearch.js'));
const emojis = JSON.parse(fs.readFileSync(path.join(base, 'emojis.json'), 'utf8'));
const find = q => search.filterEmojis(emojis, q, emojis.length).map(x => x.e);
for (const [query, expected] of [['feliz','😄'], ['risa','😂'], ['corazón','❤️'],
  ['corazon','❤️'], ['corazon rojo','❤️'], ['fiesta','🥳'], ['confeti','🎉'],
  ['aprobado','👍'], ['happy','😄']]) assert.ok(find(query).includes(expected), query);
assert.deepEqual(find('CORAZÓN'), find('corazon'));
assert.equal(find('zzzsinemojizzz').length, 0);
assert.ok(emojis.every(e => e.e && e.k && e.n));
assert.equal(search.filterEmojis(emojis, '', 4).length, 4);
assert.equal(search.filterEmojis(emojis, '', 0).length, 0);
assert.deepEqual(search.parseEmojis('{bad'), []);
console.log('Spanish/English emoji search, accents, multiword, empty and limits passed.');
