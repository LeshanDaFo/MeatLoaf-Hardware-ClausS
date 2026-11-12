const board = document.querySelector("#board");
const module = document.querySelector("#module");
const status = document.querySelector("#status");
const panel = document.querySelector("#package");
const installer = document.querySelector("esp-web-install-button");
const download = document.querySelector("#download");

async function init() {
  const response = await fetch("./firmware/catalog.json");
  if (!response.ok) throw new Error("Firmware catalog missing");
  const catalog = await response.json();
  let installerReady = false;

  function update() {
    const selected = catalog[board.value + "-" + module.value];
    panel.hidden = !selected;
    installer.hidden = !selected || !installerReady;
    status.textContent = selected ? "" : "Select your board and module.";
    if (!selected) return;

    installer.setAttribute("manifest", selected.manifest);
    download.href = selected.download;
    document.querySelector("#name").textContent = selected.name;
    document.querySelector("#details").textContent = selected.version + " · " +
      (selected.web ? "Web interface included" : "Web interface not included");
    if (!installerReady) {
      status.textContent = "Browser installation requires Web Serial and ESP Web Tools. The ZIP download is available.";
    }
  }

  board.addEventListener("change", update);
  module.addEventListener("change", update);
  update();

  if (!window.isSecureContext || !("serial" in navigator)) return;
  await import("https://unpkg.com/esp-web-tools@10.1.1/dist/web/install-button.js?module");
  await customElements.whenDefined("esp-web-install-button");
  installerReady = true;
  update();
}

init().catch((error) => {
  console.error(error);
  status.textContent = panel.hidden
    ? "Firmware catalog unavailable. Run prepare.py and reload."
    : "Browser installer unavailable. You can download the selected ZIP.";
});
