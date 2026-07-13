import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const paths = process.argv.slice(2);
for (const path of paths) {
  const input = await FileBlob.load(path);
  const workbook = await SpreadsheetFile.importXlsx(input);
  const result = await workbook.inspect({ kind: "sheet", include: "id,name", maxChars: 12000 });
  console.log(JSON.stringify({ path, inspect: result.ndjson }));
}
