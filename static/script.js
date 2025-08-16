// Simple fade-in animation for tasks
document.addEventListener("DOMContentLoaded", () => {
  const tasks = document.querySelectorAll(".list-group-item");
  tasks.forEach((task, i) => {
    task.style.opacity = 0;
    setTimeout(() => {
      task.style.transition = "opacity 0.6s ease-in";
      task.style.opacity = 1;
    }, i * 150);
  });
});
