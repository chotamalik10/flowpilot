const $ = (selector) => document.querySelector(selector);
const notice = (message) => {
  const node = $("#notice");
  node.textContent = message;
  node.classList.add("show");
  window.setTimeout(() => node.classList.remove("show"), 3200);
};
async function request(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed.");
  return data;
}
async function refreshWorkflows() {
  const list = $("#workflow-list");
  try {
    const data = await request("/api/workflows");
    $("#workflow-count").textContent = data.workflows.length;
    if (!data.workflows.length) {
      list.innerHTML = '<div class="empty">No workflows yet. Create your first automation above.</div>';
      return;
    }
    list.replaceChildren();
    for (const workflow of data.workflows) {
      const row = document.createElement("article");
      row.className = "workflow-row";
      const info = document.createElement("div");
      const title = document.createElement("strong");
      title.textContent = workflow.name;
      const meta = document.createElement("small");
      meta.textContent = workflow.error || `${workflow.steps} step(s) · ${workflow.file}`;
      info.append(title, meta);
      const actions = document.createElement("div");
      actions.className = "workflow-actions";
      const run = document.createElement("button");
      run.className = "run-button";
      run.textContent = "▶ Run";
      run.disabled = Boolean(workflow.error);
      run.addEventListener("click", async () => {
        run.disabled = true;
        run.textContent = "Running…";
        try {
          const result = await request(`/api/run/${encodeURIComponent(workflow.file)}`, {
            method: "POST", body: "{}",
          });
          const passed = result.steps.filter((step) => step.success).length;
          notice(`${result.name}: ${passed}/${result.steps.length} steps passed.`);
        } catch (error) {
          notice(error.message);
        } finally {
          run.disabled = false;
          run.textContent = "▶ Run";
        }
      });
      actions.append(run);
      row.append(info, actions);
      list.append(row);
    }
  } catch (error) {
    list.innerHTML = '<div class="empty">Dashboard API unavailable. Restart FlowPilot server.</div>';
    notice(error.message);
  }
}
$("#workflow-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = event.submitter;
  button.disabled = true;
  try {
    const payload = {
      name: $("#workflow-name").value.trim(),
      steps: [{
        name: $("#step-name").value.trim(),
        type: $("#task-type").value,
        message: $("#step-message").value,
      }],
    };
    const result = await request("/api/workflows", {
      method: "POST", body: JSON.stringify(payload),
    });
    notice(`Saved “${result.name}” successfully.`);
    $("#workflow-form").reset();
    $("#step-name").value = "welcome";
    $("#step-message").value = "Hello from FlowPilot!";
    await refreshWorkflows();
  } catch (error) {
    notice(error.message);
  } finally {
    button.disabled = false;
  }
});
$("#refresh").addEventListener("click", refreshWorkflows);
$("#new-workflow").addEventListener("click", () => {
  $("#workflow-name").focus();
  $("#builder").scrollIntoView({ behavior: "smooth" });
});
refreshWorkflows();
