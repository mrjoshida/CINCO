import fs from 'fs';
import vm from 'vm';

const html = fs.readFileSync('web/emu/index.html', 'utf8');
const match = html.match(/<script type="module">([\s\S]*?)<\/script>/);

if (!match) {
  console.error("No script module block found!");
  process.exit(1);
}

const js = match[1];

// Strip import statements for pure syntax parse
const strippedJs = js.replace(/import\s+[\s\S]*?from\s+['"][^'"]+['"];?/g, '// import stripped');

try {
  new vm.Script(strippedJs);
  console.log("JavaScript syntax verification PASSED with zero errors!");
} catch (err) {
  console.error("JavaScript syntax error:", err);
  process.exit(1);
}
