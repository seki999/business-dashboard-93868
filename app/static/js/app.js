async function runBatch() {
  const result = document.querySelector("#batch-result");
  if (!result) return;

  result.textContent = "実行中...";
  const response = await fetch("/api/batch/run", { method: "POST" });
  const payload = await response.json();
  result.textContent = JSON.stringify(payload, null, 2);
}

document.querySelectorAll("[data-run-batch]").forEach((button) => {
  button.addEventListener("click", runBatch);
});
