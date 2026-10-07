const endpoint = "/api/note";
const loadButton = document.querySelector("#load");
const status = document.querySelector("#status");
const notes = document.querySelector("#notes");

loadButton.addEventListener("click", async () => {
  status.textContent = "正在加载";
  try {
    const response = await fetch(endpoint);
    const items = await response.json();
    notes.replaceChildren();
    for (const item of items) {
      const row = document.createElement("li");
      row.textContent = item.title;
      notes.append(row);
    }
    status.textContent = "加载完成";
  } catch (error) {
    status.textContent = error.message;
    console.error(error);
  }
});
